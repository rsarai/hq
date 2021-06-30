import argparse

from pathlib import Path
from datetime import datetime

from hq.config import SecondBrain as config


def append():
    parser = argparse.ArgumentParser()
    parser.add_argument("note", help="Incremental note to be saved.")
    args = parser.parse_args()

    note = args.note
    now_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    path = Path(config.export_path + "/" + config.incremental_notes_file)
    incremental_notes = path.read_text()
    incremental_notes_content = incremental_notes.split('\n')

    with open(str(path), 'w') as f:
        for i, content in enumerate(incremental_notes_content):
            if i == 1:
                f.write(f'\n- [{now_str}] {note}\n\n')
            elif content == '':
                continue
            else:
                f.write(content)
                f.write('\n')

