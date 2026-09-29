# DE · кредиты · углы 1 «мини-кредит в телефоне» и 3 «кредитка на 5 000» · статья A (24.09.2026)

- **Гео и язык:** DE, немецкий. Текст безличный, к читателю на «Sie» не обращается.
- **Провайдер:** IRONFLI, это наша статья. На VISYMO ставим тот же заголовок и те же ключи, locale de_DE, текст VISYMO соберёт сам.
- **Подход (поле `approach`):** «угол первым». По кредитам в DE своей выплаты у нас нет: 24.09 я сделал 5 выборок research_keywords DE/de, и во всех ourKeywords.topic пуст. RPC в таблице ключей — это наши доноры из других гео или класс других команд.
- **Тема (как её поймёт провайдер):** Digitale Kleinkredite in Deutschland 2026: Minikredit per App (Antrag, Auszahlungstempo, effektiver Jahreszins, Gebühren) im Vergleich zur Kreditkarte mit Verfügungsrahmen bis 5.000 Euro (Limit, Bonität, Teilzahlung, „kostenlose“ Karten).
- **Заголовок:** Digitale Kleinkredite 2026: Minikredit per App oder Kreditkarte mit 5.000 € Limit?
  - Перевод: «Цифровые мини-кредиты 2026: мини-кредит в приложении или кредитка с лимитом 5 000 €?»
  - **Что поменял:** у маркетолога было «… mit 5.000 € Rahmen?». Одно слово «Rahmen» без приставки звучит обрубленно и по-канцелярски: немец скажет Kreditrahmen, Verfügungsrahmen или Limit. «Limit» — разговорное слово. Оно стоит во всех хуках угла 3 и есть в Planner: «kreditkarte 5000 euro limit», 260 в месяц, bid $14.56. В hooks.json поправил тоже (angle1 n2, angle3 n4).
- **Объём:** 1 078 слов: заголовок, лид и 6 разделов. Служебные блоки не считал.
- **Основа:** разделы про лимит взял из черновика `DE-kreditkarte-limit-2026-09-23`, сократил и добавил два куска: «Zahlung abgelehnt» и разбор «kostenlos». Тема и набор ключей повторяют DE-связку коллег «Digitale Kleinkredite…» (b07), бренд убран.

## Структура

1. **Mini Kredit per App: Betrag wählen, Laufzeit wählen.** Как проходит заявка в приложении. Ставка на ползунке — только пример, настоящую назначают после проверки. К концу 2026 в ЕС вводят более строгие правила для мелких кредитов.
2. **Minikredit Auszahlung in 24h: Was „sofort“ wirklich heißt.** От чего зависит скорость: идентификация, документы, проверка, выходные. С 2025 года переводы идут за секунды. Отдельная доплата за экспресс-выплату.
3. **Die Zahl, die fast niemand liest.** Эффективная ставка и общая сумма к возврату. Ещё про экспресс-сборы, просрочку, платные продления и рассрочку в платёжных приложениях; 14 дней на отзыв. Этот раздел отвечает на хук угла 1.
4. **Kreditkarte mit 5000 Verfügungsrahmen: Warum er 500 € bekommt und sie 5.000 €.** Доход, тип занятости, кредитная история, тип карты. Стартовый лимит и как его повышают. Отель блокирует сумму; «Zahlung abgelehnt», хотя деньги на счёте есть. Раздел отвечает на хуки угла 3.
5. **Kreditkarte mit Ratenzahlung 5.000 Euro: Wann „kostenlos“ teuer wird.** Рассрочка по кредитке, которая бывает включена по умолчанию, и разбор «бесплатной» карты. Под ключ «Kostenlose Kreditkarte Beantragen» — только ключ и разбор в статье, так решил главный.
6. **Minikredit oder Kreditkarte: Was passt wann?** Ответ на вопрос из заголовка, отдельно про снятие наличных с кредитки.

## Сверка креативов (hooks.json) с текстом

Проверял, чтобы ни одного слитого клика не было:
- **angle1 n1:** «…doch eine Zahl liest fast niemand» → раздел 3 «Die Zahl, die fast niemand liest».
- **angle1 n2 / angle3 n4 (заголовок):** → вся статья, прямой ответ в разделе 6.
- **angle1 n3:** «Wartemarke … zwei Regler … wo der Haken steckt» → разделы 1–3 (ползунки, доплата за экспресс, продления).
- **angle1 n4:** «Was danach kommt, weiß kaum jemand» → раздел 3.
- **angle3 n1:** «Er: 500 € Limit. Sie: 5.000 €. Warum?» → раздел 4, в заголовке раздела почти дословно.
- **angle3 n2:** «Das Hotel blockiert 800 €…» → раздел 4, последний абзац (резерв отеля, временное повышение лимита).
- **angle3 n3:** «„Zahlung abgelehnt“ – obwohl … genug Geld» → раздел 4, последний абзац, фраза дословно.

