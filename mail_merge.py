import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

email = "aumlathigara17@gmail.com"
password = "usaa egrf hriy pjjx"

data = pd.read_csv("recipients.csv")

file = input("Enter file name to attach (or press Enter to skip): ").strip()

if file and not os.path.exists(file):
    print("File not found. Emails not sent.")
    exit()

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, password)

for i, row in data.iterrows():
    name = row["Name"]
    mail = row["Email"]

    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = mail
    msg["Subject"] = f"Hello {name}"

    body = f"Dear {name},\nThis email is sent using Python.\n"
    msg.attach(MIMEText(body, "plain"))

    if file:
        with open(file, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file)}")
        msg.attach(part)
        print(f"Attached {file}")

    try:
        server.send_message(msg)
        print(f"Email sent to {name}")
    except Exception as e:
        print(f"Error sending to {mail}: {e}")

server.quit()
print("All emails sent.")
