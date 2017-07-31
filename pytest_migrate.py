"""Helper for migrating to pytests

Run it like::

    python pytest_migration.py test_forcereply.py
"""

import re
import sys
from pathlib import Path

header = """#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2017
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/]."""

CLASS = r'class (.*)Test\(BaseTest, unittest.TestCase\):(?:\r?\n)([\s\S]*)if __name__'
JSON_DICT = r'self.json_dict = (\{[\s\S]*\})([\s\S]*?def)'
CLASS_VARS = r'    def setUp\(self\):\n([\s\S]*?def)'

if __name__ == '__main__':
    original = Path('tests/' + sys.argv[1]).open('r', encoding='UTF-8').read()
    new_text = header
    new_text += '\nimport json\n\nimport pytest\n\nfrom telegram import\n\n'

    match = re.search(CLASS, original)
    if not match:
        match = re.search(CLASS[:-11], original)
    name = 'Test' + match.group(1)
    new_class = 'class {}:\n{}'.format(name, match.group(2))
    new_class = re.sub(r'self\._id', 'self.id', new_class)
    new_class = re.sub(r'telegram\.', '', new_class)
    new_class = re.sub(r'self\.assertTrue\(isinstance\((.*), (.*)\)\)',
                       r'assert isinstance(\1, \2)', new_class)
    new_class = re.sub(r'self\.assertTrue\(self\.is_json\((.*)\)\)', r'json.loads(\1)', new_class)
    new_class = re.sub(r'self\.assertTrue\(self\.is_dict\((.*)\)\)',
                       r'assert isinstance(\1, dict)', new_class)
    new_class = re.sub(r'self\.assert(True|False)\((.*)\)', r'assert \2 is \1', new_class)
    new_class = re.sub(r'self\.assertIsNone\((.*)\)', r'assert \1 is None', new_class)
    new_class = re.sub(r'self\.assertIsInstance\((.*), (.*)\)',
                       r'assert isinstance(\1, \2)', new_class)
    new_class = re.sub(r'self\.assert(?:Dict)?Equals?\((.*), (.*)\)',
                       r'assert \1 == \2', new_class)
    new_class = re.sub(r'self\.assertNotEquals?\((.*), (.*)\)', r'assert \1 != \2', new_class)
    new_class = re.sub(r'self\._bot', r'bot', new_class)
    new_class = re.sub(r'self\._chat_id,', r'chat_id', new_class)

    json_dict = re.search(JSON_DICT, new_class)
    if json_dict:
        new_class = re.sub(JSON_DICT, r'\2', new_class)
        new_text += '@pytest.fixture(scope=\'class\')\ndef json_dict():\n    return '
        new_text += json_dict.group(1).replace('self.', name + '.')
        new_text += '\n\n'

    class_vars = re.search(CLASS_VARS, new_class)
    if class_vars:
        class_vars = class_vars.group(1)
        class_vars = class_vars.replace('    ', '')
        class_vars = class_vars.replace('self.', '')
        class_vars = '\n'.join(['    ' + x for x in class_vars.split('\n')])
        new_class = re.sub(CLASS_VARS, class_vars, new_class)

    new_class = re.sub(r'self.json_dict', r'json_dict', new_class)

    new_text += new_class
    new_file = Path('pytests/' + sys.argv[1]).open('w', encoding='UTF-8').write(new_text)