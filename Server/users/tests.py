import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 设置SMTP服务器地址和端口
smtp_server = "smtp.qq.com"


# 设置发件人和收件人的电子邮件地址
sender_email = "1319849186@qq.com"
receiver_email = "1319849186@qq.com"
password = "jydyrettlhrvjacd"  # 发件人的电子邮件密码

# 创建一封邮件
message = MIMEMultipart()
message["Subject"] = "Hello there"
message["From"] = sender_email
message["To"] = receiver_email

# 添加邮件正文
content = """
这是一封测试邮件。  
如果你收到这封邮件，说明你的Python代码能成功发送电子邮件了！  
"""
message.attach(MIMEText(content, "plain", 'utf-8'))

# 创建一个安全的连接，并发送邮件
with smtplib.SMTP(smtp_server) as server:
    server.starttls()  # 安全连接
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
