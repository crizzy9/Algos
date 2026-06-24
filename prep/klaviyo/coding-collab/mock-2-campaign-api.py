"""
CODING COLLAB — Mock 2: Email Campaign API
===========================================
Scenario: An intern built this API for managing email campaigns. Merchants
use it to create campaigns, add recipients from segments, and track sends.
This powers the campaign builder UI in Klaviyo's dashboard.

Victor says: "This is working in staging but we've gotten reports of slow
queries and some data issues. Can you walk me through what needs to change
before we ship this?"

YOUR JOB: Review and uplevel. There are 18+ issues.
"""

import sqlite3
import hashlib
import os
import json
from datetime import datetime

API_KEY = "sk_live_klaviyo_abc123def456"

conn = sqlite3.connect("campaigns.db")
conn.execute("PRAGMA journal_mode=WAL")

conn.execute("""
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY,
        name TEXT,
        subject TEXT,
        body TEXT,
        status TEXT DEFAULT 'draft',
        created_by TEXT,
        created_at TEXT,
        scheduled_for TEXT,
        sent_count INTEGER DEFAULT 0
    )
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS recipients (
        id INTEGER PRIMARY KEY,
        campaign_id INTEGER,
        email TEXT,
        name TEXT,
        sent INTEGER DEFAULT 0,
        opened INTEGER DEFAULT 0,
        clicked INTEGER DEFAULT 0
    )
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS templates (
        id INTEGER PRIMARY KEY,
        name TEXT,
        html TEXT,
        vars TEXT
    )
""")


def authenticate(key):
    if key == API_KEY:
        return True
    return False


def create_campaign(api_key, name, subject, body, scheduled_for=None):
    if not authenticate(api_key):
        return {"error": "unauthorized"}

    conn.execute(
        "INSERT INTO campaigns (name, subject, body, created_by, created_at, scheduled_for) "
        "VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"
        % (name, subject, body, api_key, datetime.now(), scheduled_for)
    )
    conn.commit()
    id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    return {"id": id, "status": "draft"}


def get_campaign(api_key, campaign_id):
    if not authenticate(api_key):
        return {"error": "unauthorized"}

    row = conn.execute(
        "SELECT * FROM campaigns WHERE id = %s" % campaign_id
    ).fetchone()

    if row:
        return {
            "id": row[0], "name": row[1], "subject": row[2],
            "body": row[3], "status": row[4], "created_by": row[5],
            "created_at": row[6], "scheduled_for": row[7],
            "sent_count": row[8]
        }
    return {"error": "not found"}


def list_campaigns(api_key):
    if not authenticate(api_key):
        return {"error": "unauthorized"}

    rows = conn.execute("SELECT * FROM campaigns").fetchall()
    campaigns = []
    for row in rows:
        c = get_campaign(api_key, row[0])
        campaigns.append(c)
    return campaigns


def add_recipients(api_key, campaign_id, emails):
    """Add a list of email addresses as recipients."""
    if not authenticate(api_key):
        return {"error": "unauthorized"}

    count = 0
    for email in emails:
        conn.execute(
            "INSERT INTO recipients (campaign_id, email, name) "
            "VALUES (%s, '%s', '%s')" % (campaign_id, email, "")
        )
        count += 1
    conn.commit()
    return {"added": count}


def get_recipients(api_key, campaign_id):
    if not authenticate(api_key):
        return {"error": "unauthorized"}

    rows = conn.execute(
        "SELECT * FROM recipients WHERE campaign_id = %s" % campaign_id
    ).fetchall()

    result = []
    for r in rows:
        result.append({
            "id": r[0], "email": r[2], "name": r[3],
            "sent": r[4], "opened": r[5], "clicked": r[6]
        })
    return result


def send_campaign(api_key, campaign_id):
    """Send the campaign to all recipients."""
    if not authenticate(api_key):
        return {"error": "unauthorized"}

    campaign = get_campaign(api_key, campaign_id)
    if campaign.get("error"):
        return campaign

    recipients = get_recipients(api_key, campaign_id)

    sent = 0
    for r in recipients:
        # simulate sending email
        print(f"Sending to {r['email']}: {campaign['subject']}")
        conn.execute(
            "UPDATE recipients SET sent = 1 WHERE id = %s" % r["id"]
        )
        sent += 1

    conn.execute(
        "UPDATE campaigns SET status = 'sent', sent_count = %s WHERE id = %s"
        % (sent, campaign_id)
    )
    conn.commit()
    return {"sent": sent}


def render_template(template_id, data):
    """Render an email template with variable substitution."""
    row = conn.execute(
        "SELECT * FROM templates WHERE id = %s" % template_id
    ).fetchone()

    if not row:
        return None

    html = row[2]
    for key in data:
        html = html.replace("{{" + key + "}}", data[key])

    return html


def get_campaign_stats(api_key, campaign_id):
    """Get open/click stats for a campaign."""
    if not authenticate(api_key):
        return {"error": "unauthorized"}

    recipients = get_recipients(api_key, campaign_id)
    total = len(recipients)
    opened = 0
    clicked = 0

    for r in recipients:
        if r["opened"]:
            opened += 1
        if r["clicked"]:
            clicked += 1

    return {
        "total": total,
        "sent": total,
        "opened": opened,
        "clicked": clicked,
        "open_rate": opened / total * 100,
        "click_rate": clicked / total * 100
    }


def duplicate_campaign(api_key, campaign_id):
    """Create a copy of an existing campaign."""
    if not authenticate(api_key):
        return {"error": "unauthorized"}

    original = get_campaign(api_key, campaign_id)
    if original.get("error"):
        return original

    return create_campaign(
        api_key,
        original["name"] + " (copy)",
        original["subject"],
        original["body"]
    )


def search_campaigns(api_key, query):
    """Search campaigns by name."""
    if not authenticate(api_key):
        return {"error": "unauthorized"}

    rows = conn.execute(
        "SELECT * FROM campaigns WHERE name LIKE '%%%s%%'" % query
    ).fetchall()

    results = []
    for row in rows:
        results.append({"id": row[0], "name": row[1], "status": row[4]})
    return results


def delete_campaign(api_key, campaign_id):
    if not authenticate(api_key):
        return {"error": "unauthorized"}

    conn.execute("DELETE FROM campaigns WHERE id = %s" % campaign_id)
    conn.execute("DELETE FROM recipients WHERE campaign_id = %s" % campaign_id)
    conn.commit()
    return {"deleted": True}


def schedule_campaign(api_key, campaign_id, send_time):
    """Schedule a campaign to send at a specific time."""
    if not authenticate(api_key):
        return {"error": "unauthorized"}

    conn.execute(
        "UPDATE campaigns SET status = 'scheduled', scheduled_for = '%s' WHERE id = %s"
        % (send_time, campaign_id)
    )
    conn.commit()
    return {"scheduled": True}


def process_scheduled():
    """Check for campaigns that need to be sent now."""
    now = str(datetime.now())
    rows = conn.execute(
        "SELECT * FROM campaigns WHERE status = 'scheduled' AND scheduled_for <= '%s'" % now
    ).fetchall()

    for row in rows:
        send_campaign(API_KEY, row[0])
