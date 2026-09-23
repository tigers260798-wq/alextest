#!/usr/bin/env python3
"""Генерация статики через OpenAI Images API с учётом бюджета.

  gen_image.py --prompt "..." --out ПАПКА --tag ИМЯ [--model gpt-image-2] [--quality medium] [--size 1024x1536]
  gen_image.py --spent    — сколько потрачено из бюджета

Ключ: OPENAI_API_KEY или /root/.config/openai.env (в вывод не попадает).
Журнал расходов: /root/.config/openai_ledger.json. Бюджет по умолчанию — 10 $ кредитов
(владелец 23.09: «надо выработать эти 10 дол»); перед генерацией проверяется, что
оценка не выведет за бюджет. Цены — официальные, developers.openai.com/api/docs/pricing (23.09.2026).
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

LEDGER = "/root/.config/openai_ledger.json"
BUDGET = float(os.environ.get("OPENAI_BUDGET_USD", "10"))
# $ за 1M токенов: вход текст, выход картинка; mini — по таблице цены за картинку
TOKEN_PRICE = {"gpt-image-2": (5.00, 30.00), "gpt-image-2.5-flare": (5.00, 30.00), "gpt-image-2.5-sunburst": (5.00, 30.00)}
MINI_PER_IMAGE = {("low", "1024x1024"): 0.005, ("low", "1024x1536"): 0.006, ("low", "1536x1024"): 0.006,
                  ("medium", "1024x1024"): 0.011, ("medium", "1024x1536"): 0.015, ("medium", "1536x1024"): 0.015,
                  ("high", "1024x1024"): 0.036, ("high", "1024x1536"): 0.052, ("high", "1536x1024"): 0.052}
ESTIMATE = {"gpt-image-2": 0.045, "gpt-image-2.5-flare": 0.05, "gpt-image-2.5-sunburst": 0.05}


def key():
    k = os.environ.get("OPENAI_API_KEY")
    if not k and os.path.exists("/root/.config/openai.env"):
        k = open("/root/.config/openai.env").read().strip().split("=", 1)[1]
    if not k:
        sys.exit("нет OPENAI_API_KEY")
    return k


def ledger():
    try:
        return json.load(open(LEDGER))
    except (OSError, ValueError):
        return {"budget_usd": BUDGET, "spent_usd": 0.06, "items": [{"note": "пробы 23.09 до журнала", "usd": 0.06}]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt"); ap.add_argument("--out"); ap.add_argument("--tag", default="img")
    ap.add_argument("--model", default="gpt-image-2"); ap.add_argument("--quality", default="medium")
    ap.add_argument("--size", default="1024x1536"); ap.add_argument("--spent", action="store_true")
    a = ap.parse_args()
    lg = ledger()
    if a.spent:
        print(f"потрачено {lg['spent_usd']:.3f} $ из {lg['budget_usd']:.2f} $ кредитов, картинок {len(lg['items']) - 1}")
        return
    if not a.prompt or not a.out:
        sys.exit("нужны --prompt и --out")
    est = MINI_PER_IMAGE.get((a.quality, a.size), 0.02) if a.model == "gpt-image-1-mini" else ESTIMATE.get(a.model, 0.06)
    if lg["spent_usd"] + est > lg["budget_usd"]:
        sys.exit(f"стоп: бюджет {lg['budget_usd']} $ почти исчерпан (потрачено {lg['spent_usd']:.3f} $)")
    body = json.dumps({"model": a.model, "prompt": a.prompt, "size": a.size, "quality": a.quality, "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
                                 headers={"Authorization": "Bearer " + key(), "Content-Type": "application/json"})
    t = time.time()
    try:
        d = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as err:
        sys.exit(f"OpenAI отказал: {err.code} {json.load(err).get('error', {}).get('message', '')[:200]}")
    u = d.get("usage") or {}
    if a.model in TOKEN_PRICE:
        pin, pout = TOKEN_PRICE[a.model]
        cost = u.get("input_tokens", 0) * pin / 1e6 + u.get("output_tokens", 0) * pout / 1e6
    else:
        cost = est
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, f"{a.tag}.png")
    open(path, "wb").write(base64.b64decode(d["data"][0]["b64_json"]))
    lg["spent_usd"] = round(lg["spent_usd"] + cost, 4)
    lg["items"].append({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tag": a.tag, "model": a.model,
                        "quality": a.quality, "size": a.size, "usage": u, "usd": round(cost, 4)})
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    json.dump(lg, open(LEDGER, "w"), ensure_ascii=False, indent=1)
    print(json.dumps({"file": path, "usd": round(cost, 4), "sec": round(time.time() - t, 1),
                      "spent_usd": lg["spent_usd"], "budget_usd": lg["budget_usd"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
