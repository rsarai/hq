# Matthew Wang's bash profile for general Linux/Unix
#
# Suggestion: ln -sf .bashrc .bash_profile
#
# Implementation note: all functions with name starts with '__' are considered
# private and will be unset at the end.

function __main
{
    local fn

    [[ ! -f /etc/profile ]] || source /etc/profile
    [[ ! -f /etc/bashrc ]] || source /etc/bashrc
    unset PROMPT_COMMAND    # Let tmux manage it

    for fn in \
        __setup_path \
        __setup_shell_options \
        __setup_environments \
        __setup_aliases \
        __setup_completions \
        __setup_dir_colors \
        __setup_prompt \
        __setup_custom_profiles \
    ; do
        $fn; unset -f $fn
    done
}

function __prepend_path
{
    [[ :$PATH: == *:${1:?}:* ]] || PATH=$1:$PATH
}

function __setup_path
{
    local x

    # prepend paths
    for x in /sbin /usr/sbin /bin /usr/bin /usr/local/bin ~/.local/bin; do
        __prepend_path $x
    done

    # Try load ChefDK if installed, or else rbenv if installed
    if [[ -x /opt/chefdk/bin/chef ]]; then
        eval "$(/opt/chefdk/bin/chef shell-init bash)"
    elif type -P rbenv > /dev/null; then
        eval "$(rbenv init -)"
    fi

    # ~/bin takes precedence
    __prepend_path ~/bin

    export PATH
}

function __setup_shell_options
{
    bind 'set match-hidden-files off' >& /dev/null  # No tab-expand hidden files
    ! test -t 0 || stty stop undef >& /dev/null     # Make 'C-s' to do i-search
}

function __setup_environments
{
    export HISTFILE=~/.bash_history     # In case switched from zsh temporally
    export HISTSIZE=10000
    export EDITOR=vim

    # Locale (LC_*) matters for ls and sort on Linux, see also
    # www.gnu.org/software/coreutils/faq/#Sort-does-not-sort-in-normal-order_0021
    #
    [[ $(uname -s) != Linux ]] || export LC_COLLATE=C
}

# Non "private" helper function to auto complete hostnames, note 'complete -A
# hostname' also works but it does not recognize new $HOSTFILE
#
function _host_complete
{
    local cur=${COMP_WORDS[COMP_CWORD]}
    local hosts=$(sed -ne 's/[, ].*//p' ~/.ssh/known_hosts* 2>/dev/null)
    COMPREPLY=($(compgen -W "$hosts" -- $cur))
}

function __setup_completions
{
    # https://raw.github.com/git/git/master/contrib/completion/git-completion.bash
    [[ ! -f ~/.git-completion.bash ]] || . ~/.git-completion.bash
    complete -F _host_complete ssh scp host nc ping telnet
    complete -A export unset
}

function __setup_aliases
{
    local lsprog="/bin/ls"

    alias ..='cd ..'
    alias ...='cd ../..'
    alias ....='cd ../../..'
    alias .....='cd ../../../..'
    # Skip system wide vimrc to reduce startup time
    ! type vim >& /dev/null || alias vi='vim -Xn -u ~/.vimrc'
    ! type ag >& /dev/null || alias ag='command ag --nogroup'
    alias grep='grep --color=auto'

    case $(uname -s) in
        Linux)
            lsprog="/bin/ls --color=auto"
            alias ls="$lsprog -F"
            alias l="$lsprog -lF"
            alias lsps='ps -ef f | grep -vw grep | grep -i'
            ;;
        Darwin)
            type gls >& /dev/null && lsprog="gls --color=auto"
            alias ls="$lsprog -F"
            alias l="$lsprog -lF"
            alias lsps='ps -ax -o user,pid,ppid,stime,tty,time,command | grep -vw grep | grep -i'
            ;;
        *)
            alias ls="$lsprog -F"
            alias l="$lsprog -lF"
            alias lsps='ps -auf | grep -vw grep | grep -i'
            ;;
    esac
}

function __setup_dir_colors
{
    local prog=dircolors

    [[ $(uname -s) != Darwin ]] || prog=gdircolors
    if type $prog >& /dev/null && [[ -f ~/.dircolors ]]; then
        eval $($prog -b ~/.dircolors)
    fi
}

function __has_ssh_key
{
    [[ -f ~/.ssh/$USER.key ]] || ls ~/.ssh/id_?sa >& /dev/null
}

function __load_ssh_key
{
    [[ ! -f "${1:?}" ]] || ssh-add -L | grep -qw "$1" || ssh-add "$1"
}

# ssh-add -l exits code 2 when unable to connect to the agent
function __setup_ssh_agent
{
    local rc=~/.ssh-agent.rc

    __has_ssh_key || return 0
    [[ ! -f $rc ]] || source $rc
    if [[ $(ssh-add -l >& /dev/null; echo $?) == 2 ]]; then
        print -P "%{\e[31m%}Starting a new ssh-agent process...%{\e[0m}" >&2
        rm -f ~/.ssh-agent.sock
        ssh-agent -s -a ~/.ssh-agent.sock | sed '/^echo/d' > $rc
        source $rc
    fi

    __load_ssh_key ~/.ssh/$USER.key
    __load_ssh_key ~/.ssh/id_rsa
    __load_ssh_key ~/.ssh/id_dsa
}

