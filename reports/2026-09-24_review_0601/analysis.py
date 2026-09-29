import json, glob, os, re, collections, datetime, statistics
B = '/tmp/claude-0/-home-user-alextest/f5dce882-fce7-5270-9036-ca9a0fe43d5e/scratchpad/review_0601/'
D = datetime.date
TODAY = '2026-09-24'
LAST_CLOSED_FINAL = '2026-09-21'   # выручка RSOC доезжает до D+3: дни после 21.09 неполные
M = json.load(open(B + 'raw/master.json'))
ADG = json.load(open(B + 'raw/adgroups.json'))

def r2(x, n=2):
    return None if x is None else round(x, n)

def roi(p, s):
    return round(p / s * 100, 1) if s else None

def dd(s):
    return D(*map(int, s.split('-')))

def week_of(day):
    d = dd(day)
    mon = d - datetime.timedelta(days=d.weekday())
    return mon.isoformat()

# ---------------- classification helpers ----------------
GEO_FIX = {'UK': 'GB', 'SP': 'ES', 'SW': 'CH', 'SL': 'SI', 'BAH': 'BA'}
T1 = {'US', 'GB', 'CA', 'AU', 'NZ', 'DE', 'AT', 'CH', 'NL', 'BE', 'LU', 'FR', 'IE', 'DK', 'SE', 'NO', 'FI', 'IS'}
T2 = {'IT', 'ES', 'PT', 'PL', 'CZ', 'SK', 'HU', 'SI', 'HR', 'GR', 'EE', 'LV', 'LT', 'RO', 'BG', 'CY', 'MT'}
BANNED = ('IRNFL / Account 18', 'IRNFL / Account 19', 'IRNFL / Account 12')


def parse(name):
    m = re.match(r'vb-alexz([A-Za-z0-9+]+)-(.+?)-(fb|tk)-([a-z]+)-a-(\d{4})-ge(\d+)', name, re.I)
    if m:
        return dict(bundle=m.group(1).lower(), tg=m.group(2), plat=m.group(3).lower(), geo=m.group(4).upper(), mmdd=m.group(5))
    m = re.match(r'([a-z]{2})-([a-z]{2})-(fb|tk)-tz-aleksandr-\d+-([a-z&-]+?)-\d+', name, re.I)
    if m:
        return dict(bundle='tz_' + m.group(4).lower().strip('-'), tg='tz', plat=m.group(3).lower(), geo=m.group(1).upper(), mmdd=None)
    if 'VISYMO' in name:
        return dict(bundle='visymo_cleaning', tg='visymo', plat='fb', geo='INTL', mmdd=None)
    m = re.search(r'-(fb|tk)-', name)
    return dict(bundle='other', tg=None, plat=m.group(1) if m else None, geo=None, mmdd=None)


def vertical(b):
    if b.startswith('loans') or b.startswith('tz_loans'):
        return 'кредиты'
    if b == 'paycar':
        return 'авто в рассрочку'
    if b.startswith('cleaningjobs') or b == 'visymo_cleaning':
        return 'работа: уборка'
    if 'constructionjobs' in b or b.startswith('tz_construction'):
        return 'работа: стройка'
    if 'jobs' in b or b in ('workinginretirementit', 'onboardingsystemsswfr', 'sitesecurityde'):
        return 'работа: прочее'
    if b.startswith('heatpumps'):
        return 'тепловые насосы'
    if 'dental' in b:
        return 'стоматология'
    if b.startswith('study') or b.startswith('institutions'):
        return 'обучение'
    if b == 'test':
        return 'дома престарелых (BR test)'
    if b.startswith('allinclusive'):
        return 'туризм'
    if b.startswith('rehabilitation'):
        return 'реабилитация'
    if b.startswith('spermdonat'):
        return 'донорство'
    if b in ('remodelingca', 'guttercleaning'):
        return 'услуги для дома'
    return 'прочее'


def tier(geo):
    if not geo:
        return '?'
    if geo in ('INTL',):
        return 'мульти-гео'
    if geo in T1:
        return 'tier1'
    if geo in T2:
        return 'tier2'
    return 'tier3'

# account first spend date (in our data) -> account age
acc_first = {}
for o in M:
    for a in (o.get('accounts') or []):
        if o['firstSpend']:
            acc_first[a] = min(acc_first.get(a, '9'), o['firstSpend'])

camps = []
for o in M:
    p = parse(o['name'])
    geo = GEO_FIX.get(p['geo'], p['geo']) if p['geo'] else None
    prov = (o.get('provider') or [None])[0]
    if not prov:
        prov = 'TARZO' if '-tz-' in o['name'] else ('VISYMO' if 'VISYMO' in o['name'] else 'IRONFLI')
    ts = (o['ts'] or '').upper()
    if ts not in ('FACEBOOK', 'TIKTOK'):
        ts = 'TIKTOK' if p['plat'] == 'tk' else 'FACEBOOK'
    acc = (o.get('accounts') or ['?'])[0]
    days = o['days']
    spdays = sorted(d for d in days if days[d]['spend'] > 0)
    first = spdays[0] if spdays else None
    if not first:
        continue
    age = (dd(first) - dd(acc_first[acc])).days if acc in acc_first else None
    c = dict(id=o['id'], name=o['name'], ts=ts, bundle=p['bundle'], vertical=vertical(p['bundle']), geo=geo, tier=tier(geo),
             provider=prov, account=acc, accountAgeDays=age, banned_acc=any(b in acc for b in BANNED),
             first=first, last=spdays[-1], nSpendDays=len(spdays), spend=o['spend'], revenue=o['revenue'], revNet=o['revAdj'],
             profit=o['profitNet'], clicks=o['clicks'], leads=o['leads'], impr=o['impr'], status=o.get('campaignStatus'),
             budgetNow=o.get('budget'), disapproved=o.get('disapproved') or 0, days=days,
             pre_period=(first == '2026-06-01' and p['mmdd'] is not None and p['mmdd'] < '0601'))
    # median daily spend on days with spend >= 0.5
    ds = [days[d]['spend'] for d in spdays if days[d]['spend'] >= 0.5]
    c['medDaily'] = statistics.median(ds) if ds else 0
    # FB video vs static: video views present
    c['fbVideo'] = None
    camps.append(c)

# video flag from raw daily rows (videoViews) -> need to re-read quickly
vid = collections.defaultdict(float)
for f in glob.glob(B + 'raw/cd/*.json'):
    for r in json.load(open(f))['rows']:
        if r.get('videoViews'):
            vid[r['groupId']] += r['videoViews']
for c in camps:
    if c['ts'] == 'FACEBOOK':
        c['fbVideo'] = vid.get(c['id'], 0) > 0

# ---------------- agent packages (article_drafts.rkNames) ----------------
agent_rk = {}
for f in glob.glob(B + 'panel/article_drafts/*.json'):
    d = json.load(open(f)); d = d.get('data', d)
    for rk in d.get('rkNames') or []:
        agent_rk[rk['name']] = dict(package=os.path.basename(f)[:-5], approach=d.get('approach'), vertical=d.get('vertical'), geo=d.get('geo'), at=rk.get('at'))
for c in camps:
    c['agentPkg'] = agent_rk.get(c['name'])

json.dump([{k: v for k, v in c.items() if k != 'days'} for c in camps], open(B + 'raw/camps_enriched.json', 'w'), ensure_ascii=False)
print('camps', len(camps), 'agent rk found', sum(1 for c in camps if c['agentPkg']), 'of', len(agent_rk))

