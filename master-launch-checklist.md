# Master Launch Checklist: App, Website, Backend, Frontend, Admin, Plugins

How to read this: items marked (Added) are my own additions, not from the videos. Everything else is merged and de-duplicated from your saved lists.

Golden rule: make no mistakes. Do not launch until every box in sections 1 and 2 is ticked.

---

## 1. Hard launch blockers (your rules)
- [ ] Custom domain connected
- [ ] Favicon added (not the default builder icon)
- [ ] "Made with AI" tag or any builder badge removed
- [ ] Privacy policy page live
- [ ] Terms and conditions page live
- [ ] (Added) Both legal pages linked in the footer and on every signup or checkout form
- [ ] (Added) HTTPS works on the custom domain, and http redirects to https
- [ ] (Added) www and non-www both resolve to one canonical address

## 2. Design and content rules (your rules)
Never use:
- [ ] Purple gradients
- [ ] Pill-shaped buttons
- [ ] Fake reviews or testimonials
- [ ] Fake metrics or fake customer counters
- [ ] Vague hero text
- [ ] Emoji as icons
- [ ] Em dashes
- [ ] Over-the-top scroll animation
- [ ] Cursor animation
- [ ] AI-slop photos
- [ ] AI-slop copy
- [ ] (Added) Lorem ipsum or placeholder text anywhere
- [ ] (Added) Generic stock hero layouts that could belong to any product: say plainly what the product does, for whom, in one sentence

---

## 3. Frontend
- [ ] Never put secrets, API keys or service keys in frontend code
- [ ] Never trust user IDs, roles or prices sent from the frontend
- [ ] Remove auth tokens from local storage (prefer HttpOnly cookies)
- [ ] Sanitize user-generated content and forms, block XSS
- [ ] Remove exposed source maps from production
- [ ] Check for exposed files (.env, .git, backups, test pages)
- [ ] (Added) Add a Content Security Policy (CSP) header
- [ ] (Added) Never render raw HTML from users (avoid dangerouslySetInnerHTML and similar unless sanitized)
- [ ] (Added) Show friendly error states and a real 404 page, never raw errors
- [ ] (Added) Accessibility basics: alt text, contrast, keyboard navigation, visible focus, labels on form fields
- [ ] (Added) Mobile check on a real phone, not only a browser resize
- [ ] (Added) Performance check (Lighthouse): compress images, lazy-load below the fold, no huge bundles
- [ ] (Added) SEO basics: unique title and meta description per page, Open Graph image, sitemap.xml, robots.txt

## 4. Backend and APIs
- [ ] Validate every input on the server side
- [ ] Secure all API endpoints (auth required unless intentionally public)
- [ ] Keep API secrets on the server only
- [ ] Verify webhook signatures
- [ ] Check for SSRF (never fetch user-supplied URLs without an allowlist)
- [ ] Protect against SQL and NoSQL injection (parameterized queries, ORM, no string-built queries)
- [ ] Add rate limiting, especially on login, signup, password reset and expensive endpoints
- [ ] Disable debug mode in production
- [ ] Hide detailed errors and stack traces from users
- [ ] Keep sensitive data (passwords, tokens, personal data) out of logs
- [ ] (Added) Return consistent, minimal error messages (no hints about whether an email exists)
- [ ] (Added) Set request size limits and timeouts
- [ ] (Added) Make webhook handlers idempotent so a retried event does not double-process
- [ ] (Added) Separate dev, staging and production environments with different keys

## 5. Authentication and access control
- [ ] Add proper authentication
- [ ] Hash passwords securely (bcrypt, scrypt or argon2, never plain or fast hashes)
- [ ] Add multi-factor authentication (at minimum for admins)
- [ ] Verify permissions on the server side for every request
- [ ] Fix broken object-level authorization: a user can only read or change their own objects
- [ ] Isolate user data
- [ ] Protect admin routes
- [ ] Secure JWT secrets, and keep tokens short-lived
- [ ] Change all default credentials
- [ ] (Added) Cookie flags: HttpOnly, Secure, SameSite
- [ ] (Added) Session expiry, logout that really invalidates the session, and re-auth for sensitive actions
- [ ] (Added) Secure password reset: single-use, expiring tokens, no account enumeration
- [ ] (Added) Email verification before granting full access
- [ ] (Added) Principle of least privilege for every role and every service key

## 6. Database and storage
- [ ] Lock down database permissions
- [ ] Enable row-level security (RLS) where supported (Supabase, Postgres)
- [ ] Secure Firebase, Supabase and storage bucket rules (no public write, no public read of private data)
- [ ] Secure file uploads: validate type and size, random filenames, store outside the web root or in a private bucket
- [ ] Secure the database network access (no public database port)
- [ ] (Added) Never expose the Supabase service_role key or any admin database key to the client
- [ ] (Added) Automated backups turned on, and one restore actually tested
- [ ] (Added) Database migrations tracked in version control
- [ ] (Added) Encrypt sensitive fields and use TLS for database connections

