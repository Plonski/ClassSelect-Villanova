import smtplib

def sendMail(crn, username):
    fromaddr = 'NOTIFICATIONEMAIL'
    toaddrs  = username + '@villanova.edu'
    msg = 'Subject: %s\n\n%s' % ("Your class has an open slot", crn + " is ready to be added.")
    username = 'NOTIFICATIONEMAIL'
    password = 'MYPASSWORD'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)

    server.quit()