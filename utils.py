import re

from stop_words import safe_get_stop_words
from snowballstemmer import stemmer


def tokenize(string):
    """
    Разбиение строки на слова
    :param string: исходная строка
    :return: список слов
    """
    return map(lambda x: x.lower(), tokenize.pattern.split(string))
tokenize.pattern = re.compile("\W+")


def delete_stop_words(query):
    """
    Удаление стоп-слов
    :param query: исходный список слов
    :return: список с удалёнными стоп-словами
    """
    return (token for token in query if token not in delete_stop_words.stop_words_set)
delete_stop_words.stop_words_set = stop_words_set = set(safe_get_stop_words("ru") + safe_get_stop_words("en"))


def stem(word):
    """
    Стемминг слова
    :param word: исходное слово
    :return: основа слова
    """
    return min(stem.en.stemWord(word), stem.ru.stemWord(word), key=lambda x: len(x))
stem.ru = stemmer('russian')
stem.en = stemmer('english')


def stem_phrase(string):
    """
    Стемминг фразы
    :param string: исходная строка
    :return: список основ значимых слов
    """
    return (stem(x) for x in delete_stop_words(tokenize(string)))


def format_result(file, counters):
    """
    Форматирование строки поисковой выдачи
    :param file: имя файла
    :param counters: словарь с результатами поиска по файлу {основа: число вхождений}
    :return: строка
    """
    return "{sep}\n{file}\n\tнайдено слов: {total}\n\tвхождения:\n\t\t{data}\n{sep}\n".format(
        file=file, total=len(counters), sep="="*80,
        data="\n\t\t".join(
            map(lambda x: "{x[0]}: {x[1]}".format(x=x), counters.items())
        )
    )
