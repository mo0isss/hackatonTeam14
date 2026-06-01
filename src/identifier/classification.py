import pymorphy3

class Classification:
    def words_in_text(self, words, text):
        for word in words:
            if word in text:
                return True
        return False
    
    def classify(self, email):
        subject = (email.subject or "").lower()
        body = email.body.lower()
        attachments = email.attachments
        date = email.date

        full_text = subject + " " + body

        if self.words_in_text([
            "розыгрыш",
            "приз",
            "банковской карты",
            "подозрительный вход",
            "логина и пароля",
            "скидка",
            "акция",
            "вы выиграли",
            "верифик",
            "доступ будет заблокирован",
            "rozygrysh",
            "priz",
            "bankovskoy karty",
            "podozritelnyy vhod",
            "logina i parolya",
            "vy vyigrali",
            "aktsiya",
            "skidka",
            "verifi",
            "dostup budet zablokirovan", 
        ], full_text):
            return "spam"

        if (("не работает" in full_text and "день" in full_text) or 
        ("ne rabotaet" in full_text and "den" in full_text) or 
        self.words_in_text([
                "критич",
                "ошибка 500",
                "остановлена",
                "всего отдела",
                "всех отдела",
                "по-прежнему недоступ",
                "массовый сбой",
                "несколько коллег",
                "срочно разобраться",
                "srochno razobratsya",
                "urgent",
                "kritich",
                "oshibka 500",
                "ostanovlena",
                "vsego otdela",
                "vseh otdela",
                "po-prezhnemu nedostup",
                "massovyy sboy",
                "neskolko kolleg"
            ], full_text)):
                return "urgent_cases"

        if self.words_in_text([
            "мониторинг",
            "uptime",
            "healthcheck",
            "cpu usage",
            "disk usage",
            "warning",
            "monitoring"
        ], full_text):
            return "system_monitoring"

        if self.words_in_text([
            "дайджест",
            "технические работы",
            "итоги квартала",
            "daydzhest",
            "tekhnicheskie raboty",
            "itogi kvartala"
        ], full_text):
            return "news_letter"

        if self.words_in_text([
            "outlook",
            "adobe reader",
            "антивирус",
            "браузер",
            "chrome",
            "не открывает",
            "не запускается",
            "не устанавливается",
            "зарегистрироваться",
            "кнопка",
            "antivirus",
            "brauzer",
            "ne otkryvaet",
            "ne zapuskaetsya",
            "knopka",
            "zoom",
            "excel",
            "api",
            "unauthorized"
        ], full_text):
            return "software_problem"
        
        if self.words_in_text([
            "оборудован",
            "ноутбук",
            "гарнитур",
            "мышь",
            "принтер",
            "клавиатур",
            "сканер",
            "ремонт",
            "диагностик",
            "замен",
            "oborudovan",
            "noutbuk",
            "garnitur",
            "mysh",
            "printer",
            "klaviatur",
            "remont",
            "skaner"
        ], full_text):
            return "equipment"

        if self.words_in_text([
            "доступ",
            "права",
            "не могу войти",
            "dostup",
            "prava",
            "ne mogu voyti"
        ], full_text):
            return "access_requests"


        if self.words_in_text([
            "договор",
            "инструкц",
            "реквизит",
            "счёт",
            "оплат",
            "задан",
            "акт",
            "dogovor",
            "instruk",
            "rekvizit",
            "schet",
            "oplat",
            "zadan",
            "akt"
        ], full_text):
            return "documents"

        if self.words_in_text([
            "отпуск",
            "больнич",
            "график работы",
            "otpusk",
            "bolnich",
            "grafik raboty"
        ], full_text):
            return "hr"

        if self.words_in_text([
            "приглашаем",
            "демо",
            "мероприят",
            "priglashaem",
            "demo",
            "meropriyati",
            "созвон",
            "sozvon"
        ], full_text):
            return "invitation"
        
        return f'other: {self.unknownTypeClassification(subject, attachments, date, body)}'
    
    def unknownTypeClassification(self, subject: str, attachments: str, date: str, text: str) -> str:
        if subject is not None and subject != "" and "re" not in subject.lower() and "fwd" not in subject.lower():
            return subject
        elif attachments is not None:
            return attachments[0]
        elif date is not None and date != "":
            return date
        else:
            for symbol in ':,.;/-=_':
                text = text.replace(symbol, " ")

            morph = pymorphy3.MorphAnalyzer()
            frequency = {}
            banWords = ['день', 'добрый', 'уважаемый', 'смотреть', 'вечер', 'здравствуйте', 'приветствую']

            for word in text.split():
                normalForm = morph.parse(word)[0].normal_form
                if len(normalForm) <= 3 or normalForm in banWords:
                    continue
                if normalForm not in frequency.keys():
                    frequency.update({normalForm: 1})
                else:
                    frequency[normalForm] += 1

            return max(frequency, key=lambda x: frequency[x])