import pytest
from src.parser.Email import Email
from src.parser.EmailParser import EmailParser

@pytest.fixture
def createTmpFile(tmp_path):
    def _create(content: str, filename: str = "test.txt") -> str:
        filePath = tmp_path / filename
        filePath.write_text(content, encoding='utf-8')
        return str(filePath)
    return _create

def test_parseMinimalEmail(createTmpFile):
    content = """
        From: test@test.ru

        Hello, World!.
    """
    path = createTmpFile(content, "minimal.txt")
    parser = EmailParser()
    email = parser.parse(path)
    
    assert email.sender == "test@test.ru"
    assert email.subject is None
    assert email.body == "Hello, World!."
    assert email.recipient is None
    assert email.date is None
    assert email.attachments is None
    assert email.isAReply is False
    assert email.isAForward is False
    assert email.sentFromIphone is False

def test_parseMaximalEmail(createTmpFile):
    content = """
        From: testFrom@test.ru
        To: testTo@test.ru
        Date: 1337-01-01
        Subject: Some subject

        Text here.

        Прикрепил: doc.pdf screenshot.png
        Otpravleno s iPhone
    """
    path = createTmpFile(content, "full.txt")
    parser = EmailParser()
    email = parser.parse(path)
  
    assert email.sender == "testFrom@test.ru"
    assert email.recipient == "testTo@test.ru"
    assert email.date == "1337-01-01"
    assert email.subject == "Some subject"
    assert email.body == "Text here."
    assert email.attachments == ["doc.pdf", "screenshot.png"]
    assert email.sentFromIphone is True
    assert email.isAReply is False
    assert email.isAForward is False

def test_parseRussianHeaders(createTmpFile):
    content = """
        От кого: тестОтКого@тест.ру
        Кому: тестКому@тест.ру
        Дата: 1337-01-01
        Тема: Привет, проверяющий!


        Тело письма.
    """
    path = createTmpFile(content, "russian.txt")
    parser = EmailParser()
    email = parser.parse(path)
  
    assert email.sender == "тестОтКого@тест.ру"
    assert email.recipient == "тестКому@тест.ру"
    assert email.date == "1337-01-01"
    assert email.subject == "Привет, проверяющий!"
    assert email.body == "Тело письма."

def test_parseReply(createTmpFile):
    content = """From: test@test.ru
                Subject: Re: Original subject


                This is a reply."""
    path = createTmpFile(content, "reply.txt")
    parser = EmailParser()
    email = parser.parse(path)
    assert email.isAReply is True
    assert email.subject == "Original subject"


def test_parseForwardFlag(createTmpFile):
    content = """
                From: test@test.ru
                Subject: Fwd: Forwarded message


                Forwarded content."""
    path = createTmpFile(content, "forward.txt")
    parser = EmailParser()
    email = parser.parse(path)
    assert email.isAForward is True
    assert email.subject == "Forwarded message"


def test_parseTransliteratedHeaders(createTmpFile):
    content = """Ot kogo: test@test.ru
                Tema: Test
                Data: 1337-01-01


                Body."""
    path = createTmpFile(content, "translit.txt")
    parser = EmailParser()
    email = parser.parse(path)
    assert email.sender == "test@test.ru"
    assert email.subject == "Test"
    assert email.date == "1337-01-01"


def test_onlyNecessaryFields(createTmpFile):
    content = """From: test@test.ru


                Only body."""
    path = createTmpFile(content, "missing.txt")
    parser = EmailParser()
    email = parser.parse(path)
    assert email.sender == "test@test.ru"
    assert email.subject is None
    assert email.recipient is None
    assert email.date is None
    assert email.body == "Only body."


def test_emptySubject(createTmpFile):
    content = """From: test@test.ru
                Subject:


                Body text."""
    path = createTmpFile(content, "empty_subj.txt")
    parser = EmailParser()
    email = parser.parse(path)
    assert email.subject == None
    assert email.body == "Body text."

def test_attachmentsMultiple(createTmpFile):
    content = """From: test@test.ru
                Subject: Attachments


                Файл: doc.pdf image.png
                Вложение: archive.zip"""
    path = createTmpFile(content, "attach.txt")
    parser = EmailParser()
    email = parser.parse(path)
    assert "doc.pdf" in email.attachments
    assert "image.png" in email.attachments
    assert "archive.zip" in email.attachments


def test_noFalseAttachments(createTmpFile):
    content = """From: test@test.ru
                Subject: No attachments


                Просто текст, в котором есть слово "файл", но без двоеточия.
                Также есть расширение .pdf но не после двоеточия."""
    path = createTmpFile(content, "no_attach.txt")
    parser = EmailParser()
    email = parser.parse(path)
    assert email.attachments is None or email.attachments == []


def test_iphoneSignature(createTmpFile):
    content = """From: test@test.ru
                Subject: Sent from iPhone


                Message.
                Otpravleno s iPhone"""
    path = createTmpFile(content, "iphone.txt")
    parser = EmailParser()
    email = parser.parse(path)
    assert email.sentFromIphone is True
    assert "Otpravleno s iPhone" not in email.body

def test_fileNotFound():
    parser = EmailParser()
    with pytest.raises(FileNotFoundError):
        parser.parse("nonexistent_file.txt")

def test_unsupportedFormat(createTmpFile):
    content = "This is just plain text without any email headers."
    path = createTmpFile(content, "plain.txt")
    parser = EmailParser()
    with pytest.raises(ValueError, match="File is not an email"):
        parser.parse(path)

def test_emptyFile(createTmpFile):
    path = createTmpFile("", "empty.txt")
    parser = EmailParser()
    with pytest.raises(ValueError, match="File is not an email"):
        parser.parse(path)


def test_noSender(createTmpFile):
    content = """Subject: No sender
                Body here."""
    path = createTmpFile(content, "no_sender.txt")
    parser = EmailParser()
    with pytest.raises(ValueError, match="File is not an email"):
        parser.parse(path)

def test_lowercase(createTmpFile):
    content = """from: test@test.ru
    subject: test message

                MiXeD CaSe in the body.\nIt should remain unchanged.
                """
    path = createTmpFile(content, "lowercase.txt")
    parser = EmailParser()
    email = parser.parse(path)

    assert email.sender == "test@test.ru"
    assert email.subject == "test message"
    expected_body = """MiXeD CaSe in the body.\nIt should remain unchanged."""
    assert email.body == expected_body