class VeraEngine:
    def __init__(self, store):
        self.store = store

    def compose(self, merchant_id, trigger):
        merchant = self.store.get_merchant(merchant_id)

        if not merchant:
            return self.default_response(merchant_id)

        owner = merchant.get("identity", {}).get("owner_name", "there")
        category = merchant.get("category", "").lower()
        offers = merchant.get("offers", [])
        performance = merchant.get("performance", {})

        top_items = performance.get("top_items", ["best seller"])
        top_item = top_items[0]

        offer_price = "₹299"
        if offers and isinstance(offers, list):
            offer_price = str(offers[0].get("price", "₹299"))

        trigger_type = trigger.get("type", "opportunity").lower()
        reason = trigger.get("reason", "demand rising nearby")
        trigger_id = trigger.get("id", "t1")

        suppression_key = f"{merchant_id}_{trigger_id}"

        # RESTAURANT
        if category == "restaurant":
            if trigger_type in ["dip", "slow", "revenue_dip"]:
                return {
                    "message": f"Hi {owner}, lunch orders dipped today. Push a {top_item} combo at {offer_price} to nearby hungry users?",
                    "cta": "Launch Deal",
                    "send_as": "VERA",
                    "suppression_key": suppression_key,
                    "rationale": "Revenue dip + hero product + immediate CTA"
                }

            return {
                "message": f"Hi {owner}, food demand is rising nearby. Promote your {top_item} now at {offer_price}?",
                "cta": "Promote Now",
                "send_as": "VERA",
                "suppression_key": suppression_key,
                "rationale": "Demand spike + best seller"
            }

        # DENTIST
        elif category == "dentist":
            return {
                "message": f"Hi Dr. {owner}, more people nearby searched dental checkups. Offer a checkup at {offer_price} this week?",
                "cta": "Yes, Do It",
                "send_as": "VERA",
                "suppression_key": suppression_key,
                "rationale": "Clinical trust + search demand + clear booking action"
            }

        # SALON / SPA
        elif category in ["salon", "spa"]:
            return {
                "message": f"Hi {owner}, makeover searches are trending nearby. Fill afternoon slots with a {offer_price} beauty offer?",
                "cta": "Fill Slots",
                "send_as": "VERA",
                "suppression_key": suppression_key,
                "rationale": "Trend demand + unused inventory slots"
            }

        # GYM
        elif category == "gym":
            return {
                "message": f"Hi {owner}, fitness interest is rising nearby. Launch a {offer_price} trial membership today?",
                "cta": "Start Trial Offer",
                "send_as": "VERA",
                "suppression_key": suppression_key,
                "rationale": "High intent + low-friction trial"
            }

        # PHARMACY
        elif category == "pharmacy":
            return {
                "message": f"Hi {owner}, repeat medicine demand is active nearby. Promote fast refill orders today?",
                "cta": "Enable Orders",
                "send_as": "VERA",
                "suppression_key": suppression_key,
                "rationale": "Utility urgency + repeat demand"
            }

        return self.default_response(merchant_id)

    def default_response(self, merchant_id):
        return {
            "message": "Hi, nearby demand is active. Shall I help increase sales today?",
            "cta": "Show Me",
            "send_as": "VERA",
            "suppression_key": f"default_{merchant_id}",
            "rationale": "Safe fallback"
        }