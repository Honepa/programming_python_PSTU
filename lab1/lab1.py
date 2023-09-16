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
from PIL import Image
import numpy as np
from sympy import Line, Point

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
        if len(data['text'][i]) < 4:
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
        
        text_list.append([data['text'][i], i, center, S])
    return image_copy, text_list

def get_valliers(text_list):
    pass

if __name__ == '__main__':
    #Скачали карту с сайта зоопарка (расчехлять request для этого не считаю нужным), но она большого размера и шакального качества
    #из чего следует, что надо цвета нужного текста (с названиями животных)
    #заменить на чёрный цвет, а остальные на белый.
    #Код работает долго, можно применить множество разных ухищрений,
    #но пока что просто сохраним и будем использовать дальше
    #Update: Пришлось немного подшамать в фотошопе.
    #cv.imwrite("kkkk.jpg", convert_img(cv.imread("zoomapnew1.jpg"))) 
    image = cv.imread("kkkk.jpg")

    data = pytesseract.image_to_data(image, lang='rus', output_type=pytesseract.Output.DICT)
    image_copy, text_list = get_text_location(img, data)
    valliers = get_valliers(text_list)

    cv.imwrite('lines.jpg', image_copy)
    print(text_list, file=open('aaaa.txt', 'w'))