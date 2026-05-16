import os
from unittest.mock import MagicMock, patch

import pytest

from email_sender import SMTPConfig, send_email


def _config(**overrides):
    base = dict(host="smtp.example.com", port=587, username="u", password="p")
    base.update(overrides)
    return SMTPConfig(**base)


@patch("email_sender.smtplib.SMTP")
def test_basic_text_send(mock_smtp_cls):
    client = MagicMock()
    client.send_message.return_value = {}
    mock_smtp_cls.return_value = client

    result = send_email(
        _config(),
        sender="from@example.com",
        recipients=["a@example.com"],
        subject="hi",
        body="hello",
    )

    mock_smtp_cls.assert_called_once_with("smtp.example.com", 587, timeout=30.0)
    client.starttls.assert_called_once()
    client.login.assert_called_once_with("u", "p")
    client.send_message.assert_called_once()
    sent_msg = client.send_message.call_args.args[0]
    assert sent_msg["From"] == "from@example.com"
    assert sent_msg["To"] == "a@example.com"
    assert sent_msg["Subject"] == "hi"
    assert "hello" in sent_msg.get_content()
    assert result["accepted"] == ["a@example.com"]
    assert result["refused"] == {}
    assert result["message_id"].startswith("<")


@patch("email_sender.smtplib.SMTP")
def test_html_alternative(mock_smtp_cls):
    client = MagicMock()
    client.send_message.return_value = {}
    mock_smtp_cls.return_value = client

    send_email(
        _config(),
        sender="from@example.com",
        recipients=["a@example.com"],
        subject="s",
        body="plain",
        html_body="<p>html</p>",
    )

    sent_msg = client.send_message.call_args.args[0]
    assert sent_msg.is_multipart()
    payloads = [p.get_content_type() for p in sent_msg.iter_parts()]
    assert "text/plain" in payloads
    assert "text/html" in payloads


@patch("email_sender.smtplib.SMTP_SSL")
def test_ssl_path(mock_smtp_ssl_cls):
    client = MagicMock()
    client.send_message.return_value = {}
    mock_smtp_ssl_cls.return_value = client

    send_email(
        _config(use_tls=False, use_ssl=True, port=465),
        sender="from@example.com",
        recipients=["a@example.com"],
        subject="s",
        body="b",
    )

    mock_smtp_ssl_cls.assert_called_once_with("smtp.example.com", 465, timeout=30.0)
    client.starttls.assert_not_called()


@patch("email_sender.smtplib.SMTP")
def test_cc_and_bcc_routing(mock_smtp_cls):
    client = MagicMock()
    client.send_message.return_value = {}
    mock_smtp_cls.return_value = client

    send_email(
        _config(),
        sender="from@example.com",
        recipients=["a@example.com"],
        subject="s",
        body="b",
        cc=["c@example.com"],
        bcc=["bcc@example.com"],
    )

    sent_msg = client.send_message.call_args.args[0]
    to_addrs = client.send_message.call_args.kwargs["to_addrs"]
    assert sent_msg["Cc"] == "c@example.com"
    assert sent_msg["Bcc"] is None or "bcc@example.com" not in (sent_msg["Bcc"] or "")
    assert "bcc@example.com" in to_addrs
    assert "c@example.com" in to_addrs


@patch("email_sender.smtplib.SMTP")
def test_reply_to_header(mock_smtp_cls):
    client = MagicMock()
    client.send_message.return_value = {}
    mock_smtp_cls.return_value = client

    send_email(
        _config(),
        sender="from@example.com",
        recipients=["a@example.com"],
        subject="s",
        body="b",
        reply_to="reply@example.com",
    )

    sent_msg = client.send_message.call_args.args[0]
    assert sent_msg["Reply-To"] == "reply@example.com"


@patch("email_sender.smtplib.SMTP")
def test_attachment_from_path(mock_smtp_cls, tmp_path):
    client = MagicMock()
    client.send_message.return_value = {}
    mock_smtp_cls.return_value = client

    f = tmp_path / "note.txt"
    f.write_bytes(b"file-bytes")

    send_email(
        _config(),
        sender="from@example.com",
        recipients=["a@example.com"],
        subject="s",
        body="b",
        attachments=[str(f)],
    )

    sent_msg = client.send_message.call_args.args[0]
    parts = list(sent_msg.iter_attachments())
    assert len(parts) == 1
    att = parts[0]
    assert att.get_filename() == "note.txt"
    assert att.get_content_type() == "text/plain"
    assert att.get_payload(decode=True) == b"file-bytes"


@patch("email_sender.smtplib.SMTP")
def test_refused_recipient(mock_smtp_cls):
    client = MagicMock()
    client.send_message.return_value = {"bad@example.com": (550, b"User unknown")}
    mock_smtp_cls.return_value = client

    result = send_email(
        _config(),
        sender="from@example.com",
        recipients=["a@example.com", "bad@example.com"],
        subject="s",
        body="b",
    )

    assert "bad@example.com" in result["refused"]
    assert result["accepted"] == ["a@example.com"]


@patch("email_sender.smtplib.SMTP")
def test_no_username_skips_login(mock_smtp_cls):
    client = MagicMock()
    client.send_message.return_value = {}
    mock_smtp_cls.return_value = client

    send_email(
        _config(username="", password=""),
        sender="from@example.com",
        recipients=["a@example.com"],
        subject="s",
        body="b",
    )
    client.login.assert_not_called()


def test_attachment_missing_raises(tmp_path):
    missing = tmp_path / "nope.txt"
    with pytest.raises(FileNotFoundError):
        send_email(
            _config(),
            sender="from@example.com",
            recipients=["a@example.com"],
            subject="s",
            body="b",
            attachments=[str(missing)],
        )


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(config=SMTPConfig(host="", port=587)),
        dict(config=SMTPConfig(host="h", port=0)),
        dict(config=SMTPConfig(host="h", port=70000)),
        dict(config=SMTPConfig(host="h", port=587, use_tls=True, use_ssl=True)),
        dict(sender=""),
        dict(recipients=[]),
    ],
)
def test_invalid_inputs_raise(kwargs):
    base = dict(
        config=_config(),
        sender="from@example.com",
        recipients=["a@example.com"],
        subject="s",
        body="b",
    )
    base.update(kwargs)
    with pytest.raises(ValueError):
        send_email(**base)