## 7. Secrets and configuration
- [ ] Hide API keys
- [ ] Keep .env files hidden and in .gitignore
- [ ] Never hardcode secrets in code
- [ ] Check environment variables in production
- [ ] Check git history for leaked secrets, and rotate any secret that was ever committed
- [ ] (Added) Use a secret scanner (for example gitleaks) before every push
- [ ] (Added) Rotate keys when a team member leaves or a key might be exposed
- [ ] (Added) Use separate keys per environment and per service

## 8. Hardening
- [ ] Tighten CORS (specific origins only, never wildcard with credentials)
- [ ] Add security headers (CSP, X-Content-Type-Options, Referrer-Policy, frame protection, HSTS)
- [ ] Add CSRF protection
- [ ] Update vulnerable dependencies, remove unused ones
- [ ] (Added) Commit lockfiles and run npm audit or the equivalent regularly
- [ ] (Added) Turn on Dependabot or similar update alerts
- [ ] (Added) Enable bot protection (CAPTCHA or similar) on public forms if abuse appears

---

## 9. Admin panel
Goal: small changes should never need a developer call.
- [ ] User management: view, verify, block users
- [ ] Content control: change banners, categories, listings and content without an app update
- [ ] Payments and transactions: track payments, handle refunds, see failed payments
- [ ] Notifications: send offers and important updates to users directly
- [ ] Reports: generate and export business reports without asking the team for data
- [ ] Access control: decide who can access what (roles)
- [ ] Less manual work and faster decisions
- [ ] (Added) Audit log of every admin action: who did what and when
- [ ] (Added) Admin panel behind MFA, ideally on a separate path or subdomain with IP restriction if possible
- [ ] (Added) Destructive actions (delete user, refund) need confirmation
- [ ] (Added) Admin actions enforced on the server, never only hidden in the UI
- [ ] (Added) Export features respect permissions and never leak other users' data

## 10. Payments (if the app takes money) (Added)
- [ ] Use the payment provider's hosted checkout or SDK, never store card data yourself
- [ ] Confirm payment status only through verified server-side webhooks, never from the client
- [ ] Handle failed, pending and refunded states
- [ ] Store prices on the server, never trust prices from the client
- [ ] Clear refund and cancellation terms in the terms page

## 11. Legal, privacy and trust (Added)
- [ ] Privacy policy describes what data you actually collect, why, and who it is shared with
- [ ] Terms and conditions cover accounts, payments, refunds, acceptable use and liability
- [ ] Cookie or tracking notice if you use analytics or ads
- [ ] A working contact or support email
- [ ] A way for users to request data deletion
- [ ] Have the policies reviewed by a qualified lawyer, especially for India's DPDP Act, payments or other regulated data. I am not a lawyer, so treat templates as a starting point only.

## 12. Operations (Added)
- [ ] Uptime monitoring and alerts
- [ ] Error tracking (for example Sentry) with personal data scrubbed
- [ ] Basic analytics that respect privacy
- [ ] SPF, DKIM and DMARC set up for your domain so emails do not land in spam or get spoofed
- [ ] A simple incident plan: who gets alerted, how to rotate keys, how to roll back a deploy
- [ ] Rollback path for deployments

---

## 13. Tools and plugins
Verify each tool from its official site or repository before installing. Do not install anything from an unknown link.
- [ ] Supabase: database and auth, manageable from the terminal
- [ ] Playwright CLI: browser automation, reads pages, takes screenshots, navigates, helps find and fix errors
- [ ] Strix: attacks your site like a real attacker to find security gaps
- [ ] Skill UI: UI/UX design help, modern components, improves existing UI
- [ ] Context 7: keeps Claude supplied with up-to-date library docs (for example Next.js)

My notes (Added):
- Supabase, Playwright and Context 7 are well-known tools. I could not verify Strix and Skill UI from memory, so check their repositories, maintainers, stars, last update and permissions before giving them access to your project.
- Run security-testing tools only against your own staging site, never against sites you do not own.
- Give any AI agent or plugin the minimum access it needs. Do not hand it production keys.
- Commit to git before letting an AI agent make big changes, so you can roll back.

---

## 14. Testing and final audit
- [ ] Test the app as an untrusted user: try other users' IDs, direct URLs to admin pages, edited requests
- [ ] Run a full security audit with your AI agent, and fix everything it finds
- [ ] (Added) Run an automated scan (for example OWASP ZAP) against staging
- [ ] (Added) Test signup, login, password reset, payment and logout end to end on a real device
- [ ] (Added) Try to break forms: empty input, very long input, special characters, script tags
- [ ] (Added) Manually review the AI-generated code for auth and database queries, since AI often skips permission checks
- [ ] (Added) Ask the AI agent to explain each security-sensitive file, then verify the claims yourself

## 15. Final pass before pressing launch
- [ ] Sections 1 and 2 fully ticked
- [ ] No secrets in repo or git history
- [ ] Debug off, source maps removed, default credentials changed
- [ ] RLS and server-side permission checks verified
- [ ] Backups on and restore tested
- [ ] Legal pages live and linked
- [ ] Real photos, real copy, no fake numbers anywhere
- [ ] A second person (or a fresh review pass) has checked the whole list
