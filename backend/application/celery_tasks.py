from main import app, celery, cache, mail, db
from application.models import Users, Books, BorrowedBooks
from flask_mail import Message
from flask import render_template_string
from datetime import datetime
from pytz import timezone

@celery.task
def daily_visit_reminder():
    with app.app_context():
        users = Users.query.filter_by(is_admin=False).all()
        for user in users:
            with open('users.txt', 'a') as f:
                f.write(f"{user.username} {user.email}\n")
            to = user.email
            template = """
            
            """
            rendered = render_template_string(template, user=user)

            
            subject = "Daily Visit Reminder"
            body = f"Hello {user.username},\n\nThis is a reminder to visit the library today.\n\nThank you."
            msg = Message(subject, recipients=[to], body=body)
            try:
                mail.send(msg)
            except Exception as e:
                print(e)
                continue
    

@celery.task
def revoke_overdue_books():
    with app.app_context():
        borrowed_books = BorrowedBooks.query.filter_by(returned=False).all()
        for book in borrowed_books:
            if (datetime.now().date() - book.borrowed_date.date()).days > 7:
                book.returned = True
                book.returned_date = datetime.now(timezone('Asia/Kolkata'))
                db.session.delete(book)
                db.session.commit()


@celery.task
def export_books():
    with app.app_context():
        books = Books.query.all()
        with open('books.csv', 'w') as f:
            for book in books:
                f.write(f"{book.title},{book.author},{book.genre},{book.publisher}\n")
        with open('books.csv', 'r') as f:
            msg = Message("Books Export", recipients=['21f1001435@ds.study.iitm.ac.in'], body="Books exported successfully")
            msg.attach('books.csv', 'text/csv', f.read())
            mail.send(msg)


@celery.task
def monthly_report():
    with app.app_context():
        template_string = """
<html>
    <head>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>Monthly Report</h1>
        <table>
            <tr>
                <th>Title</th>
                <th>Section</th>
                <th>Date Granted</th>
                <th>Date Returned</th>

            </tr>
            {% for book in books %}
            <tr>
                <td>{{ book.title }}</td>
                <td>{{ book.section }}</td>
                <td>{{ book.borrowed_date }}</td>
                <td>{{ book.returned_date }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
</html>
        """
        
        users = Users.query.filter_by(is_admin=False).all()
        for user in users:
            borrowed_books = BorrowedBooks.query.filter_by(user_id=user.id, ).all()
            rendered = render_template_string(template_string, books=borrowed_books)
            to = user.email
            subject = "Monthly Report"
            msg = Message(subject, recipients=[to], html=rendered)
            try:
                mail.send(msg)
            except Exception as e:
                print(e)
                continue


        