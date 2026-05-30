class Email:
    def __init__(self, sender, body, subject=None, recipient=None, date=None, attachments=None):
        if sender is None:
            raise ValueError("Sender cannot be None")
        if body is None:
            raise ValueError("Message cannot be None")
        
        self._sender = sender
        self._body = body
        self._subject = subject
        self._recipient = recipient
        self._date = date
        self._attachments = attachments

    @property
    def sender(self):
        return self._sender
    
    @property
    def body(self):
        return self._body
    
    @property
    def subject(self):
        return self._subject
    @property
    def recipient(self):
        return self._recipient
    @property
    def date(self):
        return self._date
    @property
    def attachments(self):
        return self._attachments
        
email = Email("Sasha", "Text")
print(email.sender)