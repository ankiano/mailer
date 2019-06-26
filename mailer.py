#!/usr/bin/env python3.6
# coding=utf-8

import click
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP


def get_recipients(to):
    """Prepare list of recipients"""

    if os.path.exists(to):
        with open(to, 'r') as f:
            return ", ".join([e.replace('\n', '') for e in f])
    else:
        return ", ".join(to.replace('\n', '').split(','))


def get_body(body):
    """Extract email body text from specified file (.txt,.html)"""

    if os.path.exists(body):
        text = open(body, 'r').read()
        if body.endswith('.html'):
            return MIMEText(text, 'html')
        else:
            return MIMEText(text, 'plain')
    else:
        return MIMEText(body, 'plain')


def get_attachment(attachment):
    """Prepare attachment"""

    if os.path.exists(attachment):
        submessage = MIMEBase('application', 'octet-stream')
        submessage.set_payload(open(attachment, 'rb').read())
        encoders.encode_base64(submessage)
        submessage.add_header('Content-Disposition', 'attachment; filename={}'
                              .format(attachment))
        return submessage


@click.command()
@click.option('--from', 'from_', required=True,
              help="Sender email address")
@click.option('--appkey', required=True,
              help="""To get application password for your google account:\n
              https://security.google.com/settings/security/apppasswords
              """)
@click.option('--to', required=True,
              help="Recipient email address. \
                    You can use a file with a mailing list.")
@click.option('-s', '--subject', default='')
@click.option('-b', '--body', default='', type=click.Path(),
              help="Message text. You can use a file or plain text.")
@click.option('-a', '--attachment', multiple=True,
              type=click.Path(exists=True, dir_okay=False),
              help="File to be attached. Сan add several files by specifying \
                    additional keys. Total max size of all attached files \
                    should be less then 35Mb")
@click.option('--debug', is_flag=True,
              help="Will print values of options without sending mail.")
def cli(from_, appkey, to, subject, body, attachment, debug):
    """Mailer is a command line tool for sending emails from gmail account."""

    if debug:
        click.echo('from: {}'.format(from_))
        click.echo('appkey: {}'.format(appkey))
        click.echo('to: {}'.format(to))
        click.echo('subject: {}'.format(subject))
        click.echo('body text: {}'.format(get_body(body)))
        click.echo('attachment: {}'.format(attachment))
    else:
        # create message
        msg = MIMEMultipart('alternative')
        # set message params
        msg['From'] = from_
        msg['To'] = get_recipients(to)
        msg['Subject'] = subject
        msg.attach(get_body(body))
        for a in attachment:
            click.echo(a)
            msg.attach(get_attachment(a))
        # send email
        with SMTP(host="smtp.gmail.com", port=587) as server:
            server.noop()
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(user=from_, password=appkey)
            server.sendmail(from_, to, msg.as_string())
            server.close()


if __name__ == '__main__':
    cli()