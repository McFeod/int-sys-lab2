import os
from collections import Counter

from utils import stem_phrase, format_result


class Engine:
    def __init__(self, file_path, extension='.txt'):
        self.file_path = file_path
        self.file_extension = extension
        self.phrase = None
        self.counts = None

    def search_phrase(self, string, max_items=None):
        """
        Запуск поиска
        :param max_items: ограничение числа результатов выдачи
        :param string: запрос
        """
        self.counts = {}
        self.phrase = set(stem_phrase(string))
        self.walk()
        return self.perform_result(max_items)

    def search_in_file(self, filename):
        """
        Поиск по файлу
        :param filename: путь к файлу
        """
        result = Counter()
        with open(filename) as file:
            for line in file:
                for word in stem_phrase(line):
                    if word in self.phrase:
                        result[word] += 1
        self.counts[filename] = result

    def walk(self):
        """
        рекурсивный обход файлов в директории self.file_path и запуск поиска по файлам с расширением self.file_extension
        """
        for d, dirs, files in os.walk(self.file_path):
            for filename in files:
                if filename.endswith(self.file_extension):
                    self.search_in_file(os.path.join(d, filename))

    def perform_result(self, items):
        """
        Фильтрация и сортировка результатов поиска
        :param items: максимальное число элементов в выдаче
        :return:
        """
        result = [i for i in self.counts.items() if len(i[1]) > 0]  # убираем пустые результаты

        def sort_order(dict_pair):
            return (
                len(dict_pair[1]),  # число найденных слов
                sum(map(lambda x: x[1], dict_pair[1].items()))  # общее число вхождений
            )

        result.sort(key=sort_order, reverse=True)  # сортируем результаты
        return map(lambda x: format_result(x[0], x[1]), result[:items])