# =============== 1. DYNAMICS ===============
DATA = {'meta': {}}
daytot = {}
for f in sorted(glob.glob(B + 'raw/cd/*.json')):
    day = os.path.basename(f)[:-5]
    j = json.load(open(f)); t = j.get('totalRow') or {}
    daytot[day] = {k: t.get(k, 0) or 0 for k in ('spend', 'revenue', 'revenueAdjusted', 'profitAdjusted', 'clicks', 'trafficSourceLeads', 'impressions', 'conversions', 'locationFee')}
launch = {}
for mth in ('06', '07', '08', '09'):
    for d in json.load(open(B + 'raw/launch_%s.json' % mth))['days']:
        t = d['total']
        launch[d['day']] = dict(campaignsLaunched=t['campaignsLaunched'], creativesLaunched=t['creativesLaunched'], creativesLaunchedUniq=t['creativesLaunchedUniq'],
                                accountsLaunching=t['accountsLaunching'],
                                campFB=d['bySource'].get('FACEBOOK', {}).get('campaignsLaunched', 0), campTT=d['bySource'].get('TIKTOK', {}).get('campaignsLaunched', 0))
# per day by platform + active counts from campaigns
plat_day = collections.defaultdict(lambda: collections.defaultdict(float))
active_day = collections.defaultdict(set)
for c in camps:
    for d, v in c['days'].items():
        plat_day[(d, c['ts'])]['spend'] += v['spend']; plat_day[(d, c['ts'])]['profit'] += v['profitAdjusted']
        plat_day[(d, c['ts'])]['revNet'] += v['revenueAdjusted']; plat_day[(d, c['ts'])]['clicks'] += v['clicks']
        if v['spend'] >= 0.5:
            active_day[d].add(c['id'])
first_by_id = {c['id']: c['first'] for c in camps}


def agg_period(days_list, label):
    s = sum(daytot[d]['spend'] for d in days_list)
    rv = sum(daytot[d]['revenue'] for d in days_list)
    rn = sum(daytot[d]['revenueAdjusted'] for d in days_list)
    p = sum(daytot[d]['profitAdjusted'] for d in days_list)
    cl = sum(daytot[d]['clicks'] for d in days_list)
    ld = sum(daytot[d]['trafficSourceLeads'] for d in days_list)
    im = sum(daytot[d]['impressions'] for d in days_list)
    act = set().union(*[active_day[d] for d in days_list]) if days_list else set()
    newl = [c for c in camps if c['first'] in days_list and not c['pre_period']]
    fb = sum(plat_day[(d, 'FACEBOOK')]['spend'] for d in days_list); tt = sum(plat_day[(d, 'TIKTOK')]['spend'] for d in days_list)
    fbp = sum(plat_day[(d, 'FACEBOOK')]['profit'] for d in days_list); ttp = sum(plat_day[(d, 'TIKTOK')]['profit'] for d in days_list)
    la = [launch.get(d, {}) for d in days_list]
    return dict(period=label, days=len(days_list), spend=r2(s), revenueRaw=r2(rv), revenueNet=r2(rn), profitNet=r2(p), roiNet=roi(p, s),
                profitPerDay=r2(p / len(days_list)) if days_list else None, spendPerDay=r2(s / len(days_list)) if days_list else None,
                clicks=int(cl), leads=int(ld), cpc=r2(s / cl, 3) if cl else None, rpcNet=r2(rn / cl, 3) if cl else None,
                cpl=r2(s / ld, 3) if ld else None, rplNet=r2(rn / ld, 3) if ld else None, cpm=r2(s / im * 1000, 2) if im else None,
                ctr=r2(cl / im * 100, 2) if im else None,
                activeRK=len(act), avgActiveRKperDay=r2(sum(len(active_day[d]) for d in days_list) / len(days_list), 1) if days_list else None,
                newRKwithSpend=len(newl), newRKlaunched_panel=sum(x.get('campaignsLaunched', 0) for x in la),
                creativesLaunched=sum(x.get('creativesLaunched', 0) for x in la), creativesUniq=sum(x.get('creativesLaunchedUniq', 0) for x in la),
                fbSpend=r2(fb), fbRoi=roi(fbp, fb), ttSpend=r2(tt), ttRoi=roi(ttp, tt), ttShare=roi(tt, fb + tt))

alldays = sorted(daytot)
months = collections.OrderedDict()
for d in alldays:
    months.setdefault(d[:7], []).append(d)
weeks = collections.OrderedDict()
for d in alldays:
    weeks.setdefault(week_of(d), []).append(d)
DATA['dynamics_monthly'] = [agg_period(v, k) for k, v in months.items()]
DATA['dynamics_weekly'] = [agg_period(v, 'нед. с ' + k) for k, v in weeks.items()]
DATA['dynamics_total'] = agg_period(alldays, '01.06–24.09')
DATA['dynamics_daily'] = [dict(day=d, spend=r2(daytot[d]['spend']), profitNet=r2(daytot[d]['profitAdjusted']), roiNet=roi(daytot[d]['profitAdjusted'], daytot[d]['spend']),
                               activeRK=len(active_day[d]), launched=launch.get(d, {}).get('campaignsLaunched')) for d in alldays]
for row in DATA['dynamics_monthly']:
    print(row['period'], 'sp', row['spend'], 'p', row['profitNet'], 'roi', row['roiNet'], 'act', row['activeRK'], 'new', row['newRKwithSpend'], 'panel', row['newRKlaunched_panel'], 'cpc', row['cpc'], 'rpc', row['rpcNet'], 'tt', row['ttShare'], row['ttRoi'], 'fb', row['fbRoi'])
for row in DATA['dynamics_weekly']:
    print(row['period'], 'sp', row['spend'], 'p', row['profitNet'], 'roi', row['roiNet'], 'act', row['activeRK'], 'avgAct', row['avgActiveRKperDay'], 'new', row['newRKwithSpend'], 'panel', row['newRKlaunched_panel'], 'uniqCr', row['creativesUniq'], 'cpc', row['cpc'], 'rpc', row['rpcNet'], 'tt%', row['ttShare'], 'ttRoi', row['ttRoi'], 'fbRoi', row['fbRoi'])

# =============== 2. BUNDLES (связки) ===============
def bundle_key(c):
    return (c['vertical'], c['bundle'], c['geo'], c['ts'], c['provider'])

bund = collections.defaultdict(list)
for c in camps:
    bund[bundle_key(c)].append(c)

acc_last = collections.defaultdict(str)
for c in camps:
    acc_last[c['account']] = max(acc_last[c['account']], c['last'])


