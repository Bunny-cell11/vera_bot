import time

class VeraEngine:
    def __init__(self, store):
        self.store = store

    def compose(self, merchant_id, trigger):
        merchant = self.store.get_merchant(merchant_id)

        if not merchant:
            return self.default_response(merchant_id)

        owner = merchant.get("identity", {}).get("owner_name", "there")
        category = merchant.get("category", "").lower()

        trigger_name = trigger.get("type", "opportunity")
        trigger_reason = trigger.get("reason", "local demand")

        key = f"{merchant_id}_{int(time.time())}"

        if category == "restaurant":
            return {
                "message": f"Hi {owner}, {trigger_reason}. Shall I promote your best combo to nearby hungry customers today?",
                "cta": "Launch Deal",
                "send_as": "VERA",
                "suppression_key": key
            }

        elif category in ["salon", "spa"]:
            return {
                "message": f"Hi {owner}, beauty demand is rising nearby. Shall I open priority bookings this afternoon?",
                "cta": "Book Now",
                "send_as": "VERA",
                "suppression_key": key
            }

        elif category == "dentist":
            return {
                "message": f"Hi Dr. {owner}, appointment interest is rising. Shall I promote checkups this week?",
                "cta": "Yes, do it",
                "send_as": "VERA",
                "suppression_key": key
            }

        elif category == "gym":
            return {
                "message": f"Hi {owner}, fitness searches increased nearby. Shall I push trial memberships today?",
                "cta": "Start Offer",
                "send_as": "VERA",
                "suppression_key": key
            }

        return {
            "message": f"Hi {owner}, {trigger_reason}. Shall I help increase sales today?",
            "cta": "Show Me",
            "send_as": "VERA",
            "suppression_key": key
        }

    def default_response(self, merchant_id):
        return {
            "message": "Hi, shall I help grow your business today?",
            "cta": "Show Me",
            "send_as": "VERA",
            "suppression_key": f"default_{merchant_id}"
        }