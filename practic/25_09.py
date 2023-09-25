from random import randint

def first():
	l = [randint(0, 100) for x in range(50)]
	print("Изначальный список:")
	print(l)
	print("Перевёрнутый:")
	print(l[::-1])

if __name__ == '__main__':
	first()