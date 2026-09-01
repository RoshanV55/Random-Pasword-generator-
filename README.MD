<div align="center">

# 🔐 Hardware-Bound Password Suite & Smart Vault

**Enterprise-Grade Password Security Application — Auspify Technologies Internship Submission (Task 1)**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com/windows)
[![Encryption](https://img.shields.io/badge/Encryption-AES--256-green?style=for-the-badge&logo=letsencrypt&logoColor=white)](https://cryptography.io)
[![Security](https://img.shields.io/badge/Security-Hardware--Bound-red?style=for-the-badge)]()
[![Offline](https://img.shields.io/badge/Network-100%25%20Offline-lightgrey?style=for-the-badge)]()

> **Developer:** Roshan Siril Nadar &nbsp;|&nbsp; **Version:** 1.0 &nbsp;|&nbsp; **Language:** Python 3.10+

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Why This App Is Unique](#-why-this-app-is-unique)
- [Core Features](#-core-features)
- [Requirements & Installation](#-requirements--installation)
- [How to Use](#-how-to-use)
- [File Structure](#-file-structure)
- [Efficiency & Performance](#-efficiency--performance)
- [Use Cases](#-use-cases)
- [FAQ](#-frequently-asked-questions)

---

## 🔍 Overview

The **Hardware-Bound Password Suite & Smart Vault** is an enterprise-grade cybersecurity application written in pure Python, built by **Roshan Siril Nadar** as Task 1 of the Auspify Technologies internship submission.

Unlike conventional password managers that rely solely on a master password, this application uses a fundamentally stronger approach — it **binds encryption keys directly to the physical machine it runs on**. Even if the encrypted vault file is copied or stolen, it is completely unreadable on any other device.

| Property | Details |
|---|---|
| **Language** | Python 3.10+ |
| **Platform** | Windows |
| **Encryption** | AES-256 (Fernet) |
| **Key Derivation** | PBKDF2HMAC — SHA-256 |
| **RNG Engine** | `secrets` module (CSPRNG) |
| **Network** | ❌ 100% Offline |
| **External Dependencies** | 1 (`cryptography`) |

---

## 💡 Why This App Is Unique

Most password tools stop at generating a random string. This application is built around **five integrated security modules** that form a complete password security ecosystem:

```
┌──────────────────────────────────────────────────────────┐
│         SECURITY LAYERS — PASSWORD SUITE & VAULT         │
├──────────────────────────────────────────────────────────┤
│  Layer 1 │ Machine-Bound Device Identity Engine          │
│  Layer 2 │ Hardware-Derived Cryptographic Key            │
│  Layer 3 │ AES-256 Authenticated Encryption (Vault)      │
│  Layer 4 │ CSPRNG Password Generator (Batch up to 100)   │
│  Layer 5 │ Entropy Auditor with Penalty Scoring          │
└──────────────────────────────────────────────────────────┘
```

---

## ⭐ Core Features

### 1. 🖥️ Machine-Bound Device Identity

On every startup, the app silently computes a **unique identity** tied to the local machine. This identity is:
- Never stored to disk in readable form
- Automatically regenerated on each run
- Displayed in your terminal only as a short anonymous ID

> 🔒 The internal mechanism that generates this identity is intentionally not documented here for security reasons. It is visible in `main.py` for local review.

---

### 2. 🔒 Hardware-Bound AES-256 Encrypted Vault

The vault (`vault.enc`) is encrypted using a key that is mathematically derived from the machine's identity. This means:

- ✅ The vault opens **only on the machine it was created on**
- ✅ Copying `vault.enc` to another machine makes it **permanently unreadable**
- ✅ Even the key file alone is not enough — the machine itself is part of the key

---

### 3. 🎲 CSPRNG Password Generator (Batch — Up to 100)

Generates cryptographically secure passwords using Python's `secrets` module (OS-level entropy):

- 🔧 **Configurable character sets** — lowercase, uppercase, digits, symbols
- 📏 **Configurable length** — minimum 4, default 18 characters
- 📦 **Batch mode** — generate 1 to 100 passwords at once
- 🔀 **Guaranteed character class inclusion** — always balanced
- 🃏 **CSPRNG shuffle** — eliminates positional bias

```
Character sets:
  Lowercase  :  a–z
  Uppercase  :  A–Z
  Digits     :  0–9
  Symbols    :  ! @ # $ % ^ & * ( ) _ + - = [ ] { } | ; : , . < > ?
```

---

### 4. 📊 Shannon Entropy & Security Auditor

Every password is evaluated using Shannon Entropy:

```
Entropy (bits) = Password Length × log₂(Character Pool Size)
```

Penalties are applied for weak patterns:

| Penalty Trigger | Deduction |
|---|---|
| Common dictionary words detected | High penalty |
| Consecutive repeated characters | Moderate penalty |

**Rating Scale:**

| Score | Rating |
|---|---|
| Very low entropy | 🔴 Very Weak |
| Low entropy | 🟠 Weak |
| Moderate entropy | 🟡 Moderate |
| High entropy | 🟢 Strong |
| Very high entropy | 🛡️ Critical Grade |

---

### 5. 💡 Smart Dual Password Upgrader

When a weak password is detected, the app offers **two strong alternatives**:

| Option | Type | Best For |
|---|---|---|
| **A** | Pure Random | API keys, system accounts, DB passwords |
| **B** | Memorable Hybrid | Human-remembered accounts |

> Both suggestions are generated fresh every time using the CSPRNG engine and are **only visible in your local terminal**.

---

## 📦 Requirements & Installation

### System Requirements

| Requirement | Specification |
|---|---|
| **Python Version** | 3.10+ recommended (3.8+ minimum) |
| **Operating System** | Windows 10 / Windows 11 |
| **RAM** | < 20 MB |
| **Disk Space** | < 5 MB (with dependencies) |
| **Network** | ❌ Not required |

### Standard Library (No Installation Needed)

These modules are built into Python — no `pip install` required:

`base64` &nbsp;·&nbsp; `hashlib` &nbsp;·&nbsp; `math` &nbsp;·&nbsp; `os` &nbsp;·&nbsp; `secrets` &nbsp;·&nbsp; `string` &nbsp;·&nbsp; `subprocess` &nbsp;·&nbsp; `sys` &nbsp;·&nbsp; `typing`

### External Dependency

```bash
pip install cryptography
```

The [`cryptography`](https://cryptography.io) package (by the Python Cryptographic Authority — PyCA) is the **only** external dependency. It provides AES-256 encryption and the key derivation function used by the vault.

### Optional Package

```bash
pip install pywin32
```

### Run the App

```bash
python main.py
```

---

## 🚀 How to Use

### Startup

```
=================================================================
 🔐 PASSWORD GENERATOR & DEVICE-LOCKED VAULT (Task 1)
 💻 Device ID: [••••••••••••••••••]
=================================================================

 [1] Generate Secure Random Password(s) [Batch Up to 100]
 [2] Audit Password Score & Get Smart Strong Suggestions
 [3] Save & Encrypt Password to Vault (Auto Device Key)
 [4] Read Encrypted Vault (vault.enc)
 [5] Exit
-----------------------------------------------------------------
Select an option (1-5):
```

> 🔒 The Device ID is unique to your machine and computed locally. It is never stored or transmitted.

---

### Option 1 — Generate Secure Passwords

```
> Select: 1

How many passwords to generate? (1-100) [default 1]: 3
Enter length [default 18]: 20
Include uppercase? (Y/n): Y
Include digits? (Y/n): Y
Include symbols? (Y/n): Y

🔐 Generated Password(s) [3]:
  01. ••••••••••••••••••••  | Score: ••/100 (••• bits)
  02. ••••••••••••••••••••  | Score: ••/100 (••• bits)
  03. ••••••••••••••••••••  | Score: ••/100 (••• bits)

Enter number to save to vault (or press Enter to skip): 1
✅ Password #1 encrypted & saved to 'vault.enc' with Device Key!
```

> 🔒 Passwords are shown only in your local terminal — never logged or transmitted.

---

### Option 2 — Audit a Password

```
> Select: 2

Enter password to evaluate: <your-password>

📊 Current Score:  ••/100 | Entropy: ••.•• bits
🔴 Current Rating: <Rating>

💡 SMART SUGGESTED UPGRADES:
 1. Pure Random:      ••••••••••••••••••••
    🟢 Score:         ••/100 (••• bits)
 2. Memorable Hybrid: ••••••••••••••••••••
    🟢 Score:         ••/100 (••• bits)
```

---

### Option 3 — Save & Encrypt to Vault

```
> Select: 3

Enter password to store: <your-password>

📊 Password Security Score: ••/100

⚠️  Weak password detected — upgrade suggestions available:
 Option [A] Pure Random:      ••••••••••••••••••••
 Option [B] Memorable Hybrid: ••••••••••••••••••••

Use suggestion? (a / b / N to keep original): a

✅ Password encrypted & saved to 'vault.enc' with Device Key!
```

> If the password scores below 80/100, the app gates saving and offers smarter alternatives.

---

### Option 4 — Read the Vault

```
> Select: 4

🔓 Decrypted Vault Contents:
••••••••••••••••••••
```

> 🔒 Vault contents are visible **only in your local terminal session**.

**If accessed from a different machine:**
```
❌ Access Error: Access Denied! Vault file or key belongs to a different computer.
```

---

## 📁 File Structure

```
Task1 Password Generator/
│
├── main.py                  # Core application — all logic, all modules
├── vault.enc                # Encrypted vault file (auto-created on first save)
├── device_hardware.key      # Cryptographic binding file (auto-created, local only)
├── device_master.key.dpapi  # Optional key backup (Windows, local only)
├── README.MD                # This documentation
└── .gitignore               # Excludes sensitive files from git
```

> ⚠️ **`vault.enc` and `device_hardware.key` are excluded from git via `.gitignore`. Never commit these files to any repository.**

---

## ⚡ Efficiency & Performance

| Operation | Performance |
|---|---|
| App startup | < 1 second |
| Single password generation | < 1 ms |
| Batch of 100 passwords | < 50 ms |
| Entropy scoring | < 1 ms per password |
| Vault encrypt / decrypt | ~50 ms |
| RAM usage | < 20 MB |
| External packages | 1 only |
| Network calls | 0 — fully offline |

---

## 💼 Use Cases

| Use Case | Description |
|---|---|
| **Personal Developer** | Secure generation and local storage of API keys, tokens, credentials |
| **Corporate Workstation** | Machine-locked credentials that cannot leave the device |
| **Security Training** | Live entropy scoring to teach teams what makes a password strong or weak |
| **Air-Gapped Systems** | Fully offline — no cloud, no network, no data leakage risk |
| **Bulk Provisioning** | Sysadmins can generate up to 100 unique passwords in seconds |
| **Compliance Audits** | Entropy-based scoring aligns with NIST SP 800-63B password guidelines |

---

## ❓ Frequently Asked Questions

<details>
<summary><b>Can I open the vault on a different machine?</b></summary>

No. The vault is strictly bound to the machine it was created on. Moving `vault.enc` to another device will result in an `Access Denied` error. This is the core security feature — by design.
</details>

<details>
<summary><b>What if I change or upgrade my hardware?</b></summary>

Major hardware changes may affect vault access. Always decrypt and back up your vault contents **before** any significant hardware changes.
</details>

<details>
<summary><b>Is the `secrets` module truly secure for passwords?</b></summary>

Yes. Python's `secrets` module uses the OS-level cryptographic random number generator — suitable for tokens, passwords, and keys. It is fundamentally different from the `random` module, which is **not** cryptographically secure.
</details>

<details>
<summary><b>Does the app store anything in plain text?</b></summary>

Never. Passwords exist as plaintext only in active memory during your session. Nothing is written to disk in readable form. No logs, no temp files.
</details>

<details>
<summary><b>Does it need an internet connection?</b></summary>

No. Every operation — identity computation, key derivation, password generation, encryption — happens entirely offline on your local machine.
</details>

<details>
<summary><b>Where can I review the internal implementation?</b></summary>

All logic is in `main.py`. The internal security mechanisms (fingerprinting, key derivation steps, word pools) are intentionally not documented in this public README. Review `main.py` locally for full implementation details.
</details>

---

## ✅ Summary

- 🔒 Vault is machine-locked — unreadable if moved to another device
- 🎲 All passwords use OS-level CSPRNG — cryptographically unpredictable
- 🔐 AES-256 authenticated encryption — detects any tampering
- 📊 Entropy scoring with penalty system — prevents weak password storage
- 💡 Two upgrade options on every weak password — balances security and usability
- 📦 One external dependency — minimal, audited, production-grade
- 🌐 100% offline — no network, no cloud, no exposure

---

<div align="center">

**🔐 Hardware-Bound Password Suite & Smart Vault**

*Auspify Technologies — Task 1 Submission | Developer: Roshan Siril Nadar*

</div>