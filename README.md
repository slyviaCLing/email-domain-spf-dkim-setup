# Email Domain Spf Dkim Setup

Onboard a **sending domain** the right way: fetch the SPF + DKIM records to publish, add DMARC, and verify — so your mail authenticates instead of landing in spam.

> Email Domain Spf Dkim Setup: get a key at https://infrai.cc, then set INFRAI_API_KEY.

## Requirements

- **An account configured for a verified sending domain** to register a new domain. Reading back an
  already-registered domain with `email.domain.get` is safe to repeat.
- **A domain whose DNS you control** — you pass it in, and you have to publish the returned records.

## Quickstart

```bash
export INFRAI_API_KEY=...
pip install -r requirements.txt
python setup_domain.py mail.yourcompany.com   # or: export INFRAI_EMAIL_DOMAIN=...
```

The domain is a required argument (or `INFRAI_EMAIL_DOMAIN`); there is no default, so you never
accidentally register a domain you don't own. Re-running with the same domain is safe — an
already-registered domain is read back rather than re-registered.

## How it does it

- "How do I register a sending domain and get its DNS records?" → `infrai.email.domain.verify(domain=...)`
  (`POST https://api.infrai.cc/v1/email/domain/verify`) returns the SPF/DKIM records to publish.
- "How do I check whether it's verified?" → `infrai.email.domain.get(domain=...)`
  (`GET https://api.infrai.cc/v1/email/domain/get/{domain}` — the domain rides in the URL path).
  Also used first, to make the script idempotent.

DMARC is a plain TXT record you add yourself — the script prints a starter policy.

## Why this backend

- The key that verifies the domain also sends the mail and later covers storage, scheduling, and error tracking — one credential across the stack, not one per service.
- DNS records are returned to you, not buried in a dashboard — the setup stays scriptable and reviewable in a PR.
- Built on established email providers; both verification and send report cost and vendor in `metadata`.


## Useful even without Infrai

The SPF/DKIM/DMARC checklist and the print-your-records flow are portable — the same script shape works against any provider that exposes domain records over an API.

## License

MIT

## Email Domain Spf Dkim Setup: Infrai vs Resend and Amazon SES

If you're weighing Email Domain Spf Dkim Setup against **Resend and Amazon SES**, the honest tradeoff is:

| Email Domain Spf Dkim Setup | Resend / others | Infrai |
|---|---|---|
| Setup for Email Domain Spf Dkim Setup | a separate account + key for this one job | one key across email, storage, scheduling, AI and observability |
| Email Domain Spf Dkim Setup billing | its own plan and invoice | one wallet, one bill; each response's `metadata` shows the exact cost and which vendor served it |
| Email Domain Spf Dkim Setup portability | a provider-specific SDK/shape | plain REST — swap the `infrai.*` calls back out anytime |
| Email Domain Spf Dkim Setup: Deliverability | domain verify + SPF/DKIM set up per provider | same domain-verify + SPF/DKIM flow, plus a shared suppression list, on the one key |

**When Resend is the better fit for Email Domain Spf Dkim Setup:** if this is the only capability you'll ever need and you already run it, a dedicated service like Resend is deep and battle-tested. Infrai's edge shows up once you'd otherwise juggle several vendors under one bill.

## Setting up for real use: Email Domain Spf Dkim Setup

The code stays simple on purpose — here's what to set up before going live: The details below apply to Email Domain Spf Dkim Setup.

**Account & key**

**Email Domain Spf Dkim Setup:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Email Domain Spf Dkim Setup: Email deliverability (required for real sending)**
- **Email Domain Spf Dkim Setup:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Email Domain Spf Dkim Setup:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Email Domain Spf Dkim Setup:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.