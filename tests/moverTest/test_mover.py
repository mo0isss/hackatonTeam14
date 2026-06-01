import pytest
import shutil
from pathlib import Path
from src.mover.mover import mover

@pytest.fixture
def temp_env():
    import time
    tmp = Path(f"tmp_test_{int(time.time())}")
    inbox = tmp / "inbox"
    inbox.mkdir(parents=True)
    file = inbox / "test.txt"
    file.write_text("Checking")
    yield tmp, inbox, file  
    if tmp.exists():
        shutil.rmtree(tmp, ignore_errors=True)
    if Path("treated").exists():
        shutil.rmtree("treated", ignore_errors=True)

class TestMover:
    def test_just_move(self, temp_env):
        tmp, inbox, file = temp_env
        mover(str(file), "spam", str(tmp / "treated"))
        expected = tmp / "treated" / "spam" / "test.txt"
        assert expected.exists()
    
    def test_there_is_no_such_folder(self, temp_env):
        tmp, inbox, file = temp_env
        mover(str(file), "new", str(tmp / "treated"))
        assert (tmp / "treated" / "new").exists()
    
    def test_there_is_no_letter(self, temp_env):
        tmp, inbox, file = temp_env
        with pytest.raises(FileNotFoundError):
            mover("no_such_file.txt", "spam", str(tmp / "treated"))
    
    def test_duplicate(self, temp_env):
        tmp, inbox, file = temp_env
        mover(str(file), "spam", str(tmp / "treated"))
        file2 = inbox / "test.txt"
        file2.write_text("another")
        mover(str(file2), "spam", str(tmp / "treated"))
        assert (tmp / "treated" / "spam" / "test_1.txt").exists()
    
    def test_default_folder(self, temp_env):
        tmp, inbox, file = temp_env
        mover(str(file), "spam")
        assert Path("treated/spam/test.txt").exists()