#!/usr/bin/env python3.10

import logging
import yaml
import click
import os
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
import ssl
from smtplib import SMTP, SMTP_SSL

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
    """Prepare attachment with correct MIME type."""

    if os.path.exists(attachment):
        mime_type, _ = mimetypes.guess_type(attachment)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        
        main_type, sub_type = mime_type.split('/', 1)
        submessage = MIMEBase(main_type, sub_type)
        submessage.set_payload(open(attachment, 'rb').read())
        encoders.encode_base64(submessage)
        
        # encode the filename using Header
        filename = os.path.basename(attachment)
        encoded_filename = Header(filename, 'utf-8').encode()
        
        # add header with encoded filename
        submessage.add_header('Content-Disposition', 'attachment', filename=encoded_filename)
        return submessage

@click.command()
@click.option('--to', required=True,
              help="Recipient email address. \
                    You can use a file with a mailing list.")
@click.option('-s', '--subject', default='')
@click.option('-b', '--body', default='', type=click.Path(),
              help="Message text. You can use a file or plain text.")
@click.option('-a', '--attachment', multiple=True,
              type=click.Path(exists=True, dir_okay=False),
              help="File to be attached. Сan add several files by specifying \
                    additional keys.")
def cli(to, subject, body, attachment):
    """Mailer is a command line tool for sending emails from smtp server account"""

    # create message
    msg = MIMEMultipart('alternative')
    # set message params
    msg['From'] = _config.username
    msg['To'] = get_recipients(to)
    msg['Subject'] = subject
    msg.attach(get_body(body))
    for a in attachment:
        msg.attach(get_attachment(a))

    if _config.use_ssl:
        # create a secure SSL context
        context = ssl.create_default_context()
        server = SMTP_SSL(host=_config.host, port=_config.port, context=context)
        server.noop()
        server.ehlo()
    else:
        server = SMTP(host=_config.host, port=_config.port)
        server.starttls()

    if hasattr(_config, 'password') and _config.password is not None:
        # The _config.pass attribute is present and not None
        server.login(user=_config.username, password=_config.password)

    server.sendmail(_config.username, msg['To'].split(','), msg.as_string())
    log.info('message sent to email')
    server.close()

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)-5s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger()

# read config from yaml file
class Config:
    pass
config_file =  os.path.expanduser('~/.mailer.yml')
with open(config_file, 'r') as config_file:
    config_data = yaml.safe_load(config_file)
    log.debug(f'config: {config_data}')
    _config = Config()
    for key, value in config_data.items():
        setattr(_config, key, value)

if __name__ == '__main__':
    cli()