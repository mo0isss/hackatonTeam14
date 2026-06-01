import pytest
from src.identifier.classification import Classification
from src.parser.Email import Email

@pytest.fixture
def classifier():
    return Classification()

@pytest.mark.parametrize("body, subject, expected_category",
        [("Поздравляем! Вы стали победителем в ррозыгрыше. Перейдите по ссылке чтобы получить приз",
        "Заберите свой приз",
        "spam"),

        ("Работа vsego otdela приостановлена. Интернет не работает во всём здании",
        "Очень срочная ситуация",
        "urgent_cases"),

        ("Мама, не работает код! Дай мне dostup к файлу, я поменяю его. Спасибо",
        "Прошу выдать разрешение",
        "access_requests"),

        ("Высылаю реквизиты счёта. Пожалуйста, проверьте их",
        "Реквизиты счёта в банке",
        "documents"),

        ("Не включается ноутбук, не знаю что делать, уже всё перепробовала",
        "Поломка ноутбука",
        "equipment"),

        ("Nemedlenno требую продлить мне otpusk, я устала!",
        "Otpusk Хан Диане",
        "hr"),

        ("Давайте sozvonimsya сегодня вечером, а то нам сдавать хакатон уже пора",
        "Встреча команды 14",
        "invitation"),
        
        ("Высылаю вам итоги за эти 3 месяца",
        "Итоги квартала",
        "news_letter"),
        
        ("Excel перестал работать, как можно исправить эту проблему?",
        "Проблема с работой Excel",
        "software_problem"),
        
        ("Проверка сервиса: healthcheck завершился с ошибкой.",
        "Cистемное уведомление",
        "system_monitoring"),
        
        ("Ксюша, привет! Диана зовет тебя сегодня в гости",
        "В гости",
        "other_в гости"),

        ("ne rabotaet. Уже пятый den. Если вопрос не к вам — перенаправьте, пожалуйста.",
        "Re:",
        "urgent_cases"),
        
         ("Клиент обращается повторно - заявка висит без ответа уже 3 дня. Прошу срочно разобраться.",
        "URGENT: Запрос от внешнего пользователя",
        "urgent_cases"),

        ("Не включается noutbuk, требуется remont",
        "",
        "equipment"),
        
        ("",
        "",
        "other_unknown"),
        
        ("Ваш пароль истекает. Доступ будет заблокирован. Нужны права для восстановления.",
        "Срочно обновите пароль",
        "spam"), 
        
        ("Не могу включить printer, требуется remont.", 
         None, 
         "equipment"), 

        ("Massovyy sboy u vsego otdela. Также направляю bolnichnyy list.",
        "Обращение сотрудника",
        "urgent_cases"),
        
        ("ПрОшу прОверИТЬ РЕКВиЗиТы перед отправкой документа.",
        "Уточнение по СчЁтУ",
        "documents"), 

        ("Спасибо, буду ждать подробности.",
        "Приглашение на meropriyatie",
        "invitation")])

def test_classification(classifier, body, subject, expected_category):
    email = Email("hacatonTeam14", body, subject)
    assert classifier.classify(email) == expected_category


@pytest.mark.parametrize("body, subject, date, attachments, expected_category", 
    [ ("Прошу посмотреть вложение.", 
       "Re:", 
       None, 
       ["screenshot.png"], 
       "other_screenshot.png"), 

       ("Нет подходящей категории.", 
        "", 
        "2025-06-20", 
        None, 
        "other_2025-06-20" ), 
        
        ( "Статус пока неизвестен. Прошу уточнить статус. Жду статус.", 
         "", 
         None, 
         None, 
         "other_статус" )]) 

def test_other_category_creation(classifier, body, subject, date, attachments, expected_category): 
    email = Email( "hacatonTeam14", body, subject, None, date, attachments ) 
    assert classifier.classify(email) == expected_category