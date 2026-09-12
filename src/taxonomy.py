INTENTS = {
    "software_update": "Problems installing, updating, restoring, or reverting an operating-system update, including problems directly caused by an iOS or macOS update.",
    "device_performance": "General device instability, performance, crashing, freezing, unexpected restarting, overheating, shutdowns, or other device-level problems.",
    "app_or_feature_issue": "A specific Apple app, feature, or functionality is malfunctioning or behaving unexpectedly.",
    "connectivity": "Wi-Fi, Bluetooth, cellular, phone-call, or other network and connection problems.",
    "account_security": "Account access, authentication, suspicious communications, phishing, security concerns, or being locked out of a device or account.",
    "purchase_repair_support": "Purchases, trade-ins, repairs, replacements, damaged hardware, store support, or questions about obtaining service for a product.",
    "information_request": "Primarily requesting information, compatibility details, feature explanations, how-to guidance, or other non-problem-specific product information.",
    "unclear": "There is not enough information to confidently determine the customer's intent.",
}

def taxonomy_text():
    return "\n".join(f"- {k}: {v}" for k, v in INTENTS.items())
