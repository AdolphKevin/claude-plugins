---
name: data-security-compliance
description: Use when reviewing code for data security compliance, checking data classification levels, or implementing security controls for sensitive data like phone numbers, IDs, or financial information.
---

# Data Security Compliance Review

## Overview

Review code for data security compliance based on project data classification standards. Apply the 7-stage compliance framework.

## Data Sensitivity Classification

| Level | Description | Examples |
|-------|-------------|----------|
| **L4** | Highest sensitivity - E2E encryption, dual auth, explicit consent | phone_number, id_card_number, bank_card_number, GPS, IMEI, device_id, MAC_address, email, password, SSN |
| **L3** | Medium-high - encryption required, access control | login_name, ip_address, cookie_id, session_id, user_agent, postal_code |
| **L2** | Low sensitivity - basic access control | user_id, nickname, masked_phone, country/city |

**Common errors:** phone_number is **L4** (not L3), GPS is **L4** (not L3), device_id is **L4**

## 7-Stage Checklist

| Stage | Key Checks |
|-------|------------|
| **1. Collection** | Explicit consent? Minimisation? Legal basis? |
| **2. Transmission** | HTTPS/TLS? E2E for L4? No URL exposure? |
| **3. Storage** | Field encryption for L4? RBAC? Audit logs? |
| **4. Usage** | Purpose limitation? Role permissions? No real data in dev? |
| **5. Sharing** | DPA signed? Anonymized? User consent? |
| **6. Retention** | Defined periods? Auto-cleanup? User export/delete? |
| **7. Deletion** | Secure wipe for L4? Timely response? Unrecoverable? |

## Quick Reference

| Issue | L4 | L3 | L2 |
|-------|----|----|-----|
| Storage | Field encryption | Standard encryption | Access control |
| Return | Masked/never | Masked | OK |
| Sharing | Prohibited | Internal only | Controlled |
| Deletion | Secure wipe | Multi-pass | Standard |
| Consent | Explicit | Implied | Not required |

## Common Vulnerabilities

1. **Plaintext storage** - L4 without encryption
2. **Plaintext returns** - API exposing full sensitive data
3. **Missing consent** - L4 without authorization
4. **Excessive logging** - Sensitive data in logs
5. **URL exposure** - L4 in GET parameters
6. **Missing audit** - No L4 access logs
7. **No retention policy** - Data kept indefinitely
8. **Unsafe deletion** - Not secure wipe for L4

## Severity

| Severity | Issues |
|----------|--------|
| **Critical** | L4 plaintext storage/return, unauthorized L4 access |
| **High** | Missing L4 encryption, missing consent, missing audit |
| **Medium** | L3 gaps, missing access control |
| **Low** | L2 improvements |

## Code Pattern

```go
// ❌ L4 WRONG
user := &User{Phone: req.Phone}
return &Response{Phone: user.Phone}

// ✅ L4 CORRECT
if !userConsent { return ErrUnauthorized }
encrypted := encrypt(req.Phone)  // field encryption
logAudit("user_created", user.ID)
return &Response{Phone: maskPhone(req.Phone)}  // masked
```
