"""Волна 2 пакетов «Готово к заливу» 30.09: 10 пакетов 60+ (US / UK / CA, всё на EN), по 4 статики 1:1.
Шаблоны — общие p60_templates (a сетка, b опросник, c сравнение, d сцена) + свои иконки/сцены/«merge» из p60w2_art.
Цены на картинках — только диапазоны из гипотез (sourceNote / article), где цены нет — «?».
Запуск:
    python3 p60w2_packs.py            — все пакеты
    python3 p60w2_packs.py 3 5        — пакеты 3 и 5
    python3 p60w2_packs.py 3:a,c      — пакет 3, буквы a и c
Пишет <OUT>/<docId>/<a|b|c|d>.png и <OUT>/<docId>/creatives.json."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p60_lib import OUT
import p60_templates as T
import p60w2_art as A

WH = (255, 255, 255)
CONCEPT = {"a": "сетка выбора (fake interactivity)", "b": "карточка-опросник", "c": "сколько стоит / сравнение", "d": "сцена-иллюстрация"}
PACKS = {}

# ---------------------------------------------------------------- 1. US · уход на дому (home care)
TERRA, NAVY1, TEAL1 = (214, 98, 64), (36, 52, 84), (40, 120, 128)
PACKS[1] = dict(
    doc="P60-home-care-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(253, 246, 238), ink=NAVY1, sub=(96, 100, 110), acc=TERRA, btn=TERRA, tile=WH, tile_ink=NAVY1,
             icon=NAVY1, iconbg=(252, 228, 212)),
    a=dict(layout="list4", title="In-home care 2026: which kind of help?", sub="Pick a type to see what it covers", size=58,
           hero=A.hero_homecare, hero_h=290,
           tiles=[("person_heart", "Companion care"), ("care_hands", "Personal care"), ("med_bag", "Home health care"),
                  ("coins", "Who pays for it?")],
           note="панель «дом с сердцем + часы + календарь», 4 строки-кнопки по видам ухода из статьи"),
    b=dict(layout="phone", title="Home care quiz:", title2="the Medicare question", sub="4 questions families ask before hiring help",
           size=56, tag="HOME CARE QUIZ", step="Question 1 of 4", prog=0.25,
           q="Does Medicare pay for ongoing companion care at home?",
           opts=["Yes, in full", "Limited home health", "Only after age 80", "Not sure"],
           pal=dict(bg=(32, 48, 80), bg2=(18, 28, 52), ink=WH, sub=(206, 214, 230), acc=(236, 128, 84), btn=TERRA),
           note="тёмно-синий фон, телефон с тестом; вопрос о правилах Medicare, не о зрителе (ответ в статье: только ограниченный home health)"),
    c=dict(layout="twocol", title="Agency caregiver or independent caregiver?", sub="Companion care: about $28–$42 an hour (US guide, 2026)",
           size=52, cols=[("AGENCY", "briefcase", TEAL1), ("INDEPENDENT", "person", TERRA)],
           rows=[("PRICE", "often higher", "can cost less"), ("SCREENING & SCHEDULING", "handled by the agency", "falls on the family"),
                 ("BACKUP IF SICK", "agency arranges cover", "family arranges cover")],
           foot="What families wish they'd checked first",
           note="агентство против частной сиделки; цена $28–42/час — из sourceNote гипотезы (aplaceformom, seniorliving.org)"),
    d=dict(style="card", scene="w2_home_visit", card_box=(80, 36, 1000, 492), kicker="IN-HOME CARE 2026",
           title="What an hour of home care really costs", sub="Companion care vs personal care – and who pays", size=62,
           pal=dict(frame=TEAL1, ink=NAVY1, sub=(96, 100, 110), acc=TERRA, btn=TERRA),
           note="гостиная: сиделка подаёт чай пожилой женщине в кресле (люди без лиц), часы на стене; карточка в рамке"),
)

# ---------------------------------------------------------------- 2. US · доставка готовой еды
GREEN2, TOM, INK2, BLUE2 = (56, 132, 72), (222, 84, 50), (36, 52, 40), (52, 110, 180)
PACKS[2] = dict(
    doc="P60-meal-delivery-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(248, 245, 236), ink=INK2, sub=(90, 96, 88), acc=GREEN2, btn=TOM, tile=WH, tile_ink=INK2,
             icon=GREEN2, iconbg=(226, 240, 222), tile_line=(224, 230, 218)),
    a=dict(layout="row4", title="Senior meal delivery 2026: pick a menu", sub=None, size=58, hero=A.hero_meal, hero_h=360,
           tiles=[("salt", "Low-sodium"), ("drop_check", "Diabetic-\nfriendly"), ("heart_plain", "Heart-healthy"), ("soup_bowl", "Soft-food")],
           note="поднос с обедом сверху, 4 плитки-диеты из статьи (low-sodium / diabetic-friendly / heart-healthy / soft-food)"),
    b=dict(layout="card2x2", title="What does senior meal delivery cost?", title2="Take a guess", sub="2026 guide", size=56,
           tag="PRICE QUIZ", step="Question 1 of 3", prog=0.33,
           q="One delivered senior meal in 2026 usually costs about…",
           opts=["Under $3", "$7–$12", "Over $25", "Not sure"],
           pal=dict(bg=(46, 110, 60), bg2=(24, 64, 36), ink=WH, sub=(214, 234, 214), acc=GREEN2, t2=(255, 214, 102), deco=True),
           note="ценовой квиз; верный ответ $7–12 за порцию — ориентир 2026 из гипотезы и статьи, остальное — варианты-отвлекалки"),
    c=dict(layout="split", title="Fresh or frozen meal delivery?", sub="Senior meals: about $7–$12 each (US guide, 2026)", size=54,
           cols=[("FRESH", "meal_plate", GREEN2, ["Delivered on a schedule", "Just reheat and eat", "Shorter shelf life"]),
                 ("FROZEN", "snowflake", BLUE2, ["Longer shelf life", "Eat when it suits", "A little less fresh"])],
           pal=dict(bg=(248, 245, 236)), note="две половины: свежие против замороженных (свойства из статьи), $7–12 за порцию — из гипотезы"),
    d=dict(style="top", scene="w2_doorstep_meals", kicker="MEAL DELIVERY FOR SENIORS 2026",
           title="Ready-made meals at the door: what one really costs", sub="Fresh or frozen, special diets, Meals on Wheels",
           size=58, sticker="$7–$12 a meal", sticker_xy=(905, 470, 100), btn_y=1000,
           pal=dict(ink=INK2, sub=(80, 88, 80), acc=TOM, sticker=(255, 208, 60)),
           note="крыльцо: дверь, термосумка и контейнеры на скамейке, жёлтый стикер с ценой порции (ориентир 2026)"),
)

# ---------------------------------------------------------------- 3. US · завещание и доверенность
BURG, NAVY3, INK3 = (128, 32, 48), (30, 44, 90), (36, 32, 52)
PACKS[3] = dict(
    doc="P60-will-estate-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(247, 242, 234), ink=INK3, sub=(96, 90, 100), acc=BURG, btn=NAVY3, tile=WH, tile_ink=INK3,
             icon=NAVY3, iconbg=(234, 230, 242)),
    a=dict(layout="2x2", title="Estate planning 2026: where to start?", sub="Pick a document to see what it does",
           tiles=[("doc_sign", "Last will"), ("doc_coin", "Financial power of attorney"), ("doc_heart", "Healthcare proxy"),
                  ("scales", "Attorney or online service?")],
           note="2×2 документов из статьи на кремовом; у каждой «Learn more»"),
    b=dict(layout="card", title="Without a will, who decides?", size=60, tag="WILL QUIZ", step="Question 1 of 4", prog=0.25,
           q="If there's no valid will, what usually decides who inherits?",
           opts=["The eldest child", "State law", "The bank", "Not sure"],
           pal=dict(bg=NAVY3, bg2=(18, 26, 56), ink=WH, sub=(210, 214, 230), acc=BURG, btn=BURG, deco=True),
           note="тёмно-синий фон, вопрос о правилах (ответ в статье: закон штата)"),
    c=dict(layout="stacked", title="Will or power of attorney?", sub="Two documents, two very different jobs", size=56,
           cols=[("LAST WILL", "doc_sign", BURG, WH, INK3, ["takes effect after death", "names an executor", "can name a guardian for children"]),
                 ("POWER OF ATTORNEY", "doc_coin", NAVY3, NAVY3, WH, ["works during a lifetime", "names an agent to act", "financial or healthcare"])],
           foot="The difference many families learn too late", pal=dict(acc=BURG, hl=(255, 220, 120)),
           note="две карточки друг над другом: завещание / доверенность"),
    d=dict(style="card", scene="w2_will_desk", card_box=(90, 60, 990, 500), kicker="WILLS & POWER OF ATTORNEY 2026",
           title="The 2 documents many families put off for years", sub="What a will and a POA actually do", size=60,
           pal=dict(frame=BURG, ink=INK3, sub=(96, 90, 100), acc=BURG, btn=NAVY3),
           note="стол сверху: лист LAST WILL AND TESTAMENT с подписью, перьевая ручка, очки, ключи, конверт; карточка в рамке"),
)

# ---------------------------------------------------------------- 4. US · слуховые аппараты (здоровье)
BLUE4, NAVY4, AMB4 = (30, 110, 180), (20, 40, 70), (232, 120, 40)
PACKS[4] = dict(
    doc="P60-hearing-aids-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(238, 245, 250), ink=NAVY4, sub=(80, 96, 116), acc=BLUE4, btn=AMB4, tile=WH, tile_ink=NAVY4,
             icon=BLUE4, iconbg=(222, 236, 248), hl=(255, 220, 110)),
    a=dict(layout="row2", title="Hearing aids 2026: OTC or prescription?", sub="Price per pair – 2026 guide", size=58,
           hero=A.hero_hearing, hero_h=360, tiles=[("otc_box", "OTC"), ("bte_aid", "Prescription")],
           foot="Does Medicare pay? The 2026 answer",
           note="сетка из 2 вариантов; ценники $200–3,000 и $2,000–7,000+ за пару — из sourceNote (HearingTracker 2026)"),
    b=dict(layout="card2x2", title="Does Medicare cover hearing aids?", sub="A quick 2026 check", size=58,
           tag="QUICK CHECK", step="Question 1 of 3", prog=0.33,
           q="Does Original Medicare pay for routine hearing aids?",
           opts=["Yes, in full", "Half the cost", "Generally no", "Not sure"],
           pal=dict(bg=(24, 70, 130), bg2=(12, 36, 76), ink=WH, sub=(206, 222, 240), acc=BLUE4, deco=True),
           note="вопрос о покрытии Medicare, не о слухе зрителя (ответ в статье: как правило, нет)"),
    c=dict(layout="table", title="OTC vs prescription hearing aids", sub="Price per pair – 2026 guide", size=54,
           cols=[("OTC", "otc_box", (90, 100, 116)), ("Prescription", "bte_aid", BLUE4)],
           rows=[("Price per pair", "$200–$3,000", "$2,000–$7,000+"), ("Prescription", "not needed", "needed"),
                 ("Fitting", "no professional fitting", "fitted by an audiologist"),
                 ("Designed for", "mild to moderate hearing loss", "more significant hearing loss")],
           foot="Plus: what Medicare does and doesn't pay", pal=dict(acc=AMB4),
           note="таблица OTC / по рецепту; все строки из статьи гипотезы"),
    d=dict(style="bars", scene="w2_hearing_table", y=56,
           bars=[("HEARING AIDS 2026:", WH, BLUE4), ("WHY ONE PAIR COSTS $200", NAVY4, None), ("AND ANOTHER $7,000+?", NAVY4, None)],
           bar_size=80, cond=0.8, btn_y=440, btn_size=48, pal=dict(btn=AMB4),
           note="плашки (формула рабочих крео владельца) + стол: коробка OTC с ценником $200 и футляр клиники с ценником $7,000+"),
)

# ---------------------------------------------------------------- 5. US · тревожная кнопка (здоровье)
NAVY5, TEAL5, RED5, AMB5 = (22, 36, 60), (0, 128, 110), (214, 48, 48), (236, 160, 40)
PACKS[5] = dict(
    doc="P60-medical-alert-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(240, 246, 244), ink=NAVY5, sub=(80, 96, 100), acc=TEAL5, btn=RED5, tile=WH, tile_ink=NAVY5,
             icon=NAVY5, iconbg=(222, 240, 236), tile_line=(214, 226, 222)),
    a=dict(layout="row4", title="Medical alert systems 2026: pick a type", sub=None, size=58, hero=A.hero_alert, hero_h=390,
           tiles=[("pendant", "Pendant"), ("wristband", "Wristband"), ("base_station", "Home base"), ("gps_phone", "Mobile GPS")],
           note="тёмная панель с большой красной кнопкой и чипами «24/7» / «1 button», 4 плитки-типа устройства из статьи"),
    b=dict(layout="calc", title="Medical alert cost check 2026", sub="3 choices that change the monthly price", size=58,
           steps=[("Device", "done"), ("Fall detection", "now"), ("Contract", "todo")],
           tag="STEP 2 OF 3", step="", prog=0.66, q="Add automatic fall detection?",
           opts=["Yes", "No", "What does it do?", "What does it cost?"],
           pal=dict(bg=(236, 244, 242), bg2=(214, 230, 226), ink=NAVY5, sub=(80, 96, 100), acc=TEAL5, btn=RED5),
           note="форма-калькулятор со степпером; цены на карточке нет (главный 29.09: только $20–60/мес с пометкой «2026 guide»)"),
    c=dict(layout="bars", title="What does a medical alert system cost?", sub="Typical monthly prices – 2026 US guide", size=54,
           bill="MONTHLY BILL", bill_r="2026",
           bars=[("Monitoring plan", 0.8, "$20–$60", NAVY5), ("Fall detection add-on", None, "extra per month", TEAL5),
                 ("Equipment or activation fee", None, "$0 or a one-time fee", AMB5)],
           foot="Many plans are month-to-month", pal=dict(acc=NAVY5),
           note="«счёт за месяц»: $20–60 абонплата (ориентир 2026 из гипотезы); fall detection и сбор за устройство — «?»"),
    d=dict(style="left", scene="w2_nightstand_alert", y=60, x=70,
           bars=[("MEDICAL ALERT", WH, RED5), ("SYSTEMS 2026:", WH, RED5), ("WHAT DOES 24/7", NAVY5, None), ("MONITORING COST?", NAVY5, None)],
           bar_size=96, cond=0.8, btn_y=575, btn_size=44, max_w=640, pal=dict(btn=TEAL5),
           note="плашки слева + спальня: тумбочка с базовой станцией и кулоном, лампа, край кровати; без людей"),
)

# ---------------------------------------------------------------- 6. UK · катаракта и очки
IND, INK6, AMB6, YEL6 = (70, 56, 170), (36, 30, 80), (226, 118, 20), (255, 214, 90)
PACKS[6] = dict(
    doc="P60-senior-glasses-uk-2026-09-30", cta="Learn more",
    pal=dict(bg=(245, 243, 251), ink=INK6, sub=(96, 92, 120), acc=IND, btn=AMB6, tile=WH, tile_ink=INK6,
             icon=IND, iconbg=(232, 228, 250)),
    a=dict(layout="2x2", title="Cataract surgery 2026: NHS or private?", sub="Pick a topic:",
           tiles=[("eye", "What the NHS includes"), ("pound_tag", "Private cost per eye"), ("lens", "Toric lens supplement"),
                  ("glasses_icon", "Glasses after surgery")],
           note="2×2 тем из статьи на лавандовом"),
    b=dict(layout="card", title="After cataract surgery:", title2="the glasses question", size=58,
           tag="QUICK CHECK", step="Question 1 of 3", prog=0.33,
           q="After NHS surgery with a standard lens, do most people still need reading glasses?",
           opts=["Yes, for close-up", "No, never again", "Only for driving", "Not sure"],
           pal=dict(bg=(60, 46, 150), bg2=(30, 22, 90), ink=WH, sub=(220, 216, 246), acc=IND, t2=INK6, hl=YEL6, deco=True),
           note="вопрос про линзу и очки, не про зрение зрителя (ответ в статье: да, для чтения)"),
    c=dict(layout="split", title="NHS or private cataract surgery?", sub="2026 guide figures, side by side", size=54, diag=30,
           cols=[("NHS", "eye", IND, ["No direct cost if eligible", "About 12–18 weeks' wait", "Standard monofocal lens"]),
                 ("PRIVATE", "pound_tag", (40, 36, 60), ["£2,500–£5,500 per eye", "Premium lens options", "Toric: +£300–£500 per eye"])],
           pal=dict(bg=(248, 246, 252), ink=INK6, btn=AMB6, vs_bg=AMB6, vs_ink=WH),
           note="диагональный сплит NHS / частно; цифры — из sourceNote (SpaMedica, Optegra, TreatCompare 2026); без «до/после»"),
    d=dict(style="top", scene="w2_optician_wall", kicker="CATARACT SURGERY 2026",
           title="No cost on the NHS – so why budget for new glasses?", sub="What's included, what isn't, and the private price per eye",
           size=56, btn_y=1000, pal=dict(ink=INK6, sub=(90, 86, 116), acc=IND),
           note="оптика: таблица для проверки зрения, полки с оправами, раскрытая книга с очками"),
)

# ---------------------------------------------------------------- 7. UK · боль в суставах (здоровье)
GREEN7, INK7, ORG7 = (46, 130, 80), (30, 56, 40), (228, 108, 36)
PACKS[7] = dict(
    doc="P60-joint-pain-uk-2026-09-30", cta="Learn more",
    pal=dict(bg=(242, 247, 240), ink=INK7, sub=(86, 100, 90), acc=GREEN7, btn=ORG7, tile=WH, tile_ink=INK7,
             icon=GREEN7, iconbg=(224, 240, 226)),
    a=dict(layout="list4", title="Knee pain after 60: the options explained", sub="Pick one to see how it works (2026 guide)", size=58,
           hero=A.hero_park, hero_h=290,
           tiles=[("stretch", "Physiotherapy"), ("syringe", "Steroid injections"), ("hot_pack", "Heat, cold & TENS"),
                  ("pound_tag", "Private knee replacement cost")],
           note="парк со скамейкой и кроссовками, 4 строки-варианта под статью «Knee Pain Relief After 60…» (без обещаний результата; цены на картинке нет)"),
    b=dict(layout="phone", title="Steroid joint injections:", title2="how long does relief last?", sub="A 3-question check", size=54,
           tag="JOINT QUIZ", step="Question 1 of 3", prog=0.33,
           q="How long does relief from a steroid joint injection usually last?",
           opts=["A few days", "Weeks to 2 months", "Several years", "Not sure"],
           pal=dict(bg=(36, 96, 64), bg2=(20, 60, 40), ink=WH, sub=(214, 234, 220), acc=(232, 132, 50), btn=ORG7),
           note="вопрос о методе лечения, не о состоянии зрителя (ответ в статье: от нескольких недель до пары месяцев)"),
    c=dict(layout="stacked", title="Steroid injection or physiotherapy?", sub="Two NHS options that do very different jobs", size=52,
           cols=[("STEROID INJECTION", "syringe", ORG7, WH, INK7,
                  ["can reduce inflammation fairly quickly", "relief: weeks to a couple of months", "used alongside other approaches"]),
                 ("PHYSIOTHERAPY", "stretch", GREEN7, GREEN7, WH,
                  ["a tailored exercise plan", "builds supporting muscle strength", "a long-term approach"])],
           foot="Why a GP check usually comes first", pal=dict(acc=ORG7, hl=(255, 222, 120)),
           note="две карточки: инъекция / физиотерапия (формулировки статьи, без «вылечит»)"),
    d=dict(style="card", scene="w2_park_walk", card_box=(90, 60, 990, 500), kicker="KNEE & JOINT PAIN · 2026 GUIDE",
           title="The NHS options many people never ask about", sub="Physio, injections, TENS – what each one does", size=60,
           pal=dict(frame=GREEN7, ink=INK7, sub=(86, 100, 90), acc=GREEN7, btn=ORG7),
           note="парк: пожилая пара гуляет по тропинке (без лиц), скамейка; карточка в рамке; без «до/после»"),
)

# ---------------------------------------------------------------- 8. UK · автостраховка 60+
BLUE8, INK8, GREEN8, RED8 = (20, 90, 180), (16, 32, 64), (0, 136, 96), (214, 48, 40)
PACKS[8] = dict(
    doc="P60-car-insurance-uk-2026-09-30", cta="Learn more",
    pal=dict(bg=(242, 245, 250), ink=INK8, sub=(80, 92, 110), acc=BLUE8, btn=GREEN8, tile=WH, tile_ink=INK8,
             icon=BLUE8, iconbg=(226, 234, 248)),
    a=dict(layout="2x2", title="Car insurance over 60: 4 things that can change a quote", sub="Pick one to see how it works (2026)", size=56,
           tiles=[("odometer", "Lower annual mileage"), ("black_box", "Black box policy"), ("compare_docs", "Compare, don't auto-renew"),
                  ("steering", "Advanced driving course")],
           note="2×2 способов из статьи (пробег, телематика, сравнение вместо автопродления, курс вождения)"),
    b=dict(layout="card2x2", title="After 70, does car insurance", title2="get cheaper or dearer?", size=56,
           tag="DRIVER QUIZ", step="Question 1 of 4", prog=0.25,
           q="What happens to car insurance prices after 70?",
           opts=["Always cheaper", "Always dearer", "Depends on the insurer", "Not sure"],
           pal=dict(bg=(20, 50, 110), bg2=(10, 26, 64), ink=WH, sub=(206, 216, 240), acc=BLUE8, t2=(255, 210, 80), deco=True),
           note="вопрос о рынке, не о зрителе (ответ в статье: зависит от страховщика)"),
    c=dict(layout="twocol", title="Specialist or mainstream insurer?", sub="Car insurance for over-60s: which is cheaper?", size=54,
           cols=[("SPECIALIST", "car_shield", BLUE8), ("MAINSTREAM", "car", (96, 104, 120))],
           rows=[("MADE FOR", "older drivers", "all drivers"), ("EXTRAS", "low-mileage, agreed value", "standard cover"), ("PRICE", "?", "?")],
           foot="It's rarely the one people assume",
           note="специализированный против обычного страховщика; цен в гипотезе нет — «?»"),
    d=dict(style="bars", scene="w2_driveway", y=56,
           bars=[("CAR INSURANCE OVER 60:", WH, RED8), ("THE RENEWAL MISTAKE", INK8, None), ("THAT COSTS MONEY", INK8, None)],
           bar_size=82, cond=0.8, btn_y=420, btn_size=48, pal=dict(btn=GREEN8),
           note="плашки + дом с гаражом, машина на дорожке, письмо RENEWAL; хук совпадает с заголовком статьи (ошибка при продлении — автопродление без сравнения)"),
)

# ---------------------------------------------------------------- 9. UK · скидки 60+
PURP, INK9, ORG9, GRN9 = (120, 60, 160), (46, 30, 70), (234, 100, 26), (40, 150, 110)
PACKS[9] = dict(
    doc="P60-senior-discounts-uk-2026-09-30", cta="Learn more",
    pal=dict(bg=(255, 247, 236), ink=INK9, sub=(100, 90, 110), acc=PURP, btn=ORG9, tile=WH, tile_ink=INK9,
             icon=PURP, iconbg=(240, 230, 248), tile_line=(236, 226, 240)),
    a=dict(layout="row4", title="Over-60s discounts 2026: pick a category", sub=None, size=58, hero=A.hero_badge60, hero_h=330,
           tiles=[("bus", "Bus travel"), ("train", "Rail fares"), ("pill_bottle", "Prescriptions"), ("ticket", "Days out")],
           note="бейдж «60+» с ценниками %, 4 плитки-категории из статьи (транспорт, ж/д, рецепты, досуг)"),
    b=dict(layout="card", title="Free prescriptions in England:", title2="from what age?", size=58,
           tag="QUICK CHECK", step="Question 1 of 4", prog=0.25,
           q="At what age do NHS prescriptions become free in England?",
           opts=["55", "60", "At State Pension age", "70"],
           pal=dict(bg=PURP, bg2=(70, 30, 100), ink=WH, sub=(230, 216, 240), acc=PURP, t2=INK9, hl=(255, 214, 90), deco=True, btn=ORG9),
           note="квиз о правилах (ответ в статье: с 60 в Англии; автобус — с пенсионного возраста)"),
    c=dict(layout="table", title="Full price or over-60s price?", sub="Where concessions can apply in 2026", size=56,
           cols=[("Full price", "coins", (110, 100, 120)), ("Concession", "percent_tag", GRN9)],
           rows=[("Bus", "pay each fare", "free or cheaper from State Pension age"), ("Rail", "full fare", "Senior Railcard discount"),
                 ("Prescriptions", "standard charge", "free from 60 in England"), ("Cinemas, museums", "full price", "senior rate – ask")],
           foot="Savings many people never claim", pal=dict(acc=ORG9, hl=(255, 214, 90)),
           note="таблица полная цена / льгота; сумм нет (в гипотезе их нет), только правила из статьи"),
    d=dict(style="top", scene="w2_wallet_table", kicker="SENIOR DISCOUNTS UK 2026",
           title="Bus pass over 60: the new rules for 2026", sub="…and 6 other discounts many people miss",
           size=60, btn_y=1000, pal=dict(ink=INK9, sub=(100, 90, 110), acc=PURP),
           note="стол сверху: кошелёк, проездные с пиктограммами (без логотипов), пакет из аптеки, чек %, корзина, билет"),
)

# ---------------------------------------------------------------- 10. CA · консолидация долгов (кредиты)
TEAL10, INK10, COR10 = (0, 116, 128), (18, 40, 56), (226, 84, 64)
PACKS[10] = dict(
    doc="P60-debt-consolidation-ca-2026-09-30", cta="Learn more",
    pal=dict(bg=(240, 246, 247), ink=INK10, sub=(80, 96, 104), acc=TEAL10, btn=COR10, tile=WH, tile_ink=INK10,
             icon=TEAL10, iconbg=(220, 238, 240), dot=COR10),
    a=dict(layout="2x2", title="Debt consolidation in Canada 2026: 4 routes", sub="Pick one to see how it works", size=56,
           tiles=[("merge_arrows", "Consolidation loan"), ("card_transfer", "Balance transfer"), ("chat", "Credit counselling plan"),
                  ("scales", "Consumer proposal")],
           note="2×2 четырёх путей из статьи; без сумм, ставок и логотипов банков"),
    b=dict(layout="phone", title="Debt consolidation:", title2="what does it actually do?", sub="3 quick questions", size=54,
           tag="QUIZ", step="Question 1 of 3", prog=0.33, q="What does debt consolidation do?",
           opts=["Erases the debt", "One payment, not 4", "Stops all interest", "Not sure"],
           pal=dict(bg=(18, 60, 76), bg2=(10, 34, 46), ink=WH, sub=(200, 222, 228), acc=(236, 132, 60), btn=COR10),
           note="квиз о механике (не «Are you in debt?», не о финансах зрителя)"),
    c=dict(layout="merge", title="Several payments or one?", sub="How debt consolidation works in Canada (2026)", size=58,
           items=[("card", "Credit card"), ("card", "Store card"), ("doc", "Line of credit"), ("car", "Car loan")],
           right_head="ONE PAYMENT", right_rows=["One due date", "Interest rate: ?", "Compare the total cost"],
           foot="Loan, balance transfer or credit counselling?", pal=dict(hl=(255, 220, 120)),
           note="4 долга стрелками сходятся в один платёж; ставка — «?», без цифр"),
    d=dict(style="bars", scene="w2_bills_table", y=56,
           bars=[("DEBT CONSOLIDATION", WH, COR10), ("CANADA 2026:", WH, COR10), ("WHAT BANKS DON'T", INK10, None), ("TELL RETIREES?", INK10, None)],
           bar_size=84, cond=0.8, btn_y=540, btn_size=48, pal=dict(btn=TEAL10),
           note="формула рабочих кредитных крео владельца (плашки + «что банки не говорят»); стол: выписки, карты без логотипов, стрелки в один конверт"),
)


# ---------------------------------------------------------------- сборка
def _clean(s):
    return s.replace("-\n", "-").replace("\n", " ").replace("­", "")


def texts(t, cta):
    """Весь текст на картинке — для creatives.json."""
    out = []
    for k in ("kicker", "title", "title2", "sub"):
        if t.get(k):
            out.append(t[k])
    if t.get("bars") and len(t["bars"][0]) == 3:
        out.append(" ".join(b[0] for b in t["bars"]))
    for k in ("tag", "step", "q"):
        if t.get(k):
            out.append(t[k])
    if t.get("steps"):
        out.append(" · ".join(s[0] for s in t["steps"]))
    if t.get("opts"):
        out.append(" / ".join(t["opts"]))
    if t.get("tiles"):
        out.append(" / ".join(x[1] for x in t["tiles"]) + f" (у каждой «{cta}»)")
    if t.get("cols"):
        out.append(" vs ".join(x[0] for x in t["cols"]))
        for x in t["cols"]:
            if isinstance(x[-1], list):
                out.append(x[0] + ": " + " · ".join(x[-1]))
    if t.get("rows"):
        out.append(" · ".join(f"{r[0]}: {r[1]} / {r[2]}" for r in t["rows"]))
    if t.get("items"):
        out.append(" + ".join(x[1] for x in t["items"]) + " → " + t["right_head"] + ": " + " · ".join(t["right_rows"]))
    if t.get("bill"):
        out.append(t["bill"] + " " + t.get("bill_r", ""))
    if isinstance(t.get("bars"), list) and t.get("bars") and len(t["bars"][0]) == 4:
        out.append(" · ".join(f"{b[0]} {b[2]}" for b in t["bars"]))
    for k in ("hero_text", "sticker", "foot"):
        if t.get(k):
            out.append(t[k])
    return _clean(" / ".join(out))


HERO_TEXT = {"hero_hearing": "$200–$3,000 · $2,000–$7,000+", "hero_alert": "24/7 · 1 button", "hero_badge60": "60+"}


def build(n, letters="abcd"):
    P = PACKS[n]
    doc = P["doc"]
    items = []
    for L in "abcd":
        t = dict(P[L])
        if t.get("hero") and t["hero"].__name__ in HERO_TEXT:
            t["hero_text"] = HERO_TEXT[t["hero"].__name__]
        PP = dict(P, pal={**P["pal"], **t.get("pal", {})})
        if L in letters:
            if t.get("layout") == "merge":
                c = A.merge(PP, t)
            else:
                fn = {"a": T.grid, "b": T.quiz, "c": T.compare, "d": T.scene}[L]
                c = fn(PP, t)
            c.save(f"{doc}/{L}.png")
        items.append(dict(letter=L, file=f"cr/packs/{doc}/{L}.png", concept=CONCEPT[L] + " — " + t.get("note", ""),
                          text=texts(t, P["cta"]), cta=P["cta"]))
    with open(os.path.join(OUT, doc, "creatives.json"), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    args = sys.argv[1:] or [str(k) for k in PACKS]
    for a in args:
        if ":" in a:
            n, ls = a.split(":")
            build(int(n), ls.replace(",", ""))
        else:
            build(int(a))
