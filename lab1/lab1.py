'''
Лабораторная работа № 1.
Задача:
1. Установить интепретатор Python версии 3.11 (или 3.10 — не рекомендуется. но можно),
2. Изучить установку внешних пакетов через `pip` (https://pypi.org),
3. Установить Jupyter Notebook [если используете VS Code, то он нужен для работы интерактивной оболочки],
4. Изучить основные типы данных, операнды, структуры данных (списки, словари, кортежи. множества),
5. Описать структуру Московского зоопарка при помощи встроенных типов и структур данных.,
6. Написать код, который возвращает соседей манула Тимофея (т.е. просто соседние с манулами вольеры)"
Доп:
создание парсера сайта Московского зоопарка с подгрузкой информации о заданном виде животного вместе 
с демонстрацией расположения вольера на карте зоопарка по запросу пользователя 
(in: манул; out: текст + отметка на карте-схеме зоопарка

'''
import pytesseract
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from sympy import Line, Point
from math import degrees
import pandas as pd 
from progress.bar import IncrementalBar

bad_words = ["ЁЁ:'ЕЁЦЭ",
"Ле'г_;тла",
"ЛЭ&”Ш@ЁНФГШЭ",
"Ёд‚ма",
"СЛ@МЫ'[",
"ЛЭШП‘Л‚",
"/Ё%Ё{:Ё?",
"ему;",
"Т…ъ{]г",
")(:КИ!Ё›—",
"]‚::",
"“ледведш",
"ОРЛЗНЬ|"]

adjfs = ["Ядовитые",
"голубые",
"Большая",
"Кустарниковая",
"Гималайский",
"`Полярные/",
"Карликовый",
"Японские",
"Гривистый",
"Гималайский",
"Магелланов",
"полярная",
"Северный",
"Полосатые",
"Красный",
"Гигантская",
"Азиатские",
"Давида",
"Беннета",
"Бурый",
"Серый",
"ночные",
"Малая"]

def convert_img(img):
    def check_first_color(now_color):
        now = list(now_color)
        output = []
        if now[0] < 155 and now[0] > 90:
            output.append(True)
        else:
            output.append(False)
        if now[1] < 257 and now[1] > 100:
            output.append(True)
        else:
            output.append(False)
        if now[2] < 265 and now[2] > 100:
            output.append(True)
        else:
            output.append(False)
        return np.array(output).all()
    
    def check_second_color(now_color):
        now = list(now_color)
        output = []
        if now[0] < 220 and now[0] > 100:
            output.append(True)
        else:
            output.append(False)
        if now[1] < 257 and now[1] > 130:
            output.append(True)
        else:
            output.append(False)
        if now[2] < 200 and now[2] > 100:
            output.append(True)
        else:
            output.append(False)
        return np.array(output).all()
    
    for i in range(len(img)):
        for j in range(len(img[0])):
            if check_second_color(img[i][j]) or check_first_color(img[i][j]):
                img[i][j] = np.array([0, 0, 0])
            else:
                img[i][j] = np.array([255, 255, 255])
    return img

def get_text_location(img, data):
    image_copy = img
    text_list = list()
    for i in range(len(data['text'])):
        if len(data['text'][i]) < 4 or data['text'][i] in bad_words:
            continue

        # извлекаем ширину, высоту, верхнюю и левую позицию для обнаруженного слова
        w = data["width"][i]
        h = data["height"][i]
        l = data["left"][i]
        t = data["top"][i]
        # определяем все точки окружающей рамки
        p1 = Point(l, t)
        p2 = Point(l + w, t)
        p3 = Point(l + w, t + h)
        p4 = Point(l, t + h)
        
        S = p1.distance(p2) * p1.distance(p4)

        center = Line(p1, p3).intersection(Line(p2, p4))
        center = (int(center[0][0]), int(center[0][1]))
        cv.circle(image_copy, center, 4, (0, 255, 0), -1)
        
        text_list.append([data['text'][i], i, center, h])
    return image_copy, text_list

