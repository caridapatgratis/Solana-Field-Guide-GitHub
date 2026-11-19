#!/usr/bin/env python3
"""Finite, wallet-free collection and paper accounting. No signatures, swap builder or broadcast."""
import argparse, csv, sqlite3, sys, uuid, math
from pathlib import Path
from common import *
from chain import creations,getrug,chain_gates,flow,wallet_note
class Ledger:
    def __init__(self,path,mode=None):
        self.d=sqlite3.connect(path,timeout=15);self.d.row_factory=sqlite3.Row
        self.d.executescript('CREATE TABLE IF NOT EXISTS config(mode TEXT, policy TEXT); CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, ts TEXT NOT NULL, run TEXT, mint TEXT, kind TEXT NOT NULL, payload TEXT NOT NULL); CREATE INDEX IF NOT EXISTS ix ON events(mint,kind);')
        v=self.d.execute('SELECT * FROM config').fetchone()
        if not v:
            if mode is None:raise Problem('empty ledger; run scan or calibrate first')
            self.d.execute('INSERT INTO config VALUES (?,?)',(mode,POLICY));self.d.commit();self.mode=mode
        else:
            self.mode=v['mode'];
            if (mode and mode!=self.mode) or v['policy']!=POLICY:
                self.d.close();raise Problem('different ledger mode/policy; use a separate file with the original rules')
        self.run=uuid.uuid4().hex[:12]
    def add(self,kind,m='',**payload):
        cur=self.d.execute('INSERT INTO events(ts,run,mint,kind,payload) VALUES (?,?,?,?,?)',(utc(),self.run,m,kind,json.dumps(payload,separators=(',',':'),allow_nan=False)));self.d.commit();return cur.lastrowid
    def rows(self,kind=None,m=None):
        where=['1'];vals=[]
        if kind:where+=['kind=?'];vals+=[kind]
        if m:where+=['mint=?'];vals+=[m]
        for r in self.d.execute('SELECT * FROM events WHERE '+' AND '.join(where)+' ORDER BY id',vals):yield {**dict(r),'payload':json.loads(r['payload'])}
    def last(self,kind,m):return next(iter(reversed(list(self.rows(kind,m)))),None)
    def book(self):
        cash=R['bankroll_lamports'];opened={};net=day=0;today=utc()[:10];closed=0
        for row in self.d.execute("SELECT * FROM events WHERE kind IN ('PAPER_BUY','PAPER_SELL','PAPER_FAIL_FEE') ORDER BY id"):
            p=json.loads(row['payload']);k=row['kind'];d=0
            if k=='PAPER_BUY':cash-=p['stake']+p['fee']+p['rent_reserve'];opened[p['position']]=p
            elif k=='PAPER_FAIL_FEE':cash-=p['fee'];d=-p['fee']
            else:
                b=opened.pop(p['position']);cash+=p['proceeds']-p['fee']+b['rent_reserve'];d=p['proceeds']-p['fee']-b['fee']-b['stake'];closed+=1
            net+=d;day+=d if row['ts'][:10]==today else 0
        return dict(cash_lamports=cash,realized_net_lamports=net,utc_day_net_lamports=day,closed_positions=closed,open_positions=opened,conservative_equity_floor_lamports=cash)

def decide(g):
    if any(x['state']=='FAIL' for x in g.values()):return 'REJECT'
    if not g or any(x['state']!='PASS' for x in g.values()):return 'WATCH'
    return 'PAPER_ELIGIBLE'
def review(m,profile,folder):
    path=Path(folder)/(m+'.json') if folder else None
    if not path or not path.is_file():
        return gate('PASS','flow profile does not require social or repo evidence') if profile=='flow' else gate('UNKNOWN','no independent local '+profile+' review')
    if path.stat().st_size>64000:raise Problem('oversize review')
    j=json.loads(path.read_text());age=time.time()-epoch(j['observed_at']);e=j.get(profile) or {};refs=e.get('references',[])
    if j.get('mint')!=m or j.get('role')!='independent-reviewer' or not j.get('reviewer') or not 0<=age<=R['review_max_age_seconds']:raise Problem('wrong, stale or future review')
    for track in ('builder','social'):
        note=j.get(track) or {}
        if note.get('conflict') is True and len(set(note.get('references',[])))>=2:return gate('FAIL','documented public identity conflict',references=note['references'])
    if profile=='flow':return gate('PASS','no documented conflict in supplied review; optional social evidence not scored')
    checks=['mint_bound','release_verified','demo_verified'] if profile=='builder' else ['mint_bound','timestamped_growth','independent_sources','paid_separated']
    if e.get('conflict') is True:return gate('FAIL','verified public identity conflict',references=refs)
    if e.get('conflict') is not False or not all(e.get(k) is True for k in checks) or len(set(refs))<2:return gate('UNKNOWN','incomplete evidence for this profile',references=refs)
    return gate('PASS','reviewer evidence supplied; not inferred from stars or followers',reviewer=j['reviewer'],asof=j['observed_at'],references=refs)

