# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
 
# create message object instance
msg = MIMEMultipart()
 
 
message = "Thank you"
html = """
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       Connect to Zoom conversation AT 10:00AM<br>
       <a href="https://nvmbr-hub.github.io/virus_hackaton/"> Connect</a>
    </p>
  </body>
</html>
"""

# setup the parameters of the message
password = "Abcd123!"
msg['From'] = "zoom.mosdorit@gmail.com"
msg['Subject'] = "Обзвон сотрудников от IT-службы"

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="tg_bot",
  password="gjikbgbnmgbdj",
  database="tg_bot"
)
mycursor = mydb.cursor()
mycursor.execute(
    """SELECT mail 
        FROM users_data;
    """)
arr_of_mails = mycursor.fetchall()

# add in the message body
msg.attach(MIMEText(message, 'plain'))
msg.attach(MIMEText(html, 'html'))
#create server
server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
# Login Credentials for sending the mail
server.login(msg['From'], password)
# send the message via the server.
for mail in arr_of_mails:
    msg['To'] = mail
    server.sendmail(msg['From'], msg['To'], msg.as_string())
 
server.quit()
 
print("successfully sent email to %s:" % (msg['To']))