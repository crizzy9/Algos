echo 'Hello'

# requirements

# - checkout is only events

# - volume - (start 10/sec events across 20k users then scale later)

# - will by async thread for email

# -

# questions

# - what are ways to make it keep working if the databse host

# UI

- sends api calls to server regarding cart

# API Server

- sending current cart data as events

# Cron 1

- reads current cart data and queries the payment provider (gets all payment data first for the cart and then checks current cart data . Get all completed cart_ids from stripe and deletes those)

# Cron 2

- analyzing the abandon carts from the db and sending emails

table 1 - carts
{
"cart_id",
"store_id",
"user_details",
"timestamp"
}

cart_items
{

}

# db goes down

db1 - primary replica
db2 - secondary read replica
db3 - ...

partitioning

- partioining events by year, month, day

[ sns, kafka]
[API server, checkout started] -> [sns] -> [sqs] -> [db]
-> [if db fail] -> [hold items in queue until db is back up] -> start feeding events into the db

consumer on a schedule (sns, kafka) -> (lets assume 1 day timeout after which events for checkout completed are checked) -> start a new async thread which sends email (dont read db)

[kafka, ]

(delay hours setting) (for abandoned for 2 hours)

-> send checkout event started, we also send delay_hours

-> create a customizable consumer pipeline which maintains a queue of checkout started events to processes as the time gets closer to delay_hours
-> abandoned: yes/no
-> start async thread for sending emails

server is getting saturated with api requests
10/sec to 5k/sec

10 reqs are handled by 1 pod then 5k requests 500 pods

add caching mechanism

most of events are coming from a single customer - add throttling

---

Question:

You are hired as the lead engineer for a small startup working in eCommerce. One of this
startup's products is "abandoned cart" emails. The company provides an integration with
storefront providers that sends an email to shoppers when they have left items in their
cart. Store owners interact with your web UI to configure their abandoned cart emails.

The existing system consists of five hand-configured servers deployed in AWS, running
Linux (see the diagram below). When the code runs in the various steps detailed on the
diagram, the end result is emails being sent to stores' customers with notifications
about their abandoned carts.

This interview is split into two parts. The first part is focused on operating and
maintaining the current system. The second part is focused on extending the system and
adding new features. Note that there is no one right answer to these questions.
Sometimes incremental changes are appropriate, for others bigger architectural changes
may be better.
