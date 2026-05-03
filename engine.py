class VeraEngine:
    def __init__(self, store):
        self.store = store

    def compose(self, merchant_id, trigger, customer=None):
        merchant = self.store.get_merchant(merchant_id)

        category = merchant.get("category", "business").lower()
        owner = merchant.get("identity", {}).get("owner_name", "Partner")

        trigger_type = trigger.get("type", "opportunity").lower()

        top_offer = self.get_offer(category)

        message = f"Hi {owner}, local demand is rising. Promote {top_offer} today?"
        cta = "Promote Now"

        if trigger_type in ["dip", "revenue_dip", "slow"]:
            message = f"Hi {owner}, sales dipped today. Recover with {top_offer} offer now?"
            cta = "Recover Sales"

        elif trigger_type in ["festival", "holiday"]:
            message = f"Hi {owner}, festive demand is high. Launch {top_offer} tonight?"
            cta = "Launch Offer"

        elif trigger_type in ["search_spike", "trend"]:
            message = f"Hi {owner}, nearby searches increased. Promote {top_offer} now?"
            cta = "Capture Demand"

        elif trigger_type in ["regulation_change"]:
            message = f"Hi {owner}, policy changes may create new demand. Promote {top_offer} now?"
            cta = "Launch Campaign"

        return {
            "actions": [
                {
                    "action": "pitch",
                    "message": message,
                    "cta": cta,
                    "send_as": "VERA"
                }
            ]
        }

    def get_offer(self, category):
        offers = {
            "restaurant": "best seller combo",
            "dentist": "checkup package",
            "gym": "trial membership",
            "salon": "beauty package",
            "spa": "spa package",
            "pharmacy": "quick refill service"
        }

        return offers.get(category, "special offer")