""" Лабораторная работа №2 по Случайным процессам """
""" Тема: Случайные блуждания """
""" 
Данный код моделирует движение животных в поисках корма со следующими условиями: 
    - Существует двумерная плоскость, покрытая сеткой
    - В начальный момент времени животное находится в произвольном узле сетки
    - При увеличении времени на 1, животное может перейти только в соседний узел 
    - Переход между узлами не равновероятен 
    и между мекоторыми узлами вероятность перехода должна быть равна нулю (обрыв)
    (в данном случае, для генерирования вероятностей перехода между узлами 
    применяется равномерное распределение np.random.rand(), которое задает случайные значения от 0 до 1)
    - В произвольном узле (не совпадающим с исходным узлом животного) установлен датчик, показывающий, 
    через сколько шагов животное до него дойдет и дойдет ли вообще
    - В результате работы программы строится гистограмма - сколько попыток требуется, 
    чтобы достичь датчика, а также график - карта перемещений

"""
""" Для запуска программы нет каких-то специфических инструкций, просто прогоняем код.
Сначала появится гистограмма, после ее закрытия (в зависимости от того, где запускается код) 
появляется и график траекторий блуждания, который будет меняться со временем. 
Отображение легенды означает, что все изменения на графике произошли. 
Красный квадрат - датчик, кружки - начальные положения животных.
Серым отмечены пути тех животных, что не дошли до датчика.

Для получения других результатовв коде можно поменять: 
size (размер сетки), animals (количество животных), 
mask в функции generate_probabilities() (сколько сгенерируется обрывов),
число в paths[:5] в ф-ии animate_paths() (траектории скольких животных отобразятся на графике),
число в plt.pause(0.2) (задержка между шагами) """

import numpy as np
import matplotlib.pyplot as plt
import random

# import time

# размер равносторонней сетки (можно изменить для других экспериментов)
size = 10

# количество животных (можно увеличить для более точных результатов на гистограмме)
animals = 100


# создание пустой сетки заданного размера:
def generate_grid(size):
    return np.zeros((size, size))


# размещение датчика в случайном узле сетки:
def place_sensor(size):
    return random.randint(0, size - 1), random.randint(0, size - 1)


# генерация матрицы вероятностей перехода между узлами:
def generate_probabilities(size):
    # равномерное распределение:
    probabilities = np.random.rand(size, size, 4)  # 4 направления: вверх, вниз, влево и вправо
    mask = np.random.rand(size, size) < 0.2  # [0; 1] - какая часть узлов будет обрываться
    """__________________________________^_____ можно поменять, чтобы было больше/меньше обрывов """
    probabilities[mask] = [0, 0, 0, 0]  # обнуление вероятностей в узлах, где обрыв

    for i in range(size):
        for j in range(size):
            probs = probabilities[i, j]
            if np.sum(probs) > 0:  # ненулевые вероятности
                # здесь обнуляются вероятности, которые ведут за пределы сетки:
                probs[0] = 0 if i == 0 else probs[0]  # верх
                probs[1] = 0 if i == size - 1 else probs[1]  # низ
                probs[2] = 0 if j == 0 else probs[2]  # лево
                probs[3] = 0 if j == size - 1 else probs[3]  # право
                # здесь нормализуются вероятности, чтобы в каждом узле их сумма равнялась единице:
                total = np.sum(probs)
                if total > 0:
                    probabilities[i, j] = probs / total
                else:
                    probabilities[i, j] = [0.25, 0.25, 0.25, 0.25]
                # если сумма всех направлений total > 0,
                # то делим каждую вероятность на total
                # если все вероятности узла равны нулю (будто он окружен обрывами),
                # устанавливаем равную вероятность для всех направлений
            else:
                probabilities[i, j] = [0.25, 0.25, 0.25, 0.25]  # то же самое

    return probabilities


# один шаг случайного блуждания животного:
def move_animal(pos, probabilities, size):
    i, j = pos
    if not (0 <= i < size and 0 <= j < size):  # проверка, что индексы в пределах массива
        return pos

    moves = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    prob = probabilities[i, j]
    if np.sum(prob) == 0:  # если нет доступных ходов, оставляем на месте
        return pos
    move = np.random.choice(4, p=prob)
    new_pos = moves[move]
    return (max(0, min(size - 1, new_pos[0])), max(0, min(size - 1, new_pos[1])))  # ограничение пределов сетки


# животные блуждают по сетке до датчика:
def simulate_walks(size, sensor, animals):
    step_counts = []
    paths = []
    probabilities = generate_probabilities(size)

    for _ in range(animals):
        while True:
            start = (random.randint(0, size - 1), random.randint(0, size - 1))
            if start != sensor:
                break

        path = [start]
        steps = 0
        while path[-1] != sensor:
            new_pos = move_animal(path[-1], probabilities, size)
            if new_pos == path[-1]:  # если животное застряло,
                break  # прерываем
            path.append(new_pos)
            steps += 1

        # if path[-1] == sensor: # на графике отобразятся только те животные, что успешно дошли до датчика
        #     step_counts.append(steps)
        #     paths.append(path)

        paths.append(path)  # на графике отобразятся все животные
        if path[-1] == sensor:
            step_counts.append(steps)

    return step_counts, paths


# анимация траекторий движения животных:
def animate_paths(size, sensor, paths):
    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-0.5, size - 0.5)
    ax.set_ylim(-0.5, size - 0.5)
    ax.set_xticks(range(size))
    ax.set_yticks(range(size))
    ax.grid(True)
    ax.scatter(sensor[1], sensor[0], c='r', marker='s', label='Датчик')

    colors = ['b', 'g', 'm', 'c', 'y', 'orange', 'purple', 'pink', 'lime', 'navy']

    """________ можно поменять ______\/______ для отображения большего/меньшего количества траекторий на графике """
    for idx, path in enumerate(paths[:5]):  # на графике отобразятся первые 5 траекторий,
        # чтобы не перегружать график слишком большим количеством линий
        x, y = zip(*path)

        # color = colors[idx % len(colors)]

        # если животное не дошло до датчика, то цвет его пути будет серым:
        if path[-1] == sensor:
            color = colors[idx % len(colors)]
        else:
            color = 'gray'

        ax.scatter(y[0], x[0], c=color, marker='o', label=f'Старт {idx + 1} животного')

        for i in range(len(path) - 1):
            ax.plot([y[i], y[i + 1]], [x[i], x[i + 1]], color=color, linestyle='-', alpha=0.5)
            plt.pause(0.2)  # задержка между шагами
            """________^_____ можно поменять, чтобы ускорить/замедлить анимацию """

    plt.ioff()
    plt.legend()
    plt.show()


# гистограмма количества шагов, необходимых для достижения датчика:
def plot_histogram(step_counts):
    plt.figure(figsize=(7, 5))
    """ макс. кол-во колонок __\/______ можно увеличить для более детализированной гистограммы """
    plt.hist(step_counts, bins=20, alpha=0.75, color='b', edgecolor='black')
    plt.xlabel('Шаги до датчика')
    plt.ylabel('Частота')
    plt.title('Гистограмма количества шагов')
    plt.show()


# случайное положение датчика:
sensor = place_sensor(size)

# симуляция блуждания:
step_counts, paths = simulate_walks(size, sensor, animals)

# гистограмма количества шагов до датчика:
plot_histogram(step_counts)

# анимация перемещения животных:
animate_paths(size, sensor, paths)