""" Лабораторная работа №1 по Случайным процессам """
""" Тема: Марковские цепи """
""" 
В данном коде:
1) Берется большой научный текст;
2) Проводится лемматизация текста;
3) Реализуется интеллектуальный поиск.

Алгоритм:
    Ввод: N слов
    Вывод: 1 подсказка
    Если для N слов нет подсказки, то ищется для N-1
    Если совсем нет подсказок, выдается предупреждение
"""
""" Для запуска программы нет каких-то специфических инструкций, просто прогоняем код 
и вводим запрос в консоль. Для выхода из цикла можно нажать Enter без ввода запроса.
Можно выбрать другой текст для реализации интеллектуального поиска. Для этого можно поменять 
значение у file_path или, что удобнее, раскомментировать нужную строку. 
Также можно добавить свой текст.txt в ту же директорию, где находится код, и изменить file_path.
Тексты (некоторые источники недостоверны, в файлах в основном текст, нет формул):
    - Poisson.txt - текст о Пуассоновском процессе (432 слова, 2 892 знака без пробелов)
    - Markov.txt - текст о Марковском процессе (1 688 слов, 11 275 знаков без пробелов)
    - Random_walk.txt - текст о Случайных блужданиях (1 774 слова, 12 017 знаков без пробелов) """

import os
import re
from collections import defaultdict
# Пакет для лемматизации текста на русском языке:
# import pymorphy2
from pymystem3 import Mystem


class MarkovSearch:
    # инициализация класса и построение цепи Маркова:
    def __init__(self, text):
        self.markov_chain = defaultdict(lambda: defaultdict(int))
        self.mystem = Mystem()
        self.build_chain(text)

    # очистка текста, лемматизация и разбиение на слова:
    def preprocess(self, text):
        text = text.lower()     # перевод символов в нижний регистр
        text = re.sub(r'[^а-яё\s]', '', text)   # очистка текста перед лемматизацией
        # (удаление всех символов, кроме кириллических в нижнем регистре и пробелов)
        # чтобы избежать влияние знаков препинания и посторонних символов
        words = self.mystem.lemmatize(text)     # лемматизация
        return [word.strip() for word in words if word.strip()]     # очистка списка
        # от лишних пробелов и пустых строк

    # # простая лемматизация (замена окончаний, если возможно):
    # def lemmatize(self, word):
    #     # простая лемматизация (замена окончаний, если возможно)
    #     if word.endswith(('ые', 'ие', 'ый', 'ий', 'ое', 'ая', 'яя')):
    #         return word[:-2]  # - окончания прилагательных
    #     if word.endswith(('ов', 'ев', 'ей', 'ами', 'ями', 'ем', 'ом')):
    #         return word[:-2]  # - окончания существительных
    #     if word.endswith(('ть', 'ти', 'ешь', 'ет', 'ем', 'ут', 'ют')):
    #         return word[:-2]  # - окончания глаголов
    #     return word
    #
    # # cоздание Марковской цепи:
    # def build_chain(self):
    #     words = self.preprocess(self.text)
    #     lemmatized_words = [self.lemmatize(word) for word in words]
    #     for i in range(len(lemmatized_words) - 1):
    #         word, next_word = lemmatized_words[i], lemmatized_words[i + 1]
    #         self.markov_chain[word][next_word] += 1

    # создание Марковской цепи:
    def build_chain(self, text):
        words = self.preprocess(text)
        # создание пар последовательных слов:
        for word, next_word in zip(words, words[1:]):
            self.markov_chain[word][next_word] += 1

    # получение наиболее вероятного следующего слова:
    def get_suggestion(self, query):
        words = self.preprocess(query)
        while words:
            last_word = words[-1]
            if last_word in self.markov_chain:
                return max(self.markov_chain[last_word], key=self.markov_chain[last_word].get)
            words.pop()
        return "Нет подсказки"


# чтение текста из файла:
script_dir = os.path.dirname(os.path.abspath(__file__))     # путь к файлу с кодом
# путь к файлу с текстом, который лежит в папке с кодом:
file_path = os.path.join(script_dir, "Poisson.txt")   # текст о Пуассоновском процессе
# file_path = os.path.join(script_dir, "Markov.txt")   # текст о Марковском процессе
# file_path = os.path.join(script_dir, "Random_walk.txt")   # текст о Случайных блужданиях

try:
    with open(file_path, "r", encoding="utf-8") as file:
        text_data = file.read()
except FileNotFoundError:
    print(f"Файл {file_path} не найден.")
    text_data = ""

# работа с пользователем (ввод и вывод):
if text_data:
    markov_search = MarkovSearch(text_data)
    while True:
        query = input("Введите запрос (или нажмите Enter для выхода): ").strip()
        if not query:
            break
        print(f'Подсказка: {markov_search.get_suggestion(query)}')