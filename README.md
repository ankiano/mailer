### mailer
Mailer is a command line tool for sending emails from gmail account.

### installation:
    sudo -H pip3 install git+https://github.com/ankiano/mailer.git -U

### example of usage:

    mailer --help

    mailer --to user1@example.com,user2@example.com \
           --subject "Subject of the mail" \
           --body "Some body message"

    `--to` param can pass one or several recipients separated by ,

    mailer --to mailing.list \
           --subject "Subject of the mail" \
           --body message.txt
           --attachment file1.zip
           --attachment file2.zip

    `--to` param cap pass file containg a list of recipients separated by \n (new line)

### example of .mail.yml for simple smtp:

    host: smtp.example.com
    port: 25
    use_ssl: False
    username: user@example.com

### example of .mail.yml for ssl smtp:

    host: smtp.gmail.com
    port: 465
    use_ssl: True
    username: user@gmail.com
    password: appkey
    #https://security.google.com/settings/security/apppasswords
