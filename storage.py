class ContextStore:
    def __init__(self):
        self.merchants = {}
        self.customers = {}
        self.categories = {}

    def save(self, scope, context_id, payload):
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

    def get_category(self, category_id):
        return self.categories.get(category_id, {})