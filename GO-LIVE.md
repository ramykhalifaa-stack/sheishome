# Putting www.sheishome.co.uk live

Plain steps, in order. Nothing here costs money.

## 1. The domain (done)

`sheishome.co.uk` is registered with Tasjeel (my.tasjeel.ae). You only ever needed the domain
from them, not their hosting. Keep the renewal reminder in your calendar.

## 2. Choose where the site is served from

The site is a folder of finished pages, so any of these will serve it for free, for ever.
Pick one. Cloudflare Pages is the one I would choose.

| Host | What it costs | What you have to do |
| --- | --- | --- |
| Cloudflare Pages | Free | Make a Cloudflare account, connect the GitHub repository, set the custom domain |
| Vercel | Free | Make a Vercel account, import the repository, add the domain |
| GitHub Pages | Free | Turn Pages on in the repository settings (the repository has to be public) |

All three give you HTTPS (the padlock) automatically and at no cost.

## 3. Publish the code

The site lives in this folder on the Mac. To publish it the first time:

```bash
cd ~/Projects/sheishome && ./deploy.sh "First publish"
```

If there is no GitHub repository yet, create one called `sheishome` and connect it:

```bash
cd ~/Projects/sheishome && gh repo create sheishome --public --source . --remote origin --push
```

Whenever anything changes later, the same one line republishes it:

```bash
cd ~/Projects/sheishome && ./deploy.sh "What changed"
```

## 4. Connect the site to the host

**Cloudflare Pages:** sign in at dash.cloudflare.com, choose Workers and Pages, Create, Pages,
Connect to Git, pick the `sheishome` repository. For the build settings choose "None" as the
framework, leave the build command empty and set the output directory to `docs`. Then open the
project, go to Custom domains and add `www.sheishome.co.uk`.

**Vercel:** sign in at vercel.com, Add New, Project, import `sheishome`, framework "Other",
output directory `docs`, then Settings, Domains, add `www.sheishome.co.uk`.

**GitHub Pages:** in the repository, Settings, Pages, source "Deploy from a branch", branch
`main`, folder `/docs`, Save. Then add `www.sheishome.co.uk` as the custom domain and tick
Enforce HTTPS.

## 5. Point the domain at the host (this is the DNS step)

Sign in to my.tasjeel.ae, open the client area, find `sheishome.co.uk` and open its DNS records
(sometimes called Manage DNS or Zone Editor). You need two records.

| Type | Name (host) | Value (points to) |
| --- | --- | --- |
| CNAME | `www` | the address your host gives you |
| URL redirect or ALIAS | `@` (the bare domain) | `https://www.sheishome.co.uk` |

The address for the CNAME is:

- Cloudflare Pages: `sheishome.pages.dev` (the project address shown in your dashboard)
- Vercel: `cname.vercel-dns.com`
- GitHub Pages: `ramykhalifaa-stack.github.io`

If Tasjeel will not let you redirect the bare domain, add these four A records on `@` instead,
which is the GitHub Pages option:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Changes usually appear within an hour, occasionally up to a day. Check progress at
dnschecker.org by searching for `www.sheishome.co.uk`.

## 6. Email, when you want it

No mailbox has been set up, as agreed. When you want `hello@sheishome.co.uk`:

- **Free forwarding:** Cloudflare Email Routing forwards `hello@sheishome.co.uk` to a Gmail
  address at no cost. Good enough to start receiving.
- **A real mailbox:** Zoho Mail has a free tier for one domain, or Google Workspace at about
  £5 a month if you want Gmail proper.

Either way it is a handful of DNS records added in the same place as step 5, and I can do it
with you in ten minutes. The Join page currently sends people to the sign-up form and the
WhatsApp community instead of an email address, so nothing is broken in the meantime.

## 7. What happens when somebody joins

The sign-up form on the Join page posts to the ROSE platform you already run on Railway. Every
person who joins appears under **Community** in that dashboard, and there is a Download CSV
button so you can send the SHE Letter from whichever email tool you choose later.

## 8. Keeping it up to date

Everything a visitor reads lives in one file: `src/content/__init__.py`. Change the words there,
run `./deploy.sh "Updated the retreat dates"`, and the live site follows a minute later.
Photographs are cut from the approved page map by `tools/crop_assets.py`, so the site always
matches the designs.
