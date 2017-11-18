# -*- coding: utf-8 -*-

import smtplib


def send_test_mail(login, password, server_addr, to, port):

    message_payload = "\r\n".join((
        "From: %s" % login,
        "To: %s" % to,
        "Subject: %s" % 'Test message from Sphere Logger',
        "",
        'Test message from Sphere Logger'))

    try:
        server = smtplib.SMTP()
        server.connect(server_addr, port)
        server.starttls()
        server.login(login, password)
        server.sendmail(login, [to], message_payload)
        server.quit()

        return True

    except Exception as e:
        return False
