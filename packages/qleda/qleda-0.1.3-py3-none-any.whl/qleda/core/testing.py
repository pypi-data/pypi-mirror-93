from typing import Optional, Union
from pathlib import Path
from unittest import TestCase
from inspect import getfile

from ..constants import DIR_TEST_OUT, DIR_TEST_IN, DIR_TEST_DBS

from .dbsetup import init_db


class TestDataReader:

    def build_input_path(self, filename: str) -> Path:
        return Path(getfile(self.__class__)).parent / DIR_TEST_IN / filename

    def read_test_data(self, filename: str, *args, **kwargs) -> Union[str, bytes]:
        with open(self.build_input_path(filename), *args, **kwargs) as f:
            return f.read()


class TestDataWriter:

    def build_output_path(self, filename: str) -> Path:
        p = Path(getfile(self.__class__)).parent / DIR_TEST_OUT / filename
        if not p.parent.exists():
            p.parent.mkdir()
        return p

    def write_test_data(self, file_content: Union[str, bytes], filename: str, *args, **kwargs):
        with open(self.build_output_path(filename), *args, **kwargs) as f:
            return f.write(file_content)


class DbTestCase(TestCase):
    """
    The goal of DbTestCase is to do a different init_db function depending on how the test is run.
    If only one function is run (via Pycharm play Button) debug shall be True. Then a debug database file is created.
    Otherwise the test is run with a in memory database.
    """

    _DEBUG = False

    def setUp(self, debug: Optional[bool] = None) -> None:
        if isinstance(debug, bool):
            self._DEBUG = debug
        if self._DEBUG:
            self.engine, self.session = init_db(path=Path(getfile(self.__class__)).parent / DIR_TEST_DBS / '{}.db'.format(self.__class__.__name__),
                                   override=True)
        else:
            self.engine, self.session = init_db()
