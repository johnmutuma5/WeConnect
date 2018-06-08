import smtplib
from app import config

class Mailer():
    def __init__(self):
        self.host = config.get('EMAIL_HOST')
        self.port = config.get('EMAIL_PORT')
        self.username = config.get('EMAIL_USERNAME')
        self.password = config.get('EMAIL_PASSWORD')
        self.s = smtplib.SMTP(host=self.host, port=self.port)

    def send_reset_link(self, link, recipient):
        msg = """
        Password Reset
        Use the following link to reset
        {}
        """.format(link)

        self.s.starttls()
        self.s.login(self.username, self.password)
        self.s.sendmail(from_addr='no-reply', to_addrs = [recipient], msg=msg)
        self.s.quit()
