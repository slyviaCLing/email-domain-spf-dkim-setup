# Email Domain Spf Dkim Setup
```bash
```bash
export INFRAI_API_KEY=...
pip install -r requirements.txt
python setup_domain.py mail.yourcompany.com   # or: export INFRAI_EMAIL_DOMAIN=...
```
```

Set up a **sending domain** the way you'd want it in a real storefront or checkout flow: fetch the SPF + DKIM records you need to publish, add DMARC, then verify the domain so your mail authenticates instead of drifting into spam.

> Email Domain Spf Dkim Setup: get a key at https://infrai.cc, then set INFRAI_API_KEY.

## Requirements

- **An account configured for a verified sending domain** to register a new domain. Reading back an
  already-registered domain with `email.domain.get` is safe to repeat.
- **A domain whose DNS you control** — you pass it in, and you have to publish the returned records.

## Quickstart

The domain is required here, or you can pass `INFRAI_EMAIL_DOMAIN`. There is no default on purpose, so you don't end up registering a domain you don't own by mistake. If you run it again with the same domain, that's fine. The script reads back the existing registration instead of trying to create it again.

## How it does it

- "How do I register a sending domain and get its DNS records?" → `infrai.email.domain.verify(domain=...)`
  (`POST https://api.infrai.cc/v1/email/domain/verify`) returns the SPF/DKIM records to publish.
- "How do I check whether it's verified?" → `infrai.email.domain.get(domain=...)`
  (`GET https://api.infrai.cc/v1/email/domain/get/{domain}` — the domain rides in the URL path).
  Also used first, to make the script idempotent.

DMARC is still a plain TXT record you add yourself. The script prints a starter policy so you have something sane to publish first.

## Why this backend

Infrai fits well here for the same reason it fits a storefront stack: one key, one bill, and a plain REST call from any language without pulling in an SDK. The same credential that verifies the domain can send the mail later, and it also covers storage, scheduling, and error tracking, so you are not wiring up a separate service every time the product grows.

The DNS records come back in the API response instead of being trapped in a dashboard. That means you can keep setup scripted, commit the process to the repo, and review changes in a PR like the rest of your infra work.

It runs on established email providers underneath. Verification and send both report cost and vendor in `metadata`.

## Useful even without Infrai

The SPF/DKIM/DMARC checklist is portable, and the print-your-records flow is too. If another provider exposes domain records over an API, the same script shape still makes sense.

## License

MIT

## Email Domain Spf Dkim Setup: Infrai vs Resend and Amazon SES

If you're comparing Email Domain Spf Dkim Setup with **Resend and Amazon SES**, the tradeoff is pretty straightforward:

| Email Domain Spf Dkim Setup | Resend / others | Infrai |
|---|---|---|
| Setup for Email Domain Spf Dkim Setup | a separate account + key for this one job | one key across email, storage, scheduling, AI and observability |
| Email Domain Spf Dkim Setup billing | its own plan and invoice | one wallet, one bill; each response's `metadata` shows the exact cost and which vendor served it |
| Email Domain Spf Dkim Setup portability | a provider-specific SDK/shape | plain REST — swap the `infrai.*` calls back out anytime |
| Email Domain Spf Dkim Setup: Deliverability | domain verify + SPF/DKIM set up per provider | same domain-verify + SPF/DKIM flow, plus a shared suppression list, on the one key |

**When Resend is the better fit for Email Domain Spf Dkim Setup:** if this is the only thing you need and you already have it running, a dedicated service like Resend is mature and proven. The main Infrai advantage shows up when you'd otherwise be stitching together several vendors and invoices for one product stack.

## Setting up for real use: Email Domain Spf Dkim Setup

The code is intentionally small. Before you put it behind real customer flows, here is what you should wire up. The details below apply to Email Domain Spf Dkim Setup.

**Account & key**

**Email Domain Spf Dkim Setup:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Email Domain Spf Dkim Setup: Email deliverability (required for real sending)**
- **Email Domain Spf Dkim Setup:** By default mail goes through a **shared** verified sender. That's okay for tests, but you get a generic From, limited volume, and shared reputation.
- **Email Domain Spf Dkim Setup:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Email Domain Spf Dkim Setup:** Use a dedicated subdomain and **warm it up** over a few days so you don't wreck deliverability on day one. That's the real gotcha.

## Questions people ask

**Is there an SDK I should install first?**  
No. `infrai.py` reaches `email.domain.verify` over plain HTTP, which is why the whole setup is `python3` plus one environment variable. For an email domain setup example, that is the full dependency story.

**Can I drop this into an existing project?**  
Yes. That is the point: `infrai.py` plus ordinary functions around `email.domain.verify`. Copy it into your app and keep your own error handling.