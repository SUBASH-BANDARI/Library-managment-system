from application.models import *
from flask import jsonify, request
from application.database import db
from main import app
from application.auth import admin_required
from flask_jwt_extended import jwt_required

@app.route('/section', methods=['POST'])
@admin_required
def add_section():
    try:
        data = request.get_json()
        section = Sections(title=data['title'], desc=data['desc'], image=data['image'])
        db.session.add(section)
        db.session.commit()
        return jsonify({'message': 'Section added successfully'}), 201
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/section', methods=['GET'])
@jwt_required()
def get_sections():
    try:
        sections = Sections.query.all()
        return jsonify([section.serialize() for section in sections]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/section/<int:id>', methods=['GET'])
@jwt_required()
def get_section(id):
    try:
        section = Sections.query.get(id)
        return jsonify(section.serialize()), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/section/<int:id>', methods=['PUT'])
@admin_required
def update_section(id):
    try:
        data = request.get_json()
        section = Sections.query.get(id)
        section.title = data['title']
        section.desc = data['desc']
        section.image = data['image']
        db.session.commit()
        return jsonify({'message': 'Section updated successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/section/<int:id>', methods=['DELETE'])
@admin_required
def delete_section(id):
    try:
        section = Sections.query.get(id)
        sb = db.session.query(section_books).filter_by(section_id=id).all()
        misc_section = Sections.query.filter_by(title="Miscellaneous").first()
        for book in sb:
            book_id = book.book_id
            section_id = book.section_id
            section_obj = Sections.query.get(section_id)
            book_obj = Books.query.get(book_id)
            book_obj.sections.remove(section_obj)
            book_obj.sections.append(misc_section)
            db.session.commit()
            
        db.session.delete(section)
        db.session.commit()
        return jsonify({'message': 'Section deleted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/section_count', methods=['GET'])
@admin_required
def get_section_count():
    try:
        sections = Sections.query.all()
        section_count = []
        for section in sections:
            section_count.append({"title": section.title, "count": len(section.books)})
        return jsonify({'sections':section_count}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

    