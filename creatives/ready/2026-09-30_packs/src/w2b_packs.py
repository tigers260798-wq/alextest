"""Волна 2 «Готово к заливу» 30.09 (креативщик w2b): 10 пакетов × 4 статики 1:1, Pillow. Запуск:
    python3 w2b_packs.py            — все пакеты
    python3 w2b_packs.py 3 5        — пакеты 3 и 5
    python3 w2b_packs.py 3:a,c      — пакет 3, буквы a и c
Пишет <OUT>/<docId>/<a|b|c|d>.png и <OUT>/<docId>/creatives.json.
Шаблоны: p60_templates (grid / quiz / compare) + свои раскладки w2b_layouts и сцены w2b_scenes.
Цифры — только из гипотезы (ES: 14 pagas, доп. в июне и ноябре — seg-social; PL: 75 лет — статья гипотезы;
ES psico: 10 вопросов, 45 лет; FR: 15 вопросов). Остальное — «?»."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p60_lib import OUT
import p60_templates as T
import p60_packs as PP
import w2b_icons  # noqa: F401
import w2b_scenes as WS
import w2b_layouts as L

WH = (255, 255, 255)
CONCEPT = {"a": "сетка выбора (fake interactivity)", "b": "карточка-опросник", "c": "сколько стоит / сравнение", "d": "сцена-иллюстрация"}
PACKS = {}

# ---------------------------------------------------------------- 1. ES · paga extra (пенсии)
RED1, NAVY1, ORG1, CREAM1 = (190, 50, 50), (30, 40, 70), (226, 84, 40), (252, 244, 232)
PACKS[1] = dict(
    doc="P60-pension-13-14-es-2026-09-30", cta="Más información",
    pal=dict(bg=CREAM1, ink=NAVY1, sub=(90, 90, 100), acc=RED1, btn=ORG1, tile=WH, tile_ink=NAVY1, icon=RED1, iconbg=(250, 232, 226)),
    a=dict(fn="grid", layout="row4", title="Paga extra de noviembre 2026", sub="¿Qué quieres saber? Elige:", size=60,
           hero=WS.hero_months, hero_h=330,
           tiles=[("calendar", "¿Qué día llega?"), ("person_check", "¿Quién la cobra?"), ("euro_q", "¿Cuánto es?"), ("doc", "¿Tributa?")],
           note="сверху 2 листка календаря JUNIO/NOVIEMBRE «+1 paga extra» (14 pagas, доп. в июне и ноябре — seg-social), 4 плитки-вопроса"),
    b=dict(fn="quiz", layout="card", title="Test de la paga extra 2026", title2="la pregunta que muchos fallan", size=58,
           tag="TEST", step="Pregunta 1 de 4", prog=0.25,
           q="¿Cuántas pagas al año tiene una pensión contributiva en España?",
           opts=["12 pagas", "13 pagas", "14 pagas", "Depende de la pensión"],
           pal=dict(bg=(36, 62, 120), bg2=(18, 32, 72), ink=WH, sub=(210, 220, 240), acc=RED1, t2=(255, 214, 102), deco=True),
           note="синий фон, вопрос о правилах пенсий, не о зрителе; ответ 14 — seg-social"),
    c=dict(fn="month_bars", title="Pensión 2026 mes a mes", sub="2 meses traen paga extra. ¿Cuánto se cobra en cada uno?", size=62,
           months=["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"], extra=[5, 10],
           extra_label="+ paga", leg1="mensualidad", leg2="paga extra (¿cuánto?)",
           foot="Junio y noviembre: quién la cobra y cuándo llega",
           pal=dict(bar=(150, 170, 200), acc=RED1),
           note="12 столбиков-месяцев, в июне и ноябре надстройка «+ paga» с «?» — сумм нет"),
    d=dict(fn="scene_d", scene="scene_calendar", style="bars", y=34,
           bars=[("PAGA EXTRA DE", WH, RED1), ("NOVIEMBRE 2026:", WH, RED1), ("LO QUE POCOS SABEN", NAVY1, (255, 214, 90))],
           bar_size=78, cond=0.8, btn_y=990, btn_size=42, max_w=940,
           note="формула рабочих крео владельца (плашки + «lo que pocos saben»); кухня, настенный календарь «NOVIEMBRE 2026» со стикером «¿paga extra?» — дата не выдумана"),
)

# ---------------------------------------------------------------- 2. ES · factura de la luz / bono social
NIGHT2, YEL2, ORG2 = (26, 40, 84), (255, 200, 60), (232, 96, 36)
PACKS[2] = dict(
    doc="P60-energy-subsidy-es-2026-09-30", cta="Más información",
    pal=dict(bg=(244, 246, 252), ink=NIGHT2, sub=(80, 90, 110), acc=NIGHT2, btn=ORG2, tile=WH, tile_ink=NIGHT2, icon=NIGHT2, iconbg=(255, 240, 200)),
    a=dict(fn="grid", layout="list4", title="Factura de la luz 2026", sub="4 cosas que revisar para no pagar de más:", size=62,
           hero=WS.hero_power, hero_h=270,
           tiles=[("percent_tag", "Bono social eléctrico"), ("bulb", "Comparador de tarifas de luz"),
                  ("plug", "Potencia contratada"), ("doc", "Tarifa regulada o libre")],
           note="ночная панель с лампочкой, счётчиком и вилкой + 4 строки-кнопки"),
    b=dict(fn="quiz", layout="calc", title="¿Se paga de más por la luz?", sub="Comprobación en 3 pasos", size=58,
           steps=[("Tarifa", "done"), ("Potencia", "now"), ("Bono social", "todo")],
           tag="PASO 2 DE 3", step="", prog=0.66,
           q="¿Dónde aparece la potencia contratada?", opts=["En la factura", "En el contador", "En el contrato", "En los tres"],
           pal=dict(bg=(255, 244, 214), bg2=(255, 226, 170), ink=NIGHT2, sub=(90, 80, 60), acc=NIGHT2, btn=ORG2),
           note="форма-проверка со степпером (тариф → мощность → bono social), без цифр"),
    c=dict(fn="bill", title="¿Cuánto baja la factura con el bono social?", sub="Lo que dice cada línea de la factura", size=54,
           bill="FACTURA DE LUZ · 2026", bill_r="",
           rows=[("Potencia contratada", "? €", False), ("Energía consumida", "? €", False), ("Impuestos", "? €", False),
                 ("Descuento bono social", "− ? %", True)],
           total="TOTAL", sticker="¿Se paga de más?", foot="Bono social y comparador de tarifas: quién tiene derecho",
           pal=dict(bg=(236, 240, 250), bg2=(214, 222, 242), acc=NIGHT2, hl=(255, 226, 120), hlc=(30, 40, 70), sticker=YEL2),
           note="счёт с «? €» в каждой строке и строкой «Descuento bono social − ? %» маркером; сумм и процентов нет"),
    d=dict(fn="scene_d", scene="scene_power", style="top", size=64, y=46,
           title="Lo que la factura de la luz no cuenta", sub="Bono social 2026: quién tiene derecho y cómo comparar tarifas",
           btn_y=1000, btn_size=44,
           pal=dict(ink=WH, sub=(214, 222, 240)),
           note="кухня ночью: окно с луной, лампа, розетка, на столе счёт «TOTAL: ? €», калькулятор, очки"),
)

# ---------------------------------------------------------------- 3. ES · vista cansada (здоровье 60+)
TEAL3, NAVY3, CORAL3 = (0, 110, 140), (20, 50, 80), (232, 88, 60)
PACKS[3] = dict(
    doc="P60-vision-60-es-2026-09-30", cta="Más información",
    pal=dict(bg=(236, 246, 248), ink=NAVY3, sub=(80, 96, 110), acc=TEAL3, btn=CORAL3, tile=WH, tile_ink=NAVY3, icon=TEAL3, iconbg=(218, 238, 244)),
    a=dict(fn="grid", layout="2x2", title="Vista cansada después de los 60", sub="4 opciones en 2026. Elige una:", size=60,
           tiles=[("specs_prog", "Gafas progresivas"), ("contact", "Lentes de contacto"),
                  ("reading", "Gafas de cerca"), ("eye_lens", "Cirugía con lente intraocular")],
           note="2×2 вариантов (очки, линзы, операция) — «после 60» только как описание темы, не о зрителе"),
    b=dict(fn="quiz", layout="card2x2", title="Gafas progresivas:", title2="la pregunta que muchos fallan", size=60,
           tag="TEST", step="Pregunta 1 de 3", prog=0.33,
           q="¿Para qué distancias sirve una gafa progresiva?",
           opts=["Solo de cerca", "Solo de lejos", "Cerca, media y lejos", "No lo sé"],
           pal=dict(bg=(0, 118, 146), bg2=(10, 60, 90), ink=WH, sub=(210, 236, 240), acc=TEAL3, t2=(255, 214, 102), deco=True),
           note="бирюзовый фон, вопрос о самих очках, не о зрении зрителя"),
    c=dict(fn="price_tags", title="Vista cansada: ¿cuánto cuesta cada opción en 2026?", sub=None, size=58,
           tags=[("specs_prog", "Gafas progresivas", (0, 110, 140)), ("contact", "Lentes de contacto", (60, 90, 160)),
                 ("eye_lens", "Cirugía con lente intraocular", (190, 70, 60))],
           foot="Precios, ventajas y para quién es cada opción",
           pal=dict(bg=(250, 246, 238)),
           note="3 ценника на штанге «? €» — цен в гипотезе нет"),
    d=dict(fn="scene_d", scene="scene_optica", style="top", size=60, y=44,
           title="Gafas progresivas 2026: lo que pocos preguntan en la óptica", sub="Precios, lentes y cirugía: opciones después de los 60",
           btn_y=1000, btn_size=44,
           note="оптика: таблица букв, стеллаж оправ, прогрессивные очки на подставке; людей нет, «до/после» нет"),
)

# ---------------------------------------------------------------- 4. IT · dentista ASL (здоровье 60+)
AQUA4, NAVY4, BURG4 = (0, 136, 156), (22, 42, 110), (140, 28, 40)
PACKS[4] = dict(
    doc="P60-health-retirement-it-2026-09-30", cta="Scopri di più",
    pal=dict(bg=(240, 248, 250), ink=NAVY4, sub=(80, 96, 110), acc=AQUA4, btn=BURG4, tile=WH, tile_ink=NAVY4, icon=AQUA4, iconbg=(220, 240, 244)),
    a=dict(fn="grid", layout="row4", title="Dentista ASL 2026: cosa è coperto?", sub="Scegli la cura:", size=58,
           hero=WS.hero_tooth, hero_h=330,
           tiles=[("tooth", "Visita e pulizia?"), ("tooth_fill", "Otturazioni?"), ("denture", "Protesi?"), ("implant", "Impianti?")],
           note="зуб с облачком «ASL?» сверху, 4 плитки-вопроса по видам лечения"),
    b=dict(fn="quiz", layout="card", title="Dentista convenzionato ASL:", title2="chi ne ha diritto nel 2026?", size=56,
           tag="QUIZ", step="Domanda 1 di 4", prog=0.25,
           q="Da cosa dipendono le cure dentali gratuite con l'ASL?",
           opts=["Dall'età", "Dall'ISEE", "Dalla regione", "Da tutti e tre"],
           pal=dict(bg=(226, 242, 246), bg2=(196, 228, 236), acc=AQUA4, t2=BURG4, deco=True),
           note="вопрос о правилах ASL, не о зубах зрителя"),
    c=dict(fn="compare", layout="split", title="Dentista privato o convenzionato ASL?", sub="Cosa cambia nel 2026 – e quanto si paga", size=54,
           cols=[("PRIVATO", "euro_q", (96, 104, 120), ["Prezzo libero", "Si sceglie lo studio", "Pagamento a rate?"]),
                 ("CONVENZIONATO ASL", "tooth", AQUA4, ["Ticket o gratis", "Tramite l'ASL", "Chi ne ha diritto?"])],
           pal=dict(bg=(250, 250, 252), ink=NAVY4, sub=(90, 96, 106), btn=BURG4, vs_bg=BURG4, vs_ink=WH),
           note="сплит: частный / по ASL («Ticket o gratis» — из хука гипотезы)"),
    d=dict(fn="scene_d", scene="scene_dental", style="bottomcard", card_box=(50, 560, 1030, 1040), size=62, pad=46,
           title="Dentista convenzionato ASL", sub="Cure gratuite o a tariffa ridotta: pochi sanno come funziona nel 2026",
           btn_size=40, btn_off=74,
           note="кабинет стоматолога (кресло, лампа, шкафчик, окно) + белая карточка снизу и бордовая кнопка — приёмы рабочего крео владельца (IT 0927-GE01)"),
)

# ---------------------------------------------------------------- 5. PL · dodatki do emerytury (пособия)
NAVY5, AMB5, RED5, GRN5 = (30, 50, 90), (226, 146, 40), (196, 60, 40), (40, 110, 80)
PACKS[5] = dict(
    doc="P60-pension-benefit-pl-2026-09-30", cta="Dowiedz się więcej",
    pal=dict(bg=(250, 242, 228), ink=NAVY5, sub=(96, 90, 80), acc=AMB5, btn=RED5, tile=WH, tile_ink=NAVY5, icon=NAVY5, iconbg=(246, 230, 206)),
    a=dict(fn="grid", layout="list4", title="Dodatki do emerytury 2026", sub="Wybierz temat:", size=62,
           hero=WS.hero_autumn, hero_h=250,
           tiles=[("age75", "Dodatek po 75. roku życia"), ("stroller", "Dodatek za wychowanie dzieci"),
                  ("rings", "Renta wdowia"), ("badge_1314", "13. i 14. emerytura")],
           note="осенняя панель «75+ / 80+» (запросы гипотезы) + 4 строки-кнопки по ключам"),
    b=dict(fn="quiz", layout="card2x2", title="Dodatki do emerytury:", title2="pytanie, na którym wielu się myli", size=58,
           tag="QUIZ", step="Pytanie 1 z 4", prog=0.25,
           q="Od jakiego wieku dodatek pielęgnacyjny przysługuje z urzędu?",
           opts=["Od 65 lat", "Od 75 lat", "Od 80 lat", "Nie wiem"],
           pal=dict(bg=(40, 66, 110), bg2=(22, 36, 66), ink=WH, sub=(210, 220, 236), acc=AMB5, t2=(255, 214, 102), deco=True),
           note="вопрос о правиле (75 лет — из статьи гипотезы), не о зрителе"),
    c=dict(fn="tower", title="Ile naprawdę wynosi świadczenie seniora w 2026?", sub="Z czego może się składać – krok po kroku", size=54,
           blocks=[("Emerytura", 250, NAVY5, "?"), ("Dodatek pielęgnacyjny", 110, AMB5, "?"),
                   ("13. emerytura", 100, (70, 120, 170), "?"), ("14. emerytura", 100, GRN5, "?")],
           unit="zł", foot="Dodatki, o których mało kto wie", pal=dict(acc=RED5, hl=(255, 222, 130)),
           note="«башня» из блоков: пенсия + dodatek pielęgnacyjny + 13-я + 14-я, суммы «? zł»"),
    d=dict(fn="scene_d", scene="scene_park", style="left", y=40, x=60,
           bars=[("DODATKI DO", WH, RED5), ("EMERYTURY 2026:", WH, RED5), ("O CZYM MAŁO", NAVY5, WH), ("KTO WIE?", NAVY5, WH)],
           bar_size=76, cond=0.8, btn_size=38, max_w=620,
           note="осенний парк, двое пожилых на скамейке со спины (без лиц) + плашки слева; без гербов и флагов"),
)

# ---------------------------------------------------------------- 6. FR · test de couple (психология)
ROSE6, BLUE6, INK6 = (200, 76, 80), (40, 90, 150), (40, 36, 60)
PACKS[6] = dict(
    doc="NT-psy-couples-fr-2026-09-30", cta="En savoir plus",
    pal=dict(bg=(252, 240, 236), ink=INK6, sub=(100, 90, 96), acc=ROSE6, btn=ROSE6, tile=WH, tile_ink=INK6, icon=BLUE6, iconbg=(236, 242, 250)),
    a=dict(fn="grid", layout="2x2", title="Test de couple\u00a0: 15\u00a0questions", sub="Ce que regardent les thérapeutes. Choisissez un thème\u00a0:", size=60,
           tiles=[("talk", "Communication"), ("padlock", "Confiance"), ("compass", "Projets"), ("storm", "Disputes")],
           note="2×2 тем теста (из текста гипотезы); без «ваша пара»"),
    b=dict(fn="quiz", layout="card", title="Test de couple en 15\u00a0questions", title2="Ce que regardent les thérapeutes", size=56,
           tag="TEST", step="Question 1 sur 15", prog=1 / 15,
           q="Selon les thérapeutes, qu'est-ce qui compte le plus après une dispute\u00a0?",
           opts=["Savoir qui a raison", "Qui fait le premier pas", "Oublier très vite", "En reparler au calme"],
           pal=dict(bg=(200, 80, 84), bg2=(120, 40, 60), ink=WH, sub=(250, 220, 220), acc=ROSE6, t2=(255, 222, 150), deco=True, btn=BLUE6),
           note="вопрос о мнении терапевтов, не о паре зрителя"),
    c=dict(fn="compare", layout="table", title="Thérapie de couple 2026\u00a0: combien ça coûte\u00a0?", sub="En cabinet ou en ligne – ce qui change", size=54,
           cols=[("En cabinet", "armchair", (170, 70, 70)), ("En ligne", "laptop", BLUE6)],
           rows=[("Prix d'une séance", "?", "?"), ("Où", "chez le thérapeute", "à la maison, en visio"), ("Remboursement", "?", "?")],
           foot="Le test complet + les prix 2026", pal=dict(bg=(250, 246, 242), acc=ROSE6, hl=(255, 222, 150)),
           note="таблица кабинет / онлайн: цены и возмещение — «?»"),
    d=dict(fn="scene_d", scene="scene_mugs", style="top", size=66, y=48,
           title="Test de couple\u00a0: 15\u00a0questions", sub="Ce que regardent les thérapeutes", sub_size=36,
           btn_y=372, btn_size=42,
           note="две кружки ручками в разные стороны и карточка «15 questions» (визуал из брифа гипотезы); людей и колец нет"),
)

# ---------------------------------------------------------------- 7. ES · estudiar Psicología (обучение)
IND7, CORAL7, INK7 = (80, 64, 160), (232, 96, 70), (30, 28, 60)
PACKS[7] = dict(
    doc="NT-psy-career-es-2026-09-30", cta="Más información",
    pal=dict(bg=(244, 242, 252), ink=INK7, sub=(90, 88, 110), acc=IND7, btn=CORAL7, tile=WH, tile_ink=INK7, icon=IND7, iconbg=(232, 228, 250)),
    a=dict(fn="grid", layout="row2", title="Estudiar Psicología en 2026", sub="También después de los 45. Elige cómo:", size=62,
           hero=WS.hero_study, hero_h=340,
           tiles=[("laptop", "Online"), ("notebook", "A distancia")],
           foot="Requisitos, duración y precios de cada opción",
           note="полка с книгами, шапочка, ноутбук + 2 больших варианта (ключи «estudiar psicología online / a distancia»)"),
    b=dict(fn="quiz", layout="phone", title="¿Tienes perfil de psicólogo?", title2="Test de 10 preguntas", size=56,
           sub="Y cómo estudiar Psicología online, también después de los 45",
           tag="TEST", step="Pregunta 1 de 10", prog=0.1,
           q="Alguien cuenta un problema. ¿Qué sale primero?",
           opts=["Escuchar hasta el final", "Dar un consejo", "Contar algo parecido", "Cambiar de tema"],
           pal=dict(bg=(236, 232, 252), bg2=(214, 206, 244), ink=INK7, sub=(90, 88, 110), acc=IND7, btn=CORAL7),
           note="хук гипотезы «¿Tienes perfil de psicólogo?» + телефон с тестом"),
    c=dict(fn="compare", layout="split", title="¿A distancia u online?", sub="Lo que cambia al estudiar Psicología en 2026", size=60,
           diag=40, cols=[("A DISTANCIA", "notebook", IND7, ["Materiales y tutorías", "Ritmo propio", "Precio: ?"]),
                          ("ONLINE", "laptop", (214, 90, 60), ["Clases por internet", "Horario flexible", "Precio: ?"])],
           pal=dict(bg=(248, 246, 252), ink=INK7, sub=(90, 88, 110), btn=(40, 40, 60), vs_bg=(40, 40, 60), vs_ink=WH),
           note="диагональный сплит: заочно / онлайн, цена — «?»; без обещаний диплома и работы"),
    d=dict(fn="scene_d", scene="scene_armchair", style="top", size=64, y=40,
           title="¿Tienes perfil de psicólogo?", sub="Test de 10 preguntas + cómo estudiar Psicología online después de los 45",
           btn_y=1000, btn_size=44,
           note="кресло психолога, блокнот «10 preguntas», шапочка, стеллаж — визуал из брифа гипотезы"),
)

# ---------------------------------------------------------------- 8. PT · lar de idosos
GRN8, TERRA8, INK8 = (0, 110, 90), (200, 84, 50), (24, 50, 44)
PACKS[8] = dict(
    doc="NT-nursing-home-costs-pt-2026-09-30", cta="Saiba mais",
    pal=dict(bg=(238, 246, 240), ink=INK8, sub=(80, 96, 90), acc=GRN8, btn=TERRA8, tile=WH, tile_ink=INK8, icon=GRN8, iconbg=(222, 240, 230)),
    a=dict(fn="grid", layout="row4", title="Lar de idosos 2026: quanto custa por mês?", sub=None, size=58,
           hero=WS.hero_lar, hero_h=330,
           tiles=[("bed", "Quarto individual"), ("bed2", "Quarto duplo"), ("sun_house", "Centro de dia"), ("home_help", "Apoio domiciliário")],
           note="фасад дома с садом сверху, 4 плитки-варианта ухода"),
    b=dict(fn="quiz", layout="card", title="Lar de idosos em Portugal:", title2="4 perguntas antes de escolher", size=58,
           tag="QUIZ", step="Pergunta 1 de 4", prog=0.25,
           q="O que pesa mais no preço de um lar de idosos?",
           opts=["O tipo de quarto", "O grau de dependência", "A localização do lar", "Tudo isto"],
           pal=dict(bg=(0, 110, 90), bg2=(0, 64, 56), ink=WH, sub=(210, 236, 226), acc=GRN8, t2=(255, 214, 120), deco=True),
           note="зелёный фон, вопрос о ценообразовании, не о зрителе; «localização do lar» — о доме, не о зрителе"),
    c=dict(fn="compare", layout="table", title="Lar privado ou IPSS: quanto se paga?", sub="O que muda em 2026", size=56,
           cols=[("Lar privado", "house", (130, 90, 70)), ("IPSS", "home_help", GRN8)],
           rows=[("Mensalidade", "?", "?"), ("Quem gere", "uma empresa", "uma instituição social"), ("Lista de espera", "?", "?")],
           foot="A diferença que poucas famílias conhecem", pal=dict(bg=(246, 244, 238), acc=TERRA8, hl=(255, 222, 150)),
           note="таблица частный / IPSS: суммы и очереди — «?»"),
    d=dict(fn="scene_d", scene="scene_lar", scene_kw=dict(top=440), style="card", card_box=(70, 34, 1010, 400), size=56, pad=40,
           kicker="LARES DE IDOSOS EM PORTUGAL", title="Quanto custa um lar de idosos em 2026?", btn_size=38, btn_off=62,
           frame=True, pal=dict(frame=GRN8, ink=INK8),
           note="фасад дома для пожилых с садом, карточка в рамке сверху (ключ «quanto custa um lar de idosos em portugal»)"),
)

# ---------------------------------------------------------------- 9. ES · becas / cursos de informática 60+
BLUE9, ORG9, YEL9 = (26, 86, 180), (240, 120, 30), (255, 214, 80)
PACKS[9] = dict(
    doc="NT-becas-informatica-es-2026-09-30", cta="Más información",
    pal=dict(bg=(30, 100, 200), bg2=(16, 62, 150), ink=WH, sub=(210, 226, 250), acc=BLUE9, btn=ORG9, tile=WH, tile_ink=(30, 40, 60),
             icon=BLUE9, iconbg=(226, 236, 250)),
    a=dict(fn="laptop_grid", title="Cursos de informática para mayores 2026", sub="¿Por dónde empezar? Elige un curso:", size=58,
           tiles=[("phone", "Móvil y mensajes"), ("shield", "Internet seguro"), ("videocam", "Videollamadas"), ("laptop_doc", "Trámites online")],
           note="экран ноутбука с 4 плитками-курсами, у каждой «Más información»; синий как у рабочей связки 0918-GE06"),
    b=dict(fn="quiz", layout="card2x2", title="Cursos de informática:", title2="¿gratis para mayores de 60?", size=60,
           tag="TEST", step="Pregunta 1 de 3", prog=0.33,
           q="¿Quién puede pedir una beca para un curso de informática?",
           opts=["Solo jóvenes", "Mayores de 60", "Jubilados", "Depende de la beca"],
           pal=dict(bg=(255, 214, 80), bg2=(250, 176, 40), ink=(24, 36, 70), sub=(70, 60, 30), acc=BLUE9, t2=BLUE9, btn=BLUE9),
           note="жёлтый фон; «gratis» только вопросом (ключ «cursos de informática gratis … mayores de 60»)"),
    c=dict(fn="compare", layout="twocol", title="¿Curso con beca o de pago?", sub="Cursos de informática para jubilados en 2026", size=60,
           cols=[("CON BECA", "cap", BLUE9), ("DE PAGO", "coins", (200, 110, 40))],
           rows=[("QUIÉN PAGA", "la beca", "el alumno"), ("INSCRIPCIÓN", "en el plazo de la convocatoria", "libre"),
                 ("REQUISITOS", "según la convocatoria", "normalmente ninguno")],
           foot="¿Cómo encontrar cursos gratis?", pal=dict(bg=(240, 245, 252), bg2=(226, 234, 248), ink=(24, 36, 70), sub=(80, 90, 110), btn=ORG9),
           note="две колонки: с грантом / платно; «gratis» — вопросом"),
    d=dict(fn="scene_d", scene="scene_laptop_desk", style="top", size=62, y=46, lines=3,
           title="Becas para cursos de informática en la tercera edad: guía 2026", sub="Qué cursos hay, quién puede pedirlos y cómo",
           btn_y=440, btn_size=42, pal=dict(ink=WH, sub=(214, 228, 250)),
           note="синий фон и крупный белый заголовок (как у рабочей РК 0918-GE06, текст перефразирован), стол с ноутбуком-уроком, наушники, чай"),
)

# ---------------------------------------------------------------- 10. ES · товарка: muebles / salón
SAGE10, TERRA10, INK10 = (110, 140, 110), (200, 96, 64), (40, 44, 40)
STY = {
    "Nórdico": dict(wall=(240, 240, 236), floor=(226, 206, 176), sofa=(190, 196, 200), leg=(170, 130, 90), deco=(230, 180, 90), kind="plant", tag="madera clara, gris"),
    "Minimalista": dict(wall=(248, 246, 242), floor=(214, 210, 204), sofa=(236, 228, 214), leg=(60, 60, 60), deco=(40, 40, 44), kind="frame", tag="blanco, líneas rectas"),
    "Industrial": dict(wall=(170, 96, 70), floor=(90, 84, 80), sofa=(120, 76, 50), leg=(30, 30, 30), deco=(230, 180, 90), kind="lamp", brick=True, tag="metal, cuero, ladrillo"),
    "Japandi": dict(wall=(236, 228, 214), floor=(200, 170, 130), sofa=(150, 160, 130), leg=(120, 90, 60), deco=(214, 120, 80), kind="japandi", low=True, tag="bajo, natural, calma"),
}
PACKS[10] = dict(
    doc="NT-furniture-ideas-es-2026-09-30", cta="Más información",
    pal=dict(bg=(246, 242, 234), ink=INK10, sub=(96, 96, 90), acc=SAGE10, btn=TERRA10, tile=WH, tile_ink=INK10, icon=SAGE10, iconbg=(230, 238, 228)),
    a=dict(fn="style_grid", title="Muebles de salón 2026", sub="¿Qué estilo? Elige uno:", size=64,
           tiles=[(k, STY[k]) for k in ("Nórdico", "Minimalista", "Industrial", "Japandi")],
           note="товарка-сетка: 4 мини-гостиные в разных стилях, у каждой «Más información»"),
    b=dict(fn="poll", title="¿Qué salón parece más amplio?", sub="Mismos metros, otros muebles", size=60,
           tag="ENCUESTA", step="1 de 3",
           opts=[("Muebles altos y oscuros", dict(STY["Industrial"], note="")), ("Muebles bajos y claros", dict(STY["Japandi"], note=""))],
           pal=dict(bg=(236, 242, 234), bg2=(220, 232, 218), acc=SAGE10),
           note="опрос A/B с «?%» — fake interactivity"),
    c=dict(fn="floorplans", title="Mismo salón, 2 distribuciones", sub="¿Cuál deja más espacio libre?", size=62,
           plans=[("A", "Sofá contra la pared"), ("B", "Sofá en L y mesa redonda")],
           foot="Ideas de muebles modernos para 2026", pal=dict(sofa=SAGE10, acc=TERRA10, hl=(255, 226, 170)),
           note="два плана одной комнаты сверху (A/B, не «до/после»)"),
    d=dict(fn="scene_d", scene="scene_salon", style="top", size=64, y=40,
           title="Ideas de muebles modernos para 2026", sub="Cómo reorganizar el salón y ganar espacio",
           btn_y=1022, btn_size=40,
           note="современная гостиная: шалфейный диван, полки, картины, торшер-дуга, ковёр"),
)


# ---------------------------------------------------------------- сборка
FN = {"grid": T.grid, "quiz": T.quiz, "compare": T.compare, "scene_d": L.scene_d, "month_bars": L.month_bars, "bill": L.bill,
      "price_tags": L.price_tags, "tower": L.tower, "floorplans": L.floorplans, "laptop_grid": L.laptop_grid,
      "style_grid": L.style_grid, "poll": L.poll}


def texts(t, cta):
    out = PP.texts({k: v for k, v in t.items() if k not in ("tiles", "opts", "rows", "bars", "cols")}, cta)
    parts = [out] if out else []
    if t.get("bars"):
        parts.append(" ".join(b[0] for b in t["bars"]))
    if t.get("tag"):
        pass
    if t.get("opts"):
        parts.append(" / ".join(o if isinstance(o, str) else o[0] for o in t["opts"]))
    if t.get("tiles"):
        parts.append(" / ".join(x[0] if isinstance(x[1], dict) else x[1] for x in t["tiles"]) + f" (у каждой «{cta}»)")
    if t.get("cols"):
        parts.append(" vs ".join(x[0] for x in t["cols"]))
        for x in t["cols"]:
            if len(x) >= 4 and isinstance(x[-1], list):
                parts.append(x[0] + ": " + " · ".join(x[-1]))
    if t.get("rows"):
        parts.append(" · ".join(f"{r[0]}: {r[1]} / {r[2]}" if len(r) == 3 and not isinstance(r[2], bool) else f"{r[0]}: {r[1]}" for r in t["rows"]))
    if t.get("months"):
        parts.append(" ".join(t["months"]) + f" · {t['extra_label']} (JUN, NOV) · {t['leg1']} / {t['leg2']}")
    if t.get("tags"):
        parts.append(" · ".join(f"{x[1]}: ? €" for x in t["tags"]))
    if t.get("blocks"):
        parts.append(" + ".join(f"{b[0]} ? {t.get('unit', '')}".strip() for b in t["blocks"]))
    if t.get("plans"):
        parts.append(" · ".join(f"{a}: {b}" for a, b in t["plans"]))
    if t.get("total"):
        parts.append(f"{t['total']} ? €")
    for k in ("foot",):
        if t.get(k) and t[k] not in out:
            parts.append(t[k])
    return " / ".join(parts).replace("\n", " ").replace("­", "")


def build(n, letters="abcd"):
    P = PACKS[n]
    doc = P["doc"]
    items = []
    for Lt in "abcd":
        t = P[Lt]
        PPk = dict(P, pal={**P["pal"], **t.get("pal", {})})
        if Lt in letters:
            c = FN[t["fn"]](PPk, t)
            c.save(f"{doc}/{Lt}.png")
        items.append(dict(letter=Lt, file=f"cr/packs/{doc}/{Lt}.png", concept=CONCEPT[Lt] + " — " + t.get("note", ""),
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