def wallet_gate(c,f):
    addresses=set([c['create_user'],c['creator_field']]);buyers={e['wallet'] for e in f.get('events',[]) if e['side']=='buy'};notes=[]
    for a in sorted(addresses):notes.append(wallet_note(a,8,c['slot'],c['signature'] if a==c['create_user'] else None))
    edges=[e for n in notes for e in n['edges']];overlap=[e for e in edges if e['src'] in addresses and e['dst'] in buyers];prior={z['mint'] for n in notes for z in n['prior_creations'] if 0<=c['block_time']-z['time']<=3600}
    facts=dict(notes=notes,direct_overlap=overlap,recent_other_launches=len(prior),fee_payer_caveat='may be a service')
    if overlap or len(prior)>=2:return gate('WAIT','direct funding overlap or repeated creates; review, not proof of collusion',**facts)
    if not all(n['examined']>0 for n in notes) or not buyers:return gate('UNKNOWN','not enough pre-launch wallet history or buy sample',**facts)
    return gate('PASS','no alert in this bounded sample; not a clean-history certificate',**facts)

def qlog(l,m,a,b,n,label,curve=None):
    try:
        x=quote(a,b,n);j=x['response'];qid=l.add('QUOTE',m,use=label,**x)
        imp=float(j['priceImpact']);
        if not math.isfinite(imp) or abs(imp)>R['max_abs_impact_pct']:raise Problem('impact missing or above cap')
        if curve and not any(h.get('swapInfo',{}).get('ammKey')==curve for h in j['routePlan']):raise Problem('route does not include verified curve')
        return j,qid,epoch(x['transport']['received_at'])
    except (Problem,KeyError,ValueError,TypeError) as e:
        l.add('QUOTE_UNUSABLE',m,use=label,input_mint=a,output_mint=b,in_raw=n,reason=str(e));raise Problem(str(e)) from None

def roundtrip(l,m,curve):
    n=R['stake_lamports'];b,bid,bt=qlog(l,m,SOL,m,n,'entry signal',curve);units=haircut(int(b['outAmount']));s,sid,st=qlog(l,m,m,SOL,units,'reverse probe',curve)
    net=haircut(int(s['outAmount']))-2*R['leg_fee_lamports'];loss=(n-net)*10000/n
    facts=dict(buy_quote=bid,reverse_quote=sid,signal_out=int(b['outAmount']),min_out=int(b['otherAmountThreshold']),signal_time=bt,roundtrip_loss_bps=round(loss,2))
    if st-bt>R['quote_max_age_seconds']:return gate('WAIT','buy probe stale by reverse probe',**facts)
    return gate('PASS' if loss<=R['roundtrip_loss_cap_bps'] else 'WAIT','two-way quote within cap' if loss<=R['roundtrip_loss_cap_bps'] else 'round-trip cost above cap',**facts)
def budget(l,m):
    b=l.book();required=R['stake_lamports']+2*R['leg_fee_lamports']+R['ata_reserve_lamports']
    if b['open_positions'] or l.last('PAPER_BUY',m) or b['cash_lamports']<required or b['utc_day_net_lamports']<=-R['max_daily_net_loss_lamports']:return gate('WAIT','open position, mint already entered, cash or UTC loss limit')
    return gate('PASS','paper cash and risk limits met')
def paper_buy(l,m,g,first_evidence,curve,hold,profile):
    start=time.time(); decision=l.add('DECISION',m,decision=decide(g),profile=profile,gates=g,policy=POLICY)
    if decide(g)!='PAPER_ELIGIBLE':return decide(g)
    time.sleep(R['latency_seconds']);b=g['two_way']
    try:
        j,qid,t=qlog(l,m,SOL,m,R['stake_lamports'],'delayed entry',curve);units=haircut(int(j['outAmount']))
        if t-first_evidence>R['evidence_max_age_seconds'] or t-b['signal_time']>R['quote_max_age_seconds']:raise Problem('decision evidence expired')
        if units<max(b['min_out'],int(j['otherAmountThreshold'])):
            l.add('PAPER_FAIL_FEE',m,fee=R['leg_fee_lamports'],reason='modeled landed entry failed slippage limit',decision_id=decision);return 'FAILED_LIMIT'
        if budget(l,m)['state']!='PASS':raise Problem('budget changed')
        l.add('PAPER_BUY',m,position=f'{l.run}-{decision}',mint=m,profile=profile,units=units,stake=R['stake_lamports'],fee=R['leg_fee_lamports'],rent_reserve=R['ata_reserve_lamports'],entry_quote=qid,decision_id=decision,entry_time=t,due_at=t+hold,observed_latency_ms=round((t-start)*1000));return 'PAPER_BUY'
    except Problem as e:l.add('NO_FILL',m,reason=str(e),decision_id=decision);return 'NO_FILL'
