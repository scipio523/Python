import smtplib

#send email through gmail

user = ''
password = 'metcalf118'

from_addr = user
to_addr = ''
subject = 'Click Me'
body = '...hai'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (from_addr, to_addr, subject, body)

s = smtplib.SMTP('smtp.gmail.com', 587)
s.ehlo()
s.starttls()
s.login(user, password)
s.sendmail(from_addr, to_addr, email_text)
s.close()
print 'Email sent!'
