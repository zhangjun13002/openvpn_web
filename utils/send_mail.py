# -- coding: utf8 --
import base64
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.header import Header

from config import private_key

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from model.default import Smtp

def send_mail(email, title="", message=""):
    query = Smtp.select().first()
    if query.server and query.server != "":
        smtp_server = query.server
        smtp_ssl = query.ssl
        smtp_port = query.port
        smtp_user = query.user

        privKey = RSA.import_key(private_key)
        cipher = PKCS1_v1_5.new(privKey)
        decrypted = cipher.decrypt(base64.b64decode(query.password.encode()), None)
        if decrypted:
            smtp_passwd = decrypted.decode()
        else:
            raise ValueError("SMTP发送用户密码不正确!")

        encoding = 'utf-8'
        subject = title
        body = message
        msg = MIMEText(body.encode(encoding), 'plain', encoding)
        msg['Subject'] = Header(subject, encoding)
        msg['From'] = smtp_user
        msg['To'] = email
        msg['Date'] = formatdate()

        try:
            if smtp_ssl == 0:
                smtp = smtplib.SMTP(smtp_server, smtp_port)
            else:
                smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
            smtp.ehlo()
            smtp.login(smtp_user, smtp_passwd)
            smtp.sendmail(smtp_user, email, msg.as_string())
            smtp.quit()
        except Exception as e:
            raise ValueError("电子邮件发送失败: {0}，请检查相关设置。".format(str(e)))
    else:
        raise ValueError("SMTP服务没有配置")