"""
CODING COLLAB — Mock 1: Webhook Delivery Service
=================================================
Scenario: An intern built this webhook delivery service for Klaviyo's
integration platform. When a merchant sets up a flow (e.g., abandoned cart),
Klaviyo needs to send webhook events to the merchant's configured endpoint.

Victor says: "Take a look at this code. The intern got it working in dev,
but we need to get it production-ready. Walk me through what you'd change
and why."

YOUR JOB: Read through this code, identify all issues, and refactor it.
Think out loud as you work.

HINT: There are 15+ issues across security, scalability, correctness,
and code quality. Can you find them all?
"""

import sqlite3
import requests
import json
import time

db = sqlite3.connect("webhooks.db")

# create the table if it doesn't exist
db.execute("""
    CREATE TABLE IF NOT EXISTS webhooks (
        id INTEGER PRIMARY KEY,
        url TEXT,
        secret TEXT,
        events TEXT,
        active INTEGER
    )
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS deliveries (
        id INTEGER PRIMARY KEY,
        webhook_id INTEGER,
        event_type TEXT,
        payload TEXT,
        status TEXT,
        created_at TEXT
    )
""")


def register_webhook(url, secret, events):
    """Register a new webhook endpoint."""
    db.execute(
        "INSERT INTO webhooks (url, secret, events, active) VALUES ('%s', '%s', '%s', 1)"
        % (url, secret, json.dumps(events))
    )
    db.commit()
    return True


def delete_webhook(id):
    """Delete a webhook."""
    db.execute("DELETE FROM webhooks WHERE id = %s" % id)
    db.commit()


def get_webhooks():
    """Get all webhooks."""
    rows = db.execute("SELECT * FROM webhooks").fetchall()
    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "url": r[1],
            "secret": r[2],
            "events": r[3],
            "active": r[4]
        })
    return result


def send_webhook(event_type, data):
    """Send a webhook event to all registered endpoints."""
    webhooks = get_webhooks()

    for wh in webhooks:
        if event_type in wh["events"]:
            payload = json.dumps({
                "event": event_type,
                "data": data,
                "timestamp": time.time()
            })

            try:
                r = requests.post(
                    wh["url"],
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )

                if r.status_code == 200:
                    status = "delivered"
                else:
                    status = "failed"

            except:
                status = "failed"

            db.execute(
                "INSERT INTO deliveries (webhook_id, event_type, payload, status, created_at) VALUES (%s, '%s', '%s', '%s', '%s')"
                % (wh["id"], event_type, payload, status, time.time())
            )
            db.commit()

    return "done"


def get_deliveries(webhook_id):
    """Get delivery history for a webhook."""
    rows = db.execute(
        "SELECT * FROM deliveries WHERE webhook_id = %s" % webhook_id
    ).fetchall()
    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "webhook_id": r[1],
            "event_type": r[2],
            "payload": r[3],
            "status": r[4],
            "created_at": r[5]
        })
    return result


def retry_failed():
    """Retry all failed deliveries."""
    failed = db.execute(
        "SELECT * FROM deliveries WHERE status = 'failed'"
    ).fetchall()

    for f in failed:
        wh = db.execute(
            "SELECT * FROM webhooks WHERE id = %s" % f[1]
        ).fetchone()

        if wh:
            try:
                r = requests.post(
                    wh[1],
                    data=f[3],
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                if r.status_code == 200:
                    db.execute(
                        "UPDATE deliveries SET status = 'delivered' WHERE id = %s" % f[0]
                    )
                    db.commit()
            except:
                pass


def check_health(url):
    """Check if a webhook endpoint is healthy."""
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return True
    except:
        pass
    return False


# This runs when someone triggers an abandoned cart event
def handle_abandoned_cart(user_email, cart_items, cart_total):
    """Process an abandoned cart event."""
    data = {
        "email": user_email,
        "items": cart_items,
        "total": cart_total,
        "currency": "USD"
    }
    send_webhook("abandoned_cart", data)

    # also send a follow-up reminder after 1 hour
    time.sleep(3600)
    send_webhook("abandoned_cart_reminder", data)
