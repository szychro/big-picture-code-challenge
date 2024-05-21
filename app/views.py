from flask import Blueprint, request, jsonify
from . import db
from .models import Book
from .schema import book_schema, books_schema
from .fetch_books import fetch_books
from .isbn_validation import is_valid_isbn

main = Blueprint('main', __name__)

@main.route('/isbn/<isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    is_valid, isbn_type = is_valid_isbn(isbn)
    
    if not is_valid:
        return jsonify({"error": "Invalid ISBN"}), 400
    
    book = Book.query.filter_by(isbn_13=isbn).first() if isbn_type == 'ISBN-13' else Book.query.filter_by(isbn_10=isbn).first()
    
    if book is None:
        book_details = fetch_books(isbn)
        if book_details is None:
            return jsonify({"error": "Book not found"}), 404
        return jsonify(book_details)
    
    return jsonify(book_schema(book))

@main.route('/books', methods=['POST'])
def create_book():
    try:
        isbn = request.json.get('isbn')
        if not isbn:
            return jsonify({"error": "ISBN is required"}), 400

        is_valid, isbn_type = is_valid_isbn(isbn)
        if not is_valid:
            return jsonify({"error": "Invalid ISBN"}), 400

        existing_book = Book.query.filter_by(isbn_13=isbn).first() if isbn_type == 'ISBN-13' else Book.query.filter_by(isbn_10=isbn).first()
        if existing_book:
            return jsonify({"error": "Book already registered"}), 400

        book_details = fetch_books(isbn)
        if book_details is None:
            return jsonify({"error": "Book not found"}), 404

        new_book = Book(
            isbn_10=book_details['isbn_10'],
            isbn_13=book_details['isbn_13'],
            title=book_details['title'],
            author=book_details['author'],
            summary=book_details['summary'],
            cover=book_details['cover']
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify(book_schema(new_book)), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@main.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify(books_schema(books))
