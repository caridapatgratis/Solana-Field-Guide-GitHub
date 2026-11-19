"""Narrow Pump decoder. Layouts pinned to pump-public-docs @639b87fb45c3adeffa6f7c4a1bf0cb85e392bf22."""
import hashlib, struct
from collections import Counter
from common import *
C1=hashlib.sha256(b'global:create').digest()[:8]; C2=hashlib.sha256(b'global:create_v2').digest()[:8]
ECPI=bytes.fromhex('e445a52e51cb9a1d'); EC=hashlib.sha256(b'event:CreateEvent').digest()[:8]; ET=hashlib.sha256(b'event:TradeEvent').digest()[:8]
BC=hashlib.sha256(b'account:BondingCurve').digest()[:8]
def strings(d,p):
    out=[]
    for cap in (128,64,1024):
        if p+4>len(d):raise Problem('short string length')
        n=int.from_bytes(d[p:p+4],'little');p+=4
        if n>cap or p+n>len(d):raise Problem('unsupported string')
        out.append(d[p:p+n].decode('utf-8'));p+=n
    return out,p
def creations(t):
    if not t['meta'] or t['meta']['err'] is not None:return []
    instructions=[(un58(i['data']),i.get('accounts',[])) for i in ixlist(t) if i.get('programId')==PUMP and 'data' in i];events=set()
    for d,_ in instructions:
        if d[:16]==ECPI+EC:
            _,p=strings(d,16)
            if len(d)>=p+128:events.add(tuple(b58(d[j:j+32]) for j in range(p,p+128,32)))
    out=[]; payer=t['transaction']['message']['accountKeys'][0]['pubkey']
    for d,ac in instructions:
        if d[:8] not in (C1,C2):continue
        names,p=strings(d,8);v2=d[:8]==C2
        if len(d)<p+32 or len(ac)<(16 if v2 else 14) or ac[1]!=AUTH:continue
        m,curve,user,creator=ac[0],ac[2],ac[5 if v2 else 7],b58(d[p:p+32])
        if (m,curve,user,creator) not in events:continue
        out.append(dict(mint=key(m),curve=key(curve),vault=key(ac[3]),create_user=key(user),creator_field=key(creator),fee_payer=key(payer),name=names[0],symbol=names[1],uri_untrusted=names[2],program=PUMP,token_program=ac[7 if v2 else 9],instruction='create_v2' if v2 else 'create',signature=t['transaction']['signatures'][0],slot=t['slot'],block_time=t['blockTime'],finality='finalized'))
    return out

def mint_info(a):
    d=raw(a);owner=a['owner']
    if owner not in (SPL,T22) or len(d)<82 or d[45]!=1:raise Problem('not a supported initialized mint')
    m=int.from_bytes(d[:4],'little');f=int.from_bytes(d[46:50],'little');ext=[]
    if m not in (0,1) or f not in (0,1):raise Problem('invalid authority layout')
    if owner==SPL and len(d)!=82:raise Problem('legacy layout changed')
    if owner==T22 and len(d)!=82:
        if len(d)<166 or d[165]!=1:raise Problem('unrecognized mint layout')
        p=166
        while p<len(d) and any(d[p:]):
            if p+4>len(d):raise Problem('incomplete extension')
            typ,n=struct.unpack_from('<HH',d,p);p+=4
            if not typ or typ in ext or p+n>len(d):raise Problem('invalid TLV')
            ext.append(typ);p+=n
    return dict(program=owner,supply=int.from_bytes(d[36:44],'little'),decimals=d[44],mint_authority=b58(d[4:36]) if m else None,freeze_authority=b58(d[50:82]) if f else None,extension_types=ext)
def mint_gate(mi,expected):
    if mi['program']!=expected:return gate('FAIL','token program mismatch',**mi)
    if mi['mint_authority'] or mi['freeze_authority']:return gate('FAIL','mint or freeze authority still present (strict policy)',**mi)
    # transfer fee, default state, nontransferable, permanent delegate and hook: skip this supported policy
    if set(mi['extension_types']) & {1,6,9,12,14}:return gate('FAIL','restricted or fee-capable mint outside this policy',**mi)
    if set(mi['extension_types'])-{18,19}:return gate('UNKNOWN','unsupported mint extension; not treated as safe',**mi)
    return gate('PASS','no mint/freeze keys; no unapproved mint extensions',**mi)