def bundle_stats(key, cs):
    days = collections.defaultdict(lambda: collections.defaultdict(float))
    for c in cs:
        for d, v in c['days'].items():
            for k in ('spend', 'profitAdjusted', 'revenueAdjusted', 'clicks', 'trafficSourceLeads'):
                days[d][k] += v[k]
    sp = sum(v['spend'] for v in days.values()); p = sum(v['profitAdjusted'] for v in days.values())
    rn = sum(v['revenueAdjusted'] for v in days.values()); cl = sum(v['clicks'] for v in days.values())
    spd = sorted(d for d in days if days[d]['spend'] >= 0.5)
    if not spd:
        spd = sorted(d for d in days if days[d]['spend'] > 0)
    wk = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    for d, v in days.items():
        w = wk[week_of(d)]; w[0] += v['spend']; w[1] += v['profitAdjusted']; w[2] += v['revenueAdjusted']; w[3] += v['clicks']
    peak = max(wk.items(), key=lambda kv: kv[1][1]) if wk else (None, [0, 0, 0, 0])
    last_day = spd[-1] if spd else None
    # last 7 active days
    tail = spd[-7:]
    ts_ = sum(days[d]['spend'] for d in tail); tp = sum(days[d]['profitAdjusted'] for d in tail)
    tr = sum(days[d]['revenueAdjusted'] for d in tail); tc = sum(days[d]['clicks'] for d in tail)
    accs = collections.Counter()
    for c in cs:
        for d in tail:
            if d in c['days']:
                accs[c['account']] += c['days'][d]['spend']
    ban_share = sum(v for a, v in accs.items() if any(b in a for b in BANNED)) / max(ts_, 1e-9)
    live = last_day is not None and last_day >= '2026-09-22'
    if live:
        how = 'жива (спенд 22–24.09)'
    elif ban_share > 0.6 and last_day and '2026-08-12' <= last_day <= '2026-08-17':
        how = 'встала вместе с баном IRNFL 18/19 (14–15.08)'
    elif peak[1][0] > 0 and roi(peak[1][1], peak[1][0]) and roi(peak[1][1], peak[1][0]) >= 20 and (roi(tp, ts_) or 0) < 0:
        how = 'выгорела: ROI с %s%% в пиковую неделю до %s%% за последние 7 дней, выключена' % (roi(peak[1][1], peak[1][0]), roi(tp, ts_))
    elif (roi(tp, ts_) or 0) >= 0:
        how = 'выключена в плюсе (последние 7 дней ROI %s%%)' % roi(tp, ts_)
    else:
        how = 'выключена в минусе (последние 7 дней ROI %s%%)' % roi(tp, ts_)
    return dict(vertical=key[0], bundle=key[1], geo=key[2], platform=key[3], provider=key[4], nRK=len(cs), accounts=sorted({c['account'].split('/')[-1].strip() for c in cs})[:8],
                spend=r2(sp), profitNet=r2(p), roiNet=roi(p, sp), rpcNet=r2(rn / cl, 3) if cl else None, cpc=r2(sp / cl, 3) if cl else None,
                firstDay=spd[0] if spd else None, lastDay=last_day, lifeDays=(dd(last_day) - dd(spd[0])).days + 1 if spd else 0, activeDays=len(spd),
                peakWeek=peak[0], peakWeekSpend=r2(peak[1][0]), peakWeekProfit=r2(peak[1][1]), peakWeekRoi=roi(peak[1][1], peak[1][0]),
                peakWeekRpc=r2(peak[1][2] / peak[1][3], 3) if peak[1][3] else None,
                last7Spend=r2(ts_), last7Roi=roi(tp, ts_), last7Rpc=r2(tr / tc, 3) if tc else None, bannedAccShareLast7=r2(ban_share * 100, 0), end=how,
                weekly=[dict(week=w, spend=r2(v[0]), profit=r2(v[1]), roi=roi(v[1], v[0])) for w, v in sorted(wk.items()) if v[0] >= 1])

BST = [bundle_stats(k, v) for k, v in bund.items()]
top_profit = sorted(BST, key=lambda x: -x['profitNet'])[:15]
top_loss = sorted(BST, key=lambda x: x['profitNet'])[:15]
DATA['bundles_top15_profit'] = top_profit
DATA['bundles_top15_loss'] = top_loss
pos = [b for b in BST if b['profitNet'] > 0]
DATA['bundles_summary'] = dict(nBundles=len(BST), nProfitable=len(pos), profitFromProfitable=r2(sum(b['profitNet'] for b in pos)),
                               lossFromLosing=r2(sum(b['profitNet'] for b in BST if b['profitNet'] < 0)),
                               top5ShareOfGrossProfit=roi(sum(b['profitNet'] for b in sorted(pos, key=lambda x: -x['profitNet'])[:5]), sum(b['profitNet'] for b in pos)),
                               top15ProfitSum=r2(sum(b['profitNet'] for b in top_profit)))
print(DATA['bundles_summary'])
for b in top_profit:
    print('%-16s %-24s %-5s %-2s %-7s n%3d sp %6.0f p %5.0f roi %5.1f rpc %s | %s..%s (%sd) peak %s %s%% | %s' % (b['vertical'][:16], b['bundle'][:24], b['geo'], b['platform'][:2], b['provider'], b['nRK'], b['spend'], b['profitNet'], b['roiNet'], b['rpcNet'], b['firstDay'], b['lastDay'], b['lifeDays'], b['peakWeek'], b['peakWeekRoi'], b['end']))
print('--- loss')
for b in top_loss:
    print('%-16s %-24s %-5s %-2s %-7s n%3d sp %6.0f p %5.0f roi %5.1f rpc %s | %s..%s | %s' % (b['vertical'][:16], b['bundle'][:24], b['geo'], b['platform'][:2], b['provider'], b['nRK'], b['spend'], b['profitNet'], b['roiNet'], b['rpcNet'], b['firstDay'], b['lastDay'], b['end']))

# pre/post ban split for top bundles
BAN_DAY = '2026-08-15'
def split_ban(key):
    cs = bund[key]
    pre = [0, 0]; post = [0, 0]; pre_ban_acc = [0, 0]
    for c in cs:
        for d, v in c['days'].items():
            tgt = pre if d < BAN_DAY else post
            tgt[0] += v['spend']; tgt[1] += v['profitAdjusted']
            if d < BAN_DAY and c['banned_acc']:
                pre_ban_acc[0] += v['spend']; pre_ban_acc[1] += v['profitAdjusted']
    return dict(preBanSpend=r2(pre[0]), preBanRoi=roi(pre[1], pre[0]), preBanProfit=r2(pre[1]), postBanSpend=r2(post[0]), postBanRoi=roi(post[1], post[0]), postBanProfit=r2(post[1]),
                preBanSpendInBannedAccs=r2(pre_ban_acc[0]))
for b in DATA['bundles_top15_profit'] + DATA['bundles_top15_loss']:
    b.update(split_ban((b['vertical'], b['bundle'], b['geo'], b['platform'], b['provider'])))


def relabel(b):
    key = (b['vertical'], b['bundle'], b['geo'], b['platform'], b['provider'])
    s = p_ = 0.0
    for c in bund[key]:
        for d, v in c['days'].items():
            if d >= '2026-09-19':
                s += v['spend']; p_ += v['profitAdjusted']
    b['spend_19_24'] = r2(s); b['roi_19_24'] = roi(p_, s)
    pre, post = b['preBanSpend'] or 0, b['postBanSpend'] or 0
    if b['lastDay'] and b['lastDay'] >= '2026-09-22':
        if s >= 5 and (roi(p_, s) or 0) <= -50:
            b['end'] = 'формально жива, но с 19.09 статья не платит: 19–24.09 спенд $%s, ROI %s%%' % (r2(s), roi(p_, s))
        else:
            b['end'] = 'жива: 19–24.09 спенд $%s, ROI %s%% (выручка 22–24.09 доезжает)' % (r2(s), roi(p_, s))
        if pre >= 0.6 * (pre + post) and b['preBanRoi'] is not None and b['preBanRoi'] >= 20 and (b['postBanRoi'] or -999) < b['preBanRoi'] - 15:
            b['end'] = 'после бана IRNFL 18/19 не восстановилась: ROI до 15.08 %s%% на $%s → после %s%% на $%s; ' % (b['preBanRoi'], round(pre), b['postBanRoi'], round(post)) + b['end']
    elif b['lastDay'] and b['lastDay'] >= '2026-08-12' and pre >= 0.6 * (pre + post) and b['preBanRoi'] is not None and b['preBanRoi'] >= 20 and (b['postBanRoi'] is None or b['postBanRoi'] < b['preBanRoi'] - 15):
        b['end'] = 'умерла после бана IRNFL 18/19: ROI до 15.08 %s%% на $%s → после %s%% на $%s; ' % (b['preBanRoi'], round(pre), b['postBanRoi'], round(post)) + b['end']
for b in DATA['bundles_top15_profit'] + DATA['bundles_top15_loss']:
    relabel(b)