def manage(l):
    for pos,b in l.book()['open_positions'].items():
        if time.time()<b['due_at']:continue
        m=b['mint'];n=b['units']
        if l.book()['cash_lamports']<R['leg_fee_lamports']:
            l.add('EXIT_UNFILLED',m,position=pos,units=n,reason='no paper fee budget',risk_mark_lamports=0);continue
        try:
            # Do not require entry's original venue to still exist. A real migrated route can be used.
            pre,pid,t0=qlog(l,m,m,SOL,n,'exit signal');time.sleep(R['latency_seconds']);after,qid,t1=qlog(l,m,m,SOL,n,'delayed exit');received=haircut(int(after['outAmount']))
            if t1-t0>R['quote_max_age_seconds']:raise Problem('exit signal stale')
            if received<max(int(pre['otherAmountThreshold']),int(after['otherAmountThreshold'])):
                l.add('PAPER_FAIL_FEE',m,position=pos,fee=R['leg_fee_lamports'],reason='modeled landed exit failed limit');raise Problem('sell below limit')
            net=received-b['stake']-R['leg_fee_lamports']-b['fee'];l.add('PAPER_SELL',m,position=pos,units=n,proceeds=received,fee=R['leg_fee_lamports'],released_rent=b['rent_reserve'],net_before_failed_attempt_fees=net,quote=qid,signal_quote=pid,held_seconds=round(t1-b['entry_time'],2),reason='first available timed exit');print('PAPER_SELL',m,net,'lamports before any failed-attempt fees')
        except Problem as e:l.add('EXIT_UNFILLED',m,position=pos,units=n,reason=str(e),risk_mark_lamports=0);print('EXIT_UNFILLED',m,str(e))

def assess(l,c,profile,folder=None):
    m=c['mint'];start=time.time();age=start-c['block_time'];g={'creation':gate('PASS' if 0<=age<=R['age_limit_seconds'] else 'WAIT','finalized create and matching program event; age window',age_s=round(age,1),signature=c['signature'],slot=c['slot'])}
    if g['creation']['state']!='PASS':l.add('DECISION',m,decision='WATCH',gates=g,profile=profile,policy=POLICY);return 'WATCH'
    try:g['rug_report'],hints=getrug(m)
    except (Problem,KeyError,ValueError,TypeError) as e:g['rug_report']=gate('UNKNOWN',str(e));hints=[]
    try:g['authorities'],g['market'],g['distribution']=chain_gates(c,hints)
    except (Problem,TypeError,KeyError,ValueError,IndexError) as e:
        for k in ('authorities','market','distribution'):g[k]=gate('UNKNOWN',str(e))
    # Avoid costly history/quotes for assets already blocked. Record what was NOT inspected.
    g['public_profile']=safe(review,m,profile,folder);g['budget']=budget(l,m)
    if decide(g)=='PAPER_ELIGIBLE':
        g['flow']=safe(flow,c);g['wallet_links']=safe(wallet_gate,c,g['flow'])
    else:
        for k in ('flow','wallet_links'):g[k]=gate('NOT_RUN','earlier checkpoint not met')
    if decide(g)=='PAPER_ELIGIBLE':g['two_way']=safe(roundtrip,l,m,c['curve'])
    else:g['two_way']=gate('NOT_RUN','earlier checkpoint not met')
    if time.time()-start>R['evidence_max_age_seconds']:g['freshness']=gate('UNKNOWN','evidence took too long')
    return paper_buy(l,m,g,start,c['curve'],R['hold_seconds'],profile)

