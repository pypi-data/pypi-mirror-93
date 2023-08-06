from email.mime.base import MIMEBase
import base64
import copy

from django.core.mail import EmailMultiAlternatives, EmailMessage, get_connection
from .settings import EMAIL_BACKEND


def _serialize_email_message(email_message):
    message_dict = {
        'subject': email_message.subject,
        'body': email_message.body,
        'from_email': email_message.from_email,
        'to': email_message.to,
        'bcc': email_message.bcc,
        'attachments': [],
        'headers': email_message.extra_headers,
        'cc': email_message.cc,
        'reply_to': email_message.reply_to
    }

    if hasattr(email_message, 'alternatives'):
        message_dict['alternatives'] = email_message.alternatives

    if email_message.content_subtype != EmailMessage.content_subtype:
        message_dict["content_subtype"] = email_message.content_subtype

    if email_message.mixed_subtype != EmailMessage.mixed_subtype:
        message_dict["mixed_subtype"] = email_message.mixed_subtype

    attachments = email_message.attachments
    for attachment in attachments:
        if isinstance(attachment, MIMEBase):
            filename = attachment.get_filename('')
            binary_contents = attachment.get_payload(decode=True)
            mimetype = attachment.get_content_type()

        else:
            filename, binary_contents, mimetype = attachment
            # For a mimetype starting with text/, content is expected to be a string.
            if isinstance(binary_contents, str):
                binary_contents = binary_contents.encode()

        contents = base64.b64encode(binary_contents).decode('ascii')
        message_dict['attachments'].append((filename, contents, mimetype))

    return message_dict


def _deserialize_email_message(serialized_email_message):
    message_kwargs = copy.deepcopy(serialized_email_message)  # prevents missing items on retry

    # remove items from message_kwargs until only valid EmailMessage/EmailMultiAlternatives
    #  kwargs are left and save the removed items to be used as EmailMessage/EmailMultiAlternatives
    #  attributes later

    message_attributes = ['content_subtype', 'mixed_subtype']
    attributes_to_copy = {}
    for attr in message_attributes:
        if attr in message_kwargs:
            attributes_to_copy[attr] = message_kwargs.pop(attr)

    # remove attachments from message_kwargs then reinsert after base64 decoding
    attachments = message_kwargs.pop('attachments')
    message_kwargs['attachments'] = []
    for attachment in attachments:
        filename, contents, mimetype = attachment
        contents = base64.b64decode(contents.encode('ascii'))

        # For a mimetype starting with text/, content is expected to be a string.
        if mimetype and mimetype.startswith('text/'):
            contents = contents.decode()

        message_kwargs['attachments'].append((filename, contents, mimetype))

    if 'alternatives' in message_kwargs:
        message = EmailMultiAlternatives(
            connection=get_connection(backend=EMAIL_BACKEND),
            **message_kwargs,
        )
    else:
        message = EmailMessage(
            connection=get_connection(backend=EMAIL_BACKEND),
            **message_kwargs,
        )

    # set attributes on message with items removed from message_kwargs earlier
    for attr, val in attributes_to_copy.items():
        setattr(message, attr, val)

    return message
