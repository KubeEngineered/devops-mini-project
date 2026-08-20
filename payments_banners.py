def get_payment_offer_banner(payment_method: str) -> dict:
    banners = {
        "UPI": {
            "title": "UPI Offer",
            "message": "Get 10% instant cashback up to ₹100 on UPI transactions!",
        },
        "CREDIT_CARD": {
            "title": "Card Discount",
            "message": "Enjoy No-Cost EMI for up to 6 months on major credit cards.",
        },
        "NET_BANKING": {
            "title": "Bank Special",
            "message": "Flat ₹50 off on transactions above ₹1,000 via Net Banking.",
        },
        "WALLET": {
            "title": "Wallet Bonus",
            "message": "Earn 500 reward points when paying with your digital wallet.",
        },
    }

    # Normalize input and retrieve banner, fallback to a default generic offer
    method_key = payment_method.upper().strip()
    return banners.get(
        method_key,
        {
            "title": "Exclusive Payment Offer",
            "message": "Complete your purchase now to earn loyalty rewards on your next order!",
        },
    )


# --- Example Usage ---
user_preferred_method = "upi"
banner = get_payment_offer_banner(user_preferred_method)

print(f"[{banner['title']}] {banner['message']}")


# End of file