def scan(l,n,profile,folder,rechecks=0):
    manage(l);mainnet();rows=signatures(AUTH,n);l.add('SAMPLE_WINDOW',source='finalized signatures mentioning Pump mint-authority',requested=n,count=len(rows),first_slot=min((r['slot'] for r in rows),default=None),last_slot=max((r['slot'] for r in rows),default=None),coverage='bounded latest-N sample, NOT a census')
    for s in reversed(rows):
        if s['err'] is not None:l.add('FAILED_CHAIN_TX',signature=s['signature'],slot=s['slot']);continue
        try:
            t=tx(s['signature']);found=creations(t)
            if not found:l.add('UNSUPPORTED_OR_NONCREATE',signature=s['signature'],slot=s['slot'])
            for c in found:
                m=c['mint'];
                if l.last('DISCOVERED',m):continue
                l.add('DISCOVERED',m,**c);res=assess(l,c,profile,folder);print(res,m)
        except (Problem,KeyError,ValueError,TypeError,IndexError) as e:l.add('DATA_GAP',signature=s['signature'],reason=str(e));print('DATA_GAP',str(e))

    if rechecks:
        # Revisit existing WATCH cases after at least 60s; oldest prior decision first.
        todo=[];now=time.time()
        for e in l.rows('DISCOVERED'):
            c=e['payload'];d=l.last('DECISION',c['mint'])
            if d and d['payload']['decision']=='WATCH' and now-epoch(d['ts'])>=60 and 0<=now-c['block_time']<=R['age_limit_seconds']:
                todo.append((d['id'],c))
        for _,c in sorted(todo,key=lambda x:x[0])[:rechecks]:print('RECHECK',assess(l,c,profile,folder),c['mint'])

def export(l,out):
    p=Path(out);p.mkdir(parents=True,exist_ok=True); rows=list(l.rows());b=l.book();counts={}
    with (p/'events.jsonl').open('w') as f,(p/'history.csv').open('w',newline='') as c:
        w=csv.writer(c);w.writerow('utc event_id run mint event decision_or_reason position stake_raw token_raw proceeds_raw fee_raw rent_reserved_or_released_raw net_before_failed_attempt_fees_raw quote_event_id'.split())
        for row in rows:
            f.write(json.dumps(row,ensure_ascii=True)+'\n');j=row['payload'];k=row['kind'];counts[k]=counts.get(k,0)+1
            if k not in ('QUOTE','SAMPLE_WINDOW'):
                w.writerow([row['ts'],row['id'],row['run'],row['mint'],k,j.get('decision') or j.get('reason'),j.get('position'),j.get('stake'),j.get('units'),j.get('proceeds'),j.get('fee'),j.get('rent_reserve') or j.get('released_rent'),j.get('net_before_failed_attempt_fees'),j.get('quote') or j.get('entry_quote')])
    report={'mode':l.mode,'policy_hash':POLICY,'exported_at':utc(),'event_counts':counts,'book':b,'units':'SOL cash in integer lamports; token quantities in mint base units','note':'All fills simulated. Cash floor excludes all open assets and rent. No open balance is realized income.'};(p/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',default='paper.sqlite');s=p.add_subparsers(dest='cmd',required=True)
    a=s.add_parser('scan');a.add_argument('--limit',type=int,default=3);a.add_argument('--rechecks',type=int,default=0);a.add_argument('--profile',choices=['flow','builder','social'],default='flow');a.add_argument('--reviews')
    a=s.add_parser('recheck');a.add_argument('mint');a.add_argument('--profile',choices=['flow','builder','social'],default='flow');a.add_argument('--reviews');s.add_parser('manage');s.add_parser('calibrate');a=s.add_parser('report');a.add_argument('--out',default='report');args=p.parse_args()
    if args.cmd=='scan' and not (1<=args.limit<=50 and 0<=args.rechecks<=20):p.error('limit must be 1..50 and rechecks 0..20')
    # Entire command is single-writer, including network wait. Never share a file across active workers.
    locker=sqlite3.connect(args.db+'.lock',timeout=1);locker.execute('BEGIN EXCLUSIVE')
    try:
        mode='new-launch' if args.cmd in ('scan','recheck') else 'calibration-only' if args.cmd=='calibrate' else None;l=Ledger(args.db,mode)
        if args.cmd=='scan':scan(l,args.limit,args.profile,args.reviews,args.rechecks)
        elif args.cmd=='recheck':
            mainnet();manage(l);m=key(args.mint);found=l.last('DISCOVERED',m)
            if not found:raise Problem('mint not discovered in this ledger')
            print(assess(l,found['payload'],args.profile,args.reviews),m)
        elif args.cmd=='manage':manage(l)
        elif args.cmd=='report':export(l,args.out)
        else:
            start=time.time();m=BONK;g={'budget':budget(l,m),'two_way':safe(roundtrip,l,m,None)};status=paper_buy(l,m,g,start,None,12,'calibration-only');print(status,'BONK; not a new-launch strategy trade');
            if status=='PAPER_BUY':time.sleep(12.1)
            manage(l)
    finally:
        if 'l' in locals():l.d.close()
        locker.rollback();locker.close()
if __name__=='__main__':
    try:main()
    except (Problem,sqlite3.Error,KeyError,ValueError,OSError) as e:print('STOP:',e,file=sys.stderr);sys.exit(2)