---

# Digitale Kleinkredite 2026: Minikredit per App oder Kreditkarte mit 5.000 € Limit?

Die Waschmaschine, die Autowerkstatt, die nächste Reise: Oft fehlt kurzfristig ein kleiner Betrag. Dafür muss heute kaum noch jemand in eine Filiale. Ein Mini Kredit lässt sich per App beantragen, eine Kreditkarte mit hohem Limit online. Beide Wege wirken gleich einfach: Betrag wählen, Laufzeit wählen, bestätigen. Was sie am Ende kosten, steht aber an einer Stelle, die viele überspringen. Dieser Beitrag erklärt, wie beide Varianten 2026 funktionieren, wovon Tempo und Limit abhängen und welche Zahl man vor der Unterschrift kennen sollte.

## Mini Kredit per App: Betrag wählen, Laufzeit wählen

Ein Mini Kredit ist ein kleiner Kredit über meist einige hundert bis wenige tausend Euro mit kurzer Laufzeit. Wer einen Online Kredit beantragen möchte, erledigt heute fast alles auf dem Handy:

- Betrag und Laufzeit werden per Schieberegler eingestellt, die App zeigt dazu eine Beispielrate;
- im Antrag folgen Angaben zu Einkommen, festen Ausgaben und Beschäftigung;
- die Identität wird per Video oder über das eigene Online-Banking bestätigt;
- manche Anbieter bitten um einen digitalen Blick auf die Kontoumsätze der letzten Wochen, um das Einkommen zu prüfen.

Die Regler sind bequem, zeigen aber nur einen Teil der Wahrheit. Die angezeigte Rate ist ein Rechenbeispiel, den tatsächlichen Zins legt der Anbieter erst nach der Prüfung fest, und er kann je nach Bonität höher ausfallen. Auch bei kleinen Beträgen werden Daten zur bisherigen Zahlungsgeschichte abgefragt. Für Ende 2026 sind in der EU zudem strengere Regeln vorgesehen, nach denen auch sehr kleine Kredite und viele Ratenkäufe gründlicher geprüft werden sollen.

## Minikredit Auszahlung in 24h: Was „sofort“ wirklich heißt

Viele Angebote werben mit Tempo: Minikredit Auszahlung in 24h, Minikredit mit Sofortauszahlung oder ein Kredit mit zeitnaher Auszahlung. Technisch ist schnelles Geld kein Problem mehr. Seit 2025 können Banken in der EU Überweisungen innerhalb von Sekunden ausführen. Wenn es trotzdem dauert, liegt es fast immer an den Schritten davor:

- der Identitätsprüfung: Ein Video-Termin am späten Abend kann den Antrag auf den nächsten Tag verschieben;
- den Unterlagen: Fehlt ein Einkommensnachweis, bleibt der Antrag liegen;
- der Kreditprüfung: Sie läuft meist automatisch, bei Unklarheiten schaut ein Mitarbeiter nach;
- dem Wochentag: Manche Anbieter prüfen am Wochenende nur eingeschränkt.

Wer einen Online Kredit sofort braucht, sollte außerdem auf Aufpreise achten. Einige Anbieter verlangen für die Expressauszahlung eine eigene Gebühr. Bei wenigen hundert Euro kann ein solcher Aufschlag mehr kosten als die Zinsen selbst. „Sofort“ bezieht sich meist auf die Entscheidung, nicht auf das Geld auf dem Konto.

## Die Zahl, die fast niemand liest

Im Vertrag und im Informationsblatt vor der Unterschrift steht eine Zahl, die mehr über die Kosten verrät als jede Rate: der effektive Jahreszins. Er enthält neben dem Sollzins auch Pflichtkosten und macht Angebote vergleichbar. Direkt daneben steht der Gesamtbetrag, also die Summe, die über die ganze Laufzeit zurückgezahlt wird.

Bei kleinen Krediten lohnt sich außerdem ein Blick auf:

