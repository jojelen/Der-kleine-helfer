import datetime
import smtplib


def send(cfg, content):
    """Send content as an email in accordance with config file"""

    subject = "Recipes from der kleine Helfer"
    for ill in ["\n", "\r"]:
        subject = subject.replace(ill, " ")

    s = smtplib.SMTP(cfg.get("mail", "smtp"), cfg.get("mail", "port"))

    if cfg.get("mail", "sender"):
        s.ehlo()
        s.starttls()
        s.ehlo()

    s.login(cfg.get("mail", "sender"), cfg.get("mail", "password"))
    recievers = cfg.get("mail", "reciever").split(":")
    for reciever in recievers:
        headers = {
            "Content-Type": "text/html; charset=utf-8",
            "Content-Disposition": "inline",
            "Content-Transfer-Encoding": "8bit",
            "From": cfg.get("mail", "sender"),
            "To": reciever,
            "Date": datetime.datetime.now().strftime("%a, %d %b %Y  %H:%M:%S %Z"),
            "X-Mailer": "python",
            "Subject": subject,
        }

        # create the message
        msg = ""
        for key, value in headers.items():
            msg += "%s: %s\n" % (key, value)

        # add contents
        msg += content

        print("sending %s to %s" % (subject, headers["To"]))
        s.sendmail(headers["From"], headers["To"], msg.encode("utf-8"))
    s.quit()


def send_file_as_email(cfg, filePath):
    with open(filePath, "rt") as f:
        send(cfg, f.read())
