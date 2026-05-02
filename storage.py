class ContextStore:
    def __init__(self):
        self.merchants = {}
        self.customers = {}
        self.categories = {}
        self.versions = {}
        self.history = {}

    def save(self, scope, context_id, payload, version=1):
        key = f"{scope}:{context_id}"
        old_version = self.versions.get(key, 0)

        if version >= old_version:
            self.versions[key] = version

            if scope == "merchant":
                self.merchants[context_id] = payload
            elif scope == "customer":
                self.customers[context_id] = payload
            elif scope == "category":
                self.categories[context_id] = payload

    def get_merchant(self, merchant_id):
        return self.merchants.get(merchant_id, {})

    def get_customer(self, customer_id):
        return self.customers.get(customer_id, {})

    def remember_reply(self, merchant_id, msg):
        self.history[merchant_id] = msg

    def get_last_reply(self, merchant_id):
        return self.history.get(merchant_id, "")