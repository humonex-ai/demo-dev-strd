import mimetypes
import os
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from email.utils import make_msgid


@dataclass(frozen=True)
class SMTPConfig:
    host: str
    port: int
    username: str = ""
    password: str = ""
    use_tls: bool = True
    use_ssl: bool = False
    timeout: float = 30.0


def send_email(
    config: SMTPConfig,
    sender: str,
    recipients: list,
    subject: str,
    body: str,
    *,
    html_body: str = None,
    cc: list = None,
    bcc: list = None,
    reply_to: str = None,
    attachments: list = None,
    message_id_domain: str = None,
) -> dict:
    if not config.host:
        raise ValueError("SMTPConfig.host is required")
    if not (1 <= config.port <= 65535):
        raise ValueError("SMTPConfig.port must be between 1 and 65535")
    if config.use_tls and config.use_ssl:
        raise ValueError("use_tls and use_ssl are mutually exclusive")
    if not sender:
        raise ValueError("sender is required")
    if not recipients:
        raise ValueError("recipients must contain at least one address")
    if not isinstance(recipients, list):
        raise ValueError("recipients must be a list")

    cc = cc or []
    bcc = bcc or []
    attachments = attachments or []

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = ", ".join(cc)
    if reply_to:
        msg["Reply-To"] = reply_to
    msg["Message-ID"] = make_msgid(domain=message_id_domain) if message_id_domain else make_msgid()

    msg.set_content(body)
    if html_body is not None:
        msg.add_alternative(html_body, subtype="html")

    for path in attachments:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"attachment not found: {path}")
        ctype, _ = mimetypes.guess_type(path)
        if ctype is None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        with open(path, "rb") as fh:
            data = fh.read()
        msg.add_attachment(
            data,
            maintype=maintype,
            subtype=subtype,
            filename=os.path.basename(path),
        )

    to_addrs = list(recipients) + list(cc) + list(bcc)

    smtp_cls = smtplib.SMTP_SSL if config.use_ssl else smtplib.SMTP
    client = smtp_cls(config.host, config.port, timeout=config.timeout)
    try:
        if config.use_tls and not config.use_ssl:
            client.starttls()
        if config.username:
            client.login(config.username, config.password)
        refused = client.send_message(msg, from_addr=sender, to_addrs=to_addrs)
    finally:
        try:
            client.quit()
        except Exception:
            pass

    accepted = [a for a in to_addrs if a not in refused]
    return {
        "accepted": accepted,
        "refused": refused,
        "message_id": msg["Message-ID"],
    }
