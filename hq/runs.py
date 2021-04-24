from modules import voice

suffix = ['.epub', '.mobi', '.pdf']

for content in voice.process():
    title = content.title
    for s in suffix:
        title = title.replace(s, '')

    with open(f'{title}.org', 'w+') as f:
        f.write(f'#+title: {title}')
        f.write('\n')
        f.write(f'- date :: {content.date.strftime("%d/%m/%Y")}')
        f.write('\n\n\n')
        for i in content.bookmarks:
            f.write(f'- {i}')
            f.write('\n\n')

