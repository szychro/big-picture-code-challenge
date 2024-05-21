def book_schema(book):
    return {
        "isbn_10": book.isbn_10,
        "isbn_13": book.isbn_13,
        "title": book.title,
        "author": book.author,
        "summary": book.summary,
        "cover": book.cover
    }

def books_schema(books):
    return [book_schema(book) for book in books]
