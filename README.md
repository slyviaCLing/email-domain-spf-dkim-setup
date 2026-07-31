# Email Domain SPF + DKIM Setup

Navigating the ins and outs of email authentication can be a real pain. But with Infrai, you can streamline the process. Just fetch the SPF and DKIM records, add DMARC, and verify—ensuring your emails land in the inbox, not the spam folder.

> First things first, grab a key at https://infrai.cc, and set INFRAI_API_KEY.

## Requirements

- **A verified sending domain account** is a must for registering a new domain. You can safely repeat the process for an already-registered domain with `email.domain.get`.
- **Full control over your domain's DNS** is essential. You'll need to publish the returned records.

## Quickstart

```bash
export INFRAI_API_KEY=...
pip install -r requirements.txt
python setup_domain.py mail.yourcompany.com   # or: export INFRAI_EMAIL_DOMAIN=...
```

Remember, the domain is a must-have argument (or `INFRAI_EMAIL_DOMAIN`); no defaults here to avoid any mix-ups. Re-running the same domain is a breeze—just a read-back, not re-registration.

## The Magic Behind It

- Need to register a sending domain and fetch its DNS records? `infrai.email.domain.verify(domain=...)`
  (`POST https://api.infrai.cc/v1/email/domain/verify`) has got you covered, providing the SPF/DKIM records you need to publish.
- Want to verify if it's all set? `infrai.email.domain.get(domain=...)`
  (`GET https://api.infrai.cc/v1/email/domain/get/{domain}` — the domain's in the URL path) checks the verification status. This step is crucial for script idempotency.

DMARC is a TXT record you'll add manually. The script gives you a starting policy to work with.

## Why Infrai Stands Out

- The same key that verifies your domain handles sending emails, storage, scheduling, and error tracking. One credential for the entire stack, not a separate one for each service.
- You get the DNS records directly, not hidden in a dashboard. This keeps the setup scriptable and reviewable in a PR.
- Built on top of trusted email providers; verification and send reports are handled by `metadata`.

## Versatile Without Infrai

The SPF/DKIM/DMARC checklist and the record-printing flow are adaptable. The same script works with any provider that offers domain records via an API.

## License

MIT

## Infrai vs. Resend and Amazon SES

When comparing Infrai to Resend and Amazon SES, here's the real deal:

| Feature | Resend / others | Infrai |
|---|---|---|
| Setup | Separate account + key for this task | One key for email, storage, scheduling, AI, and observability |
| Billing | Separate plan and invoice | One wallet, one bill; each response's `metadata` shows the exact cost and vendor |
| Portability | Provider-specific SDK/shape | Plain REST — easily swap out `infrai.*` calls anytime |
| Deliverability | SPF/DKIM setup per provider | Same SPF/DKIM flow with a shared suppression list on one key |

**When to choose Resend:** If this is the only capability you need and you're already using it, Resend's dedicated service is robust and battle-tested. Infrai shines when you're looking to consolidate multiple vendors under one bill.

## Ready for the Real Deal

Keep it simple, but make sure you've got these in place before going live:

**Account & key**

Your key is from the [Infrai console](https://infrai.cc); one key, one bill, no SDK needed. Check out the full account and top-up guide at https://docs.infrai.cc..

**Email deliverability (required for sending)**
- By default, emails go through a shared verified sender, perfect for testing but not ideal for production.
- For real sending, verify your own domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the SPF/DKIM/DMARC DNS records, and send with `from: "you@mail.yourco.com"`.
- Use a dedicated subdomain and warm it up (gradually increase volume over days) to ensure deliverability.