- Gebühren für Express, Zusatzleistungen oder eine Ratenpause;
- Kosten, wenn eine Rate zu spät kommt;
- Verlängerungen gegen Gebühr, bei denen aus 30 Tagen schnell 60 oder 90 werden;
- Ratenkäufe in Bezahl-Apps, die sich wie ein Einkauf anfühlen, rechtlich aber ein Kredit sind.

Eine einfache Faustregel: Wer den Gesamtbetrag nicht nennen kann, hat den Vertrag noch nicht gelesen. Nach der Unterschrift gilt bei Verbraucherkrediten in der Regel ein Widerrufsrecht von vierzehn Tagen.

## Kreditkarte mit 5000 Verfügungsrahmen: Warum er 500 € bekommt und sie 5.000 €

Die zweite digitale Variante ist die Kreditkarte. Eine Online Kreditkarte sofort zu beantragen dauert oft nur Minuten, und manche Banken stellen nach der Freigabe direkt eine virtuelle Karte fürs Handy bereit. Den Rahmen legt die Bank aber für jeden Kunden einzeln fest. Eine Kreditkarte mit 5000 Verfügungsrahmen, also mit 5.000 Euro Limit, bekommt längst nicht jeder. Zwei Menschen mit derselben Karte derselben Bank können sehr unterschiedliche Limits erhalten. Entscheidend sind:

- das Nettoeinkommen und feste Ausgaben wie Miete und laufende Raten;
- die Beschäftigung: unbefristet, befristet, in der Probezeit oder selbstständig;
- die Bonität, also die gespeicherte Zahlungsgeschichte;
- die Zahl bestehender Karten und Kredite;
- der Kartentyp: Bei einer Charge-Karte wird einmal im Monat alles abgebucht, bei einer Revolving-Karte kann in Raten zurückgezahlt werden.

Neue Kunden starten oft mit einigen hundert Euro. Wer die Karte regelmäßig nutzt und pünktlich ausgleicht, kann später eine Erhöhung beantragen; die Bank prüft dann Einkommen und Bonität erneut.

Im Alltag ist der Rahmen oft früher ausgeschöpft als gedacht. Hotels und Autovermietungen reservieren häufig mehrere hundert Euro als Sicherheit, und auch noch nicht abgerechnete Umsätze zählen bereits mit. Dann meldet das Terminal „Zahlung abgelehnt“, obwohl auf dem Girokonto genug Geld ist: Kartenlimit und Kontostand sind zwei verschiedene Dinge. Vor einer Reise lohnt es sich, den freien Betrag in der App zu prüfen und bei Bedarf eine befristete Erhöhung zu beantragen.

## Kreditkarte mit Ratenzahlung 5.000 Euro: Wann „kostenlos“ teuer wird

Bei einer Kreditkarte mit Ratenzahlung 5.000 Euro auszugeben ist leicht; den Betrag in kleinen Raten zurückzuzahlen, kann dagegen viele Monate dauern. Die Zinsen für Teilzahlungen liegen bei Kreditkarten meist deutlich über denen eines klassischen Ratenkredits. Bei manchen Karten ist die Teilzahlung sogar voreingestellt: Wer nichts ändert, zahlt jeden Monat nur einen kleinen Teil zurück, und auf den Rest laufen Zinsen.

Wer eine kostenlose Kreditkarte beantragen will, sollte genau hinschauen, was „kostenlos“ bedeutet. Meist ist nur die Jahresgebühr gemeint. Kosten entstehen trotzdem:

- durch Zinsen, wenn in Raten zurückgezahlt wird;
- für Zahlungen in Fremdwährung und für Bargeld am Automaten;
- für Ersatzkarten, Mahnungen oder Rücklastschriften;
- wenn die Gebührenfreiheit an Bedingungen wie einen Mindestumsatz geknüpft ist.

Die beste Kreditkarte mit Ratenzahlung ist deshalb nicht die mit dem höchsten Rahmen oder dem lautesten „kostenlos“, sondern die, bei der man die Teilzahlung selbst steuert und den Saldo jederzeit vollständig ausgleichen kann.

## Minikredit oder Kreditkarte: Was passt wann?

Beide Wege sind digital, schnell beantragt und für kleine Beträge gedacht. Sie passen aber zu unterschiedlichen Situationen:

- Ein Minikredit passt eher zu einer einmaligen Ausgabe mit festem Betrag, etwa einer Reparatur, die in wenigen Monaten zurückgezahlt werden kann. Laufzeit und Rate stehen von Anfang an fest.
- Eine Kreditkarte passt eher zu wiederkehrenden Ausgaben, Reisen und Buchungen mit Kaution. Günstig bleibt sie, solange der Saldo jeden Monat vollständig ausgeglichen wird.

