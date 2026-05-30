class Classification:
    def words_in_text(self, words, text):
        for word in words:
            if word in text:
                return True
        return False
    
    def classify(self, email):
        sender = email.sender.lower()
        subject = (email.subject or "").lower()
        body = email.body.lower()

        full_text = sender + " " + subject + " " + body

        if self.words_in_text([
        ], full_text):
            return "spam"

        if self.words_in_text([
        ], full_text):
            return "urgent_cases"

        if self.words_in_text([
        ], full_text):
            return "access_requests"

        if self.words_in_text([
        ], full_text):
            return "equipment"

        if self.words_in_text([
        ], full_text):
            return "software_problem"

        if self.words_in_text([
        ], full_text):
            return "system_monitoring"

        if self.words_in_text([
        ], full_text):
            return "documents"

        if self.words_in_text([
        ], full_text):
            return "hr"

        if self.words_in_text([

        ], full_text):
            return "invitation"

        if self.words_in_text([
        ], full_text):
            return "newsletter"

        return "other"