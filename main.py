import os
import sys
import time
import datetime
from classes.library import Library


def main():

	script_path = os.path.dirname(os.path.abspath(__file__))
	data_path = os.path.join(script_path, 'data.json')
	library = Library(data_path)
	current_year = datetime.datetime.now().year

	while True:
		print('\nМеню:')
		print('1. Добавить книгу')
		print('2. Удалить книгу')
		print('3. Найти книгу')
		print('4. Показать все книги')
		print('5. Изменить статус книги')
		print('6. Выйти')

		choice = input('\nвведите номер команды: ')

		if choice == '1':
			title = input('Введите название: ')
			author = input('Введите автора: ')
			# проверяет, что введён допустимый год публикации (меньше текущего года и больше года выпуска первой в мире книги)
			while True:
				try:
					year = int(input('Введите год издания: '))
					if year > current_year:
						print(f'Год {year} ещё не наступил. Введите год по {current_year}')
					elif year < 868:
						print(f'В {year} году книги ещё не печатали. Первая в мире печатная книга: "Алмазная сутра", напечатанная в Китае в 868 году.')
					else:
						break
				except ValueError:
					print('Введите корректный год (целое число)')

			library.add_book(title, author, year)

		elif choice == '2':
			# проверяет, что введен допустимый id - целое число
			while True:
				try:
					id_to_delete = int(input('введите id книги, которую хотите удалить: '))
					break
				except ValueError:
					print('Неверный формат ID. Должно быть целое число')
			library.delete_book(id_to_delete)

		elif choice == '3':
			print('По какому полю искать книгу?')
			print('1. Автор \n2. Название \n3. id')
			# пользователь выбирает по какому полю нужно искать книгу (название, автор или id)
			while True:
					field = input('введине номер поля: ')
					if field in ['1', '2', '3']:
						if field == '1':
							search_key = 'author'
						elif field == '2':
							search_key = 'title'
						elif field == '3':
							search_key = 'id'
						break
					else:
						print('Некорректный выбор. Введите 1, 2 или 3')
			reg_exp = input('Введите значение для поиска: ')
			library.find_book(search_key, reg_exp)


		elif choice == '4':
			library.show_all()

		elif choice == '5':
			# проверяет, что введен допустимый id - целое число
			while True:
				try:
					id_to_change_status = int(input('Введите id книги, статус которой хотите изменить: '))
					break
				except ValueError:
					print('Неверный формат ID. Должно быть целое число')
			library.change_status(id_to_change_status)

		elif choice == '6':
			print('Выхожу из программы...')
			sys.exit()

		else:
			print('Нет такой команды. Введите команду от 1 до 6.')

		time.sleep(3)


if __name__ == '__main__':
	main()