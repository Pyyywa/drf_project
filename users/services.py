import stripe

from config.settings import SECRET_STRIPE_KEY


class StripeAPI:
    def __init__(self):
        self.stripe = stripe
        self.stripe.api_key = SECRET_STRIPE_KEY

    def get_product(self):
        """Получение банковского продукта"""
        return self.stripe.Product.list()

    def create_product(self, name, price):
        """Создание продукта (цены)"""
        product = self.stripe.Product.create(name=name)
        return self.stripe.Price.create(
            currency="rub",
            unit_amount=price * 100,
            product=product.id,
        )

    def create_session(self, price_id):
        """Создание сессии"""
        return self.stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
        )
