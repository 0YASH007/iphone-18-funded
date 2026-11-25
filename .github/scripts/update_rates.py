"""Fetch USD->INR rates and gold prices; write market.json, mastercard.json and gold.json.

Runs in GitHub Actions. Uses plain requests that identify themselves as this bot.
Each source is optional: if one fails, the old file is kept.
"""
import json, datetime, urllib.request

UA = {"User-Agent": "iphone-18-funded-rate-bot/1.0 (+https://github.com/0YASH007/iphone-18-funded)",
      "Accept": "application/json"}
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def write(path, data):
    try:
        old = json.load(open(path))
    except Exception:
        old = None
    if old == data:
        print(path, "unchanged"); return
    with open(path, "w") as f:
        json.dump(data, f, indent=2); f.write("\n")
    print(path, "->", data)


now = datetime.datetime.now(datetime.timezone.utc)

# Market rate: Yahoo Finance USDINR=X (updates through the trading day)
market = None
try:
    j = get("https://query1.finance.yahoo.com/v8/finance/chart/USDINR=X?interval=5m&range=1d")
    meta = j["chart"]["result"][0]["meta"]
    rate, ts = float(meta["regularMarketPrice"]), int(meta.get("regularMarketTime") or now.timestamp())
    if 50 < rate < 200:
        market = {"usdInr": round(rate, 2),
                  "time": datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "source": "Yahoo Finance"}
except Exception as e:
    print("Yahoo failed:", e)
if market is None:
    try:
        j = get("https://open.er-api.com/v6/latest/USD")
        market = {"usdInr": round(float(j["rates"]["INR"]), 2),
                  "time": datetime.datetime.fromtimestamp(int(j["time_last_update_unix"]), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "source": "ExchangeRate-API"}
    except Exception as e:
        print("ExchangeRate-API failed:", e)
if market:
    write("market.json", market)

# Mastercard: ask for today's IST date (the undated link returns a stale rate), then yesterday
for d in (now.astimezone(IST).date(), now.astimezone(IST).date() - datetime.timedelta(days=1)):
    try:
        j = get("https://www.mastercard.com/marketingservices/public/mccom-services/currency-conversions/conversion-rates"
                f"?exchange_date={d.isoformat()}&transaction_currency=USD&cardholder_billing_currency=INR&bank_fee=0&transaction_amount=1")
        data = j.get("data", j)
        rate = float(data["conversionRate"])
        if 50 < rate < 200:
            write("mastercard.json", {"usdInr": round(rate, 2), "date": data["fxDate"], "source": "Mastercard"})
            break
    except Exception as e:
        print("Mastercard", d, "failed:", e)

# Gold (India, per gram): Groww's gold-rate page, parsed from its text
import re, html as _html
try:
    req = urllib.request.Request("https://groww.in/gold-rates", headers={**UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=25) as r:
        page = r.read().decode("utf-8", "ignore")
    text = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", page)))
    num = lambda k: float(re.search(r"₹\s*([\d,]+(?:\.\d+)?)\s*per gram for " + k + r" karat", text).group(1).replace(",", ""))
    k24, k22, k18 = num("24"), num("22"), num("18")
    if 3000 < k18 < k22 < k24 < 60000:
        write("gold.json", {"k24": round(k24), "k22": round(k22), "k18": round(k18),
                            "date": now.astimezone(IST).date().isoformat(),
                            "time": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "Groww"})
    else:
        print("Gold values look wrong:", k24, k22, k18)
except Exception as e:
    print("Gold failed:", e)
