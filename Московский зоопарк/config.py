"""В этом файле описаны вопросы и возможные ответы на них."""


# Правильные варианты ответов
class Zoo:
    """ В классе Zoo, находятся переменные со списками, в которых находятся подходящие ответы.

    При подсчёте голосов если буква находится в списке, то будет засчитан плюс балл тому или иному животному.
    """

    capybara = [['a','d','f'],['a'],['a'],['c']]
    manul = [['b'],['b'],['e'],['a']]
    giant_toucan = [['d'],['c'],['c'],['b']]
    blue_and_gold_macaw = [['e'],['c'],['c'],['c']]
    steppe_eagle = [['b'],['b'],['c'],['b']]
    otter = [['c'],['a'],['c'],['a']]
    jungle_cat = [['c'],['a'],['b','d'],['a']]


# Сами вопросы с вариантами ответов
class Questions_answers:
    """В классе Questions_answers находятся вопросы с возможными ответами."""

    question_1 = "Какое из нижеперечисленных блюд Вы предпочитаете больше?"
    question_2 = "Какой из видов досуга Вам предпочтительнее всего?"
    question_3 = 'В какое время суток Вы наиболее активны?'
    question_4 = 'С кем Вы предпочитаете проводить время?'



    answers_1 = {
                'a':'Арбуз',
                'b':'Куриный стейк',
                'c':'Форель',
                'd':'Инжир',
                'e':'Грецкий орех',
                'f':'Морковный салат'
            }

    answers_2 = {
                'a':'Поплавать в бассейне',
                'b':'Затаиться в тихом месте и поспать',
                'c':'Прогуляться на свежем воздухе'
            }

    answers_3 = {
                'a':'Предпочитаю спать весь день',
                'b':'Утром',
                'c':'Днём',
                'd':'Вечером',
                'e':'Ночью'
            }

    answers_4 = {
        'a':'В одиночестве',
        'b':'С семьёй',
        'c':'С друзьями'
    }