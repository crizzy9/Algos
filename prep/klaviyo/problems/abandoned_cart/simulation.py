"""
INTERN CODE — Abandoned Cart Email System
You've been handed this from a junior dev. Uplevel it to senior/staff quality.

Issues to find and fix:
- Poor naming, no type hints
- No input validation
- Inefficient data structures
- Missing edge cases
- No separation of concerns
- Security/correctness issues
"""

carts = {}
emails = []
email_count = 0
checkouts = []
last_touch = {}

def add_item(ts, uid, iid, p):
    global carts, last_touch
    if uid not in carts:
        carts[uid] = []
    carts[uid].append([iid, p])
    last_touch[uid] = ts
    total = 0
    for item in carts[uid]:
        total += item[1]
    return total

def remove_item(ts, uid, iid):
    global carts, last_touch
    if uid in carts:
        for i in range(len(carts[uid])):
            if carts[uid][i][0] == iid:
                carts[uid].pop(i)
                last_touch[uid] = ts
                return True
    return False

def get_cart(ts, uid):
    if uid in carts:
        result = ""
        items = sorted(carts[uid], key=lambda x: x[0])
        for item in items:
            result += item[0] + "(" + str(item[1]) + "), "
        return result[:-2]  # chop off last ", "
    return ""

def checkout(ts, uid):
    global carts, checkouts
    if uid in carts and len(carts[uid]) > 0:
        total = 0
        for item in carts[uid]:
            total += item[1]
        checkouts.append([uid, ts])
        carts[uid] = []
        return total
    return None

def get_abandoned(ts, timeout):
    result = []
    for uid in carts:
        if len(carts[uid]) > 0 and ts - last_touch[uid] > timeout:
            result.append([uid, last_touch[uid]])
    result.sort(key=lambda x: (x[1], x[0]))
    return [r[0] for r in result]

def schedule_email(ts, uid, template, delay):
    global emails, email_count
    if uid in carts and len(carts[uid]) > 0:
        email_count += 1
        eid = "email" + str(email_count)
        emails.append({
            "id": eid,
            "user": uid,
            "template": template,
            "scheduled": ts,
            "send_at": ts + delay,
            "sent": False
        })
        return eid
    return None

def get_pending(ts):
    result = []
    for e in emails:
        if not e["sent"] and e["send_at"] > ts:
            result.append(e["id"] + "(" + e["user"] + ")")
    return sorted(result)

def send_emails(ts):
    global emails, checkouts
    count = 0
    for e in emails:
        if not e["sent"] and e["send_at"] <= ts:
            # check if user checked out after email was scheduled
            checked_out = False
            for c in checkouts:
                if c[0] == e["user"] and c[1] > e["scheduled"]:
                    checked_out = True
            if not checked_out:
                e["sent"] = True
                count += 1
            else:
                e["sent"] = True  # mark as sent so we don't process again
    return count

def conversion_rate(ts):
    emailed_users = set()
    for e in emails:
        if e["sent"]:
            emailed_users.add(e["user"])
    if len(emailed_users) == 0:
        return "0.00"
    converted = 0
    for uid in emailed_users:
        for c in checkouts:
            if c[0] == uid:
                converted += 1
                break
    rate = (converted / len(emailed_users)) * 100
    return f"{rate:.2f}"

def top_abandoned(ts, n):
    item_counts = {}
    for uid in carts:
        if len(carts[uid]) > 0:
            # check user hasn't checked out
            has_checkout = False
            for c in checkouts:
                if c[0] == uid:
                    has_checkout = True
            if not has_checkout:
                for item in carts[uid]:
                    iid = item[0]
                    if iid in item_counts:
                        item_counts[iid] += 1
                    else:
                        item_counts[iid] = 1
    result = sorted(item_counts.items(), key=lambda x: (-x[1], x[0]))
    return [f"{iid}({count})" for iid, count in result[:n]]
