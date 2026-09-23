#!/usr/bin/env python3
"""Telegram-бот главного: приём сообщений владельца и отправка ответов.

  tg.py wait        — ждёт сообщения владельца (long polling) и завершается,
                      напечатав их; чужие сообщения молча пропускает.
  tg.py send ТЕКСТ  — отправляет владельцу; без ТЕКСТА читает stdin.

Реквизиты: переменные окружения TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID,
иначе файл /root/.config/telegram/chief.env. Токен в вывод не попадает.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

CONF = "/root/.config/telegram"
OFFSET_FILE = os.path.join(CONF, "offset")
LIMIT = 4000  # у Telegram предел 4096 знаков на сообщение


def creds():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    path = os.path.join(CONF, "chief.env")
    if (not token or not chat) and os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            key, _, val = line.strip().partition("=")
            if key == "TELEGRAM_BOT_TOKEN" and not token:
                token = val
            if key == "TELEGRAM_CHAT_ID" and not chat:
                chat = val
    if not token or not chat:
        sys.exit("нет TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID")
    return token, chat


def call(token, method, params, timeout=70):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/{method}", data=data)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:  # Telegram кладёт причину в JSON-тело
        return json.load(err)


def download(token, media):
    """Скачивает фото или файл из сообщения в CONF/media, возвращает путь или None."""
    try:
        info = call(token, "getFile", {"file_id": media["file_id"]}, timeout=30)
        remote = info["result"]["file_path"]
        os.makedirs(os.path.join(CONF, "media"), exist_ok=True)
        local = os.path.join(CONF, "media", f"{media['file_unique_id']}{os.path.splitext(remote)[1]}")
        with urllib.request.urlopen(f"https://api.telegram.org/file/bot{token}/{remote}", timeout=60) as resp, open(local, "wb") as f:
            f.write(resp.read())
        return local
    except Exception as exc:
        print(f"ошибка скачивания вложения: {type(exc).__name__}", file=sys.stderr)
        return None


def wait():
    token, chat = creds()
    while True:
        try:
            offset = int(open(OFFSET_FILE).read().strip())
        except (OSError, ValueError):
            offset = 0
        try:
            res = call(token, "getUpdates", {"timeout": 50, "offset": offset,
                                             "allowed_updates": '["message"]'})
        except Exception as exc:  # сеть моргнула — ждём и повторяем
            print(f"ошибка getUpdates: {type(exc).__name__}", file=sys.stderr)
            time.sleep(5)
            continue
        texts = []
        for upd in res.get("result", []):
            offset = upd["update_id"] + 1
            msg = upd.get("message") or {}
            if str(msg.get("chat", {}).get("id")) == chat and str(msg.get("from", {}).get("id")) == chat:
                text = msg.get("text") or msg.get("caption") or ""
                media = msg.get("photo") and msg["photo"][-1] or msg.get("document")
                if media:
                    path = download(token, media)
                    text = (text + "\n" if text else "") + (f"[вложение: {path}]" if path else "[вложение не скачалось]")
                texts.append(text or "[сообщение без текста]")
        os.makedirs(CONF, exist_ok=True)
        with open(OFFSET_FILE, "w") as f:
            f.write(str(offset))
        if texts:
            print("СООБЩЕНИЕ ВЛАДЕЛЬЦА ИЗ TELEGRAM (бот главного):")
            print("\n---\n".join(texts))
            print("\nЧто делать: простой вопрос по цифрам — ответить самому по панели; задача или разбор — "
                  "отдать агенту chief. Ответ владельцу: python3 scripts/telegram/tg.py send \"...\". "
                  "Затем снова запустить в фоне: python3 scripts/telegram/tg.py wait")
            return


def send(text):
    token, chat = creds()
    text = text.strip()
    if not text:
        sys.exit("пустой текст")
    for i in range(0, len(text), LIMIT):
        res = call(token, "sendMessage", {"chat_id": chat, "text": text[i:i + LIMIT]}, timeout=30)
        if not res.get("ok"):
            sys.exit(f"Telegram отказал: {res.get('description')}")
    print("отправлено")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "wait":
        wait()
    elif cmd == "send":
        send(" ".join(sys.argv[2:]) if len(sys.argv) > 2 else sys.stdin.read())
    else:
        sys.exit(__doc__)
