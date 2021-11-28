import smtplib #https://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email
import string


def bidSet(item, maxBid, user): #this sends an email of when the bid is set
    fromaddr = "devmail8022@gmail.com"
    toaddr = user["email"]
    text = "you have bidded " + str(maxBid) + " pounds for a " + item["name"]
    #subject = "you have set a bid"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("devmail8022", "DevMail1024")
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def surpassedBid(item, user): #this sends an email of when someones bid suppasses yours
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


def wonBid(item, finalBid, user): #this sends an email when someone suppasses their bid
    fromaddr = "devmail8022@gmail.com"
    toaddr = user["email"]
    subject = "bid won"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("devmail8022", "DevMail1024")
    text = "you have won the bid for a " + item["name"] + " for " + str(finalBid) + " pounds"
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def bidSet(item, currentPrice, user): #this sends an email of when someone wins the bid
    fromaddr = "devmail8022@gmail.com"
    toaddr = user["email"]
    text = "you have bidded for a " + str(item["name"]) + " for a maxmimum bid of " + str(currentPrice) + " pounds"
    #subject = "you have set a bid"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("devmail8022", "DevMail1024")
    server.sendmail(fromaddr, toaddr, text)
    server.quit()