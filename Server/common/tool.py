import logging
import os
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger('simple')


class Tools:

    @classmethod
    def generate_verification_code(cls):
        """隨機生成一個6位數驗證碼"""
        characters = string.digits + string.ascii_letters  # 包含数字和字母的字符集
        code = ''.join(random.choices(characters, k=6))
        return code


class Email:
    """發送驗證碼"""
    smtp_server = os.environ.get('SMTP_SERVER')  # 设置SMTP服务器地址和端口
    sender_email = os.environ.get('EMAIL_SENDER')  # 设置发件人和收件人的电子邮件地址
    password = os.environ.get('EMAIL_PASSWORD')  # 发件人的电子邮件密码

    @classmethod
    def send(cls, receiver_email: str, code: str):
        # 创建一封邮件
        message = MIMEMultipart()
        message["Subject"] = "[汘水云云] 驗證碼"
        message["From"] = cls.sender_email
        message["To"] = receiver_email

        # 添加邮件正文
        content = f"[汘水云云] 驗證碼:{code}\n您正在注冊Blog, 請勿將驗證碼告知他人,以防賬號被盜."
        message.attach(MIMEText(content, "plain", 'utf-8'))

        try:  # 创建一个安全的连接，并发送邮件
            with smtplib.SMTP(cls.smtp_server) as server:
                server.starttls()  # 安全连接
                server.login(cls.sender_email, cls.password)
                server.sendmail(cls.sender_email, receiver_email, message.as_string())
                return True
        except Exception as e:
            logger.error(e)
            return False
