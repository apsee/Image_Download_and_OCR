from pathlib import Path
import imaplib
import email
from datetime import datetime, timedelta, date

def today_date_rfc():
    day = str(date.today().day)
    month = date.today().month
    year = str(date.today().year)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    rfc_date =  day + '-' + months[month-1] + '-' + year
    return rfc_date

def increment_file_name(old_filename, old_file_path, email_recd):
    new_filename = old_filename + '_' + str(email_recd)
    new_file_path = old_file_path / new_filename
    return new_file_path

email_recd = 1 # keep track of number of emails received

dl_folder = Path('') # insert file path
if not dl_folder.exists():
    dl_folder.mkdir()

rfc_date = today_date_rfc()
filename = f'{rfc_date}' + '_' + str(email_recd)
filepath = dl_folder / filename

email_addr = "" # email address string
password = "" # google generated third party account password string
imap_url = 'imap.gmail.com'
from_addr = "" # email or mobile carrier associated email

imap = imaplib.IMAP4_SSL(imap_url)
imap.login(email_addr, password)
imap.select('Inbox')

# Get list (single binary string) of emails received today
today_emails = f'(FROM {from_addr} ON {rfc_date})'
_, email_num = imap.search(None, today_emails)

if not email_num[0]:
    print("\nHaven't received any emails today")
    print("Exiting program...\n")
    exit()

# For each email received today, return a message object from the bytes object
for msg in email_num[0].split():
    _, data = imap.fetch(msg, '(RFC822)')
    _, bytes_data = data[0]
    msg_parts = email.message_from_bytes(bytes_data)
    
    for part in msg_parts.walk():
        if part.get_content_type() == 'multipart':
            continue
        if part.get_content_type() is None:
            continue

    with filepath.open('wb') as f:

        f.write(part.get_payload(decode=1))

    filepath = increment_file_name(filename, filepath, email_recd)




    