import base64
import hashlib
import hmac


def generate_signature(data: dict, secret: str) -> str:
    """
    Builds the HMAC-SHA256 signature eSewa expects, based on the fields
    listed in data['signed_field_names'], joined in that exact order.
    """
    signed_fields = data["signed_field_names"].split(",")
    message = ",".join(f"{field}={data[field]}" for field in signed_fields)

    digest = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    return base64.b64encode(digest).decode("utf-8")


def verify_signature(payload: dict, secret: str) -> bool:
    """
    Recomputes the signature from a callback payload and compares it
    against the one eSewa sent, using a constant-time comparison so the
    check itself can't leak timing information.
    """
    try:
        expected = generate_signature(payload, secret)
    except KeyError:
        return False
    return hmac.compare_digest(expected, payload.get("signature", ""))