def acct_token(a,m,program):
    d=raw(a)
    if a['owner']!=program or len(d)<165 or b58(d[:32])!=m or d[108] not in (1,2):raise Problem('token account identity/state mismatch')
    if program==SPL and len(d)!=165 or program==T22 and len(d)>165 and d[165]!=2:raise Problem('unknown token-account layout')
    return b58(d[32:64]),int.from_bytes(d[64:72],'little')
def curve_gate(c,a):
    d=raw(a);m=c['mint']
    # Keep only the conventional, non-rewards, native SOL mode and the released layout.
    if a['owner']!=PUMP or d[:8]!=BC or len(d)<125:raise Problem('curve identity/layout unknown')
    real=int.from_bytes(d[32:40],'little');comp=d[48];creator=b58(d[49:81]);mayhem=d[81];cashback=d[82];quote=b58(d[83:115]);reward=d[124]
    fs=dict(curve=c['curve'],real_quote_raw=real,quote_mint=quote,complete=bool(comp),mayhem=bool(mayhem),cashback=bool(cashback),holder_reward=bool(reward),current_creator=creator)
    if comp:return gate('WAIT','curve complete; migration/AMM needs another decoder',**fs)
    if mayhem or cashback or reward or quote!='1'*32 or d[115:123]!=bytes(8) or d[123]!=0:return gate('WAIT','nonstandard mode or quote mint outside starter scope',**fs)
    if creator!=c['creator_field']:return gate('WAIT','creator field changed; seek role history',**fs)
    if real<R['min_real_sol_lamports'] or a['lamports']<real:return gate('WAIT','real SOL depth below policy or not backed at this account',**fs)
    return gate('PASS','verified active conventional curve and real SOL reserve',**fs)

def getrug(m):
    j,h=readjson('https://api.rugcheck.xyz/v1/tokens/'+key(m)+'/report')
    if j.get('mint')!=m or not isinstance(j.get('risks'),list) or not isinstance(j.get('rugged'),bool):raise Problem('incomplete risk report / different mint')
    risks=[{'name':i.get('name'),'level':i.get('level')} for i in j['risks']];critical=any(str(i.get('level')).lower() not in ('info','warn','warning','low') for i in risks)
    result=gate('WAIT' if j['rugged'] or critical else 'PASS','vendor warning for review' if j['rugged'] or critical else 'report retrieved; not a safety certificate',risks=risks,rugged=j['rugged'],vendor_detected_at=j.get('detectedAt'),transport=h,graph_insiders=j.get('graphInsidersDetected'))
    return result, [i['address'] for i in (j.get('topHolders') or []) if i.get('address')]

def mult(keys,slot):return rpc('getMultipleAccounts',[keys,{'encoding':'base64','commitment':'finalized','minContextSlot':slot}])
def chain_gates(c,hints):
    m,slot=c['mint'],c['slot'];r=mult([m,c['curve'],c['vault']],slot);ma,ca,va=r['value'];mi=mint_info(ma)
    mg=mint_gate(mi,c['token_program']);mg['slot']=r['context']['slot'];cg=safe(curve_gate,c,ca);cg['slot']=mg['slot']
    try:
        if acct_token(va,m,mi['program'])[0]!=c['curve']:raise Problem('wrong curve vault authority')
    except (Problem,KeyError,IndexError,ValueError) as e:cg=gate('UNKNOWN',str(e))
    dg=safe(holders,c,mi['program'],hints,mg['slot']);return mg,cg,dg