def get_valliers(text_list):
    def get_middle_coor_segment(p1, p2):
        x_middle = int((p1[0] + p2[0]) * 0.5)
        y_middle = int((p1[1] + p2[1]) * 0.5)
        return (x_middle, y_middle)

    angle    = 2
    distance = 1
    text     = 0

    valliers = []

    text_noun = [x for x in text_list if not x[0] in adjfs]
    text_adjf = [x for x in text_list if x[0] in adjfs]
    axis = Line(Point(0, 0), Point(10, 0))
    for adjf in text_adjf:
        fl = 0
        text_distance = []
        for noun in text_noun:
            text_distance.append([noun, 
                                float(Point(noun[2]).distance(Point(adjf[2]))), 
                                degrees(Line(Point(noun[2]), Point(adjf[2])).angle_between(axis)),
                                get_middle_coor_segment(Point(noun[2]), Point(adjf[2]))])
        
        for text in text_distance:
            if text[angle] < 4 or text[angle] > 175:
                if text[distance] < 235:
                    #print(adjf[0], '----', text[0][0], '---', text[3])
                    valliers.append([adjf[0] + " " + text[0][0], text[0][1], text[3]])
                    fl = 1
                    continue
        if not fl:
            text_distance.sort(key= lambda x: x[1])
            if text_distance[0][1] < 500:
                #print(adjf[0], '----', text_distance[0][0][0], '---', text_distance[0][3])
                valliers.append([adjf[0] + " " + text_distance[0][0][0], text_distance[0][0][1], text_distance[0][3]])

    id_found_noun = [x[1] for x in valliers]
    not_found_noun = [x[:3] for x in text_noun if not x[1] in id_found_noun]
    
    return valliers + not_found_noun

def get_neighboring_valliers(valliers):
    distance = []
    for vallier in valliers:
        vallier_dist = list()
        not_valliers = [x for x in valliers if not x[0] == vallier[0]]
        for x in not_valliers:
            vallier_dist.append([x, 
                            float(Point(vallier[2]).distance(Point(x[2])))])
        vallier_dist.sort(key=lambda x: x[1])
        vallier_dist = vallier_dist[:4]
        distance.append([vallier, vallier_dist])
    return distance

def convert_to_graph(distance):
    preparing_text = str()
    preparing_text += "digraph g {\n\trankdir=LR;\n"
    for dist in distance:
        for x in dist[1]:
            preparing_text += "\t\"%s\" -> \"%s\" " % (dist[0][0] + " " + str(dist[0][1]), x[0][0] + " " + str(x[0][1]))
    preparing_text += "}\n"
    print(preparing_text, file = open("/tmp/aux.dot", 'w'))
    return preparing_text

def get_id(text_list, name):
    return [x for x in text_list if x[0] == name][0][1]

def get_neighbors(dist, id_):
    return [x for x in dist if x[0][1] == id_][0]

def nice_print_neighbors(neightbors):
    print(f"Соседи вольера {neightbors[0][0]}:")
    for x in neightbors[1]:
        print(" ", x[0][0])

if __name__ == '__main__':
    #Скачали карту с сайта зоопарка (расчехлять request для этого не считаю нужным), но она большого размера и шакального качества
    #из чего следует, что надо цвета нужного текста (с названиями животных)
    #заменить на чёрный цвет, а остальные на белый.
    #Код работает долго, можно применить множество разных ухищрений,
    #но пока что просто сохраним и будем использовать дальше
    #Update: Пришлось немного подшамать в фотошопе.
    #cv.imwrite("kkkk.jpg", convert_img(cv.imread("zoomapnew1.jpg"))) 
    image = cv.imread("kkkk.jpg")
    print("[INFO] - Загрузили рисунок московского зоопарка")
    data = pytesseract.image_to_data(image, lang='rus', output_type=pytesseract.Output.DICT)
    print("[INFO] - Разобрали рисунок плана московского зоопарка")
    image_copy, text_list = get_text_location(image, data)
    print("[INFO] - Разобрались с расположением слов в пространстве")
    valliers = get_valliers(text_list)
    print("[INFO] - Получили список вальеров с их местоположением")
    dist = get_neighboring_valliers(valliers)
    print("[INFO] - Разобрались со связями вальеров (кривовастенько)")
    graph = convert_to_graph(dist)
    print("[INFO] - Переделали всё в граф")

    manul_id = get_id(text_list, "Манул")
    manul_neightbors = get_neighbors(dist, manul_id)
    nice_print_neighbors(manul_neightbors)

    cv.imwrite('lines.jpg', image_copy)
    print(dist, file=open('aaaa.txt', 'w'))
    print("[INFO] - Записали связи вольеров в файл 'aaaa.txt'")