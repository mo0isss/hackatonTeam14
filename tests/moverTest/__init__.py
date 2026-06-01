import pytest
import shutil
from pathlib import Path
from src.mover.mover import mover
class TestMover:
    def setup_method(self):
        import time
        self.tmp = Path(f"tmp_test_{int(time.time())}")
        self.inbox = self.tmp / "inbox"
        self.inbox.mkdir(parents=True)
        self.file = self.inbox / "test.txt"
        self.file.write_text("Checking")
    def teardown_method(self): 
        if self.tmp.exists():
            shutil.rmtree(self.tmp, ignore_errors=True)
        if Path("treated").exists():
            shutil.rmtree("treated", ignore_errors=True)
    def test_just_move(self):
        mover(str(self.file), "spam", str(self.tmp / "treated"))
        expected = self.tmp / "treated" / "spam" / "test.txt"
        assert expected.exists()
    def test_there_is_no_such_folder(self):
        mover(str(self.file), "new", str(self.tmp / "treated"))
        assert (self.tmp / "treated" / "new").exists()
    def test_there_is_no_letter(self):
        with pytest.raises(FileNotFoundError):
            mover("no_such_file.txt", "spam", str(self.tmp / "treated"))
    def test_duplicate(self):
        mover(str(self.file), "spam", str(self.tmp / "treated"))
        file2 = self.inbox / "test.txt"
        file2.write_text("another")
        mover(str(file2), "spam", str(self.tmp / "treated"))
        assert (self.tmp / "treated" / "spam" / "test_1.txt").exists()
    def test_default_folder(self):
        mover(str(self.file), "spam")
        assert Path("treated/spam/test.txt").exists()