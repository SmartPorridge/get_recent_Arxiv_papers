# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

class Email():
    def __init__(self,
                mail_sender,
                mail_pass,
                mail_sender_name=None,
                mail_type='QQ'
                ):
        self.mail_sender = mail_sender
        self.mail_pass = mail_pass
        self.mail_type = mail_type
        if self.mail_type == 'QQ':
            self.mail_smtp_host = 'smtp.qq.com'
            self.mail_ssl_port = 465
        
        if mail_sender_name == None:
            self.mail_sender_name = self.mail_sender
        else:
            self.mail_sender_name == mail_sender_name  

    def send_mail(self, mail_receiver,mail_content, mail_subject=' '):
        msg = MIMEText(mail_content,'plain','utf-8')
        msg['From'] = formataddr([self.mail_sender_name, self.mail_sender])
        msg['Subject'] = mail_subject

        # 发件人邮箱中的SMTP服务器，端口是25
        server=smtplib.SMTP_SSL(self.mail_smtp_host, self.mail_ssl_port)  
        # 括号中对应的是发件人邮箱账号、邮箱密码
        # print(self.mail_sender,self.mail_pass)
        server.login(self.mail_sender, self.mail_pass)  
        # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(self.mail_sender,[mail_receiver,],msg.as_string())  
        server.quit()  # 关闭连接

        print('mail send successful！')

if __name__=='__main__':
    qq_email = Email('@qq.com','jevcecdnbwzlbfah')
    qq_email.send_mail('@163.com',mail_subject='test',mail_content='Test')
