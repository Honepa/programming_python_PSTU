import pytesseract
import cv2 as cv
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

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



if __name__ == '__main__':
    #cv.imwrite("kkkk.jpg", convert_img(cv.imread("zoomapnew1.jpg")))
    image = cv.imread("kkkk.jpg")

    data = pytesseract.image_to_data(image, lang='rus', output_type=pytesseract.Output.DICT)
    image_copy = image
    text_list = list()
    for i in range(len(data['text'])):
        if len(data['text'][i]) < 4:
            continue

        text_list.append([data['text'][i], i])
    # извлекаем ширину, высоту, верхнюю и левую позицию для обнаруженного слова
        w = data["width"][i]
        h = data["height"][i]
        l = data["left"][i]
        t = data["top"][i]
        # определяем все точки окружающей рамки
        p1 = (l, t)
        p2 = (l + w, t)
        p3 = (l + w, t + h)
        p4 = (l, t + h)
        # рисуем 4 линии (прямоугольник)
        image_copy = cv.line(image_copy, p1, p2, color=(255, 0, 0), thickness=2)
        image_copy = cv.line(image_copy, p2, p3, color=(255, 0, 0), thickness=2)
        image_copy = cv.line(image_copy, p3, p4, color=(255, 0, 0), thickness=2)
        image_copy = cv.line(image_copy, p4, p1, color=(255, 0, 0), thickness=2)
    cv.imwrite('lines.jpg', image_copy)
    print(text_list, file=open('aaaa.txt', 'w'))