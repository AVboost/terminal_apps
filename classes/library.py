from .book import Book
import json

class Library:

	def __init__(self, data_path):
		self.data_path = data_path
		self.data = self.read_data()


	def read_data(self):
		'''
		Возвращает из data.json список объектов класса "Book", каждый из которых содержит информацию о книге.
		Если файл data.json отсутствует, создаст его и вернёт пустой список
		'''
		try:
			with open(self.data_path, 'r', encoding='utf-8') as f:
				data = json.load(f)
				return [Book.from_library(book) for book in data]
		except (json.JSONDecodeError):
			pass # если файл пустой просто возвращаем пустой список
		except (FileNotFoundError):
			open(self.data_path, 'w')
		return []


	def write_to_data(self):
		'''
		Записывает все имеющиеся книги из self.data в файл data.json
		'''
		try:
			with open(self.data_path, 'w', encoding="utf-8") as write_file:
				json.dump([book.to_library() for book in self.data], write_file)
		except IOError as error:
			print(f'Ошибка при записи в файл: {error}')


	def get_id(self):
		'''
		Генерирует уникальный id для книги (целое число).
		Находит максимальный существующий id и возвращает значение, увеличенное на 1.
		'''
		if not self.data:
			return 1
		else:
			next_id = max(book.id for book in self.data)
			return next_id + 1

	def add_book(self, title, author, year):
		'''
		Добавляет созданную пользователем книгу в библиотеку:
		Принимает значения, которые ввёл пользователь: название, авто, год публикации
		Получает уникальный id для книги, вызывая функцию get_id
		Создаёт объект класса "Book" и добавляет его в общий список книг.
		Запускает перезапись файла json
		'''
		book_id = self.get_id()
		book = Book(title, author, year, book_id=book_id)
		self.data.append(book)
		self.write_to_data()
		print(f'Книга "{book.title}" добавлена, присвоен id {book.id}')

	def delete_book(self, id_to_delete):
		'''
		Удаляет книгу из общего списка книг:
		Принимает id, который ввёл пользователь
		Если книга с таким id есть в базе - удалит её и запустит перезапись файла json
		'''
		book_found = False
		for book in self.data:
			if book.id == id_to_delete:
				book_found = True
				self.data.remove(book)
				self.write_to_data()
				print(f'Книга "{book.title}" удалена')
				break
		if not book_found:
			print("Книга не найдена")


	def find_book(self, search_key, reg_exp):
		'''
		Находит книгу по указанному полю и значению:
		принимает указанное пользователем поле (search_key) и значение (reg_exp)
		Ищет все книги по указанному полю и значению, разбивает результат на частичное и полное совпадения
		Показывает пользователю все результаты поиска
		'''
		full_matches = []
		partial_matches = []

		target = str(reg_exp).lower()

		for book in self.data:
			attr_value = str(getattr(book, search_key)).lower()
			if search_key in ['title', 'author']:
				if attr_value == target:
					full_matches.append(book)
				elif target in attr_value:
					partial_matches.append(book)
			else:
				if attr_value == target:
					full_matches.append(book)

		if full_matches:
			print(f'Найдено полное совпадение у книг:')
			for book in full_matches:
				print(f'ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}')
		else:
			print('Полное совпадение не найдено.')

		if partial_matches:
			print(f'Найдено частичное совпадение у книг:')
			for book in partial_matches:
				print(f'ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}')
		else:
			if search_key in ['title', 'author']:
				print('Частичное совпадение не найдено.')


	def show_all(self):
		'''
		Печатает все книги и содержания всех полей книг
		'''
		if not self.data:
			print('Пустая библиотека. Добавьте хотя бы одну книгу')
		else:
			for book in self.data:
				print(f'ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}')


	def change_status(self, id_to_change_status):
		'''
		Изменяет статус книги на противоположный:
		Получает от пользователя id книги, у которой нужно изменить статус
		В случае подтверждения операции пользователем менят статус "в наличии" на "выдан" или наоборот
		'''
		book_found = False
		for book in self.data:
			if book.id == id_to_change_status:
				book_found = True
				opposit_status = "выдана" if book.status == "в наличии" else "в наличии"
				print(f'Книга "{book.title}". \nТекущий статус "{book.status}"')
				confirmation = input(f'Изменить статус на "{opposit_status}"? [да/нет]: ')
				if confirmation.lower() in ['да', 'д', 'lf']:
					book.status = opposit_status
					self.write_to_data()
					print(f'Статус изменён на "{opposit_status}"')
				else:
					print("Статус книги не изменён")
				break
		if not book_found:
			print("Книга не найдена")
