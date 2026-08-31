import base64
import json
import logging
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order, OrderItem, Transaction
from .utils import generate_signature, verify_signature

logger = logging.getLogger(__name__)


@login_required(login_url="login")
def pay_with_esewa(request):
    """
    Reads the cart from the session, creates a PENDING Transaction record,
    signs the payload, and renders a page that auto-submits the form to
    eSewa. The Transaction row is our source of truth — the callback view
    below only trusts data that matches a row we created here.
    """
    cart = request.session.get("cart") or {}
    if not cart:
        return redirect("cart_detail")

    subtotal = sum(item["quantity"] * float(item["price"]) for item in cart.values())
    tax = round(subtotal * 0.13, 2)
    total = round(subtotal + tax, 2)

    txn = Transaction.objects.create(
        user=request.user,
        product_code=settings.ESEWA_PRODUCT_CODE,
        amount=subtotal,
        tax_amount=tax,
        total_amount=total,
    )

    data = {
        "amount": f"{subtotal:.2f}",
        "tax_amount": f"{tax:.2f}",
        "total_amount": f"{total:.2f}",
        "transaction_uuid": str(txn.transaction_uuid),
        "product_code": settings.ESEWA_PRODUCT_CODE,
        "product_service_charge": "0",
        "product_delivery_charge": "0",
        "success_url": request.build_absolute_uri("/esewa/success/"),
        "failure_url": request.build_absolute_uri("/esewa/failure/"),
        "signed_field_names": "total_amount,transaction_uuid,product_code",
    }
    data["signature"] = generate_signature(data, settings.ESEWA_SECRET_KEY)

    return render(request, "redirect_to_esewa.html", {"data": data})


@login_required(login_url="login")
def esewa_success(request):
    encoded_data = request.GET.get("data")
    if not encoded_data:
        return HttpResponse("Invalid response", status=400)

    try:
        payload = json.loads(base64.b64decode(encoded_data).decode("utf-8"))
    except Exception:
        return HttpResponse("Invalid data", status=400)

    if not verify_signature(payload, settings.ESEWA_SECRET_KEY):
        logger.warning("eSewa signature mismatch: %s", payload)
        return render(
            request,
            "failure_esewa.html",
            {"reason": "We couldn't verify this payment's signature."},
        )

    # Must be a transaction WE created for THIS user — never trust the
    # payload alone to decide whose order this is.
    txn = get_object_or_404(
        Transaction,
        transaction_uuid=payload.get("transaction_uuid"),
        user=request.user,
    )

    # Guard against the URL being bookmarked, refreshed, or copy-pasted:
    # if this transaction was already settled, just show that result again
    # instead of re-running the checks and re-clearing the (now possibly
    # different) cart.
    if txn.status == Transaction.STATUS_COMPLETE:
        return render(request, "payments/success_esewa.html", {"transaction": txn})
    if txn.status == Transaction.STATUS_FAILED:
        return render(
            request,
            "failure_esewa.html",
            {"reason": "This payment was already marked as failed."},
        )

    # The amount eSewa confirms must match what we originally charged for.
    # Compare as Decimal, not raw strings — "1623.6" and "1623.60" are the
    # same amount but wouldn't match with a plain string comparison.
    try:
        received_amount = Decimal(str(payload.get("total_amount")))
    except (InvalidOperation, TypeError):
        logger.warning("Non-numeric total_amount on transaction %s", txn.transaction_uuid)
        txn.status = Transaction.STATUS_FAILED
        txn.save(update_fields=["status", "updated_at"])
        return render(
            request,
            "failure_esewa.html",
            {"reason": "Invalid amount received — payment not accepted."},
        )

    if txn.total_amount != received_amount:
        logger.warning("Amount mismatch on transaction %s", txn.transaction_uuid)
        txn.status = Transaction.STATUS_FAILED
        txn.save(update_fields=["status", "updated_at"])
        return render(
            request,
            "failure_esewa.html",
            {"reason": "Amount mismatch detected — payment not accepted."},
        )

    if payload.get("status") != "COMPLETE":
        txn.status = Transaction.STATUS_FAILED
        txn.save(update_fields=["status", "updated_at"])
        return render(
            request,
            "failure_esewa.html",
            {"reason": "Payment was not completed."},
        )

    txn.status = Transaction.STATUS_COMPLETE
    txn.transaction_code = payload.get("transaction_code", "")
    txn.save(update_fields=["status", "transaction_code", "updated_at"])

    # get_or_create keyed on `transaction` (a OneToOneField) means: if an
    # Order for this transaction already exists, just fetch it — don't
    # build a second one. `created` tells us whether this is the first
    # time we've reached this point for this payment.
    order, created = Order.objects.get_or_create(
        transaction=txn,
        defaults={
            "user": request.user,
            "total_amount": txn.total_amount,
        },
    )

    if created:
        cart = request.session.get("cart") or {}
        for item in cart.values():
            OrderItem.objects.create(
                order=order,
                product_id=item["product_id"],
                name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                image=item.get("image", ""),
            )
        request.session["cart"] = {}

    return render(
        request,
        "success_esewa.html",
        {"transaction": txn, "order": order},
    )


@login_required(login_url="login")
def esewa_failure(request):
    txn_uuid = request.GET.get("transaction_uuid")
    if txn_uuid:
        Transaction.objects.filter(
            transaction_uuid=txn_uuid, user=request.user
        ).exclude(status=Transaction.STATUS_COMPLETE).update(
            status=Transaction.STATUS_FAILED
        )

    return render(
        request,
        "failure_esewa.html",
        {"reason": "Payment was cancelled or failed."},
    )