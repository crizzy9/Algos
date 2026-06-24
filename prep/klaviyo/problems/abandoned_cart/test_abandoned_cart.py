"""
Tests for Abandoned Cart Email System.
Run: pytest prep/klaviyo/problems/abandoned_cart/test_abandoned_cart.py -v
"""
import pytest


class TestLevel1_CartTracking:
    """Basic cart operations: add, remove, get"""

    def test_add_single_item(self, system):
        assert system.add_item(1000, "user1", "shoes", 5999) == 5999

    def test_add_multiple_items(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        assert system.add_item(1100, "user1", "socks", 999) == 6998

    def test_add_item_different_users(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        assert system.add_item(1000, "user2", "hat", 2499) == 2499

    def test_remove_item_success(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        assert system.remove_item(1100, "user1", "shoes") is True

    def test_remove_item_not_in_cart(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        assert system.remove_item(1100, "user1", "hat") is False

    def test_remove_item_no_cart(self, system):
        assert system.remove_item(1000, "user1", "shoes") is False

    def test_get_cart_sorted(self, system):
        system.add_item(1000, "user1", "socks", 999)
        system.add_item(1100, "user1", "belt", 2499)
        system.add_item(1200, "user1", "shoes", 5999)
        assert system.get_cart(1300, "user1") == "belt(2499), shoes(5999), socks(999)"

    def test_get_cart_empty(self, system):
        assert system.get_cart(1000, "user1") == ""

    def test_get_cart_after_remove_all(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.remove_item(1100, "user1", "shoes")
        assert system.get_cart(1200, "user1") == ""


class TestLevel2_AbandonmentDetection:
    """Checkout and abandoned cart detection"""

    def test_checkout_returns_total(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.add_item(1100, "user1", "socks", 999)
        assert system.checkout(2000, "user1") == 6998

    def test_checkout_clears_cart(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.checkout(2000, "user1")
        assert system.get_cart(2100, "user1") == ""

    def test_checkout_empty_cart(self, system):
        assert system.checkout(1000, "user1") is None

    def test_checkout_already_empty(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.checkout(2000, "user1")
        assert system.checkout(3000, "user1") is None

    def test_abandoned_carts_basic(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.add_item(2000, "user2", "hat", 2499)
        # timeout=5000, at ts=8000: user1 inactive for 7000ms (>5000), user2 for 6000ms (>5000)
        result = system.get_abandoned_carts(8000, 5000)
        assert result == ["user1", "user2"]

    def test_abandoned_carts_excludes_active(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.add_item(2000, "user2", "hat", 2499)
        system.add_item(7500, "user2", "belt", 1999)  # user2 active again
        result = system.get_abandoned_carts(8000, 5000)
        assert result == ["user1"]

    def test_abandoned_carts_excludes_checked_out(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.add_item(2000, "user2", "hat", 2499)
        system.checkout(3000, "user2")
        result = system.get_abandoned_carts(8000, 5000)
        assert result == ["user1"]

    def test_abandoned_carts_sort_order(self, system):
        system.add_item(3000, "charlie", "shoes", 5999)
        system.add_item(2000, "bob", "hat", 2499)
        system.add_item(1000, "alice", "belt", 1999)
        # All abandoned. Sort by last_activity asc, then name asc
        result = system.get_abandoned_carts(20000, 5000)
        assert result == ["alice", "bob", "charlie"]

    def test_abandoned_carts_same_timestamp_alpha_sort(self, system):
        system.add_item(1000, "zara", "shoes", 5999)
        system.add_item(1000, "alice", "hat", 2499)
        result = system.get_abandoned_carts(8000, 5000)
        assert result == ["alice", "zara"]


class TestLevel3_EmailCampaigns:
    """Email scheduling and sending"""

    def test_schedule_email(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        eid = system.schedule_email(2000, "user1", "cart_reminder", 3600000)
        assert eid == "email1"

    def test_schedule_email_no_cart(self, system):
        assert system.schedule_email(1000, "user1", "cart_reminder", 3600000) is None

    def test_schedule_email_empty_cart(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.remove_item(1100, "user1", "shoes")
        assert system.schedule_email(2000, "user1", "cart_reminder", 3600000) is None

    def test_schedule_multiple_emails(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.add_item(1000, "user2", "hat", 2499)
        assert system.schedule_email(2000, "user1", "tmpl1", 5000) == "email1"
        assert system.schedule_email(2000, "user2", "tmpl1", 5000) == "email2"

    def test_get_pending_emails(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.add_item(1000, "user2", "hat", 2499)
        system.schedule_email(2000, "user1", "tmpl1", 5000)  # sends at 7000
        system.schedule_email(2000, "user2", "tmpl1", 3000)  # sends at 5000
        result = system.get_pending_emails(4000)
        assert result == ["email1(user1)", "email2(user2)"]

    def test_get_pending_excludes_past_send_time(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.schedule_email(2000, "user1", "tmpl1", 1000)  # sends at 3000
        result = system.get_pending_emails(4000)
        assert result == []

    def test_send_emails_basic(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.schedule_email(2000, "user1", "tmpl1", 3000)  # sends at 5000
        assert system.send_emails(5000) == 1

    def test_send_emails_not_if_checked_out(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.schedule_email(2000, "user1", "tmpl1", 5000)  # sends at 7000
        system.checkout(3000, "user1")  # checked out after scheduling
        assert system.send_emails(7000) == 0

    def test_send_emails_only_ready(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.add_item(1000, "user2", "hat", 2499)
        system.schedule_email(2000, "user1", "tmpl1", 3000)  # sends at 5000
        system.schedule_email(2000, "user2", "tmpl1", 8000)  # sends at 10000
        assert system.send_emails(5000) == 1

    def test_send_emails_idempotent(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.schedule_email(2000, "user1", "tmpl1", 3000)
        system.send_emails(5000)
        assert system.send_emails(6000) == 0  # already sent


class TestLevel4_Analytics:
    """Conversion rate and top abandoned items"""

    def test_conversion_rate_no_emails(self, system):
        assert system.get_conversion_rate(1000) == "0.00"

    def test_conversion_rate_basic(self, system):
        # 3 users get emails, 1 converts
        for uid in ["user1", "user2", "user3"]:
            system.add_item(1000, uid, "shoes", 5999)
            system.schedule_email(2000, uid, "tmpl1", 3000)
        system.send_emails(5000)
        # user1 checks out after getting email
        system.add_item(5500, "user1", "shoes", 5999)
        system.checkout(6000, "user1")
        assert system.get_conversion_rate(7000) == "33.33"

    def test_conversion_rate_all_convert(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.schedule_email(2000, "user1", "tmpl1", 3000)
        system.send_emails(5000)
        system.add_item(5500, "user1", "shoes", 5999)
        system.checkout(6000, "user1")
        assert system.get_conversion_rate(7000) == "100.00"

    def test_top_abandoned_items(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.add_item(1000, "user2", "shoes", 5999)
        system.add_item(1000, "user3", "shoes", 5999)
        system.add_item(1000, "user1", "hat", 2499)
        system.add_item(1000, "user2", "hat", 2499)
        system.add_item(1000, "user1", "belt", 1999)
        result = system.get_top_abandoned_items(20000, 2)
        assert result == ["shoes(3)", "hat(2)"]

    def test_top_abandoned_excludes_checked_out(self, system):
        system.add_item(1000, "user1", "shoes", 5999)
        system.add_item(1000, "user2", "shoes", 5999)
        system.checkout(2000, "user1")
        result = system.get_top_abandoned_items(20000, 5)
        assert result == ["shoes(1)"]

    def test_top_abandoned_tiebreak(self, system):
        system.add_item(1000, "user1", "zebra", 100)
        system.add_item(1000, "user2", "apple", 200)
        result = system.get_top_abandoned_items(20000, 5)
        # same count (1 each), sort alphabetically
        assert result == ["apple(1)", "zebra(1)"]


@pytest.fixture
def system():
    """Provide a fresh AbandonedCartSystem for each test."""
    from prep.klaviyo.problems.abandoned_cart.simulation import AbandonedCartSystem
    return AbandonedCartSystem()
