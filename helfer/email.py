import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send(cfg, content):
    """ Send a simple, stupid, text, UTF-8 mail in Python """

    subject = "Random recipes from Hellofresh"
    for ill in ["\n", "\r"]:
        subject = subject.replace(ill, ' ')

    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Disposition': 'inline',
        'Content-Transfer-Encoding': '8bit',
        'From': cfg.get('mail', 'sender'),
        'To': cfg.get('mail', 'reciever'),
        'Date': datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'),
        'X-Mailer': 'python',
        'Subject': subject
    }

    # create the message
    msg = ''
    for key, value in headers.items():
        msg += "%s: %s\n" % (key, value)

    # add contents
    msg += content
    #msg += "\n{}\n".format(content.replace('\n', '<br />'))

    s = smtplib.SMTP(cfg.get('mail', 'smtp'), cfg.get('mail', 'port'))

    if cfg.get('mail', 'sender'):
        s.ehlo()
        s.starttls()
        s.ehlo()

    s.login(cfg.get('mail', 'sender'), cfg.get('mail', 'password'))

    print ("sending %s to %s" % (subject, headers['To']))
    s.sendmail(headers['From'], headers['To'], msg.encode('utf-8'))
    s.quit()


def send_file_as_email(cfg, filePath):
    with open(filePath, 'rt') as f:
        send(cfg, f.read())
