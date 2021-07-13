print("Importing packages...")
import imaplib, email, getpass, urllib.request
from email import policy

imap_host = 'imap.gmail.com'
imap_user = 'eric.m.mcdaniel@gmail.com'

# init imap connection
print("Logging into mail")
mail = imaplib.IMAP4_SSL(imap_host, 993)
rc, resp = mail.login(imap_user, 'qausieavgwrhvzkg')

# select only unread messages from inbox
print("Checking Unread Mail")
mail.select('Inbox')
status, data = mail.search(None, '(UNSEEN)')

for num in data[0].split():
    # get a single message and parse it by policy.SMTP (RFC compliant)
    status, data = mail.fetch(num, '(BODY.PEEK[])')
    email_msg = data[0][1]
    email_msg = email.message_from_bytes(email_msg, policy=policy.SMTP)
    subject = str(email_msg['Subject'] )
    if "Package delivered by" in subject:
        with urllib.request.urlopen('http://192.168.1.193/cm?cmnd=POWER2%20On') as response:
            html = response.read()
        mail.store(num, "+FLAGS", "\\Seen")
        print("Package delivered, light on")
        exit()

print("No packages.")