# Non "private" helper function used to setup PS1
function _git_active_branch
{
    local branch info age track

    [[ $(git rev-parse --is-inside-work-tree 2>/dev/null) == true ]] || return
    branch=$(git symbolic-ref HEAD 2>/dev/null)
    branch=${branch#refs/heads/}
    info=$(git status -s 2>/dev/null)
    age=$(git log --pretty=format:'%cr' -1 refs/heads/$branch 2>/dev/null)
    track=$(git status -sb 2>/dev/null | sed -n 's/^##.*\[\(.*\)\].*/, \1/p')

    # NOTE: have to use $'string' for ansi escape sequence here
    if [[ -z $info ]]; then
        echo -ne $'\e[32m'" ($branch) "$'\e[36m'"[${age}${track}]"
    elif [[ -z $(echo "$info" | grep -v '^??') ]]; then
        echo -ne $'\e[35m'" ($branch) "$'\e[36m'"[${age}${track}]"
    else
        echo -ne $'\e[31m'" ($branch) "$'\e[36m'"[${age}${track}]"
    fi
}

# Fancy PS1, prompt exit status of last command, currenet time, hostname, time,
# cwd, git status and branch, also prompt the '%' in reverse color when we have
# background jobs. '\[' and '\]' is to mark ansi colors to allow shell to
# calculate prompt string length correctly
#
function __setup_prompt
{
    local _DR="\[\e[31m\]"        # red
    local _DG="\[\e[32m\]"        # green
    local _DY="\[\e[33m\]"        # yellow
    local _DB="\[\e[34m\]"        # blue
    local _DM="\[\e[35m\]"        # magenta
    local _DC="\[\e[36m\]"        # cyan
    local _RV="\[\e[7m\]"         # reverse
    local _NC="\[\e[0m\]"         # no color

    PS1="\$([[ \$? == 0 ]] && echo '${_DG}✔' || echo '${_DR}✘') \t "

    # Detect whether this box has ssh keys, distinguish hostname color and setup
    # ssh-agent related environment accordingly
    #
    if __has_ssh_key; then
        # I am on my own machine, try load ssh-agent related environments
        PS1="${PS1}${_DB}"                              # blue hostname
    else
        # Otherwise assume I am on other's box, highlight hostname in magenta
        PS1="${PS1}${_DM}"                              # magenta hostname
    fi

    # Highlight hostname in reverse green if inside a container
    if [[ -n $container_uuid ]] || [[ -f /.dockerenv ]]; then
        PS1="${PS1}${_RV}${_DG}"
    fi
    PS1="${PS1}$(hostname)"
    PS1="${PS1}${_NC}:${_DY}\w${_NC}"                   # yellow cwd
    PS1="${PS1}\$(_git_active_branch)"                  # git branch name
    PS1="${PS1}${_DC} ⤾\n"                              # cyan wrap char, newline
    PS1="${PS1}\$([[ -z \$(jobs) ]] || echo '$_RV')"    # reverse bg job indicator
    PS1="${PS1}\\\$${_NC} "                             # $ or #
}

# Load custom settings from ~/.profile.d/*.sh, typical settings are
# docker-machine env, GOPATH, customized PATH etc.
#
function __setup_custom_profiles
{
    local p

    ls ~/.profiles.d/*.sh >& /dev/null || return 0

    for p in ~/.profiles.d/*.sh; do
        source $p
    done
}

# Find a file which name matches given pattern (ERE, case insensitive)
function f
{
    local pat=${1?'Usage: f ERE-pattern [path...]'}
    shift
    find ${@:-.} \( -path '*/.svn' -o -path '*/.git' -o -path '*/.idea' \) \
        -prune -o -print -follow | grep -iE "$pat"
}

# Load file list generated by f() in vim, type 'gf' to jump to the file
function vif
{
    local tmpf=/tmp/viftmpfile.$RANDOM$$
    f "$@" > $tmpf && vi -c "/$1" $tmpf && rm -f $tmpf
}

# Grep a ERE pattern in cwd or given path
function g
{
    local string_pat=${1:?"Usage: g ERE-pattern [grep opts] [path...]"}
    shift
    local grep_opts="--color=auto"
    local paths

    while (( $# > 0 )); do
        case "$1" in
            -*) grep_opts="$grep_opts $1"; shift;;
            *) paths="$paths $1"; shift;;
        esac
    done
    [[ -n "$paths" ]] || paths="."

    find $paths \( -path '*/.svn' -o -path '*/.git' -o -path '*/.idea' \) \
        -prune -o -type f -print0 -follow \
        | eval "xargs -0 -P128 grep -EH $grep_opts '$string_pat'"
}

########################################################################
# Setup everything and unset "private" functions
########################################################################

__main
unset -f __prepend_path __has_ssh_key __load_ssh_key __main

# vim:set et sts=4 sw=4 ft=sh:

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_SCRIPT=/usr/local/bin/virtualenvwrapper.sh
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.8
source /usr/local/bin/virtualenvwrapper_lazy.sh
export BOOK_NOTES_HIGHLIGHT_PASS=""

# Install Ruby Gems to ~/gems
export GEM_HOME="$HOME/gems"
export PATH="$HOME/gems/bin:$PATH"

alias brain_sync="bash ~/github-projects/second-brain/gitsync.sh new"
