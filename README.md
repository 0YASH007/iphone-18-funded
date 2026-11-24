# 💎 iPhone 18 Pro Max Fund

**Live:** https://0yash007.github.io/iphone-18-funded/

A savings tracker for my next phone: **iPhone 18 Pro Max · 256 GB · Glacier Blue**.

**Target:** $1,299 + 9% tax = **$1,415.91**, converted to rupees at the live USD → INR rate.

## Features

- **Market rate.** XE's mid-market rate is saved to `market.json` every hour (9 am – 6 pm IST); the page also checks free daily sources and shows whichever is newest.
- **Live exchange rate.** Each time the page opens, it fetches the USD → INR rate from [ExchangeRate-API](https://www.exchangerate-api.com/), with the ECB rate via [Frankfurter](https://www.frankfurter.app/) as a backup, and recalculates the ₹ target.
- **Mastercard rate.** Shown next to the market rate, with the target at both rates and a switch to set the target to either. `mastercard.json` is refreshed daily.
- **Rate history.** A sparkline of past rates, plus "₹X cheaper/costlier than last time" with ▲/▼ badges.
- **Highlighted cards** for *Still needed* and *1 USD = INR today*.
- **Progress ring and phone fill.** The drawn phone fills with glacier-blue liquid as you save. Or tap **📷 Use your photo** and your own phone picture fills with colour from the bottom up.
- **Celebrations.** Confetti and ₹ coins, sparkles, a floating "+₹amount", chimes, haptics, and pop-ups at 1 / 10 / 25 / 50 / 75 / 90 / 100%.
- **Save / Withdraw** with quick-add buttons (+100 … +5K), notes and a history list.
- **At this pace:** a projected purchase date based on how fast you're saving.
- **Edit rate.** Override the rate with your bank's or card's actual rate.
- **Backup / Restore.** Download your savings as JSON and restore it on another device.

## Data & privacy

Everything is stored in your browser's `localStorage`. Nothing is sent to a server (apart from the exchange-rate request). Use **💾 Backup** regularly, because clearing browser data erases it.

## Run it

It's a single static file, so you can open `index.html` directly or host it on GitHub Pages:

1. Go to **Settings → Pages**.
2. Under *Build and deployment*, choose **Deploy from a branch**, then select `main` / `root`.
3. After about a minute it's live at `https://0yash007.github.io/iphone-18-funded/`.
