# Security policy

- Monitor only publicly accessible sources and domains you own or have written authorization to monitor.
- Never commit `.env`, `.session` files, API keys, real credentials, raw leaks, or personal information.
- Use a demo target such as `acme-demo.example` for screenshots and presentations.
- A domain/keyword match is an *unverified indicator*, not proof that a breach happened.
- Do not log entire leaked documents or passwords. Persist redacted entities, SHA-256 fingerprints and evidence links only.
- Respect platform terms, robots policies and rate limits. Never bypass auth, CAPTCHA or paywalls.
- Raw-paste links are deliberately allowlisted; add new sources only after security review.
- If using webhooks, deliver only masked alerts to a trusted HTTPS destination.
- The starter has no access control: do not expose its Streamlit dashboard to the public internet without authentication and TLS.
- Development PostgreSQL credentials are intentionally insecure; change them outside local development.
