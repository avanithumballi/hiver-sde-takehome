# Golden Annotation Guide

Use the following order when assigning an intent.

1. If the customer explicitly discusses an OS update, updating, restoring, or a problem caused by an update, use `software_update`.
2. If the main issue is account access, authentication, suspicious messages, phishing, or security, use `account_security`.
3. If the main issue is repair, replacement, warranty, physical damage, purchase, refund, or store service, use `purchase_repair_support`.
4. If the main issue is Wi-Fi, Bluetooth, cellular, signal, calls, or network connectivity, use `connectivity`.
5. If the main issue is a named Apple app/feature malfunction, use `app_or_feature_issue`.
6. If the main issue is broad device instability, freezing, crashing, rebooting, shutdowns, lag, or battery/device performance, use `device_performance`.
7. If the customer is primarily asking how/what/when/compatibility information without reporting a malfunction, use `information_request`.
8. If there is insufficient information to choose confidently, use `unclear`.

When multiple problems appear, choose the primary issue that best explains the support need.

Escalation is independent. Escalate when the case contains a strong security, financial, repair/replacement, physical damage, data-loss, severe instability, or insufficient-information signal.

For each example, record a short annotation note explaining the decisive evidence.
