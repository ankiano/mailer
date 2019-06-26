### mailer
Mailer is a command line tool for sending emails from gmail account.

### installation:
    sudo pip3 install git+https://github.com/ankiano/mailer.git -U

## example of usage:

    mailer --help

    mailer --from user@gmail.com \
           --appkey youkey \
           --to mailing.list \
           --subject "Subject of the mail" \
           --body message.txt
           --attachment file.zip
