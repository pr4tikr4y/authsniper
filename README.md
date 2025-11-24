# AuthSniper

<p align="center">
  <img src="assets/authsniper_logo.png" alt="AuthSniper Logo" width="350">
</p>
                                                                                                                   

AuthSniper is a lightweight toolkit to quickly assess authentication and session security for web
applications.

## Features (v0.1)

- Basic rate-limiting heuristic check
- Quick weak-password policy check for a single test account
- Session cookie flag review (Secure, HttpOnly, SameSite)
- Simple protected URL access check
- JWT inspection:
  - Detects `alg=none`
  - Detects mismatched algorithm vs expected
  - Flags missing `exp` or over-long token lifetime
- YAML-based per-target configuration
- JSON output for integration / reporting
- Installable as a CLI tool: `authsniper`

Usage:

authsniper -c examples/target_example.yaml --checks all --json
authsniper -c examples/target_example.yaml --checks auth
authsniper -c examples/target_example.yaml --checks session
authsniper -c examples/target_example.yaml --checks jwt


## Install (dev)

  git clone https://github.com/<your-username>/authsniper.git
  cd authsniper
  python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  pip install -e .
