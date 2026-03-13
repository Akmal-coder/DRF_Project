import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(product_name, product_description=""):
    """Создает продукт в Stripe"""
    try:
        product = stripe.Product.create(
            name=product_name,
            description=product_description,
        )
        return product.id
    except stripe.error.StripeError as e:
        print(f"Stripe error (product creation): {e}")
        return None


def create_stripe_price(amount, product_id):
    """Создает цену в Stripe"""
    try:
        price = stripe.Price.create(
            unit_amount=int(amount * 100),  # Stripe использует копейки/центы
            currency="usd",
            product=product_id,
        )
        return price.id
    except stripe.error.StripeError as e:
        print(f"Stripe error (price creation): {e}")
        return None


def create_stripe_checkout_session(price_id, success_url, cancel_url):
    """Создает сессию для оплаты"""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.url, session.id
    except stripe.error.StripeError as e:
        print(f"Stripe error (session creation): {e}")
        return None, None


def retrieve_stripe_session(session_id):
    """Получает информацию о сессии"""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session
    except stripe.error.StripeError as e:
        print(f"Stripe error (session retrieve): {e}")
        return None