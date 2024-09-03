from application.models import *
from flask import jsonify, request, current_app, send_file
from application.database import db
from main import app
from application.auth import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import cache
from werkzeug.utils import secure_filename
import os
import uuid
from urllib.parse import unquote
from application.celery_tasks import export_books


@app.route('/books', methods=['GET'])
@jwt_required()
# @cache.cached(timeout=600)
def get_books():
    try:
        books = Books.query.all()
        return jsonify({'books': [book.serialize() for book in books]}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/books/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def get_book(id):
    try:
        book = Books.query.get(id)
        return jsonify({'book': book.serialize()}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/books/requested/<int:id>', methods=['GET'])
@jwt_required()
def is_requested(id):
    try:
        user = Users.query.filter_by(email=get_jwt_identity()['email']).first()
        book = BorrowedBooks.query.filter_by(book_id=id, user_id=user.id, returned=False).first()
        if book:
            return jsonify({'requested': True}), 200
        else:
            return jsonify({'requested': False}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/books/pending', methods=['GET'])
@admin_required
def get_pending_books():
    try:
        books = BorrowedBooks.query.filter_by(grant=False).all()
        return jsonify({'books': [book.serialize() for book in books]}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/books', methods=['POST'])
@admin_required
def add_book():
    try:
        # Access form data
        title = request.form['title']
        print(title)
        author = request.form['author']
        genre = request.form['genre']
        publisher = request.form['publisher']
        desc = request.form['desc']
        image = request.form['image']

        # Handling the PDF file upload
        pdf_file = request.files['document']
        
        print(pdf_file)
        
        document_relative_path = None  # Default if no file is uploaded
        if pdf_file:
            filename = secure_filename(pdf_file.filename)
            # Ensure filename is unique
            filename = f"{uuid.uuid4().hex}_{filename}"
            pdf_path = os.path.join(current_app.config['PDF_UPLOAD_FOLDER'], filename)
            pdf_file.save(pdf_path)
            document_relative_path = os.path.join('pdfs', filename)

        # Create the book instance
        book = Books(
            title=title, author=author, genre=genre, publisher=publisher, 
            desc=desc, image=image, document=document_relative_path
        )

        # Adding sections if they exist in the form
        section_ids = request.form.getlist('section_id')  # This expects section_id to be a list of IDs
        for section_id in section_ids:
            section = Sections.query.get(section_id)
            if section:
                book.sections.append(section)

        db.session.add(book)
        db.session.commit()

        return jsonify({'message': 'Book added successfully'}), 201

    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

    
@app.route('/books/section/<int:section_id>', methods=['GET'])
@cache.cached(timeout=60)
def get_books_by_section(section_id):
    try:
        books = Books.query.filter(Books.sections.any(id=section_id)).all()
        return jsonify({'books': [book.serialize() for book in books]}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/books/granted', methods=['GET'])
@admin_required
def get_granted_books():
    try:
        books = BorrowedBooks.query.filter_by(grant=True).all()
        return jsonify({'books': [book.serialize() for book in books]}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

    
@app.route('/books/<int:id>', methods=['PUT'])
@admin_required
def update_book(id):
    try:
        data = request.get_json()
        book = Books.query.get(id)
        book.title = data['title']
        book.author = data['author']
        book.genre = data['genre']
        book.publisher = data['publisher']
        book.desc = data['desc']
        book.image = data['image']
        book.sections.clear()
        for section_id in data['section_id']:
            section = Sections.query.get(section_id)
            book.sections.append(section)
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/books/<int:id>', methods=['DELETE'])
@admin_required
def delete_book(id):
    try:
        book = Books.query.get(id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/mybooks', methods=['GET'])
@jwt_required()
def get_my_books():
    try:
        user = Users.query.filter_by(email=get_jwt_identity()['email']).first()
        borrowed_books = BorrowedBooks.query.filter_by(user_id=user.id, grant=True, returned=False).all()
        # Serialize borrowed books including document URL
        serialized_books = []
        for borrowed_book in borrowed_books:
            book = borrowed_book.book  # Access the associated book through the relationship
            serialized_book = borrowed_book.serialize()
            
            serialized_book['document'] = book.document
            
            serialized_books.append(serialized_book)
        
        return jsonify({'books': serialized_books}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/books/request/<int:id>', methods=['POST'])
@jwt_required()
def request_book(id):
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=get_jwt_identity()['email']).first()
        book = Books.query.get(id)
        user_borrowed_books = BorrowedBooks.query.filter_by(user_id=user.id, grant=True, returned=False).all()
        if len(user_borrowed_books) >= 5:
            return jsonify({'message': 'You can borrow only 4 books at a time'}), 400
        borrowed_book = BorrowedBooks(username=user.username, title=book.title, section=book.sections[0].title, days=data['days'], book_id=book.id, user_id=user.id)
        db.session.add(borrowed_book)
        db.session.commit()
        return jsonify({'message': 'Book requested successfully'}), 201
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/books/grant/<int:id>', methods=['POST'])
def grant_book(id):
    try:
        borrowed_book = BorrowedBooks.query.get(id)
        borrowed_book.grant = True
        borrowed_book.borrowed_date = datetime.now(timezone('Asia/Kolkata'))
        db.session.commit()
        return jsonify({'message': 'Book granted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/books/return/<int:id>', methods=['POST'])
def return_book(id):
    data = request.get_json()
    try:
        borrowed_book = BorrowedBooks.query.get(id)
        user = Users.query.filter_by(username=data['username']).first()
        if borrowed_book.user_id == user.id:
            borrowed_book.returned = True
            borrowed_book.returned_date = datetime.now(timezone('Asia/Kolkata'))
            db.session.delete(borrowed_book)
            db.session.commit()
            return jsonify({'message': 'Book returned successfully'}), 200
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/books/revoke/<int:id>', methods=['POST'])
def revoke_book(id):
    try:
        borrowed_book = BorrowedBooks.query.get(id)
        borrowed_book.grant = False
        db.session.delete(borrowed_book)
        db.session.commit()
        return jsonify({'message': 'Book revoked successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/pdf/<path:filename>', methods=['GET'])
def get_pdf(filename):
    try:
        return send_file(os.path.join(app.static_folder, current_app.config['PDF_UPLOAD_FOLDER'], filename), as_attachment=True)
    except Exception as e:
        print(e)
        return jsonify({'message': 'PDF file not found'}), 404
    

@app.route('/books/export', methods=['GET'])
@admin_required
def export():
    export_books.delay()
    return jsonify({'message': 'Exporting books'}), 200