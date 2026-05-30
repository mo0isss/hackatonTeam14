class Classification:
    def words_in_text(self, words, text):
        for word in words:
            if word in text:
                return True
        return False
    
    def classify(self, email):
        subject = (email.subject or "").lower()
        body = email.body.lower()

        full_text = subject + " " + body

        if self.words_in_text([
            "розыгрыш",
            "приз",
            "банковской карты",
            "подозрительный вход",
            "логина и пароля",

            "rozygrysh",
            "priz",
            "bankovskoy karty",
            "podozritelnyy vhod",
            "logina i parolya"
        ], full_text):
            return "spam"

        if self.words_in_text([
            "критич",
            "ошибка 500",
            "остановлена",
            "всего отдела",
            "всех отдела",
            "по-прежнему недоступ",
            "kritich",
            "oshibka 500",
            "ostanovlena",
            "vsego otdela",
            "vseh otdela",
            "po-prezhnemu nedostup"
        ], full_text):
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
            "tekhnicheskie raboty"
        ], full_text):
            return "newsletter"

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
            "excel"
        ], full_text):
            return "software_problem"
        
        if self.words_in_text([
            "оборудован",
            "ноутбук",
            "гарнитур",
            "мышь",
            "принтер",
            "клавиатур",
            "ремонт",
            "диагностик",
            "замен",
            "oborudovan",
            "noutbuk",
            "garnitur",
            "mysh",
            "printer",
            "klaviatur",
            "remont"
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
            "dogovor",
            "instruk",
            "rekvizit",
            "schet",
            "oplat"
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
        return "other"