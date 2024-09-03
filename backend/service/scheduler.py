import schedule
import time
from application.models import *
from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib
import ssl
from dotenv import load_dotenv
import os

load_dotenv()
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")


previous_day_5pm = datetime.now().replace(hour=17, minute=0, second=0,
                                          microsecond=0) - timedelta(days=1)
today_5pm = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

def send_email(email, subject, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = str(email)
    msg.set_content(message)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_address, email_password)
        server.send_message(msg)


def dailyReport():
    users = Users.query.all()
    for user in users:
        username = user.username
        email = user.email
        tickets=Tickets.query.filter_by(user_id=user.id).all()
        total_tickets = 0
        if datetime.now().day == 1:
            monthlyReport()
            continue
        for ticket in tickets:
            ticket_created_on = ticket.created_at
            if previous_day_5pm <= ticket_created_on <= today_5pm:
                total_tickets += ticket.quantity

        body = f"Hi {username},\n\nYou have booked {total_tickets} tickets today .\n\nRegards,\nTeam BookMyEvent"
        print(body)
        # send_mail(email, "Daily Report", body)
        send_email(email, "Daily Report", body)
        print("Mail Sent")

def monthlyReport():
    users = Users.query.all()
    now = datetime.now()
    for user in users:
        username = user.username
        email = user.email
        tickets=Tickets.query.filter_by(user_id=user.id).all()
        total_tickets = 0
        for ticket in tickets:
            ticket_created_on = ticket.created_at
            if ticket_created_on.month == now.month:
                total_tickets += ticket.quantity

        body = f"Hi {username},\n\nYou have booked {total_tickets} tickets this month .\n\nRegards,\nTeam BookMyEvent"
        send_email(email, "Monthly Report", body)
        print("Mail Sent")

def Scheduled():

    schedule.every().day.at("17:00").do(dailyReport)

    while True:
        schedule.run_pending()
        time.sleep(1)
