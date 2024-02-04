import imaplib
import email
from email.header import decode_header
import logging
import msvcrt
import getpass

# Constants
MAILBOX_NAME = 'inbox'
SUSPICIOUS_KEYWORDS = ['urgent', 'click here', 'you won', 'download apk', 'cash', 'rummy',
                       'claim', 'lottery', 'congratulations', 'inheritance', 'secret',
                       '100% more', '100% free', '100% satisfied', 'additional income',
                       'be your own boss', 'best price', 'big bucks', 'billion',
                       'cash bonus', 'cents on the dollar', 'consolidate debt', 'double your cash',
                       'double your income', 'earn extra cash', 'earn money', 'eliminate bad credit',
                       'extra cash', 'extra income', 'expect to earn', 'fast cash',
                       'financial freedom', 'free access', 'free consultation', 'free gift',
                       'free hosting', 'free info', 'free investment', 'free membership',
                       'free money', 'free preview', 'free quote', 'free trial', 'full refund',
                       'get out of debt', 'get paid', 'giveaway', 'guaranteed', 'increase sales',
                       'increase traffic', 'incredible deal', 'lower rates', 'lowest price',
                       'make money', 'million dollars', 'miracle', 'money back', 'once in a lifetime',
                       'one time', 'pennies a day', 'potential earnings', 'prize', 'promise',
                       'pure profit', 'risk-free', 'satisfaction guaranteed', 'save big money',
                       'save up to', 'special promotion']

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_suspicious_email(subject, body):
    # Check if any of the suspicious keywords is present in the subject or body
    suspicious_word = next((keyword for keyword in SUSPICIOUS_KEYWORDS if keyword in subject.lower() or keyword in body.lower()), None)
    return suspicious_word

def login_to_email():
    try:
        # Get email username from user input
        email_username = input("Enter your email username: ")

        # Get app-specific password from user input (password is hidden)
        print("Enter your app-specific password:")
        app_specific_password = getpass.getpass("Password (hidden): ")

        print(f"Entered username: {email_username}")
        print("Entered password: *****")  # Masked for security

        # Connect to Gmail IMAP server
        mail = imaplib.IMAP4_SSL('imap.gmail.com')

        # Log in to your Gmail account using the app-specific password
        mail.login(email_username, app_specific_password)
        logger.info("Connection successful")

        return mail
    except Exception as e:
        logger.error(f"Error connecting to email: {e}")
        raise


def get_hidden_input():
    # Function to get hidden input for passwords (Windows only)
    password = ""
    try:
        while True:
            char = msvcrt.getch()
            if char in [b'\r', b'\n']:
                break
            elif char == b'\b':
                if password:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)  # Remove the last character from the console
            else:
                try:
                    password += char.decode('utf-8')
                    print("*", end='', flush=True)
                except UnicodeDecodeError:
                    pass  # Ignore decoding errors and continue
        print()  # Move to the next line after password entry
        return password
    except Exception as e:
        logger.error(f"Error getting hidden input: {e}")
        raise

def get_body(email_message):
    # Function to retrieve the body of the email
    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode('utf-8', 'ignore')
    else:
        body = email_message.get_payload(decode=True).decode('utf-8', 'ignore')

    return body

def check_emails(mail):
    try:
        # Select the mailbox you want to check
        mail.select(MAILBOX_NAME)

        # Search for all emails in the mailbox
        status, messages = mail.search(None, 'ALL')

        if status == 'OK':
            for num in messages[0].split():
                # Fetch the email by its unique identifier (UID)
                _, msg_data = mail.fetch(num, '(RFC822)')
                email_message = email.message_from_bytes(msg_data[0][1])

                # Extract the subject
                subject, encoding = decode_header(email_message['Subject'])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or 'utf-8')

                # Extract the body of the email
                body = get_body(email_message)

                # Check if the email is suspicious
                suspicious_word = is_suspicious_email(subject, body)
                if suspicious_word:
                    logger.warning("Suspicious Email Found:")
                    logger.warning(f"Sender: {email_message['From']}")
                    logger.warning(f"Subject: {subject}")
                    logger.warning(f"Suspicious Word: {suspicious_word}")
                    logger.warning("")
    except Exception as e:
        logger.error(f"Error checking emails: {e}")
    finally:
        # Close the connection
        mail.logout()

if __name__ == "__main__":
    # Log in to Gmail using the app-specific password
    mail_connection = login_to_email()

    # Check for suspicious emails using IMAP
    check_emails(mail_connection)