# =============== 3. LOSSES ===============
def rule_trigger(c):
    """Первый день (конец дня), когда по закрытым дням правило владельца велело выключить.
    R12: лайфтайм спенд >= $10, лайфтайм ROI < 0 и ROI дня не лучше прошлого дня со спендом.
    R4: 3 дня подряд со спендом и выручкой 0 при спенде за серию >= $3.
    R11(мягко): спенд за 3 последних дня со спендом >= $7 и ROI этих 3 дней < 0."""
    days = c['days']; seq = sorted(d for d in days if days[d]['spend'] > 0 or days[d]['revenueAdjusted'] > 0)
    cs = cp = 0; prev_roi = None; spd = []
    for d in seq:
        v = days[d]; cs += v['spend']; cp += v['profitAdjusted']
        droi = v['profitAdjusted'] / v['spend'] if v['spend'] > 0 else None
        if v['spend'] > 0:
            spd.append(d)
        if cs >= 10 and cp < 0 and droi is not None and prev_roi is not None and droi <= prev_roi:
            return d, 'R12'
        last3 = spd[-3:]
        if len(last3) == 3:
            s3 = sum(days[x]['spend'] for x in last3); r3 = sum(days[x]['revenueAdjusted'] for x in last3); p3 = sum(days[x]['profitAdjusted'] for x in last3)
            if s3 >= 3 and r3 == 0:
                return d, 'R4'
            if s3 >= 7 and p3 < 0:
                return d, 'R11'
        if droi is not None:
            prev_roi = droi
    return None, None

for c in camps:
    t, rule = rule_trigger(c)
    c['trigger'] = t; c['triggerRule'] = rule
    if t:
        after = [d for d in c['days'] if d > t]
        c['afterSpend'] = sum(c['days'][d]['spend'] for d in after)
        c['afterProfit'] = sum(c['days'][d]['profitAdjusted'] for d in after)
    else:
        c['afterSpend'] = c['afterProfit'] = 0.0

reasons = collections.defaultdict(lambda: dict(loss=0.0, n=0, spend=0.0))
loss_rows = []
for c in camps:
    if c['profit'] >= 0:
        continue
    if c['ts'] == 'TIKTOK' and c['spend'] > 0 and c['revNet'] / c['spend'] < 0.15:
        parts = [('TT без выручки (выручка < 15% спенда)', c['profit'])]
    elif c['disapproved'] > 0 or (c['banned_acc'] and c['last'] >= '2026-08-12' and c['last'] <= '2026-08-16' and c['first'] >= '2026-08-08'):
        parts = [('бан/отклонения (отклонённые объявления или тест, оборванный баном IRNFL 18/19)', c['profit'])]
    else:
        held = min(0.0, c['afterProfit']) if c['trigger'] else 0.0
        held = max(held, c['profit'])  # не больше всего убытка
        parts = []
        if held < 0:
            parts.append(('держали слишком долго (минус после сигнала правила)', held))
        rest = c['profit'] - held
        if rest < 0:
            parts.append(('тест не взлетел (минус до сигнала правила)', rest))
    for name, val in parts:
        reasons[name]['loss'] += val; reasons[name]['n'] += 1; reasons[name]['spend'] += c['spend']
    loss_rows.append(c)

# give-back: profitable campaigns that burned after their cumulative peak
giveback = 0.0; gb_n = 0; gb_list = []
for c in camps:
    if c['profit'] <= 0:
        continue
    cum = 0; peak = 0
    for d in sorted(c['days']):
        cum += c['days'][d]['profitAdjusted']; peak = max(peak, cum)
    gb = peak - cum
    if gb > 0.5:
        giveback += gb; gb_n += 1; gb_list.append((gb, c['name'], c['profit'], peak))
reasons_out = [dict(reason=k, lossNet=r2(v['loss']), nRK=v['n'], spendOfThoseRK=r2(v['spend'])) for k, v in sorted(reasons.items(), key=lambda kv: kv[1]['loss'])]
total_loss = sum(c['profit'] for c in camps if c['profit'] < 0)
total_win = sum(c['profit'] for c in camps if c['profit'] > 0)
DATA['losses'] = dict(
    note='Убыток по РК с отрицательной чистой прибылью за 01.06–24.09. Приоритет классификации: TT без выручки → бан/отклонения → разделение минуса на «до сигнала правила» (тест) и «после сигнала» (держали). Сигнал правила — по закрытым дням: R12 (лайфтайм ≥ $10, ROI < 0, день не лучше прошлого), R4 (3 дня выручка 0 при ≥ $3), R11 мягкий (3 дня ≥ $7 и ROI < 0).',
    nLosingRK=len(loss_rows), totalLossNet=r2(total_loss), nWinningRK=sum(1 for c in camps if c['profit'] > 0), totalWinNet=r2(total_win),
    byReason=reasons_out,
    giveBackFromWinners=dict(note='Прибыльные РК, которые после пика накопленной прибыли отдали часть обратно (держали после выгорания)', amount=r2(giveback), nRK=gb_n,
                             top=[dict(name=n, finalProfit=r2(p), peakProfit=r2(pk), givenBack=r2(g)) for g, n, p, pk in sorted(gb_list, reverse=True)[:10]]),
    top15_campaigns_by_loss=[dict(name=c['name'], vertical=c['vertical'], geo=c['geo'], ts=c['ts'], account=c['account'], first=c['first'], last=c['last'],
                                  spend=r2(c['spend']), revenueNet=r2(c['revNet']), profitNet=r2(c['profit']), roiNet=roi(c['profit'], c['spend']),
                                  ruleSignal=c['trigger'], ruleName=c['triggerRule'], spendAfterSignal=r2(c['afterSpend']), profitAfterSignal=r2(c['afterProfit']))
                             for c in sorted(camps, key=lambda x: x['profit'])[:15]])
print('LOSS total', r2(total_loss), 'n', len(loss_rows), 'WIN', r2(total_win))
for r in reasons_out: print(r)
print('giveback', r2(giveback), gb_n)
for x in DATA['losses']['top15_campaigns_by_loss']: print(x['name'][:62], x['spend'], x['profitNet'], x['roiNet'], x['ruleSignal'], x['ruleName'], x['spendAfterSignal'], x['profitAfterSignal'])

# =============== 4. COHORTS ===============
# proven vs new: была ли у той же связки (bundle+платформа) прибыль до запуска
bp_days = collections.defaultdict(lambda: collections.defaultdict(lambda: [0.0, 0.0]))
for c in camps:
    k = (c['bundle'], c['ts'])
    for d, v in c['days'].items():
        x = bp_days[k][d]; x[0] += v['spend']; x[1] += v['profitAdjusted']

def proven(c):
    k = (c['bundle'], c['ts'])
    start = dd(c['first']) - datetime.timedelta(days=14)
    s = p = 0.0
    for d, (sp_, pr) in bp_days[k].items():
        if start.isoformat() <= d < c['first']:
            s += sp_; p += pr
    return s >= 20 and p > 10 and p / s >= 0.2

for c in camps:
    c['proven'] = proven(c)
    f3 = [(dd(c['first']) + datetime.timedelta(days=i)).isoformat() for i in range(3)]
    c['p3'] = sum(c['days'][d]['profitAdjusted'] for d in f3 if d in c['days'])
    c['s3'] = sum(c['days'][d]['spend'] for d in f3 if d in c['days'])
    c['f3closed'] = f3[-1] <= LAST_CLOSED_FINAL

