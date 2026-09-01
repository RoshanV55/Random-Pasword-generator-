"""
Task 1: Hardware-Bound Device-Fingerprinted Password Suite & Smart Vault
Auspify Technologies Internship Submission
Developer: Roshan Siril Nadar
"""

import base64
import hashlib
import math
import os
import secrets
import string
import subprocess
import sys
from typing import Dict, List, Tuple, Union

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class DeviceFingerprintEngine:
    """Handles Device Hardware Fingerprinting, Entropy Scoring, and Vault Encryption."""

    def __init__(self):
        self.char_sets = {
            "lowercase": string.ascii_lowercase,
            "uppercase": string.ascii_uppercase,
            "digits": string.digits,
            "symbols": "!@#$%^&*()_+-=[]{}|;:,.<>?",
        }
        self.vault_file = "vault.enc"
        self.key_file = "device_hardware.key"

        # Dictionary penalty list for predictable personal/system tokens
        self.predictable_words = [
            "admin", "password", "welcome",
            "123456", "qwerty", "0000", "123"
        ]

        # Secure word pool for memorable hybrid suggestions
        self.word_pool = [
            "Falcon", "Cipher", "Matrix", "Vortex", "Quantum",
            "Shield", "Zenith", "Nebula", "Titan", "Anchor",
            "Sentry", "Cobalt", "Harbor", "Vector", "Apex"
        ]

    # ------------------------------------------------------------------
    # 1. HARDWARE DEVICE FINGERPRINT ENGINE
    # ------------------------------------------------------------------
    def get_device_fingerprint(self) -> Tuple[str, bytes]:
        """Extracts system hardware parameters and generates Device Fingerprint."""
        try:
            cmd = "wmic csproduct get uuid & wmic cpu get processorid & wmic baseboard get serialnumber"
            output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
            raw_hw = "".join(output.split())
            if not raw_hw or "No Instance" in raw_hw:
                raise ValueError("WMI Hardware Query Failed")
        except Exception:
            raw_hw = os.environ.get("COMPUTERNAME", "Machine") + os.environ.get("PROCESSOR_IDENTIFIER", "CPU")

        fingerprint_hash = hashlib.sha256(raw_hw.encode("utf-8")).hexdigest()
        short_device_id = f"DEV-{fingerprint_hash[:8].upper()}-{fingerprint_hash[8:16].upper()}"
        return short_device_id, fingerprint_hash.encode("utf-8")

    # ------------------------------------------------------------------
    # 2. AUTOMATIC HARDWARE-BOUND ENCRYPTION KEY GENERATION
    # ------------------------------------------------------------------
    def get_or_create_device_key(self) -> bytes:
        """Generates/reads key bound strictly to local Device Hardware Fingerprint."""
        device_id, hw_bytes = self.get_device_fingerprint()

        if not os.path.exists(self.key_file):
            salt = secrets.token_bytes(16)
            with open(self.key_file, "wb") as f:
                f.write(salt)
        else:
            with open(self.key_file, "rb") as f:
                salt = f.read(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=150000,
        )
        derived_key = kdf.derive(hw_bytes)
        return base64.urlsafe_b64encode(derived_key)

    # ------------------------------------------------------------------
    # 3. ENTROPY & SMART SECURITY SCORE EVALUATOR
    # ------------------------------------------------------------------
    def calculate_score(self, password: str) -> Dict[str, Union[str, float, int]]:
        """Calculates Shannon Entropy with penalties for predictable patterns/names."""
        if not password:
            return {
                "length": 0,
                "pool_size": 0,
                "entropy": 0.0,
                "numeric_score": 0,
                "score": "0/100",
                "rating": "Empty",
            }

        pool_size = 0
        if any(c in self.char_sets["lowercase"] for c in password):
            pool_size += 26
        if any(c in self.char_sets["uppercase"] for c in password):
            pool_size += 26
        if any(c in self.char_sets["digits"] for c in password):
            pool_size += 10
        if any(c in self.char_sets["symbols"] for c in password):
            pool_size += len(self.char_sets["symbols"])

        if pool_size == 0:
            pool_size = 95

        raw_entropy = len(password) * math.log2(pool_size)

        # Apply dictionary & pattern penalties
        penalty = 0
        pwd_lower = password.lower()

        for word in self.predictable_words:
            if word in pwd_lower:
                penalty += 25  # Deduct points for predictable names/words

        for i in range(len(password) - 1):
            if password[i] == password[i + 1]:
                penalty += 5

        adjusted_entropy = max(0.0, raw_entropy - penalty)
        numeric_score = min(100, int((adjusted_entropy / 100.0) * 100))

        if adjusted_entropy < 40:
            rating = "Very Weak 🔴 (Contains Predictable Name/Words)"
        elif adjusted_entropy < 60:
            rating = "Weak 🟠"
        elif adjusted_entropy < 80:
            rating = "Moderate 🟡"
        elif adjusted_entropy < 100:
            rating = "Strong 🟢"
        else:
            rating = "Critical Grade 🛡️ (High Entropy & Unpredictable)"

        return {
            "length": len(password),
            "pool_size": pool_size,
            "entropy": round(adjusted_entropy, 2),
            "numeric_score": numeric_score,
            "score": f"{numeric_score}/100",
            "rating": rating,
        }

    # ------------------------------------------------------------------
    # 4. RANDOM GENERATOR & SMART PASSWORD UPGRADERS
    # ------------------------------------------------------------------
    def generate_random(
        self,
        length: int = 18,
        use_upper: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
    ) -> str:
        """Generates random CSPRNG password."""
        if length < 4:
            raise ValueError("Length must be at least 4 characters.")

        pool = self.char_sets["lowercase"]
        guaranteed = [secrets.choice(self.char_sets["lowercase"])]

        if use_upper:
            pool += self.char_sets["uppercase"]
            guaranteed.append(secrets.choice(self.char_sets["uppercase"]))
        if use_digits:
            pool += self.char_sets["digits"]
            guaranteed.append(secrets.choice(self.char_sets["digits"]))
        if use_symbols:
            pool += self.char_sets["symbols"]
            guaranteed.append(secrets.choice(self.char_sets["symbols"]))

        remaining = length - len(guaranteed)
        random_chars = [secrets.choice(pool) for _ in range(remaining)]
        password_list = guaranteed + random_chars

        for i in range(len(password_list) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_list[i], password_list[j] = password_list[j], password_list[i]

        return "".join(password_list)

    def generate_batch(
        self,
        count: int = 1,
        length: int = 18,
        use_upper: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
    ) -> List[str]:
        """Generates up to 100 random passwords at once."""
        count = max(1, min(100, count))
        return [self.generate_random(length, use_upper, use_digits, use_symbols) for _ in range(count)]

    def suggest_strong_upgrade(self, user_password: str) -> Tuple[str, str]:
        """
        Returns two upgraded password suggestions:
        1. Pure Random CSPRNG password
        2. Memorable Hybrid password incorporating user input with random words/symbols
        """
        has_upper = any(c in self.char_sets["uppercase"] for c in user_password)
        has_digits = any(c in self.char_sets["digits"] for c in user_password)
        has_symbols = any(c in self.char_sets["symbols"] for c in user_password)

        # 1. Pure Random Password
        random_sug = self.generate_random(
            length=max(18, len(user_password) + 4),
            use_upper=has_upper or True,
            use_digits=has_digits or True,
            use_symbols=has_symbols or True,
        )

        # 2. Memorable Hybrid Password (User Input + Random Word + Number + Symbol)
        clean_user = "".join(c for c in user_password if c.isalnum()) or "User"
        sym1 = secrets.choice(self.char_sets["symbols"])
        sym2 = secrets.choice(self.char_sets["symbols"])
        word = secrets.choice(self.word_pool)
        num = secrets.randbelow(9000) + 1000  # 4-digit number

        hybrid_sug = f"{clean_user.capitalize()}{sym1}{word}{num}{sym2}"

        return random_sug, hybrid_sug

    # ------------------------------------------------------------------
    # 5. DEVICE-BOUND ENCRYPTED VAULT
    # ------------------------------------------------------------------
    def encrypt_to_vault(self, secret_text: str) -> str:
        """Encrypts data bound to local Device Fingerprint."""
        key = self.get_or_create_device_key()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(secret_text.encode("utf-8"))
        with open(self.vault_file, "wb") as f:
            f.write(encrypted)
        return self.vault_file

    def decrypt_from_vault(self) -> str:
        """Decrypts vault data using local Device Fingerprint key."""
        if not os.path.exists(self.vault_file):
            raise FileNotFoundError("No vault file found.")

        key = self.get_or_create_device_key()
        fernet = Fernet(key)

        with open(self.vault_file, "rb") as f:
            encrypted = f.read()

        try:
            return fernet.decrypt(encrypted).decode("utf-8")
        except Exception:
            raise PermissionError("Access Denied! Vault file or key belongs to a different computer.")


# ----------------------------------------------------------------------
# CLI MENU INTERFACE
# ----------------------------------------------------------------------
def get_int(prompt: str, default: int, max_val: int | None = None) -> int:
    while True:
        val = input(prompt).strip()
        if not val:
            return default
        if val.isdigit():
            num = int(val)
            if max_val is not None and num > max_val:
                print(f"⚠️ Value cannot exceed {max_val}. Setting to {max_val}.")
                return max_val
            return num
        print("⚠️ Please enter a valid number.")


def main():
    engine = DeviceFingerprintEngine()
    device_id, _ = engine.get_device_fingerprint()

    print("=" * 65)
    print(" 🔐 PASSWORD GENERATOR & DEVICE-LOCKED VAULT (Task 1)")
    print(f" 💻 Device Hardware Fingerprint ID: [{device_id}]")
    print("=" * 65)

    while True:
        print("\n" + "-" * 55)
        print(" [1] Generate Secure Random Password(s) [Batch Up to 100]")
        print(" [2] Audit Password Score & Get Smart Strong Suggestions")
        print(" [3] Save & Encrypt Password to Vault (Auto Device Key)")
        print(" [4] Read Encrypted Vault (`vault.enc`)")
        print(" [5] Exit")
        print("-" * 55)

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            count = get_int("\nHow many passwords to generate? (1-100) [default 1]: ", 1, 100)
            length = get_int("Enter length [default 18]: ", 18)
            upper = input("Include uppercase? (Y/n): ").strip().lower() != "n"
            digits = input("Include digits? (Y/n): ").strip().lower() != "n"
            symbols = input("Include symbols? (Y/n): ").strip().lower() != "n"

            pwds = engine.generate_batch(count, length, upper, digits, symbols)

            print(f"\n🔐 Generated Password(s) [{len(pwds)}]:")
            for idx, pwd in enumerate(pwds, 1):
                score_data = engine.calculate_score(pwd)
                print(f"  {idx:02d}. {pwd}  | Score: {score_data['score']} ({score_data['entropy']} bits)")

            if len(pwds) == 1:
                save_now = input("\nDo you want to encrypt and save this password to vault now? (y/N): ").strip().lower() == "y"
                if save_now:
                    fname = engine.encrypt_to_vault(pwds[0])
                    print(f"✅ Password encrypted & saved to '{fname}' with Device Key!")
            else:
                save_idx = input("\nEnter number to save to vault (or press Enter to skip): ").strip()
                if save_idx.isdigit() and 1 <= int(save_idx) <= len(pwds):
                    fname = engine.encrypt_to_vault(pwds[int(save_idx) - 1])
                    print(f"✅ Password #{save_idx} encrypted & saved to '{fname}' with Device Key!")

        elif choice == "2":
            user_pwd = input("\nEnter password to evaluate: ").strip()
            if user_pwd:
                score_data = engine.calculate_score(user_pwd)
                rnd_sug, hyb_sug = engine.suggest_strong_upgrade(user_pwd)

                r_score = engine.calculate_score(rnd_sug)
                h_score = engine.calculate_score(hyb_sug)

                print(f"\n📊 Current Score:  {score_data['score']} | Entropy: {score_data['entropy']} bits")
                print(f"🔴 Current Rating: {score_data['rating']}")

                print("\n💡 SMART SUGGESTED UPGRADES:")
                print(f" 1. Pure Random:      {rnd_sug}")
                print(f"    🟢 Score:         {r_score['score']} ({r_score['entropy']} bits)")
                print(f" 2. Memorable Hybrid: {hyb_sug}")
                print(f"    🟢 Score:         {h_score['score']} ({h_score['entropy']} bits)")

        elif choice == "3":
            user_pwd = input("\nEnter password to store: ").strip()
            if user_pwd:
                score_data = engine.calculate_score(user_pwd)
                print(f"\n📊 Password Security Score: {score_data['score']} ({score_data['rating']})")

                numeric_val = int(score_data["numeric_score"])
                if numeric_val < 80:
                    rnd_sug, hyb_sug = engine.suggest_strong_upgrade(user_pwd)
                    print(f"\n⚠️ Your password is weak/predictable!")
                    print(f" Option [A] Pure Random:      {rnd_sug}")
                    print(f" Option [B] Memorable Hybrid: {hyb_sug}")

                    opt = input("\nUse suggestion? (a = Pure Random / b = Hybrid / N = Keep Original): ").strip().lower()
                    if opt == "a":
                        user_pwd = rnd_sug
                    elif opt == "b":
                        user_pwd = hyb_sug

                fname = engine.encrypt_to_vault(user_pwd)
                print(f"\n✅ Password encrypted & saved to '{fname}' with Device Key!")

        elif choice == "4":
            try:
                decrypted = engine.decrypt_from_vault()
                print(f"\n🔓 Decrypted Vault Contents:\n{decrypted}")
            except Exception as err:
                print(f"\n❌ Access Error: {err}")

        elif choice == "5":
            print("\nExiting application.")
            break
        else:
            print("⚠️ Invalid choice.")


if __name__ == "__main__":
    main()