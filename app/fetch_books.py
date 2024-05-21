import requests

def fetch_books(isbn):
    url = f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json'
    res = requests.get(url).json()
    book_data = res.get(f'ISBN:{isbn}')

    if not book_data:
        return None
    
    authors = book_data.get('authors', [])
    cover = book_data.get('cover', {}).get('large')
    identifiers = book_data.get('identifiers', {})
    
    return {
        "title": book_data.get('title'),
        "author": authors[0]['name'] if authors else 'Unknown Author',
        "summary": book_data.get("notes", "No summary"),
        "cover": cover,
        "isbn_10": identifiers.get("isbn_10", [""])[0],
        "isbn_13": identifiers.get("isbn_13", [""])[0]
    }
