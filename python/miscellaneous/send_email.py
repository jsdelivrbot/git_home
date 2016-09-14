import smtplib, getpass

def prompt(prompt):
    return input(prompt).strip()
from_addr = prompt("From:")
to_addrs = []

print("Enter recipent addresses:\r\n")

while True:
    try:
        new_recipient = input().strip()
        print ("new_recipient: %s" %new_recipient)
    except EOFError:
        break
    if not new_recipient:
        break
    to_addrs.append(new_recipient)

print (to_addrs)

print("Enter message, end with Ctr D:")

msg = ""

while True:
    try:
        line = input()
    except EOFError:
        break
    if not line:
        break
    msg = msg + line

print("Message length is", len(msg))

server = smtplib.SMTP(
        host="smtp-mail.outlook.com",
        port=587)

server.set_debuglevel(1)

server.starttls()

password = getpass.getpass("password for %s:" % from_addr)

server.login(user=from_addr, password=password)

for to_addr in to_addrs:
    server.sendmail(from_addr, to_addr, msg)

server.quit()
