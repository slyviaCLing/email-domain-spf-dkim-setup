"""Production email domain setup: SPF + DKIM + DMARC.

email.domain.verify registers the domain and returns the DNS records to publish;
email.domain.get reports current status once your DNS has propagated.

Usage:
    python setup_domain.py <domain>          # e.g. mail.yourcompany.com
    INFRAI_EMAIL_DOMAIN=mail.yourcompany.com python setup_domain.py

Pass a domain whose DNS you actually control — registering it publishes records
under that name.
"""
import os
import sys

import infrai

DMARC_ADVICE = (
    "Add a DMARC record too: _dmarc.<domain> TXT "
    '"v=DMARC1; p=quarantine; rua=mailto:dmarc@<domain>"'
)

def resolve_domain(argv: list[str]) -> str:
    """Domain comes from argv or INFRAI_EMAIL_DOMAIN — never a hardcoded default."""
    domain = argv[1] if len(argv) > 1 else os.environ.get("INFRAI_EMAIL_DOMAIN", "")
    domain = domain.strip().lower().rstrip(".")
    if not domain or "." not in domain:
        raise SystemExit(
            "usage: python setup_domain.py <domain>   (or set INFRAI_EMAIL_DOMAIN)\n"
            "       the domain must be one whose DNS you control, "
            "e.g. mail.yourcompany.com"
        )
    return domain


def start_domain(domain: str) -> list[dict]:
    """Register the domain; return the SPF/DKIM DNS records you must publish.

    Idempotent: an already-registered domain is read back with domain.get
    instead of being re-registered.
    """
    try:
        data = infrai.email.domain.get(domain=domain)
        return data.get("verification", {}).get("dns_records", [])
    except infrai.InfraiError as e:
        if e.code != "EMAIL_NOT_FOUND":
            raise
    data = infrai.email.domain.verify(domain=domain)
    return data.get("dns_records", [])


def check_domain(domain: str) -> str:
    """Poll verification status after your DNS changes propagate."""
    data = infrai.email.domain.get(domain=domain)
    # domain.get nests state under "verification" (status + dns_records); "reputation" is separate.
    return data.get("verification", {}).get("status", "unknown")


if __name__ == "__main__":
    domain = resolve_domain(sys.argv)
    try:
        records = start_domain(domain)
    except infrai.InfraiError as e:
        raise SystemExit(f"{e.code}: {e.hint}")
    print(f"Publish these DNS records for {domain} (SPF + DKIM):")
    for rec in records:
        print(f"  {rec.get('type')}  {rec.get('name')}  ->  {rec.get('value')}")
    print(DMARC_ADVICE)
    print("current status:", check_domain(domain))