def cohort_stats(cs, label):
    cs = [c for c in cs if c['spend'] >= 0.5]
    if not cs:
        return dict(cohort=label, n=0)
    closed = [c for c in cs if c['f3closed']]
    stopped = [c for c in cs if c['last'] < '2026-09-22']
    sp = sum(c['spend'] for c in cs); p = sum(c['profit'] for c in cs)
    winners = [c for c in cs if c['profit'] >= 20 and roi(c['profit'], c['spend']) >= 30]
    return dict(cohort=label, launchedWithSpend=len(cs), spend=r2(sp), profitNet=r2(p), roiNet=roi(p, sp),
                pctPlusFirst3Days=roi(sum(1 for c in closed if c['p3'] > 0), len(closed)) if closed else None, nWithClosed3Days=len(closed),
                roiFirst3Days=roi(sum(c['p3'] for c in closed), sum(c['s3'] for c in closed)) if closed else None,
                pctPlusLifetime=roi(sum(1 for c in cs if c['profit'] > 0), len(cs)),
                avgSpendUntilOff=r2(sum(c['spend'] for c in stopped) / len(stopped)) if stopped else None,
                medianSpendUntilOff=r2(statistics.median([c['spend'] for c in stopped])) if stopped else None,
                nWinners_ge20usd_roi30=len(winners), winnersProfit=r2(sum(c['profit'] for c in winners)),
                bestRK=max(cs, key=lambda c: c['profit'])['name'], bestRKprofit=r2(max(c['profit'] for c in cs)),
                avgRKperBundleLaunch=None)

coh = collections.OrderedDict()
for c in sorted(camps, key=lambda c: c['first']):
    lab = 'до 01.06' if c['pre_period'] else week_of(c['first'])
    coh.setdefault(lab, []).append(c)
DATA['cohorts_by_launch_week'] = []
for k, cs in coh.items():
    row = cohort_stats(cs, k)
    if k != 'до 01.06':
        wd = weeks.get(k, [])
        row['launchedInPanel_all'] = sum(launch.get(d, {}).get('campaignsLaunched', 0) for d in wd)
        row['creativesUniq'] = sum(launch.get(d, {}).get('creativesLaunchedUniq', 0) for d in wd)
    DATA['cohorts_by_launch_week'].append(row)
    print(k, {x: row.get(x) for x in ('launchedWithSpend', 'launchedInPanel_all', 'spend', 'profitNet', 'roiNet', 'pctPlusFirst3Days', 'roiFirst3Days', 'pctPlusLifetime', 'avgSpendUntilOff', 'nWinners_ge20usd_roi30')})

# AI-era split
era = [c for c in camps if c['first'] >= '2026-09-16']
DATA['cohort_ai_era'] = dict(
    note='С 16.09 решения по заливам принимаются вместе с агентами (said_log с 16.09). Пакеты главного (article_drafts.rkNames) залиты 23–24.09 — у них 0–1 закрытый день, выручка RSOC за 22–24.09 ещё доезжает.',
    all_since_16_09=cohort_stats(era, 'все запуски с 16.09'),
    agent_packages_23_24=cohort_stats([c for c in era if c['agentPkg']], 'пакеты главного 23–24.09'),
    other_since_16_09=cohort_stats([c for c in era if not c['agentPkg']], 'прочие запуски 16–24.09'),
    agent_by_approach={a: cohort_stats([c for c in era if c['agentPkg'] and c['agentPkg']['approach'] == a], a) for a in sorted({c['agentPkg']['approach'] for c in era if c['agentPkg']})},
    agent_rk_list=[dict(name=c['name'], package=c['agentPkg']['package'], approach=c['agentPkg']['approach'], first=c['first'], spend=r2(c['spend']), revenueNet=r2(c['revNet']), profitNet=r2(c['profit'])) for c in era if c['agentPkg']],
    agent_packages_launched_total=len({v['package'] for v in agent_rk.values()}), agent_rk_launched_total=len(agent_rk),
    agent_rk_with_any_spend=sum(1 for c in era if c['agentPkg']),
    since_16_09_by_bundle=sorted([dict(bundle=k, nRK=len(v), spend=r2(sum(c['spend'] for c in v)), profitNet=r2(sum(c['profit'] for c in v)), roiNet=roi(sum(c['profit'] for c in v), sum(c['spend'] for c in v)))
                                   for k, v in collections.OrderedDict((b, [c for c in era if c['bundle'] == b]) for b in {c['bundle'] for c in era}).items()], key=lambda x: -x['spend']))
for k in ('all_since_16_09', 'agent_packages_23_24', 'other_since_16_09'):
    print(k, DATA['cohort_ai_era'][k])
print(DATA['cohort_ai_era']['agent_by_approach'])
for x in DATA['cohort_ai_era']['since_16_09_by_bundle']: print(x)

# proven vs new (весь период, только запуски с закрытыми 3 днями)
pv = [c for c in camps if not c['pre_period']]
DATA['proven_vs_new'] = dict(
    note='«Проверенная связка» = у той же связки (бандл статьи + платформа) за 14 дней до запуска РК было ≥ $20 спенда и чистый ROI ≥ +20%. Остальное — новая связка/угол или клон неработающей.',
    proven=cohort_stats([c for c in pv if c['proven']], 'клон проверенной связки'),
    new=cohort_stats([c for c in pv if not c['proven']], 'новая связка / клон слабой'),
    by_month={m_: dict(proven=cohort_stats([c for c in pv if c['proven'] and c['first'][:7] == m_], 'proven ' + m_), new=cohort_stats([c for c in pv if not c['proven'] and c['first'][:7] == m_], 'new ' + m_)) for m_ in ('2026-06', '2026-07', '2026-08', '2026-09')})
print('PROVEN', DATA['proven_vs_new']['proven'])
print('NEW', DATA['proven_vs_new']['new'])
for m_, v in DATA['proven_vs_new']['by_month'].items(): print(m_, 'proven', v['proven'].get('launchedWithSpend'), v['proven'].get('roiNet'), v['proven'].get('pctPlusFirst3Days'), '| new', v['new'].get('launchedWithSpend'), v['new'].get('roiNet'), v['new'].get('pctPlusFirst3Days'))

# =============== 5. CUTS ===============
def cut(cs, keyf, label, min_spend=0):
    g = collections.defaultdict(list)
    for c in cs:
        k = keyf(c)
        if k is not None:
            g[k].append(c)
    out = []
    for k, v in g.items():
        sp = sum(c['spend'] for c in v); p = sum(c['profit'] for c in v); cl = sum(c['clicks'] for c in v); rn = sum(c['revNet'] for c in v); ld = sum(c['leads'] for c in v)
        if sp < min_spend:
            continue
        out.append(dict(group=k, nRK=len(v), spend=r2(sp), profitNet=r2(p), roiNet=roi(p, sp), cpc=r2(sp / cl, 3) if cl else None, rpcNet=r2(rn / cl, 3) if cl else None,
                        rplNet=r2(rn / ld, 3) if ld else None, pctRKinPlus=roi(sum(1 for c in v if c['profit'] > 0), len(v)),
                        pctPlusFirst3=roi(sum(1 for c in v if c['f3closed'] and c['p3'] > 0), sum(1 for c in v if c['f3closed'])) if any(c['f3closed'] for c in v) else None))
    return dict(cut=label, rows=sorted(out, key=lambda x: -x['spend']))

def budget_bucket(c):
    if c['ts'] != 'FACEBOOK' or c['medDaily'] <= 0:
        return None
    m_ = c['medDaily']
    if m_ <= 6: return 'FB ≈$5/день (медиана дневного спенда ≤ $6)'
    if m_ <= 12: return 'FB ≈$10/день ($6–12)'
    if m_ <= 25: return 'FB ≈$15–20/день ($12–25)'
    return 'FB > $25/день'

def acc_age(c):
    if c['accountAgeDays'] is None: return None
    if c['account'] and acc_first.get(c['account']) == '2026-06-01':
        return 'старый аккаунт (был до 01.06)'
    return 'новый аккаунт (РК в первые 14 дней аккаунта)' if c['accountAgeDays'] <= 14 else 'аккаунт 15+ дней'

def platform_period(c):
    return c['ts']

