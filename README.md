# AuthSniper
```html
d8888  888     888 88888888888 888    888  .d8888b.  888b    888 8888888 8888888b.  8888888888 8888888b.  
d88888 888     888     888     888    888 d88P  Y88b 8888b   888   888   888   Y88b 888        888   Y88b 
d88P888 888     888     888     888    888 Y88b.      88888b  888   888   888    888 888        888    888 
d88P 888 888     888     888     8888888888  "Y888b.   888Y88b 888   888   888   d88P 8888888    888   d88P 
d88P  888 888     888     888     888    888     "Y88b. 888 Y88b888   888   8888888P"  888        8888888P"  
d88P   888 888     888     888     888    888       "888 888  Y88888   888   888        888        888 T88b   
d8888888888 Y88b. .d88P     888     888    888 Y88b  d88P 888   Y8888   888   888        888        888  T88b  
d88P     888  "Y88888P"      888     888    888  "Y8888P"  888    Y888 8888888 888        8888888888 888   T88b

                                  【 AUTHENTICATION • SESSION • JWT 】
                                                                                                                
                                                                                 - pratikhere01

AuthSniper is a lightweight toolkit to quickly assess **authentication** and **session security** for web applications.

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
