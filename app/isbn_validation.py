def is_valid_isbn(isbn):
    if not isbn.isdigit():
        return False, None
    
    if len(isbn) == 10:
        return True, 'ISBN-10'
    elif len(isbn) == 13:
        return True, 'ISBN-13'
    
    return False, None
