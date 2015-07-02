#-*- coding: utf-8 -*-
from email.MIMEBase import MIMEBase

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import get_connection
from django.utils.encoding import smart_unicode
from django.conf import settings

from database_email_backend.models import Email, Attachment


class DatabaseEmailBackend(BaseEmailBackend):

    def __init__(self, *args, **kwargs):
        super(DatabaseEmailBackend, self).__init__(*args, **kwargs)
        if settings.SECOND_EMAIL_BACKEND:
            self.second_backend = get_connection(
                                        backend=settings.SECOND_EMAIL_BACKEND,
                                        **kwargs)
        else:
            self.second_backend = None

    def open(self):
        if hasattr(self.second_backend, 'open'):
            return self.second_backend.open()
        return False

    def close(self):
        if hasattr(self.second_backend, 'close'):
            self.second_backend.close()
        return False

    def send_messages(self, email_messages):
        sent_messages = 0
        new_conn = self.open()
        for message in email_messages:
            sent_messages += self._send(message)
        if new_conn:
            self.close()
        return sent_messages

    def _send(self, message):
        if self.second_backend is not None and \
           not self.second_backend.send_messages((message,)):
            return 0

        try:
            email = Email.objects.create(
                from_email = u'%s' % message.from_email,
                to_emails = u', '.join(message.to),
                cc_emails = u', '.join(message.cc),
                bcc_emails = u', '.join(message.bcc),
                all_recipients = u', '.join(message.recipients()),
                subject = u'%s' % message.subject,
                body = u'%s' % message.body,
                raw = smart_unicode(message.message().as_string())
            )
            for attachment in message.attachments:
                if isinstance(attachment, tuple):
                    filename, content, mimetype = attachment
                elif isinstance(attachment, MIMEBase):
                    filename = attachment.get_filename()
                    content = attachment.get_payload(decode=True)
                    mimetype = None
                else:
                    continue
                Attachment.objects.create(
                    email=email,
                    filename=filename,
                    content=content,
                    mimetype=mimetype
                )
        except:
            if self.second_backend is None and not self.fail_silently:
                raise
        return 1

