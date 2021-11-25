import smtplib #https://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email



def bidSet(item, maxBid, user):
    fromaddr = "devmail8022@gmail.com"
    toaddr = user["email"]
    subject = "you have set a bid"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("devmail8022", "DevMail1024")
    text = "you have bidded " + str(maxBid) + " pounds for a " + item["name"]
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def surpassedBid(item, user):
    fromaddr = "devmail8022@gmail.com"
    toaddr = user["email"]
    subject = "surpassed bid"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("devmail8022", "DevMail1024")
    text = "your bid for a " + item["name"] + " has been surpassed"
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print(toaddr)


def wonBid(item, user):
    fromaddr = "devmail8022@gmail.com"
    toaddr = user["email"]
    subject = "bid won"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("devmail8022", "DevMail1024")
    text = "you have won the bid for a " + item["name"]
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
