import os.path
import re
from pathlib import Path
from typing import List, Tuple

import pycodestyle  # noqa
from pkg_resources import DistributionNotFound, get_distribution

from .err import ERROR

dist_name = "test_style_checker"
try:
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"


class CheckerTestFile:
    """Base class"""
    files_name = {}
    cases = []

    name = dist_name
    version = __version__

    def __init__(self, tree, filename='(none)', file_tokens=None):
        self.filename = 'stdin' if filename in ('stdin', '-', None) else filename
        self.tree = tree
        self.tokens = file_tokens

    def run(self):
        """Auto Call Validation"""

        formatted_filename = self.filename.replace('\\', '_').replace('/', '_')
        if re.match(r'.*(tests_ui).+', formatted_filename):
            sanitized_filename = os.path.splitext(os.path.basename(self.filename))[0]
            if not sanitized_filename.startswith('test_'):
                if sanitized_filename not in ('conftest', '__init__'):
                    yield 0, 0, ERROR['MC100'], type(self)
            else:
                errors = []
                path = Path(self.filename)
                if path.name in self.files_name:
                    errors.append((-1, 0, ERROR['MC101'].format(str(self.files_name[path.name]), str(self.filename))))
                else:
                    self.files_name[path.name] = self.filename

                read_line = list(pycodestyle.readlines(self.filename))
                for line_number, line in enumerate(read_line):
                    if line.strip().startswith('def'):
                        errors += function_validator(line, line_number, read_line)

                # if self.tokens:
                #     errors += token_parser(self.tokens)
                #
                for error in errors:
                    yield error[0] + 1, error[1], error[2], type(self)


def function_validator(line: str, num: int, read_line: List[str]) -> List[Tuple[int, int, str]]:
    errors = []
    start = line.find('def')
    col = start + len('def') + 1
    if line[start:].startswith('def test'):
        errors.extend([(num, col, i) for i in function_test_validator(num, read_line)])
    else:
        errors.extend([(num, col, i) for i in function_other_validator(num, read_line)])
    return errors


def function_test_validator(num: int, read_line: List[str]) -> List[str]:
    errors = []
    if func_name := re.findall(r'def\stest(.+)\(', read_line[num]):
        func_name_list = func_name[0].replace('_', '')
        if len(func_name_list) < 3:
            errors.append(ERROR['MC102'].format(func_name))
    step = 6
    start = num - step if num - step > 0 else 0
    testcase_decorator = '\n'.join(read_line[start: num])
    case_id_decorator = re.findall(r'@testcase\(\s*[\'\"]([A-Z]{2,5}-\d+)[\'\"],\s*', testcase_decorator)
    if not case_id_decorator:
        errors.append(ERROR['MC103'])
    if case_id_decorator[0] in CheckerTestFile.cases:
        errors.append(ERROR['MC104'].format(case_id_decorator[0]))
    CheckerTestFile.cases.append(case_id_decorator[0])
    return errors


def function_other_validator(num: int, read_line: List[str]) -> List[str]:
    errors = []
    step = 3
    start = num - step if num - step > 0 else 0
    fixture_decorator = '\n'.join(read_line[start: num])
    decorator = re.findall(r'(@pytest.fixture)', fixture_decorator)
    if not decorator:
        errors.append(ERROR['MC105'])
    return errors
