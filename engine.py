class VeraEngine:
    def __init__(self, store):
        self.store = store

    def compose(self, merchant_id, trigger, customer=None):
        merchant = self.store.get_merchant(merchant_id)

        if not merchant:
            return self.fallback(merchant_id)

        category = merchant.get("category", "").lower()
        identity = merchant.get("identity", {})
        perf = merchant.get("performance", {})
        offers = merchant.get("offers", [])

        owner = identity.get("owner_name", "there")
        top_item = perf.get("top_items", ["best seller"])[0]
        price = "₹299"

        if offers and isinstance(offers, list):
            price = str(offers[0].get("price", "₹299"))

        trigger_type = trigger.get("type", "opportunity").lower()
        reason = trigger.get("reason", "local demand rising")
        trigger_id = trigger.get("id", "t1")

        suppression_key = f"{merchant_id}_{trigger_id}"

        # PRIORITY ENGINE

        # 1 Revenue dip
        if trigger_type in ["dip", "revenue_dip", "slow"]:
            if category == "restaurant":
                return self.response(
                    f"Hi {owner}, lunch orders dipped today. Push your {top_item} at {price} to nearby hungry users now?",
                    "Launch Deal",
                    suppression_key,
                    "Revenue dip + hero item + urgency"
                )

            if category in ["salon", "spa"]:
                return self.response(
                    f"Hi {owner}, bookings are slower today. Fill empty slots with a {price} beauty offer now?",
                    "Fill Slots",
                    suppression_key,
                    "Idle capacity recovery"
                )

        # 2 Search spike
        if trigger_type in ["spike", "search_spike", "trend"]:
            if category == "dentist":
                return self.response(
                    f"Hi Dr. {owner}, dental checkup searches are rising nearby. Offer appointments at {price} this week?",
                    "Yes, Do It",
                    suppression_key,
                    "Intent spike + trust category"
                )

            if category == "gym":
                return self.response(
                    f"Hi {owner}, fitness searches surged nearby. Launch a {price} trial membership today?",
                    "Start Trial",
                    suppression_key,
                    "Intent spike + trial conversion"
                )

        # 3 Festival / seasonal
        if trigger_type in ["festival", "holiday"]:
            if category == "restaurant":
                return self.response(
                    f"Hi {owner}, festive demand is active nearby. Promote your {top_item} special at {price} tonight?",
                    "Promote Tonight",
                    suppression_key,
                    "Seasonal demand"
                )

        # 4 Pharmacy utility
        if category == "pharmacy":
            return self.response(
                f"Hi {owner}, repeat medicine demand is active nearby. Turn on quick refill orders today?",
                "Enable Orders",
                suppression_key,
                "Utility demand"
            )

        # 5 Generic category-specific fallback
        if category == "restaurant":
            return self.response(
                f"Hi {owner}, food demand is active nearby. Promote your {top_item} at {price} today?",
                "Promote Now",
                suppression_key,
                "Default restaurant action"
            )

        if category == "dentist":
            return self.response(
                f"Hi Dr. {owner}, should I help fill this week's appointment slots at {price}?",
                "Book Patients",
                suppression_key,
                "Default dentist action"
            )

        if category in ["salon", "spa"]:
            return self.response(
                f"Hi {owner}, should I help fill today's beauty appointments with a {price} offer?",
                "Fill Appointments",
                suppression_key,
                "Default salon action"
            )

        if category == "gym":
            return self.response(
                f"Hi {owner}, should I attract nearby users with a {price} trial plan today?",
                "Start Offer",
                suppression_key,
                "Default gym action"
            )

        return self.fallback(merchant_id)

    def response(self, msg, cta, key, rationale):
        return {
            "message": msg,
            "cta": cta,
            "send_as": "VERA",
            "suppression_key": key,
            "rationale": rationale
        }

    def fallback(self, merchant_id):
        return {
            "message": "Hi, nearby demand is active. Shall I help grow sales today?",
            "cta": "Show Me",
            "send_as": "VERA",
            "suppression_key": f"default_{merchant_id}",
            "rationale": "Safe fallback"
        }