Wer nach einer Kreditkarte mit Sofort Geld in Deutschland sucht, meint oft beides zugleich: schnelles Bargeld und einen dauerhaften Rahmen. Bargeld mit der Kreditkarte ist allerdings meist die teuerste Variante, weil oft eine Gebühr und ab dem ersten Tag Zinsen anfallen. Für einen einmaligen Betrag ist ein kleiner Ratenkredit mit festem Ende in der Regel die übersichtlichere Lösung.

Bei beiden Varianten entscheidet am Ende nicht der Regler in der App, sondern die Zahl im Vertrag: der effektive Jahreszins und der Gesamtbetrag.

---

## Ключи на утверждение

12 ключей углов 1 и 3, каждый дословно стоит в своём разделе (скрипт проверял без учёта регистра). По DE своей выплаты у нас нет. Где RPC взят у донора, это наш ключ из другого гео; где указан класс, это другие команды, их деньги не показываются. Всё это порядок величины, а не прогноз. Planner DE — за 2026-08, bid означает верхнюю ставку в топе выдачи и служит прокси RPC. Дешёвые кликабельные ключи («Mini Kredit», «Minikredit …», bid $7–8) стоят в лиде и начале статьи. Дорогие («Online Kredit beantragen / sofort» $22–24, карточные $14–16) — в теле.

| # | Ключ | Перевод | RPC $ | Planner DE | Куда в статье |
|---|------|---------|-------|------------|---------------|
| 1 | Online Kredit beantragen | оформить онлайн-кредит | DE не измерен; у других команд в CH «Online Kredit Beantragen» — high; донор (наш, HU) «Gyorskölcsön Azonnal» $0.459 (57 кл.) | 4 400/мес, bid $23.55 — самый высокий в наборе | раздел 1: «Wer einen Online Kredit beantragen möchte, …» |
| 2 | Online Kredit sofort | онлайн-кредит сразу | донор HU $0.459 | 5 400/мес, −46%, bid $22.72 | раздел 2: «Wer einen Online Kredit sofort braucht, …» |
| 3 | Kreditkarte mit Ratenzahlung 5.000 Euro | кредитка с рассрочкой на 5 000 € | у других команд DE — high; своего донора по картам нет | «kreditkarte mit ratenzahlung» 1 600/мес, bid $16.31 | заголовок раздела 5 + первая фраза |
| 4 | Beste Kreditkarte mit Ratenzahlung | лучшая кредитка с рассрочкой | у других DE — high | то же, 1 600/мес, $16.31 | раздел 5, последний абзац |
| 5 | Kostenlose Kreditkarte Beantragen | оформить бесплатную кредитку | у других DE — high | 480/мес, +23%, bid $15.99 | раздел 5, абзац-разбор: «Wer eine kostenlose Kreditkarte beantragen will, sollte genau hinschauen …». **Только в статье, на креативе никогда** (решение главного) |
| 6 | Kreditkarte mit Sofort Geld in Deutschland | кредитка с деньгами сразу, Германия | в DE не измерен; у других в CH «Kreditkarte mit Sofort Geld» — high; ключ из DE-связки коллег (b07) | «kreditkarte mit sofort geld» 1 000/мес, bid $15.66 | раздел 6: «Wer nach einer Kreditkarte mit Sofort Geld in Deutschland sucht, …» |
| 7 | Kreditkarte mit 5000 Verfügungsrahmen | кредитка с лимитом 5 000 | у других в DE — mid, в CH — high; есть в DE- и CH-связках коллег | «kreditkarte mit verfügungsrahmen» 2 900/мес, $14.99; «kreditkarte 5000 euro limit» 260, $14.56 | заголовок раздела 4 + первый абзац |
| 8 | Online Kreditkarte Sofort | онлайн-кредитка сразу | у других в DE и CH — high | точной строки нет; ближайшая «kreditkarte mit sofort verfügungsrahmen» 260/мес, $13.83 | раздел 4, первая фраза |
| 9 | Mini Kredit | мини-кредит | у других в AT «Mini Kredit Österreich» — high; донор (наш, HU) «Kis Összegű Kölcsön Azonnal» $0.386 (32 кл.) | 5 400/мес, bid $8.33 | лид + заголовок раздела 1 |
| 10 | Minikredit Auszahlung in 24h | мини-кредит с выплатой за 24 ч | не измерен; ключ DE-связки коллег; донор HU $0.459 | «mini kredit sofort auszahlung» 720/мес, +50%, $7.19 | заголовок раздела 2 + первая фраза |
| 11 | Minikredit mit Sofortauszahlung | мини-кредит с мгновенной выплатой | донор HU $0.459 | 1 300/мес, $7.01 | раздел 2, первая фраза |
| 12 | Kredit mit zeitnaher Auszahlung | кредит с быстрой выплатой | не измерен; ключ DE-связки коллег; донор HU $0.459 | Planner строку не вернул | раздел 2, первая фраза |

