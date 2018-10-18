#! /usr/bin/python3
import os
from urllib import request
import smtplib
from datetime import datetime
from email.message import EmailMessage

def main():
    try:
        ip_addr = request.urlopen('https://api.ipify.org').read().decode('utf-8')
    
        ip_addr_file = '/home/wenduowang/ip_address.txt'
        if os.path.exists(ip_addr_file):
            with open(ip_addr_file) as f:
                old_ip_addr = f.readline()
    
            if ip_addr == old_ip_addr:
                return 0
    
        with open(ip_addr_file) as f:
            f.write(ip_addr)

        msg = EmailMessage()
        msg.set_content(ip_addr)
        
        msg['Subject'] = 'SSH IP'
        msg['From'] = 'kiponfitin@hotmail.com'
        msg['To'] = 'wenduo.wang@hotmail.com'
        
        sender = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        sender.starttls()
        sender.login(msg['From'], '12345qwerT')
        sender.sendmail(msg['From'], [msg['To']], msg.as_string())
        sender.quit()

    except:
        return 1

if __name__ == '__main__':
    main()
