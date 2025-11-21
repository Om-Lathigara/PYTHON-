import pandas as om
import smtplib
from email.mime.text import MIMEText as Mtext
from email.mime.multipart import MIMEMultipart as Mpart
from email.mime.base import MIMEBase as Mbase
from email import encoders

email = "aumlathigara17@gmail.com"
password = "usaa egrf hriy pjjx"

data = om.read_csv("recipients.csv")

file = input("Enter file name to attach (or press Enter to skip): ").strip()

if file:
    try:
        f = open(file, "rb")
        f.close()
    except:
        print("File not found or cannot be opened. Emails not sent.")
        exit()

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, password)

for i, row in data.iterrows():
    name = row["Name"]
    mail = row["Email"]

    msg = Mpart()
    msg["From"] = email
    msg["To"] = mail
    msg["Subject"] = f"Hello {name}"

    body = f"Dear {name},\nThis email is sent using Python.\n"
    msg.attach(Mtext(body, "plain"))

    if file:
        f = open(file, "rb")
        datafile = f.read()
        f.close()

        part = Mbase("application", "octet-stream")
        part.set_payload(datafile)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=" + file)
        msg.attach(part)

        print("Attached", file)

    try:
        server.send_message(msg)
        print("Email sent to", name)
    except Exception as e:
        print("Error sending to", mail, ":", e)

server.quit()
print("All emails sent.")
