import random

text = """Мне надоело петь про эту заграницу 
Надену валенки и красное пальто 
Пойду проведаю любимую столицу 
Хоть в этом виде не узнает и никто 
Возьму с собой я на прогулку кавалера 
Он песенки мои все знает наизусть 
Не иностранец и не сын миллионера 
Бухгалтер он простой да ну и пусть 
Бухгалтер милый мой бухгалтер 
Вот он какой такой простой 
Бухгалтер милый мой бухгалтер 
А счастье будет если есть в душе покой 
Бухгалтер милый мой бухгалтер 
Вот он какой такой простой 
Бухгалтер милый милый мой бухгалтер 
Зато родной зато весь мой 
Придя в холодную и пыльную конторку 
Разложит с папками бумаги на столе 
Закрутит в трубочку советскую махорку 
И будет думать только только обо мне 
Рабочий день его почти уже закончен 
А дебет с кредитом остался не сведён 
Ему плевать на это лишь бы днём и ночью 
Я пела эту песенку о нём 
Бухгалтер милый мой бухгалтер 
Вот он какой такой простой 
Бухгалтер милый мой бухгалтер 
А счастье будет если есть в душе покой 
Бухгалтер милый мой бухгалтер 
Вот он какой такой простой 
Бухгалтер милый милый мой бухгалтер 
Зато родной зато весь мой 
Бухгалтер милый мой бухгалтер 
Вот он какой такой простой 
Бухгалтер милый мой бухгалтер 
А счастье будет если есть в душе покой 
Бухгалтер милый мой бухгалтер 
Вот он какой такой простой 
Бухгалтер милый милый мой бухгалтер 
Зато родной зато весь мой""".split('\n')


def song(bot, update):
    lines_count = len(text)
    first_line = random.randint(0, int(lines_count / 2) - 1)
    line = first_line * 2

    message = '{}...'.format('\n'.join(text[line:line+2]))
    update.message.reply_text(message, quote=False)