recent = [c for c in camps if c['last'] >= '2026-08-25']
def period_slice(cs, d1, d2):
    """пересчёт РК только по дням в окне"""
    res = []
    for c in cs:
        ds = {d: v for d, v in c['days'].items() if d1 <= d <= d2}
        if not ds:
            continue
        x = dict(c); x['days'] = ds
        x['spend'] = sum(v['spend'] for v in ds.values()); x['profit'] = sum(v['profitAdjusted'] for v in ds.values())
        x['clicks'] = sum(v['clicks'] for v in ds.values()); x['revNet'] = sum(v['revenueAdjusted'] for v in ds.values()); x['leads'] = sum(v['trafficSourceLeads'] for v in ds.values())
        if x['spend'] > 0:
            res.append(x)
    return res

last30 = period_slice(camps, '2026-08-25', '2026-09-24')
cuts = {}
for nm, cs in (('весь период 01.06–24.09', camps), ('последние 30 дней 25.08–24.09', last30)):
    cuts[nm] = [
        cut(cs, lambda c: c['ts'], 'FB против TT'),
        cut(cs, lambda c: c['provider'], 'провайдер'),
        cut(cs, lambda c: c['vertical'], 'вертикаль'),
        cut(cs, lambda c: c['tier'], 'гео tier'),
        cut(cs, budget_bucket, 'бюджет FB (прокси: медиана дневного спенда РК)'),
        cut(cs, acc_age, 'возраст аккаунта'),
        cut(cs, lambda c: ('FB видео' if c['fbVideo'] else 'FB статика') if c['ts'] == 'FACEBOOK' else None, 'тип крео FB (видео = есть просмотры видео)'),
        cut(cs, lambda c: 'IRNFL 18/19 (забанены 14–15.08)' if c['banned_acc'] else 'остальные аккаунты', 'забаненные аккаунты'),
        cut(cs, lambda c: c['geo'], 'гео (топ по спенду)', min_spend=150),
    ]
DATA['cuts'] = cuts
for nm, lst in cuts.items():
    print('=====', nm)
    for ct in lst:
        print('--', ct['cut'])
        for r in ct['rows'][:14]:
            print('   %-48s n%4d sp %8.0f p %6.0f roi %6.1f cpc %s rpc %s rpl %s plus%% %s plus3 %s' % (str(r['group'])[:48], r['nRK'], r['spend'], r['profitNet'], r['roiNet'] or 0, r['cpc'], r['rpcNet'], r['rplNet'], r['pctRKinPlus'], r['pctPlusFirst3']))

# =============== 6. WHAT PROFITABLE PERIODS HAD ===============
def window(d1, d2, label):
    dl = [d for d in alldays if d1 <= d <= d2]
    base = agg_period(dl, label)
    cs = period_slice(camps, d1, d2)
    sp = sum(c['spend'] for c in cs)
    # концентрация
    by_rk = sorted([c['spend'] for c in cs], reverse=True)
    bb = collections.defaultdict(lambda: [0.0, 0.0])
    for c in cs:
        x = bb[(c['bundle'], c['ts'])]; x[0] += c['spend']; x[1] += c['profit']
    bsorted = sorted(bb.items(), key=lambda kv: -kv[1][0])
    hhi = sum((v[0] / sp) ** 2 for _, v in bb.items()) * 10000 if sp else None
    prof_sorted = sorted(bb.items(), key=lambda kv: -kv[1][1])
    gross = sum(v[1] for _, v in bb.items() if v[1] > 0)
    fb = [c for c in cs if c['ts'] == 'FACEBOOK']
    fbsp = sum(c['spend'] for c in fb)
    base.update(dict(
        nBundlesWithSpend10=sum(1 for _, v in bb.items() if v[0] >= 10),
        top5RKshareOfSpend=roi(sum(by_rk[:5]), sp), top1BundleShareOfSpend=roi(bsorted[0][1][0], sp) if bsorted else None,
        top1Bundle='%s/%s' % bsorted[0][0] if bsorted else None,
        top1BundleShareOfGrossProfit=roi(prof_sorted[0][1][1], gross) if prof_sorted and gross else None,
        top1ProfitBundle='%s/%s' % prof_sorted[0][0] if prof_sorted else None,
        hhiBundles=r2(hhi, 0),
        spendPerActiveRKperDay=r2(sp / sum(len(active_day[d]) for d in dl), 2) if dl and sum(len(active_day[d]) for d in dl) else None,
        launchesPerDay=r2(base['newRKlaunched_panel'] / len(dl), 1) if dl else None,
        shareSpendProvenClones=roi(sum(c['spend'] for c in cs if c['proven']), sp),
        shareSpendTier1=roi(sum(c['spend'] for c in cs if c['tier'] == 'tier1'), sp),
        shareFbSpendVideo=roi(sum(c['spend'] for c in fb if c['fbVideo']), fbsp) if fbsp else None,
        shareSpendRKatLeast10perDay=roi(sum(c['spend'] for c in cs if c['medDaily'] >= 6), sp),
        shareSpendBannedAccs=roi(sum(c['spend'] for c in cs if c['banned_acc']), sp),
        topProfitBundles=[dict(bundle='%s/%s' % k, spend=r2(v[0]), profit=r2(v[1]), roi=roi(v[1], v[0])) for k, v in prof_sorted[:5]]))
    return base

W = [('2026-07-06', '2026-07-19', 'пик 1: 06–19.07'), ('2026-08-24', '2026-09-06', 'пик 2: 24.08–06.09'), ('2026-09-12', '2026-09-18', 'пик 3 (BR): 12–18.09'),
     ('2026-08-03', '2026-08-09', 'провал: 03–09.08'), ('2026-09-19', '2026-09-24', 'сейчас: 19–24.09 (выручка 22–24.09 доезжает)')]
DATA['periods_compare'] = [window(a, b, l) for a, b, l in W]
for w in DATA['periods_compare']:
    print(w['period'], {k: w.get(k) for k in ('spendPerDay', 'profitPerDay', 'roiNet', 'cpc', 'rpcNet', 'cpl', 'rplNet', 'ctr', 'cpm', 'avgActiveRKperDay', 'launchesPerDay', 'spendPerActiveRKperDay', 'nBundlesWithSpend10', 'top5RKshareOfSpend', 'top1BundleShareOfSpend', 'top1Bundle', 'top1BundleShareOfGrossProfit', 'top1ProfitBundle', 'hhiBundles', 'shareSpendProvenClones', 'shareSpendTier1', 'shareFbSpendVideo', 'shareSpendRKatLeast10perDay', 'ttShare', 'ttRoi', 'fbRoi', 'creativesUniq')})

# article concentration from article windows
def art_summary(fn, label):
    d = json.load(open(B + 'raw/' + fn)); rc = d.get('rowsCommon', {}); tr = d.get('totalRow', {})
    rows = [{**rc, **r} for r in d['rows']]
    gross = sum(max(0, r.get('profitAdjusted', 0)) for r in rows)
    out = []
    for r in rows[:8]:
        a = r.get('article') or {}
        out.append(dict(article=a.get('title', '')[:90], bucket=a.get('keyword'), spend=r2(r['spend']), profitNet=r2(r.get('profitAdjusted')), roiNet=roi(r.get('profitAdjusted', 0), r['spend']),
                        rpcNet=r2(r.get('revenueAdjusted', 0) / r['clicks'], 3) if r.get('clicks') else None))
    top = max(rows, key=lambda r: r.get('profitAdjusted', 0))
    return dict(window=label, spend=r2(tr.get('spend')), profitNet=r2(tr.get('profitAdjusted')), roiNet=roi(tr.get('profitAdjusted', 0), tr.get('spend', 0)),
                nArticles=d.get('total'), topArticleShareOfGrossProfit=roi(top.get('profitAdjusted', 0), gross), topArticle=(top.get('article') or {}).get('title', '')[:90], rows=out)
