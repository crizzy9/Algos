"""
CODING COLLAB — Mock 3: Event Ingestion Pipeline
=================================================
Scenario: An intern built this event ingestion service that processes
customer behavior events (page views, email opens, purchases, etc.)
and updates user profiles. This feeds Klaviyo's segmentation engine.

Victor says: "We're seeing data inconsistencies in production and this
service is struggling at scale. Walk me through what you'd fix and
what you'd redesign."

YOUR JOB: Review and uplevel. There are 20+ issues.
"""

import sqlite3
import json
import time
import threading
import requests

db = sqlite3.connect("events.db")

db.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        user_email TEXT,
        event_type TEXT,
        properties TEXT,
        timestamp REAL
    )
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        email TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        properties TEXT,
        last_active REAL,
        total_revenue REAL DEFAULT 0
    )
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS segments (
        id INTEGER PRIMARY KEY,
        name TEXT,
        rules TEXT
    )
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS segment_members (
        segment_id INTEGER,
        email TEXT
    )
""")


# Global counters
events_processed = 0
errors = 0


def ingest_event(email, event_type, properties):
    """Process an incoming event."""
    global events_processed, errors

    try:
        # Store the event
        db.execute(
            "INSERT INTO events (user_email, event_type, properties, timestamp) "
            "VALUES ('%s', '%s', '%s', %s)"
            % (email, event_type, json.dumps(properties), time.time())
        )
        db.commit()

        # Update or create profile
        profile = db.execute(
            "SELECT * FROM profiles WHERE email = '%s'" % email
        ).fetchone()

        if profile:
            db.execute(
                "UPDATE profiles SET last_active = %s WHERE email = '%s'"
                % (time.time(), email)
            )
        else:
            db.execute(
                "INSERT INTO profiles (email, first_name, last_name, properties, last_active) "
                "VALUES ('%s', '', '', '{}', %s)" % (email, time.time())
            )

        # Handle purchase events
        if event_type == "purchase":
            amount = properties["total"]
            db.execute(
                "UPDATE profiles SET total_revenue = total_revenue + %s WHERE email = '%s'"
                % (amount, email)
            )

        db.commit()

        # Re-evaluate all segments for this user
        evaluate_segments(email)

        events_processed += 1
        return True

    except:
        errors += 1
        return False


def evaluate_segments(email):
    """Check if user matches any segment rules."""
    segments = db.execute("SELECT * FROM segments").fetchall()
    profile = db.execute(
        "SELECT * FROM profiles WHERE email = '%s'" % email
    ).fetchone()

    if not profile:
        return

    for seg in segments:
        rules = json.loads(seg[2])
        matches = check_rules(profile, rules)

        # Remove from segment first, then add if matches
        db.execute(
            "DELETE FROM segment_members WHERE segment_id = %s AND email = '%s'"
            % (seg[0], email)
        )

        if matches:
            db.execute(
                "INSERT INTO segment_members (segment_id, email) VALUES (%s, '%s')"
                % (seg[0], email)
            )

    db.commit()


def check_rules(profile, rules):
    """Evaluate segment rules against a profile."""
    props = json.loads(profile[3])

    for rule in rules:
        field = rule["field"]
        op = rule["operator"]
        value = rule["value"]

        if field == "total_revenue":
            actual = profile[5]
        elif field == "last_active":
            actual = profile[4]
        else:
            actual = props.get(field)

        if actual is None:
            return False

        if op == "gt" and actual <= value:
            return False
        if op == "lt" and actual >= value:
            return False
        if op == "eq" and actual != value:
            return False
        if op == "contains" and value not in str(actual):
            return False

    return True


def get_profile(email):
    """Get a user profile."""
    row = db.execute(
        "SELECT * FROM profiles WHERE email = '%s'" % email
    ).fetchone()

    if row:
        return {
            "email": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "properties": json.loads(row[3]),
            "last_active": row[4],
            "total_revenue": row[5]
        }
    return None


def get_events(email, event_type=None, limit=100):
    """Get events for a user."""
    if event_type:
        query = "SELECT * FROM events WHERE user_email = '%s' AND event_type = '%s' ORDER BY timestamp DESC LIMIT %s" % (email, event_type, limit)
    else:
        query = "SELECT * FROM events WHERE user_email = '%s' ORDER BY timestamp DESC LIMIT %s" % (email, limit)

    rows = db.execute(query).fetchall()
    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "email": r[1],
            "event_type": r[2],
            "properties": json.loads(r[3]),
            "timestamp": r[4]
        })
    return result


def update_profile(email, fields):
    """Update profile fields."""
    for key, value in fields.items():
        db.execute(
            "UPDATE profiles SET %s = '%s' WHERE email = '%s'"
            % (key, value, email)
        )
    db.commit()
    return True


def get_segment_members(segment_id):
    """Get all members of a segment."""
    rows = db.execute(
        "SELECT * FROM segment_members WHERE segment_id = %s" % segment_id
    ).fetchall()
    emails = []
    for r in rows:
        profile = get_profile(r[1])
        emails.append(profile)
    return emails


def create_segment(name, rules):
    """Create a new segment."""
    db.execute(
        "INSERT INTO segments (name, rules) VALUES ('%s', '%s')"
        % (name, json.dumps(rules))
    )
    db.commit()
    return True


def bulk_ingest(events):
    """Process a batch of events."""
    for e in events:
        ingest_event(e["email"], e["event_type"], e.get("properties", {}))
    return {"processed": len(events)}


def async_ingest(events):
    """Process events asynchronously."""
    t = threading.Thread(target=bulk_ingest, args=(events,))
    t.start()
    return {"status": "processing", "count": len(events)}


def export_segment(segment_id, webhook_url):
    """Export segment members to an external service."""
    members = get_segment_members(segment_id)
    payload = json.dumps({"members": members})
    requests.post(webhook_url, data=payload)
    return {"exported": len(members)}


def compute_metrics(email):
    """Compute engagement metrics for a user."""
    events = get_events(email)
    opens = 0
    clicks = 0
    purchases = 0
    revenue = 0

    for e in events:
        if e["event_type"] == "email_open":
            opens += 1
        if e["event_type"] == "email_click":
            clicks += 1
        if e["event_type"] == "purchase":
            purchases += 1
            revenue += e["properties"]["total"]

    return {
        "opens": opens,
        "clicks": clicks,
        "purchases": purchases,
        "revenue": revenue,
        "avg_order_value": revenue / purchases
    }


def cleanup_old_events(days=90):
    """Delete events older than N days."""
    cutoff = time.time() - (days * 86400)
    db.execute("DELETE FROM events WHERE timestamp < %s" % cutoff)
    db.commit()
