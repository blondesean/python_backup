'''
import smtplib
 
server = smtplib.SMTP('Cavemail.geico.net', 587)
server.starttls()
server.login("sduncan@geico.com", "Zxcvbn90")
 
msg = "Hello World!"
server.sendmail("sduncan@geico.com", "sduncan@geico.com", msg)
server.quit()

'''

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
emailfrom = "sduncan@geico.com"
emailto = "sduncan@geico.com"
emailCC = "sduncan@geico.com"
#fileToSend = "\\\\chnas06\\MKT-Data\\INTERNET\\INET Admin\\Sean\\Useful\\Code\\testpython.csv"
password = "Qwerty12"

x = 0
for x in range(0, 3):
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "It's possible. Good luck."
    msg.preamble = "Sent from Python"

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    print(maintype + subtype)
    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("Cavemail.geico.net")
    server.starttls()
    server.login(emailfrom,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()

    x = x + 1