**Для решения главного и маркетолога:**
- **Ключей 12, а не 5–6.** Так задано: ключи обоих углов. Если IRONFLI или VISYMO примут в термины меньше, беру топ-6 по bid: № 1, 2, 3, 5, 6, 7.
- **«Kredit mit zeitnaher Auszahlung»** Planner в трёх выборках не вернул. Ключ оставил, потому что он стоит в рабочем IRONFLI-оффере коллег (b07). Если главный хочет только ключи, подтверждённые Planner, есть замена того же смысла: «kredit sofortauszahlung», 2 900 в месяц, bid $17.46.
- **Резерв из Planner:**
  - «schnell kredit online» — 880, $22.89;
  - «kleinkredit online» — 260, $18.76;
  - «kleinkredit sofortauszahlung» — 260, $18.25;
  - «kreditkarte limit» — 1 000, $11.60;
  - «kreditkarte mit hohem limit» — 390, $9.65.
- **Отброшено:**
  - «без проверки»: «kredit ohne schufa» (49 500 — самый массовый, но запретная формулировка), «online kredit sofortzusage ohne bonität», «sofort kredit ohne prüfung», «kleinkredit trotz negativer schufa»;
  - обещание одобрения: «kredit mit sofortzusage»;
  - бренды: American Express (bid до $200, брендовый аукцион), Mastercard, Visa;
  - бренды Klarna и Twint из связки коллег (Google Pay Klarna, Klarna Kreditkarte online, Stripe Klarna Integration, Klarna für Shopify) — запрет владельца от 24.09.
- **Новых своих ключей с выплатой нет.** В keywords/all добавил 2 чужих DE-ключа, только с классом: «Ich Brauche Sofort Geld» и «Ich Brauche Jetzt Sofort Geld», оба high. Первый предлагаю в статью C.

## Чего не должно быть (статья, креатив, пост)

- **Бренды Klarna и Twint** — ни в тексте, ни в ключах, ни в крео. Банки и платёжные системы тоже не называем, логотипов нет.
- **Жёсткие запреты для крео:**
  - «Klicken Sie hier» и любое «нажмите здесь»; кнопка на картинке только «Mehr erfahren»;
  - обращение к месту: «in der Nähe», «in Ihrer Region», «in Ihrer Stadt»;
  - кнопка «Gehalt/Lohn ansehen»;
  - ролик не на немецком.
- **На креативе нельзя «kostenlos», «gratis», «ohne Ablehnung».** Эти слова живут только в статье, как ключ и разбор (решение главного).
- **Обещания одобрения и скорости как гарантии:** «garantiert», «genehmigt», «Zusage für jeden», «ohne Schufa», «ohne Prüfung». Ставок в процентах на крео нет. «5.000 €» на крео угла 3 оставлено как сравнение (решение главного). Если объявление отклонят, первой убираем сумму.
- **Ничего, что выглядит как продукт:** нарисованной формы заявки нет, «банкомата бренда» нет.
- **В тексте** нет ссылок, «laut / nach Angaben», названий законов, ведомств, бюро и сайтов, таблиц.

## Посты для РК (adPosts)

Первая строка поста — зацепка, без эмодзи. Кнопка объявления — «Mehr erfahren».
- **Угол 1 · пост 1**, 116 знаков:
  - «Kredit per App, ganz ohne Banktermin?
    Betrag wählen, Laufzeit wählen – doch eine Zahl im Vertrag liest fast niemand.»
  - Перевод: «Кредит через приложение, совсем без визита в банк? Выбрал сумму, выбрал срок — но одну цифру в договоре почти никто не читает.»
  - Зацепка: «одну цифру почти никто не читает».
