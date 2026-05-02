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

        if category == "restaurant":
            return {
                "message": f"Hi {owner}, orders are slow today. Shall I push your top combo to nearby customers?",
                "cta": "Launch Deal",
                "send_as": "VERA",
                "suppression_key": f"{merchant_id}_{int(time.time())}"
            }

        elif category in ["salon", "spa"]:
            return {
                "message": f"Hi {owner}, beauty searches are rising nearby. Shall I promote priority bookings today?",
                "cta": "Book Now",
                "send_as": "VERA",
                "suppression_key": f"{merchant_id}_{int(time.time())}"
            }

        elif category == "dentist":
            return {
                "message": f"Hi Dr. {owner}, checkup demand is increasing. Shall I promote appointments this week?",
                "cta": "Yes, do it",
                "send_as": "VERA",
                "suppression_key": f"{merchant_id}_{int(time.time())}"
            }

        return self.default_response(merchant_id)

    def default_response(self, merchant_id):
        return {
            "message": "Hi, would you like to boost sales today?",
            "cta": "Show me",
            "send_as": "VERA",
            "suppression_key": f"default_{merchant_id}"
        }