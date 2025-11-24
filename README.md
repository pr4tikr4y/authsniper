# AuthSniper

<p align="center">
  <img src="assets/authsniper_logo.png" alt="AuthSniper Logo" width="350">
</p>

AuthSniper is a lightweight toolkit to quickly assess authentication and session security for web applications.

---

## 🚀 Features (v0.1)

- 🔫 **Rate-limiting heuristic check**
- 🔐 **Weak-password policy test** for a sample account
- 🍪 **Session cookie audit** (`Secure`, `HttpOnly`, `SameSite`)
- 🛡️ **Protected endpoint access check**
- 🔑 **JWT Inspection**
  - Detects **`alg=none`**
  - Flags **mismatched algorithms**
  - Highlights **missing `exp` or over-long token lifetime**
- 📌 **YAML-based per-target config**
- 📊 **JSON output for reporting/integration**
- 🧰 **Installable CLI tool:** `authsniper`

---

## 📦 Installation

### 🔧 Option 1: Developer Setup (Recommended)

```bash
git clone https://github.com/pr4tikr4y/authsniper.git
cd authsniper
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -e .

