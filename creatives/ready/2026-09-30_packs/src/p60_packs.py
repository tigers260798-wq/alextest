"""Тексты и палитры 8 пакетов «Готово к заливу» 30.09 + сборка. Запуск:
    python3 p60_packs.py            — все пакеты, все буквы
    python3 p60_packs.py 3 5        — пакеты 3 и 5
    python3 p60_packs.py 3:a,c      — пакет 3, буквы a и c
Пишет <OUT>/<docId>/<a|b|c|d>.png и <OUT>/<docId>/creatives.json."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p60_lib import OUT, mix
import p60_templates as T
import p60_scenes as S

WH = (255, 255, 255)
CONCEPT = {"a": "сетка выбора (fake interactivity)", "b": "карточка-опросник", "c": "сколько стоит / сравнение", "d": "сцена-иллюстрация"}

PACKS = {}

# ---------------------------------------------------------------- 1. UK · Attendance Allowance
TEAL, CORAL, PURPLE = (18, 104, 112), (226, 84, 56), (104, 70, 150)
PACKS[1] = dict(
    doc="P60-attendance-allowance-uk-2026-09-30", cta="Learn more",
    pal=dict(bg=(250, 245, 236), ink=(24, 44, 52), sub=(84, 96, 102), acc=TEAL, btn=CORAL, tile=WH, tile_ink=(30, 40, 48),
             icon=TEAL, iconbg=(222, 240, 238)),
    a=dict(layout="2x2", title="Attendance Allowance 2026", sub="Not means-tested. Paid weekly. Pick a topic:",
           tiles=[("person_check", "Who can get it"), ("calendar", "The 2 weekly rates"),
                  ("key_plus", "Other benefits it can unlock"), ("laptop", "How to apply")],
           note="2×2 плитки с иконками на кремовом, у каждой «Learn more»"),
    b=dict(layout="card", title="The Attendance Allowance question", title2="many get wrong",
           tag="QUICK CHECK", step="Question 1 of 4", prog=0.25,
           q="Do savings or income affect Attendance Allowance?",
           opts=["Yes, both count", "Only savings count", "No, neither counts", "Not sure"],
           pal=dict(bg=(20, 110, 118), bg2=(10, 58, 70), ink=WH, sub=(210, 236, 236), acc=TEAL, deco=True, hl=(255, 214, 102)),
           note="вопрос о правилах пособия, не о зрителе; бирюзовый фон"),
    c=dict(layout="twocol", title="Attendance Allowance vs Pension Credit", sub="Two different benefits – and a link many miss",
           cols=[("ATTENDANCE ALLOWANCE", "heart_hands", TEAL), ("PENSION CREDIT", "coins", PURPLE)],
           rows=[("BASED ON", "care needs", "income"), ("MEANS-TESTED", "no", "yes"), ("PAID", "weekly, 2 rates", "weekly top-up")],
           foot="Can one raise the other?", size=52),
    d=dict(style="top", scene="living", kicker="ATTENDANCE ALLOWANCE 2026", title="The weekly benefit that ignores savings",
           sub="Who can get it – and what else it can unlock", size=66, btn_y=1000,
           note="гостиная: кресло, плед, чай и письмо на столике, окно; людей нет"),
)

# ---------------------------------------------------------------- 2. UK · Council Tax Reduction
GREEN, NAVY2, YEL = (22, 110, 72), (22, 40, 70), (240, 190, 40)
PACKS[2] = dict(
    doc="P60-council-tax-reduction-uk-2026-09-30", cta="Learn more",
    pal=dict(bg=(240, 247, 242), ink=NAVY2, sub=(80, 92, 104), acc=GREEN, btn=GREEN, tile=WH, tile_ink=NAVY2,
             icon=GREEN, iconbg=(220, 238, 226)),
    a=dict(layout="list4", title="Council Tax 2026: 4 ways to pay less", sub="Pick one to see who qualifies",
           hero=S.hero_cc_house, hero_h=290, size=58,
           tiles=[("person", "Single person discount"), ("clock", "Pension-age reduction"),
                  ("house_ramp", "Disability band reduction"), ("people2", "Second adult rebate")],
           note="дом с ярлыками % сверху, 4 строки-кнопки"),
    b=dict(layout="phone", title="Council Tax quiz 2026", sub="4 questions that can change the bill",
           tag="QUIZ", step="Question 2 of 4", prog=0.5,
           q="Is Council Tax Reduction the same in every council?",
           opts=["Yes, one national rule", "No, it varies", "Only for pensioners", "Not sure"],
           pal=dict(bg=(226, 240, 230), bg2=(200, 226, 210)), note="телефон с тестом справа"),
    c=dict(layout="bars", title="How much lower can a Council Tax bill be?", sub="Same home, same band – three different bills",
           bill="COUNCIL TAX BILL", bill_r="2026/27", size=54,
           bars=[("Full bill", 1.0, "100%", NAVY2), ("Single person discount (−25%)", 0.75, "75%", GREEN),
                 ("Council Tax Reduction", None, "depends on income", (200, 140, 20))],
           foot="Pension-age rules explained step by step"),
    d=dict(style="top", scene="street", title="Council Tax 2026: the reductions pensioners often miss",
           sub="Single person discount, pension-age reduction and more", size=60, btn_y=990,
           pal=dict(ink=NAVY2, sub=(50, 64, 80)), note="улица таунхаусов, ярлык % у двери, письмо в щели"),
)

# ---------------------------------------------------------------- 3. UK · bathroom grant
AQUA, NAVY3, CORAL3 = (0, 136, 156), (20, 50, 90), (238, 96, 64)
PACKS[3] = dict(
    doc="P60-bathroom-grant-uk-2026-09-30", cta="Learn more",
    pal=dict(bg=(236, 246, 249), ink=NAVY3, sub=(80, 96, 110), acc=AQUA, btn=CORAL3, tile=WH, tile_ink=NAVY3,
             icon=AQUA, iconbg=(220, 240, 244)),
    a=dict(layout="row4", title="Bathroom grants 2026: what can they cover?", sub=None, size=58,
           hero=S.hero_bath_crop, hero_h=400,
           tiles=[("shower", "Walk-in shower"), ("bath", "Walk-in bath"), ("rail", "Grab rails"), ("floor_tiles", "Non-slip floor")],
           note="кадр душевой сверху, 4 плитки-варианта"),
    b=dict(layout="card2x2", title="Walk-in shower grants:", title2="4 questions before any quote",
           tag="GRANT CHECK", step="Question 1 of 4", prog=0.25,
           q="Who usually decides if a bathroom adaptation qualifies?",
           opts=["The fitter", "An occupational therapist", "The GP", "Not sure"],
           pal=dict(bg=(0, 120, 140), bg2=(10, 70, 100), ink=WH, sub=(210, 236, 240), acc=AQUA, t2=(255, 214, 102), deco=True),
           note="ответы 2×2 с буквами A–D"),
    c=dict(layout="split", title="Walk-in shower or walk-in bath?", sub="What changes day to day – and what a grant may cover", size=56,
           cols=[("WALK-IN SHOWER", "shower", AQUA, ["Level or low-step entry", "Fold-down seat", "No waiting to fill"]),
                 ("WALK-IN BATH", "bath", (60, 90, 150), ["Door in the side", "Built-in seat", "Fill and drain while seated"])],
           pal=dict(bg=WH), note="две половины: душ против ванны (не «до/после»)"),
    d=dict(style="card", scene="bathroom", kicker="WALK-IN SHOWER GRANTS FOR PENSIONERS", title="The bathroom grant few people ask about",
           sub="What it can cover in 2026 – and who decides", card_box=(90, 70, 990, 560), size=64,
           pal=dict(frame=(0, 136, 156), ink=NAVY3), note="ванная с душем без поддона, поручнем и сиденьем; карточка в рамке"),
)

# ---------------------------------------------------------------- 4. UK · кредитки 60+ (кредиты)
NAVY4, GOLD4, RED4, BLUE4 = (18, 32, 72), (226, 176, 60), (204, 32, 40), (28, 88, 196)
PACKS[4] = dict(
    doc="P60-credit-card-seniors-uk-2026-09-30", cta="Learn more",
    pal=dict(bg=(244, 245, 250), ink=NAVY4, sub=(84, 92, 110), acc=NAVY4, btn=BLUE4, tile=WH, tile_ink=NAVY4,
             icon=NAVY4, iconbg=(230, 234, 244)),
    a=dict(layout="row4", title="Credit cards for pensioners 2026", sub="Is there an age limit? Pick an age:", size=60,
           hero=S.hero_cards, hero_h=330, big_size=80,
           tiles=[(None, "60+"), (None, "70+"), (None, "80+"), (None, "85+")],
           pal=dict(acc=RED4, tile_line=(220, 224, 236)), note="сетка возрастов 60+/70+/80+/85+ («до какого возраста» — вопросом)"),
    b=dict(layout="phone", title="Credit cards after 60:", title2="what do lenders check first?", size=54,
           tag="CREDIT QUIZ", step="Question 1 of 5", prog=0.2,
           q="What do card lenders look at first?", opts=["Age", "Pension income", "Credit history", "Home ownership"],
           pal=dict(bg=(20, 34, 78), bg2=(12, 20, 50), ink=WH, sub=(200, 210, 230), acc=GOLD4, btn=BLUE4),
           note="тёмно-синий, телефон с тестом; вопрос о кредиторах, не о зрителе"),
    c=dict(layout="twocol", title="Standard card or credit builder card?", sub="What changes after 60 – explained simply",
           cols=[("STANDARD CARD", "card", NAVY4), ("CREDIT BUILDER CARD", "card_up", (24, 130, 90))],
           rows=[("MADE FOR", "a strong credit history", "a thin or damaged history"), ("STARTING LIMIT", "usually higher", "usually lower"),
                 ("MAIN GOAL", "spending & rewards", "rebuilding a credit score")],
           foot="Which one do lenders offer over-60s?", size=52),
    d=dict(style="bars", scene="table_card", y=56,
           bars=[("CREDIT CARDS FOR", WH, RED4), ("PENSIONERS 2026:", WH, RED4), ("WHAT BANKS DON'T", NAVY4, None), ("TELL OVER-60s?", NAVY4, None)],
           bar_size=92, cond=0.8, btn_y=600, btn_size=50,
           note="формула рабочих кредитных крео владельца (AT 0819-GE02 / LT): плашки + «что банки не говорят»; стол с пенсионным письмом, очками, чаем и картой без логотипа"),
)

# ---------------------------------------------------------------- 5. DE · Beamtenkredit (кредиты)
PET, ORG5, DARK5 = (14, 74, 92), (240, 118, 28), (22, 30, 40)
PACKS[5] = dict(
    doc="P60-loans-civil-servants-de-2026-09-30", cta="Mehr erfahren",
    pal=dict(bg=(16, 80, 98), bg2=(8, 44, 58), ink=WH, sub=(196, 222, 228), acc=ORG5, btn=ORG5, tile=WH, tile_ink=DARK5,
             icon=PET, iconbg=(224, 238, 242), sh=120),
    a=dict(layout="2x2", title="Beamtenkredit 2026", sub="Konditionen je nach Status – bitte wählen:",
           tiles=[("padlock", "Beamte auf Lebenszeit"), ("clock", "Beamte auf Probe"),
                  ("doc", "Beamten­anwärter"), ("briefcase", "Öffentlicher Dienst (Tarif)")],
           note="2×2 статусов на петролевом фоне, у каждой «Mehr erfahren»"),
    b=dict(layout="calc", title="Beamtenkredit-Rechner 2026", sub="3 Angaben, die die Bank wirklich prüft",
           steps=[("Status", "done"), ("Laufzeit", "now"), ("Verwendung", "todo")],
           tag="SCHRITT 2 VON 3", step="", prog=0.66,
           q="Welche Laufzeit ist gewünscht?", opts=["bis 5 Jahre", "bis 10 Jahre", "bis 20 Jahre", "bis zur Pension"],
           pal=dict(bg=(236, 242, 245), bg2=(214, 226, 232), ink=DARK5, sub=(80, 92, 104), acc=PET, btn=ORG5),
           note="форма-калькулятор со степпером (ключ «beamtenkredit rechner»); без сумм и ставок"),
    c=dict(layout="split", title="Warum Banken Beamten andere Zinsen anbieten", sub="Was die Bank sieht – der Unterschied in 3 Punkten", size=52,
           diag=40, cols=[("ANGESTELLT", "briefcase", (96, 108, 124), ["Kündigung möglich", "Einkommen kann wegfallen", "Zinsen: Standard"]),
                          ("VERBEAMTET", "padlock", PET, ["Kündigung kaum möglich", "Feste Besoldung", "Zinsen: ?"])],
           pal=dict(bg=(248, 246, 242), ink=DARK5, sub=(90, 96, 106), btn=ORG5, vs_bg=ORG5, vs_ink=WH), note="диагональный сплит: angestellt / verbeamtet"),
    d=dict(style="bars", scene="desk_top", y=190, veil=(70, 160, 1010, 630), veil_alpha=238,
           bars=[("BEAMTENKREDIT 2026:", WH, ORG5), ("WAS BANKEN BEAMTEN", WH, DARK5), ("VERSCHWEIGEN?", WH, DARK5)],
           bar_size=90, cond=0.8, btn_y=548, btn_size=48, max_w=900,
           pal=dict(btn=(28, 88, 196)),
           note="формула рабочих кредитных крео владельца (плашки + «что банки скрывают»); стол сверху: Bezügemitteilung без герба, калькулятор «2026», ручка, папка, кофе"),
)

# ---------------------------------------------------------------- 6. FR · prêts enseignants (кредиты)
CHALK, YEL6, RED6 = (40, 78, 62), (250, 214, 72), (214, 52, 40)
PACKS[6] = dict(
    doc="P60-loans-teachers-fr-2026-09-30", cta="En savoir plus",
    pal=dict(bg=(40, 78, 62), ink=WH, sub=(210, 226, 216), acc=YEL6, btn=RED6, tile=WH, tile_ink=(40, 40, 40),
             icon=(40, 60, 90), iconbg=(255, 255, 255)),
    a=dict(layout="2x2", title="Prêt enseignant 2026 : quel projet ?", sub="Ce que proposent les banques, projet par projet", size=58,
           tiles=[("car", "Voiture"), ("roller", "Travaux"), ("box", "Mutation"), ("star", "Projet perso")],
           pal=dict(note=[(255, 244, 170), (214, 240, 250), (255, 222, 206), (222, 246, 206)], iconbg=(255, 255, 255), sh=140),
           note="«стикеры» со скотчем на школьной доске"),
    b=dict(layout="card2x2", title="Simulation de prêt enseignant", sub="Prêts pour les enseignants : ce que proposent les banques en 2026",
           tag="SIMULATION", step="Étape 1 sur 3", prog=0.33, q="Sur quelle durée ?",
           opts=["12 mois", "36 mois", "60 mois", "Jusqu'à 120 mois"],
           pal=dict(chalk=True, acc=(40, 110, 80), ink=WH, sub=(214, 230, 220)),
           note="симуляция на доске (ключи «casden simulation», без бренда на картинке); только срок, без сумм и ставок"),
    c=dict(layout="table", title="Banque classique ou offre enseignants ?", sub="Ce qui change vraiment en 2026", size=56,
           cols=[("Banque classique", "bank", (90, 100, 116)), ("Offre enseignants", "book_apple", (40, 110, 80))],
           rows=[("Pour qui", "tous les clients", "enseignants et personnels de l'éducation"), ("Adhésion", "non", "souvent une part sociale"),
                 ("Durée", "selon la banque", "jusqu'à 120 mois"), ("Conditions", "standard", "?")],
           foot="La différence que peu de profs connaissent",
           pal=dict(bg=(246, 242, 232), ink=(30, 40, 36), sub=(90, 96, 90), acc=RED6, hl=YEL6),
           note="таблица: обычный банк / предложение для учителей"),
    d=dict(style="chalk", scene="classroom", y=86,
           bars=[("PRÊTS POUR LES", (30, 30, 30), YEL6), ("ENSEIGNANTS 2026 :", (30, 30, 30), YEL6),
                 ("CE QUE LES BANQUES", WH, None), ("NE DISENT PAS", WH, None)],
           bar_size=84, cond=0.8, btn_y=585, btn_size=46, max_w=900,
           note="формула рабочих кредитных крео владельца на школьной доске; на столе тетради, яблоко, очки, красная ручка"),
)

# ---------------------------------------------------------------- 7. PL · kredyt dla mundurowych (кредиты)
OLIVE, SAND, RED7, DARK7 = (74, 88, 52), (238, 232, 214), (196, 30, 40), (36, 40, 30)
PACKS[7] = dict(
    doc="P60-loans-military-pl-2026-09-30", cta="Dowiedz się więcej",
    pal=dict(bg=SAND, ink=DARK7, sub=(96, 96, 80), acc=OLIVE, btn=RED7, tile=WH, tile_ink=DARK7,
             icon=OLIVE, iconbg=(232, 234, 214)),
    a=dict(layout="list4", title="Kredyt dla mundurowych 2026", sub="Oferty banków – wybierz służbę:", size=60, hero_label="Kredyt dla służb mundurowych",
           hero=S.hero_camo, hero_h=250,
           tiles=[("boots", "Wojsko"), ("peaked_cap", "Policja"), ("helmet", "Straż pożarna"), ("binoculars", "Straż Graniczna")],
           note="камуфляжная полоса + 4 службы строками; предметы без знаков различия"),
    b=dict(layout="card", title="Kredyt dla służb mundurowych:", title2="quiz w 4 pytaniach", size=56,
           tag="QUIZ", step="Pytanie 1 z 4", prog=0.25,
           q="Co bank sprawdza najpierw przy ofercie dla służb?", opts=["Staż służby", "Stałe uposażenie", "Wiek", "Historię kredytową"],
           pal=dict(bg=(84, 98, 60), bg2=(44, 54, 32), ink=WH, sub=(220, 226, 200), acc=OLIVE, t2=(250, 214, 72), deco=True),
           note="оливковый фон, вопрос о банке, не о зрителе"),
    c=dict(layout="stacked", title="Zwykły kredyt czy oferta dla mundurowych?", sub="Czym różnią się oferty banków w 2026", size=52,
           cols=[("ZWYKŁY KREDYT", "bank", (100, 104, 110), WH, DARK7, ["dla wszystkich klientów", "dochód z umowy o pracę", "warunki standardowe"]),
                 ("OFERTA DLA MUNDUROWYCH", "peaked_cap", OLIVE, OLIVE, WH, ["wojsko, policja, straże", "dochód: uposażenie", "warunki: ?"])],
           foot="Różnica, o której mało kto mówi", pal=dict(acc=RED7, hl=(250, 214, 72)),
           note="две карточки друг над другом"),
    d=dict(style="left", scene="uniform_chair", y=60, x=70,
           bars=[("KREDYT DLA", WH, RED7), ("MUNDUROWYCH 2026:", WH, RED7), ("CZEGO BANKI", DARK7, None), ("NIE MÓWIĄ?", DARK7, None)],
           bar_size=100, cond=0.8, btn_y=640, btn_size=42, max_w=940,
           pal=dict(btn=(28, 88, 196)),
           note="формула рабочих кредитных крео владельца (плашки + «чего банки не говорят»); стул с курткой-камуфляжем, кепкой и ботинками без знаков"),
)

# ---------------------------------------------------------------- 8. FR · robot lave-vitres vs laveur de vitres (товарка → клининг)
NAVY8, SKY8, YEL8, RED8 = (20, 50, 90), (120, 190, 230), (255, 208, 50), (226, 60, 50)
PACKS[8] = dict(
    doc="P60-fr-robot-vitres-menage-2026-09-30", cta="En savoir plus",
    pal=dict(bg=(238, 246, 251), ink=NAVY8, sub=(80, 96, 116), acc=(0, 120, 200), btn=RED8, tile=WH, tile_ink=NAVY8,
             icon=NAVY8, iconbg=(226, 240, 250), hl=YEL8, sticker=YEL8),
    a=dict(layout="row2", title="Robot lave-vitres ou laveur de vitres ?", sub="Lequel revient moins cher en 2026 ?", size=58,
           hero=S.hero_robot, hero_h=380, hero_label="Robot / Professionnel", tiles=[("robot", "Robot"), ("squeegee", "Professionnel")],
           foot="Crédit d'impôt 50 % : le vrai calcul", note="сетка из 2 вариантов, как в брифе №1"),
    b=dict(layout="card2x2", title="Laveur de vitres déclaré :", title2="le calcul qui surprend", size=58,
           tag="QUIZ", step="Question 1 sur 3", prog=0.33,
           q="Avec le crédit d'impôt de 50 %, on paie au final…",
           opts=["100 % de la facture", "75 % de la facture", "50 % de la facture", "Rien du tout"],
           pal=dict(bg=(40, 120, 190), bg2=(18, 60, 110), ink=WH, sub=(214, 232, 246), acc=(0, 120, 200), deco=True, hl=YEL8),
           note="квиз про 50 % налогового кредита"),
    c=dict(layout="table", title="Robot ou laveur de vitres : combien ça coûte ?", sub="Le vrai calcul pour 2026, poste par poste", size=54,
           cols=[("Robot lave-vitres", "robot", (60, 70, 86)), ("Laveur de vitres", "squeegee", (0, 110, 190))],
           rows=[("Prix", "achat unique", "à chaque passage"), ("Vitres", "oui", "oui"), ("Cadres, rebords", "non", "oui"),
                 ("Temps à y passer", "le poser vitre par vitre", "aucun")],
           banner="Service déclaré :\ncrédit d'impôt 50 %", pal=dict(acc=(0, 110, 190)),
           note="таблица робот / мойщик; про налоговый кредит — только у услуги (у робота не утверждаем)"),
    d=dict(style="top", scene="bay_window", title="Robot lave-vitres ou laveur de vitres ?", sub="Lequel revient moins cher en 2026 ?",
           size=62, sticker="Crédit d'impôt 50 %", sticker_xy=(900, 470, 104), btn_y=1000,
           note="гостиная с большим окном, робот без логотипа на стекле, жёлтый стикер"),
)


# ---------------------------------------------------------------- сборка
def texts(t, cta):
    """Весь текст на картинке — для creatives.json."""
    out = []
    for k in ("kicker", "title", "title2", "sub", "hero_label"):
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
        out.append(" / ".join(x[1].replace("­", "") for x in t["tiles"]) + f" (у каждой «{cta}»)")
    if t.get("tile_sub"):
        out.append(t["tile_sub"])
    if t.get("cols"):
        out.append(" vs ".join(x[0] for x in t["cols"]))
        for x in t["cols"]:
            if len(x) >= 4 and isinstance(x[-1], list):
                out.append(x[0] + ": " + " · ".join(x[-1]))
    if t.get("rows"):
        out.append(" · ".join(f"{r[0]}: {r[1]} / {r[2]}" for r in t["rows"]))
    if t.get("bill"):
        out.append(t["bill"] + " " + t.get("bill_r", ""))
    if isinstance(t.get("bars"), list) and t.get("bars") and len(t["bars"][0]) == 4:
        out.append(" · ".join(f"{b[0]} {b[2]}" for b in t["bars"]))
    for k in ("banner", "sticker", "foot"):
        if t.get(k):
            out.append(t[k])
    return " / ".join(out).replace("\n", " ").replace("\u00ad", "")


def build(n, letters="abcd"):
    P = PACKS[n]
    doc = P["doc"]
    items = []
    jpath = os.path.join(OUT, doc, "creatives.json")
    for L in "abcd":
        t = P[L]
        PP = dict(P, pal={**P["pal"], **t.get("pal", {})})
        if L in letters:
            fn = {"a": T.grid, "b": T.quiz, "c": T.compare, "d": T.scene}[L]
            c = fn(PP, t)
            c.save(f"{doc}/{L}.png")
        items.append(dict(letter=L, file=f"cr/packs/{doc}/{L}.png", concept=CONCEPT[L] + " — " + t.get("note", ""),
                          text=texts(t, P["cta"]), cta=P["cta"]))
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    args = sys.argv[1:] or [str(k) for k in PACKS]
    for a in args:
        if ":" in a:
            n, ls = a.split(":")
            build(int(n), ls.replace(",", ""))
        else:
            build(int(a))
