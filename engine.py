class VeraEngine:
    def __init__(self, store):
        self.store = store

    def compose(self, merchant_id, trigger, customer=None):
        merchant = self.store.get_merchant(merchant_id)

        category = merchant.get("category", "business").lower()
        identity = merchant.get("identity", {})
        perf = merchant.get("performance", {})
        offers = merchant.get("offers", [])

        owner = identity.get("owner_name", "Partner")
        top_item = self.get_top_item(perf, category)
        price = self.get_price(offers)

        trigger_type = trigger.get("type", "opportunity").lower()
        reason = trigger.get("reason", "local demand rising")
        trigger_id = trigger.get("id", "t1")

        suppression_key = f"{merchant_id}_{trigger_id}"

        action = self.trigger_message(
            owner,
            category,
            top_item,
            price,
            trigger_type,
            reason,
            suppression_key
        )

        return {
            "actions": [action]
        }

    def trigger_message(
        self,
        owner,
        category,
        top_item,
        price,
        trigger_type,
        reason,
        suppression_key
    ):

        # 1 revenue dip
        if trigger_type in ["dip", "revenue_dip", "slow"]:
            if category == "restaurant":
                return self.make_action(
                    "pitch",
                    f"Hi {owner}, lunch orders dipped today. Push {top_item} at {price} to nearby hungry users now?",
                    "Launch Deal",
                    suppression_key
                )

            if category in ["salon", "spa"]:
                return self.make_action(
                    "pitch",
                    f"Hi {owner}, bookings are slow. Fill empty slots with a {price} beauty offer?",
                    "Fill Slots",
                    suppression_key
                )

        # 2 search spike
        if trigger_type in ["spike", "search_spike", "trend"]:
            if category == "dentist":
                return self.make_action(
                    "pitch",
                    f"Hi Dr. {owner}, dental searches are rising nearby. Promote checkups at {price} this week?",
                    "Start Campaign",
                    suppression_key
                )

            if category == "gym":
                return self.make_action(
                    "pitch",
                    f"Hi {owner}, fitness demand surged nearby. Launch {price} trial membership today?",
                    "Start Trial",
                    suppression_key
                )

        # 3 festival
        if trigger_type in ["festival", "holiday"]:
            return self.make_action(
                "pitch",
                f"Hi {owner}, festive demand is active nearby. Promote {top_item} special tonight?",
                "Promote Tonight",
                suppression_key
            )

        # 4 repeat customers
        if trigger_type in ["repeat", "retention"]:
            return self.make_action(
                "pitch",
                f"Hi {owner}, previous customers are likely to reorder. Send comeback offer at {price}?",
                "Send Offer",
                suppression_key
            )

        # 5 competitor gap
        if trigger_type in ["competitor", "market_gap"]:
            return self.make_action(
                "pitch",
                f"Hi {owner}, nearby competitors look inactive. Capture extra demand now with {price} promo?",
                "Capture Demand",
                suppression_key
            )

        # 6 urgency
        if trigger_type in ["weather", "weekend", "opportunity"]:
            return self.make_action(
                "pitch",
                f"Hi {owner}, local demand is rising now. Promote {top_item} at {price} today?",
                "Promote Now",
                suppression_key
            )

        # fallback
        return self.make_action(
            "pitch",
            f"Hi {owner}, want help growing sales today?",
            "Show Me",
            suppression_key
        )

    def make_action(self, action, message, cta, key):
        return {
            "action": action,
            "message": message,
            "cta": cta,
            "send_as": "VERA",
            "suppression_key": key
        }

    def get_price(self, offers):
        if offers and isinstance(offers, list):
            try:
                return str(offers[0].get("price", "₹299"))
            except:
                return "₹299"
        return "₹299"

    def get_top_item(self, perf, category):
        items = perf.get("top_items", [])
        if items:
            return items[0]

        defaults = {
            "restaurant": "best seller combo",
            "dentist": "checkup package",
            "salon": "beauty package",
            "spa": "spa package",
            "gym": "trial membership",
            "pharmacy": "quick refill"
        }

        return defaults.get(category, "top offer")