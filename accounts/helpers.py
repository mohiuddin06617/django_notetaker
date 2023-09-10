import logging
import smtplib

from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger("emails")

MESSAGES = {
    "email_changed": "The email was successfully changed.",
    "noemail": "Sorry, but we could not find a user account with that email.",
    "wrong_pass": "You have entered the wrong password.",
}


def send_email(
        email_to: str, email_from: str, subject: str, text: str, html: str = ""
) -> bool:
    """Sends email to a user.

    Args:
        email_to: Where to send a letter.
        email_from: From whom the letter will be sent.
        subject: A letter subject.
        text: A plain/text of the letter.
        html: HTML version of the letter.

    Returns:
        Success or failure ending boolean flag.
    """
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=email_from,
            to=[email_to],
            reply_to=[email_from],
        )
        if html:
            msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)
        logger.info(
            "Sing up email sent to: {}\nSubject: {}".format(email_to, subject)
        )
        return True
    except smtplib.SMTPException as e:
        logger.error(
            "There was an error sending an email to "
            "{}: {}\nOn subject: {}".format(email_to, str(e), subject)
        )
        return False
