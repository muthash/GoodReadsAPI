store = []

class BookShelf():
    shelf_id = 0
    
    def __init__(self, title, genre, status, email):
        BookShelf.shelf_id += 1
        self.id = BookShelf.shelf_id
        self.title = title
        self.genre = genre
        self.status = status
        self.email = email
    
    def update_status(self, status):
        self.status = status
    
    def serialize(self):
        return {
            'book_id': self.id,
            'title': self.title,
            'genre':  self.genre,
            'status': self.status
        }

    def __repr__(self):
        return 'Book is {}'.format(self.title)