DATA['articles_compare'] = [art_summary('art_0817_0903.json', '17.08–03.09 (пик 2)'), art_summary('art_0915_0918.json', '15–18.09 (пик 3, до 19.09)'),
                            art_summary('art_0919_0921.json', '19–21.09 (после 19.09)'), art_summary('art_0910_0924.json', '10–24.09')]
for a in DATA['articles_compare']:
    print(a['window'], a['spend'], a['profitNet'], a['roiNet'], 'top share', a['topArticleShareOfGrossProfit'], a['topArticle'][:60])

# =============== 7. DECISION SPEED ===============
trig = [c for c in camps if c['trigger']]
burn = [c for c in trig if c['afterProfit'] < 0]
saved = [c for c in trig if c['afterProfit'] > 0]
by_month_burn = collections.defaultdict(lambda: [0.0, 0, 0.0])
for c in burn:
    x = by_month_burn[c['trigger'][:7]]; x[0] += c['afterProfit']; x[1] += 1; x[2] += c['afterSpend']
# days from signal to last spend
lag = [(dd(c['last']) - dd(c['trigger'])).days for c in burn]
# too-early kills: stopped (last < 22.09) with lifetime spend < $5 and < 3 spend days
stopped = [c for c in camps if c['last'] < '2026-09-22' and not c['pre_period']]
def per_period(cs, d1, d2):
    x = [c for c in cs if d1 <= c['first'] <= d2]
    if not x: return None
    return dict(n=len(x), avgSpendUntilOff=r2(sum(c['spend'] for c in x) / len(x)), medianSpendUntilOff=r2(statistics.median([c['spend'] for c in x])),
                pctKilledBelow5usd=roi(sum(1 for c in x if c['spend'] < 5), len(x)), pctReached10usd=roi(sum(1 for c in x if c['spend'] >= 10), len(x)))
kill_speed = {k: per_period(stopped, a, b) for k, (a, b) in {'июнь': ('2026-06-01', '2026-06-30'), 'июль': ('2026-07-01', '2026-07-31'), 'август': ('2026-08-01', '2026-08-31'),
                                                              '01–15.09': ('2026-09-01', '2026-09-15'), '16–21.09 (с агентами)': ('2026-09-16', '2026-09-21')}.items()}
# winners: how many would R1 "$2 & ROI<=0 за день" have killed on day 1 (по финальной выручке, т.е. мягче реального внутридневного)
winners = [c for c in camps if c['profit'] >= 20 and roi(c['profit'], c['spend']) >= 30 and not c['pre_period']]
def first_day_bad(c):
    d0 = c['first']; v = c['days'][d0]
    return v['spend'] >= 2 and v['profitAdjusted'] <= 0
w_bad = [c for c in winners if first_day_bad(c)]
def first_two_bad(c):
    seq = sorted(d for d in c['days'] if c['days'][d]['spend'] > 0)[:2]
    s = sum(c['days'][d]['spend'] for d in seq); p = sum(c['days'][d]['profitAdjusted'] for d in seq)
    return p <= 0
w_bad2 = [c for c in winners if first_two_bad(c)]
# ранние выключения клонов связок, которые у других клонов стали победителями
bundle_win = collections.defaultdict(list)
for c in winners:
    bundle_win[(c['bundle'], c['ts'])].append(c)
early_killed = [c for c in stopped if c['spend'] < 5 and (c['bundle'], c['ts']) in bundle_win]
given10 = [c for c in camps if c['spend'] >= 10 and (c['bundle'], c['ts']) in bundle_win and not c['pre_period']]
win_rate_given10 = sum(1 for c in given10 if c in winners) / len(given10) if given10 else 0
med_win_profit = statistics.median([c['profit'] for c in winners]) if winners else 0
DATA['decision_speed'] = dict(
    note='Сигнал правила — по финальной (доехавшей) выручке закрытых дней, т.е. с оглядкой назад: реальная внутридневная картина хуже (выручка RSOC доезжает до D+3).',
    rkWithRuleSignal=len(trig),
    burnedAfterSignal=dict(amount=r2(sum(c['afterProfit'] for c in burn)), nRK=len(burn), spendAfterSignal=r2(sum(c['afterSpend'] for c in burn)),
                           medianDaysSignalToStop=statistics.median(lag) if lag else None,
                           byMonth={k: dict(lossNet=r2(v[0]), nRK=v[1], spend=r2(v[2])) for k, v in sorted(by_month_burn.items())}),
    earnedAfterSignal_ruleWouldBeWrong=dict(amount=r2(sum(c['afterProfit'] for c in saved)), nRK=len(saved),
                                            top=[dict(name=c['name'], signal=c['trigger'], profitAfter=r2(c['afterProfit'])) for c in sorted(saved, key=lambda x: -x['afterProfit'])[:8]]),
    netEffectOfStrictRule=r2(-sum(c['afterProfit'] for c in trig)),
    killSpeedByLaunchPeriod=kill_speed,
    winners=dict(n=len(winners), profit=r2(sum(c['profit'] for c in winners)), medianProfit=r2(med_win_profit),
                 firstDayLossAt2usd=len(w_bad), firstDayLossAt2usd_profit=r2(sum(c['profit'] for c in w_bad)),
                 firstTwoDaysNonPositive=len(w_bad2), firstTwoDaysNonPositive_profit=r2(sum(c['profit'] for c in w_bad2)),
                 note='Сколько будущих победителей (лайфтайм ≥ $20 чистыми и ROI ≥ 30%) в первый день при спенде ≥ $2 были в минусе даже по ФИНАЛЬНОЙ выручке — их убило бы правило «$2 и ROI ≤ 0».'),
    earlyKilledClonesOfWinningBundles=dict(n=len(early_killed), spend=r2(sum(c['spend'] for c in early_killed)), winRateWhenGiven10usd=roi(win_rate_given10, 1),
                                           expectedMissedWinners=r2(len(early_killed) * win_rate_given10, 1), expectedMissedProfit=r2(len(early_killed) * win_rate_given10 * med_win_profit),
                                           note='Клоны связок, где были победители, выключенные до $5. Ожидание = доля победителей среди клонов этих же связок, получивших ≥ $10, × медианная прибыль победителя. Оценка, не факт.'))
print(json.dumps(DATA['decision_speed'], ensure_ascii=False, indent=0)[:3500])

# =============== bans / accounts ===============
def acc_window(pred, d1, d2):
    s = p = 0.0
    for c in camps:
        if pred(c):
            for d, v in c['days'].items():
                if d1 <= d <= d2:
                    s += v['spend']; p += v['profitAdjusted']
    nd = (dd(d2) - dd(d1)).days + 1
    return dict(spend=r2(s), profit=r2(p), roi=roi(p, s), spendPerDay=r2(s / nd), profitPerDay=r2(p / nd))
acc_rows = collections.defaultdict(lambda: dict(spend=0.0, profit=0.0, n=0, first='9', last='0', ts=set(), disapproved=0))
for c in camps:
    x = acc_rows[c['account']]; x['spend'] += c['spend']; x['profit'] += c['profit']; x['n'] += 1
    x['first'] = min(x['first'], c['first']); x['last'] = max(x['last'], c['last']); x['ts'].add(c['ts']); x['disapproved'] += c['disapproved']
