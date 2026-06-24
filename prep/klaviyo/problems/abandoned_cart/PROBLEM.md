# Abandoned Cart Email System — CodeSignal Simulation

## Context
Klaviyo helps e-commerce merchants send automated emails when customers abandon their shopping carts. You're given intern-level code that tracks cart events and triggers email notifications. Your job: uplevel it to production quality.

## Level 1: Basic Cart Tracking
Implement an `AbandonedCartSystem` that supports:
- `add_item(timestamp, user_id, item_id, price)` → Add item to user's cart. Return the cart total.
- `remove_item(timestamp, user_id, item_id)` → Remove item from cart. Return `True` if removed, `False` if item not in cart.
- `get_cart(timestamp, user_id)` → Return list of `"item_id(price)"` sorted by item_id, or empty string if no cart.

## Level 2: Abandonment Detection & Email Scheduling
- `checkout(timestamp, user_id)` → User completes purchase. Clear their cart. Return cart total or `None` if empty/no cart.
- `get_abandoned_carts(timestamp, timeout)` → Return list of user_ids whose carts have been inactive (no add/remove/checkout) for longer than `timeout` ms. Sorted by last activity time (oldest first), then alphabetically by user_id.

## Level 3: Email Campaign Management
- `schedule_email(timestamp, user_id, template_id, delay)` → Schedule an email to be sent `delay` ms after `timestamp`. Return a unique `email_id` string like `"email1"`, `"email2"`, etc. Return `None` if user has no cart or cart is empty.
- `get_pending_emails(timestamp)` → Return list of `"email_id(user_id)"` for emails that are scheduled but not yet sent (send_time > timestamp). Sorted by send time, then email_id.
- `send_emails(timestamp)` → Send all emails whose scheduled time <= timestamp. Return count of emails sent. An email should NOT be sent if the user has checked out since the email was scheduled.

## Level 4: Analytics & Personalization
- `get_conversion_rate(timestamp)` → Of all users who were sent an abandoned cart email, what percentage later checked out? Return as a string like `"33.33"` (2 decimal places). Return `"0.00"` if no emails sent.
- `get_top_abandoned_items(timestamp, n)` → Return the top `n` most frequently abandoned items (items left in carts that were never checked out). Format: `"item_id(count)"` sorted by count desc, then item_id asc.

## Notes
- All timestamps are in milliseconds
- Prices are integers (cents)
- A cart becomes "active" again on any add_item or remove_item call
- Think about: input validation, edge cases (empty carts, duplicate items), efficiency
