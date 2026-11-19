#!/usr/bin/env python3
"""Descriptive GitHub study, no API keys. One row per mint; incomplete follow-up is never a zero."""
import argparse,csv,json,random,statistics,sys
from collections import defaultdict,Counter
from common import epoch,key,utc,Problem
GROUPS=('none','link-only','verified','unknown')
def analyze(rows):
    seen=set();groups={g:[] for g in GROUPS};missing=Counter();strata=defaultdict(lambda:defaultdict(list))
    for r in rows:
        m=key(r['mint']);start=epoch(r['created_at']);g=r['repo_group'];
        if m in seen or g not in GROUPS:raise Problem('duplicate mint or invalid group')
        seen.add(m)
        if not r['evidence_at'] or not start<=epoch(r['evidence_at'])<=start+120:g='unknown'
        if r['followup']!='complete':missing[g]+=1;continue
        if epoch(r['outcome_through'])<start+1800:raise Problem('30-minute horizon incomplete')
        n=int(r['new_buy_wallets']);
        if n<0:raise Problem('negative wallet count')
        y=int(n>=20);groups[g].append(y);ds=utc(start)[:10]
        st=(ds,r['launchpad'],r['opening_depth_band'],r['prelaunch_audience_band'],r['paid_at_cutoff']);
        if all(z and z!='unknown' for z in st):strata[st][g].append(y)
    days=defaultdict(list);matched_groups=Counter();baseline=[];treated=[]
    # Direct standardization: weight common strata by the smaller arm size. Never count an unmatched stratum.
    for st,v in strata.items():
        a,b=v['verified'],v['none'];w=min(len(a),len(b));
        if w:
            av,bv=sum(a)/len(a),sum(b)/len(b);days[st[0]].append((w,av,bv));matched_groups.update({'verified':len(a),'none':len(b)});treated.append(w*av);baseline.append(w*bv)
    def diff(seq):
        rec=[x for day in seq for x in days[day]];w=sum(x[0] for x in rec);return sum(i*(a-b) for i,a,b in rec)/w
    nd=len(days);w=sum(x[0] for vs in days.values() for x in vs);interval=None;d=diff(list(days)) if w else None
    if nd>=10 and min(matched_groups.values(),default=0)>=30:
        rng=random.Random(8719);dist=sorted(diff(rng.choices(list(days),k=nd))*100 for _ in range(1000));interval=[round(dist[24],3),round(dist[974],3)]
    return {'launches':len(seen),'groups':{g:{'complete':len(v),'successful':sum(v),'rate_pct':round(100*sum(v)/len(v),2) if v else None,'missing_followup':missing[g]} for g,v in groups.items()},'matched_verified_vs_none':{'raw_arm_counts_in_common_strata':dict(matched_groups),'independent_day_blocks':nd,'weight_sum':w,'difference_percentage_points':round(d*100,3) if d is not None else None,'relative_lift_pct':round((sum(treated)/sum(baseline)-1)*100,2) if sum(baseline)>0 else None,'day_bootstrap_95pct_pp':interval},'interpretation':'Outcome: >=20 first-time non-team buy wallets in (2,30] minutes. Association only, not buyer motivation. Null = unavailable. No interval unless >=10 days and >=30 observed per matched arm; this minimum is not a power guarantee.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('csv_file');a=p.parse_args()
    try:
        with open(a.csv_file,newline='') as f:print(json.dumps(analyze(csv.DictReader(f)),indent=2))
    except (Problem,KeyError,ValueError,OSError) as e:sys.exit(str(e))
