import pytest
from src.parser.Email import Email

def test_createMinimalEmail():
    email = Email(sender = "test@test.com", body = "Hello, World!")
    assert email.sender == "test@test.com"
    assert email.body == "Hello, World!"
    assert email.subject is None
    assert email.recipient is None
    assert email.date is None
    assert email.attachments is None
    assert email.isAReply is False
    assert email.isAForward is False
    assert email.sentFromIphone is False

def test_createMaximalEmail():
    email = Email(
        sender = "testFrom@test.ru",
        body = "Hello, World!",
        subject = "Important",
        recipient = "testTo@test.ru",
        date = "2026-06-01",
        attachments = ["doc.pdf", "img.png"],
        isAReply = True,
        isAForward = True,
        sentFromIphone = True
    )
    assert email.sender == "testFrom@test.ru"
    assert email.body == "Hello, World!"
    assert email.subject == "Important"
    assert email.recipient == "testTo@test.ru"
    assert email.date == "2026-06-01"
    assert email.attachments == ["doc.pdf", "img.png"]
    assert email.isAReply is True
    assert email.isAForward is True
    assert email.sentFromIphone is True

def test_emailAttachmentsNoneByDeafault():
    email = Email(sender="test@test.ru", body="Hello, World!")
    assert email.attachments is None

def test_emailSenderNoneRaisesValueError():
    with pytest.raises(ValueError, match="Sender cannot be None"):
        Email(sender=None, body="Some text")


def test_emailBodyNoneRaisesValueErrorTest():
    with pytest.raises(ValueError, match="Message cannot be None"):
        Email(sender = "test@test.ru", body = None)

def test_emailIsReadOnlyTest():
    email = Email(sender = "test@test.ru", body = "Some text")

    with pytest.raises(AttributeError):
        email.sender = "newTest@test.ru"
    with pytest.raises(AttributeError):
        email.body = "New text"
    with pytest.raises(AttributeError):
        email.subject = "New subject"
    with pytest.raises(AttributeError):
        email.recipient = "New recipient"
    with pytest.raises(AttributeError):
        email.date = "1337-01-01"
    with pytest.raises(AttributeError):
        email.attachments = []
    with pytest.raises(AttributeError):
        email.isAReply = True
    with pytest.raises(AttributeError):
        email.isAForward = True
    with pytest.raises(AttributeError):
        email.sentFromIphone = True

def test_emailFieldTypesTest():
    email = Email(
        sender = "testFrom@test.ru",
        body = "Some text",
        subject = "Important subject",
        recipient = "testTo@test.ru",
        date = "1337-01-01",
        attachments = ["doc.txt"],
        isAReply = False,
        isAForward = True,
        sentFromIphone = False
    )
    assert isinstance(email.sender, str)
    assert isinstance(email.body, str)
    assert isinstance(email.subject, str) or email.subject is None
    assert isinstance(email.recipient, str) or email.recipient is None
    assert isinstance(email.date, str) or email.date is None
    assert isinstance(email.attachments, list) or email.attachments is None
    assert isinstance(email.isAReply, bool)
    assert isinstance(email.isAForward, bool)
    assert isinstance(email.sentFromIphone, bool)
