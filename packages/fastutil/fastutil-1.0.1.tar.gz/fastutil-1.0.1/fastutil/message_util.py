import yagmail


def send_email(title, message, to='464840061@qq.com'):
    yag_server = yagmail.SMTP(user='riskerat2688@qq.com', password='xogporujfqgabifh', host='smtp.qq.com')
    yag_server.send(to, title, message)
    yag_server.close()
