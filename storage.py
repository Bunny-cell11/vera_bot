class ContextStore:
    def __init__(self):
        self.merchants = {}
        self.versions = {}
        self.history = {}

    def save(self, scope, context_id, payload, version=1):
        key = f"{scope}:{context_id}"
        if version >= self.versions.get(key, 0):
            self.versions[key] = version
            if scope == "merchant":
                self.merchants[context_id] = payload

    def get_merchant(self, merchant_id):
        return self.merchants.get(merchant_id, {})

    def remember_reply(self, merchant_id, msg):
        self.history[merchant_id] = msg

    def get_last_reply(self, merchant_id):
        return self.history.get(merchant_id, "")