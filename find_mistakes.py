#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import os

from jsonschema import Draft4Validator


def read_file(folder):
    names = []
    for name in os.listdir(folder):
        names.append(name)
    data = {}
    for name in names:
        data_name = name.split('.')[0]
        with open(f'{folder}/{name}') as f:
            text = json.load(f)
        data[data_name] = text
    return data


def find_mistakes(schemas, files):
    mistakes = {}
    for key in files:
        file_text = files[key]
        if not file_text:
            message = 'file is empty'
        else:
            event = file_text.get('event')
            schema = schemas.get(event)
            if not schema:
                message = f'"{event}" schema not valid'
            else:
                message = ''
                validator = Draft4Validator(schema)
                i = 0
                for error in sorted(validator.iter_errors(file_text), key=str):
                    message += str(i) + '. '
                    message += error.message
                    message += '\n'
                    i += 1
        mistakes[key] = message
    return mistakes


def create_readme(mistakes):
    readme = open('README.md', 'w', encoding='utf-8')
    i = 1
    for key in mistakes:
        readme.write(f'### {i} file name: {key}.json\n#### Errors:'
                     f'\n{mistakes[key]}\n**********************\n\n')
        i += 1
    readme.close()
    print('"README.md" created.')


if __name__ == '__main__':
    schemas = read_file('./task_folder/schema')
    files = read_file('./task_folder/event')
    mistakes = find_mistakes(schemas, files)
    create_readme(mistakes)