- **Угол 1 · пост 2**, 116 знаков:
  - «Früher Wartemarke, heute zwei Regler auf dem Handy.
    Wie Minikredite per App funktionieren – und wo der Haken steckt.»
  - Перевод: «Раньше талончик в очереди, сегодня два ползунка в телефоне. Как работают мини-кредиты в приложении и в чём подвох.»
  - Зацепка: «в чём подвох мини-кредитов».
- **Угол 3 · пост 1**, 123 знака, с суммами (решение главного по крео распространил на пост):
  - «Gleiche Karte, gleiche Bank: Er bekommt 500 € Limit, sie 5.000 €.
    Wovon der Verfügungsrahmen wirklich abhängt – im Artikel.»
  - Перевод: «Та же карта, тот же банк: ему лимит 500 €, ей 5 000 €. От чего на самом деле зависит лимит — в статье.»
  - Зацепка: «одна карта — лимиты разные».
- **Угол 3 · пост 2**, 120 знаков, без сумм, это запасной вариант:
  - «„Zahlung abgelehnt“ – obwohl auf dem Konto genug Geld ist?
    Warum das Kartenlimit oft früher erreicht ist, als man denkt.»
  - Перевод: «„Платёж отклонён“ — хотя денег на счёте достаточно? Почему лимит карты часто заканчивается раньше, чем думаешь.»
  - Зацепка: «платёж отклонён, хотя деньги есть».

```json
{"adPosts": {
  "угол 1 · пост 1": {"text": "Kredit per App, ganz ohne Banktermin?\nBetrag wählen, Laufzeit wählen – doch eine Zahl im Vertrag liest fast niemand.", "ru": "Кредит через приложение, совсем без визита в банк?\nВыбрал сумму, выбрал срок — но одну цифру в договоре почти никто не читает.", "hook": "одну цифру почти никто не читает"},
  "угол 1 · пост 2": {"text": "Früher Wartemarke, heute zwei Regler auf dem Handy.\nWie Minikredite per App funktionieren – und wo der Haken steckt.", "ru": "Раньше талончик в очереди, сегодня два ползунка в телефоне.\nКак работают мини-кредиты в приложении — и в чём подвох.", "hook": "в чём подвох мини-кредитов"},
  "угол 3 · пост 1": {"text": "Gleiche Karte, gleiche Bank: Er bekommt 500 € Limit, sie 5.000 €.\nWovon der Verfügungsrahmen wirklich abhängt – im Artikel.", "ru": "Та же карта, тот же банк: ему лимит 500 €, ей 5 000 €.\nОт чего на самом деле зависит лимит — в статье.", "hook": "одна карта — лимиты разные"},
  "угол 3 · пост 2": {"text": "„Zahlung abgelehnt“ – obwohl auf dem Konto genug Geld ist?\nWarum das Kartenlimit oft früher erreicht ist, als man denkt.", "ru": "«Платёж отклонён» — хотя денег на счёте достаточно?\nПочему лимит карты часто заканчивается раньше, чем думаешь.", "hook": "платёж отклонён, хотя деньги есть"}
}}
```

## Источники для сверки (в текст статьи не идут)

Всё ниже написано по памяти, с первоисточником не сверял. Названия норм даны только здесь.
- **Мгновенные переводы в ЕС** (обязанность банков отправлять SEPA Instant с 09.10.2025) — Регламент (ЕС) 2024/886.
- **Новые правила потребкредита, применяются с 20.11.2026:** проверка кредитоспособности и для мелких сумм, и для многих BNPL и рассрочек — Директива (ЕС) 2023/2225 (CCD2). В тексте сказано «vorgesehen», потому что немецкий закон о переносе директивы я не сверял.
- **Проверка кредитоспособности** до потребкредита — § 505a BGB.
- **14 дней на отзыв** — §§ 495, 355 BGB. **Стандартный информационный лист** — Art. 247 EGBGB.
- **Эффективная ставка включает обязательные расходы; репрезентативный пример** (не меньше 2/3 клиентов получают эту ставку или лучше) — PAngV, § 6 и § 17.
- **Рассрочка и BNPL как кредитный договор** — § 506 BGB (Teilzahlungsgeschäft).
- **Отели и прокат авто блокируют сумму на карте** (Vorautorisierung), неоплаченные операции уменьшают свободный лимит — практика карточных систем.
- **Рассрочка по умолчанию у части «бесплатных» кредиток**, проценты на снятие наличных с первого дня — практика рынка DE, отмечалась в сравнениях карт.
- **Доплата за экспресс-выплату у поставщиков мини-кредитов** — практика рынка DE. Она необязательна, поэтому в эффективную ставку не входит.
