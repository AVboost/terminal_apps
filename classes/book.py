
class Book:
 
	def __init__(self, title, author, year, status="в наличии", book_id=None):
		self.title = title
		self.author = author
		self.year = year
		self.status = status
		self.id = book_id

	def to_library(self):
		return {
			"id": self.id,
			"title": self.title,
			"author": self.author,
			"year": self.year,
			"status": self.status
		}
	
	@classmethod
	def from_library(cls, data):
		return cls(data['title'], data['author'], data['year'], data['status'], data['id'])
	