DATA['accounts'] = dict(
    note='IRNFL Account 18 и 19 перестали откручивать 14–15.08 (владелец 23.09: «18 и 19 в бане»). Отклонённых объявлений по трекеру всего %d (в %d РК).' % (sum(c['disapproved'] for c in camps), sum(1 for c in camps if c['disapproved'])),
    banned_18_19_before_ban_01_14_08=acc_window(lambda c: c['banned_acc'], '2026-08-01', '2026-08-14'),
    portfolio_01_14_08=acc_window(lambda c: True, '2026-08-01', '2026-08-14'),
    portfolio_16_29_08=acc_window(lambda c: True, '2026-08-16', '2026-08-29'),
    banned_18_19_total=acc_window(lambda c: c['banned_acc'], '2026-06-01', '2026-09-24'),
    rows=sorted([dict(account=k, spend=r2(v['spend']), profitNet=r2(v['profit']), roiNet=roi(v['profit'], v['spend']), nRK=v['n'], first=v['first'], last=v['last'],
                      ts='/'.join(sorted(t[:2] for t in v['ts'])), disapproved=v['disapproved']) for k, v in acc_rows.items()], key=lambda x: -x['spend']))
print(DATA['accounts']['banned_18_19_before_ban_01_14_08'], DATA['accounts']['portfolio_01_14_08'], DATA['accounts']['portfolio_16_29_08'])

# winners concentration
winners_all = [c for c in camps if c['profit'] >= 20 and roi(c['profit'], c['spend']) >= 30]
DATA['winners'] = dict(
    definition='победитель = РК с чистой прибылью ≥ $20 и ROI ≥ +30% за жизнь',
    n=len(winners_all), nAll=len(camps), profit=r2(sum(c['profit'] for c in winners_all)), portfolioProfit=r2(sum(c['profit'] for c in camps)),
    spend=r2(sum(c['spend'] for c in winners_all)),
    restProfit=r2(sum(c['profit'] for c in camps) - sum(c['profit'] for c in winners_all)), restSpend=r2(sum(c['spend'] for c in camps) - sum(c['spend'] for c in winners_all)),
    pctWinnersPositiveFirst3Days=roi(sum(1 for c in winners if c['p3'] > 0), len(winners)),
    launchesPerWinnerByMonth={m_: r2(sum(1 for c in camps if c['first'][:7] == m_ and c['spend'] >= 0.5 and not c['pre_period']) / max(1, sum(1 for c in winners if c['first'][:7] == m_)), 1) for m_ in ('2026-06', '2026-07', '2026-08', '2026-09')},
    top20=[dict(name=c['name'], vertical=c['vertical'], geo=c['geo'], ts=c['ts'], account=c['account'].split('/')[-1].strip(), first=c['first'], last=c['last'], spend=r2(c['spend']), profitNet=r2(c['profit']), roiNet=roi(c['profit'], c['spend'])) for c in sorted(winners_all, key=lambda x: -x['profit'])[:20]])
be = []
for c in winners:
    cs_ = cp_ = 0; hit = None
    for d in sorted(c['days']):
        v = c['days'][d]; cs_ += v['spend']; cp_ += v['profitAdjusted']
        if hit is None and cp_ > 0 and cs_ >= 1: hit = cs_
    be.append(hit or 0)
be.sort()
DATA['winners']['breakEvenSpend'] = dict(median=r2(statistics.median(be)), p75=r2(be[int(len(be) * .75)]), p90=r2(be[int(len(be) * .9)]),
                                          note='накопленный спенд, при котором будущий победитель впервые вышел в плюс (по финальной выручке)')
print(DATA['winners']['n'], DATA['winners']['profit'], DATA['winners']['restProfit'], DATA['winners']['launchesPerWinnerByMonth'], DATA['winners']['breakEvenSpend'])

# top buyers benchmark (panel top_buyers 21–22.09)
tb = {}
for f in glob.glob('/tmp/claude-0/-home-user-alextest/f5dce882-fce7-5270-9036-ca9a0fe43d5e/scratchpad/dash/top_buyers/*.json'):
    d = json.load(open(f)); d = d.get('data', d)
    t = d.get('total', {})
    tb[d.get('date', os.path.basename(f)[:-5])] = dict(spend=t.get('spend'), roi=t.get('roi'), rpc=t.get('rpc'), cpc=t.get('cpc'), rpl=t.get('rpl'), CPL=t.get('CPL'),
                                                       geoFB=[g['name'] for g in d.get('byGeo', {}).get('FACEBOOK', [])][:8], providersFB=[(p_['name'], round(p_['spend'])) for p_ in d.get('byProvider', {}).get('FACEBOOK', [])])
ours = {d: agg_period([d], d) for d in ('2026-09-21', '2026-09-22')}
DATA['benchmark_top5'] = dict(note='«Топ-5 баеров» — среднее по пяти баерам с наибольшей прибылью за день (панель top_buyers). ROI у них — среднее по баерам, не чистый.',
                              top5=tb, ours={d: {k: v[k] for k in ('spend', 'roiNet', 'cpc', 'rpcNet', 'cpl', 'rplNet')} for d, v in ours.items()})
print(DATA['benchmark_top5'])

# =============== META + DUMP ===============
DATA['meta'] = dict(
    generatedAt=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ'), period='2026-06-01 — 2026-09-24 (UTC-дни трекера; 24.09 неполный)',
    source='Roots MCP: get_performance_rows groupBy=campaign по каждому дню (116 дней; 99.8 проц. спенда разнесено по РК, остаток — хвост РК с копеечным спендом, учтён в итогах по дням через totalRow), get_adgroup_stats 01.06–24.09 (1447 адгрупп со спендом ≥ 0.5: аккаунт, провайдер, гео, статус), get_launch_activity, get_performance_daily, groupBy=article по окнам; панель: article_drafts, said_log, top_buyers.',
    roiDefinition='ROI и прибыль везде чистые: revenueAdjusted = выручка × 0.97, profitAdjusted = revenueAdjusted − спенд − плата за гео (как в правилах).',
    caveats=['Выручка RSOC доезжает до D+3: 22–24.09 занижены, выводы по пакетам 23–24.09 преждевременны.',
             'История бюджетов и бида в трекере не хранится: «бюджет $5 против $10–20» — прокси по медиане дневного спенда РК; РК на $10+ получали подъём, потому что уже были в плюсе (эффект отбора).',
             'Содержание крео (превью/текст) в трекере нет; «видео/статика» на FB — по наличию просмотров видео.',
             'Сигналы правил считаются по финальной выручке закрытых дней — это мягче, чем реальное внутридневное решение.',
             'Сумма по adgroup_stats ($33.6k) выше суммы по performance ($31.5k) — другой учёт дней/аккаунтов; деньги брались из performance, adgroup_stats — только для аккаунта/провайдера/гео.'],
    counts=dict(campaignsWithSpend=len(camps), launchedInPanel=sum(v.get('campaignsLaunched', 0) for v in launch.values()), bundles=len(BST)))
DATA['campaigns'] = [dict(id=c['id'], name=c['name'], ts=c['ts'], vertical=c['vertical'], bundle=c['bundle'], geo=c['geo'], tier=c['tier'], provider=c['provider'],
                          account=c['account'], first=c['first'], last=c['last'], spendDays=c['nSpendDays'], spend=r2(c['spend']), revenueNet=r2(c['revNet']), profitNet=r2(c['profit']),
                          roiNet=roi(c['profit'], c['spend']), clicks=c['clicks'], leads=c['leads'], medDailySpend=r2(c['medDaily']), fbVideo=c['fbVideo'], proven=c['proven'],
                          profitFirst3d=r2(c['p3']), ruleSignal=c['trigger'], profitAfterSignal=r2(c['afterProfit']), agentPackage=(c['agentPkg'] or {}).get('package'), status=c['status'])
                     for c in sorted(camps, key=lambda x: -x['spend'])]
json.dump(DATA, open(B + 'data.json', 'w'), ensure_ascii=False, indent=1)
print('WROTE', B + 'data.json', os.path.getsize(B + 'data.json'))
