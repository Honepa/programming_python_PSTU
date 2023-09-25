from random import randint

def first():
	l = [randint(0, 100) for x in range(50)]
	print("Изначальный список:")
	print(l)
	print("Перевёрнутый:")
	print(l[::-1])

def second():
	l1 = [randint(0, 100) for x in range(10)]
	l2 = [randint(0, 100) for x in range(10)]
	
	print("Первый список:")
	print(l1)
	print("Второй список:")
	print(l2)

	l3 = list()
	l3 += l1[::2]
	l3 += l2[1::2]
	
	print("Третий список")
	print(l3)


if __name__ == '__main__':
	#first()
	second()