import smtplib
import schedule
import time
from email.message import EmailMessage
from threading import Thread, Lock

# Gmail credentials
EMAIL_ADDRESS = 'personalhealthcare27@gmail.com'
EMAIL_PASSWORD = 'mumz kuyo eojg svgp'

# Reminder storage
reminders = []
reminder_lock = Lock()

def send_email(to_email, subject, body):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"📧 Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

def schedule_medication(name, time_str, email):
    def job():
        subject = f"💊 Reminder: Take your medication - {name}"
        body = f"Hi! This is your daily reminder to take your medication:\n\n🕒 Time: {time_str}\n💊 Medicine: {name}"
        send_email(email, subject, body)

        with reminder_lock:
            global reminders
            reminders = [r for r in reminders if not (r['name'] == name and r['time'] == time_str and r['email'] == email)]
            print(f"🗑️ Deleted sent reminder: {name} at {time_str} for {email}")

    schedule.every().day.at(time_str).do(job)

    with reminder_lock:
        reminders.append({
            'name': name,
            'time': time_str,
            'email': email
        })

    print(f"✅ Scheduled: {name} at {time_str} for {email}")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Background scheduler thread
Thread(target=run_scheduler, daemon=True).start()