def holders(c,program,hints,slot):
    m=c['mint'];addr=[c['vault']];src='vendor address hints reconciled against chain'
    try:
        l=rpc('getTokenLargestAccounts',[m,{'commitment':'finalized'}]);addr += [x['address'] for x in l['value']];src='largest accounts plus hints reconciled against chain'
    except Problem:pass
    addr+=hints[:40];addr=list(dict.fromkeys(key(x) for x in addr));r=mult([m]+addr,slot);supply=mint_info(r['value'][0])['supply'];bank=r['context']['slot']
    balances={k:acct_token(a,m,program) for k,a in zip(addr,r['value'][1:]) if a}
    if sum(v[1] for v in balances.values())!=supply and os.environ.get('SOLANA_INDEXED')=='1':
        p=rpc('getProgramAccounts',[program,{'commitment':'finalized','minContextSlot':bank,'withContext':True,'encoding':'base64','filters':[{'memcmp':{'offset':0,'bytes':m}}]}]);bank=p['context']['slot'];src='indexed on-chain mint filter';balances={i['pubkey']:acct_token(i['account'],m,program) for i in p['value']}
    total=sum(v[1] for v in balances.values());fs=dict(snapshot_slot=bank,source=src,account_count=len(balances),supply_raw=supply,covered_raw=total)
    if total!=supply or supply<=0:return gate('UNKNOWN','holder balances do not reconcile to total supply',**fs)
    if c['vault'] not in balances or balances[c['vault']][0]!=c['curve']:raise Problem('canonical vault not verified')
    beneficial=Counter()
    for addr,(owner,amt) in balances.items():
        if addr!=c['vault'] and amt:beneficial[owner]+=amt
    free=sum(beneficial.values());fs.update(nonvault_raw=free,nonvault_owners=len(beneficial))
    if not free:return gate('WAIT','no outside-curve token balance',**fs)
    top=beneficial.most_common(10);issuer=sum(beneficial[x] for x in {c['create_user'],c['creator_field']});v=[top[0][1],sum(x[1] for x in top),issuer];limits=[R['max_owner_float_bps'],R['max_top10_float_bps'],R['max_issuer_float_bps']]
    fs.update(top1_pct=round(100*v[0]/free,3),top10_pct=round(100*v[1]/free,3),issuer_roles_pct=round(100*v[2]/free,3),denominator='supply minus exact curve vault')
    if any(x*10000>y*free for x,y in zip(v,limits)):return gate('FAIL','owner concentration above policy; not an allegation',**fs)
    return gate('PASS','all raw supply accounted for; holder caps met',**fs)

def flow(c):
    now=time.time(); rows=signatures(c['curve'],R['trade_sample_signatures']);good=[s for s in rows if s['err'] is None and now-R['flow_lookback_seconds']<=int(s['blockTime'] or 0)<=now+2 and s['slot']>=c['slot']]
    buy=set();sell=set();slots=set();evidence=[];roles={c['creator_field'],c['create_user'],c['fee_payer']}
    for s in good:
        t=tx(s['signature'])
        for i in ixlist(t):
            if i.get('programId')!=PUMP or not i.get('data'):continue
            d=un58(i['data'])
            if len(d)<97 or d[:16]!=ECPI+ET or b58(d[16:48])!=c['mint'] or d[64] not in (0,1):continue
            who=b58(d[65:97]);
            if who in roles or int.from_bytes(d[56:64],'little')<=0:continue
            (buy if d[64] else sell).add(who);slots.add(s['slot']);evidence.append(dict(wallet=who,side='buy' if d[64] else 'sell',signature=s['signature'],slot=s['slot']))
    ok=len(buy)>=R['min_buy_wallets'] and len(sell)>=R['min_sell_wallets'] and len(slots)>=R['min_trade_slots']
    return gate('PASS' if ok else 'WAIT','minimum observed two-sided activity met' if ok else 'not enough distinct non-role buyers, sellers or slots',buy_wallets=len(buy),sell_wallets=len(sell),trade_slots=len(slots),signatures_examined=len(good),events=evidence)

def wallet_note(addr,limit=8,before_slot=None,anchor_signature=None):
    rows=rpc('getSignaturesForAddress',[key(addr),{'limit':limit,'commitment':'finalized','before':anchor_signature}]) if anchor_signature else signatures(addr,limit);edges=[];related=[];seen=0
    for s in rows:
        if s['err'] is not None or (before_slot is not None and s['slot']>=before_slot):continue
        t=tx(s['signature']);seen+=1
        for i in ixlist(t):
            v=i.get('parsed',{});info=v.get('info',{}) if isinstance(v,dict) else {}
            if i.get('program')=='system' and v.get('type')=='transfer' and addr in (info.get('source'),info.get('destination')):
                edges.append(dict(src=info['source'],dst=info['destination'],lamports=info['lamports'],signature=s['signature'],slot=s['slot'],time=s['blockTime']))
        for z in creations(t):
            if addr in (z['create_user'],z['creator_field']):related.append(dict(mint=z['mint'],signature=z['signature'],slot=z['slot'],time=z['block_time']))
    return dict(address=addr,bounded_signatures=limit,examined=seen,edges=edges,prior_creations=related,limits='direct system transfers only; history may be partial; no personal identity')
