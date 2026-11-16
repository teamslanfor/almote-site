# Almonte Trading Group L.L.C. – website (new "Harbor" theme)

## Quick start (no tools needed)
The `website/` folder is the complete site, with every file at the top level and no sub-folders.:
index.html, about.html, products.html, services.html, gallery.html, contact.html, 404.html,
styles.css, main.js, chatbot.js, site-config.js, logo-mark.svg, the images, site.webmanifest, robots.txt and sitemap.xml.

- **Open locally:** double-click `index.html`.
- **GitHub + Vercel:** upload ALL files from `website/` (or the WEBSITE zip) to the TOP of the repository, not inside a folder. In Vercel choose Framework Preset "Other", with no build command and no output directory.
- **Netlify:** drag the `website` folder onto app.netlify.com/drop.
- **cPanel:** upload all files into `public_html`.

## Quote form
No business email has been verified, so the quote form and chat assistant open **WhatsApp to (787) 383-2424** with
the full request filled in (name, company, buyer type, categories and requirements). Text and call links are also
offered. Once an official email is confirmed, the form can be switched to send by email.

## Where the facts came from (verify before publishing)
- **Puerto Rico Federal Contracting Center success story (20 June 2025):** President Awilda López; four federal contracts worth "over $2.5 million" won in less than a year; tripled workforce; canned, packaged and fresh foods incl. meats and seafood; federal customers named: MDC, Fort Allen, Camp Santiago, U.S. Navy, National Guard; the "trusted federal supplier" quote.
- **HigherGov / SAM profile:** UEI TBF2WJMVM4G5; CAGE 9YA47; founded 18 July 2022; primary NAICS 424490; SBA HUBZone (9 Aug 2024) and WOSB (24 Sep 2024) certifications; product description (cookies, chocolates, tuna, confectionery, mineral water, isotonic drinks, sodas); PSC categories.
- **Client brief:** phone (787) 383-2424; physical address 305 Calle Emajagua, Hacienda Borinquen, Caguas, PR 00725; mailing address P.O. Box 5901, Caguas, PR 00726.
- **Photos:** royalty-free Unsplash stock (warehouse, port, trucks, products), labelled on the Products page as illustrative. No third-party brand images are used.

## Please confirm with the client
- Current status of the WOSB and HUBZone certifications, and permission to name federal customers (MDC, Fort Allen, Camp Santiago, U.S. Navy, National Guard).
- Official logo (a placeholder "A" mark is used), business email, product catalogue and brand names, warehouse photos, delivery areas, and domain (www.almontetradinggroup.com is a placeholder).
- The marketing copy is proposed text based on documented activities, and needs client approval.
- A Spanish version can be added (recommended for Puerto Rico buyers).

## Editing (needs Python 3)
Company details are in `SITE` at the top of `build.py`, and page content is in its page functions. The styles, scripts and images are in `assets-src/`.
Run `python3 build.py` to regenerate `website/`.
