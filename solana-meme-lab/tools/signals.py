#!/usr/bin/env python3
"""Timestamped supporting observations. A snapshot is evidence, not an entry permission."""
import argparse, re, statistics, sys
from common import *
from chain import wallet_note

def envkey(name):
    value=os.environ.get(name)
    if not value:raise Problem(name+' not configured; mark UNKNOWN')
    return value
def gh(repo,m):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9_.-]{1,100}',repo) or repo.split('/')[1] in ('.','..'):raise Problem('expected owner/repo')
    h={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN']} if os.environ.get('GITHUB_TOKEN') else {}
    base='https://api.github.com/repos/'+repo
    def get(path):return readjson(base+path,headers=h)[0]
    a=get('');b=get('/commits/'+parse.quote(a['default_branch'],safe='')); rel=get('/releases?per_page=5');sha=b['sha']
    o=dict(repository_id=a['id'],owner_id=a['owner']['id'],canonical=a['full_name'],created_at=a['created_at'],pushed_at=a['pushed_at'],archived=a['archived'],fork=a['fork'],parent=(a.get('parent') or {}).get('full_name'),license=(a.get('license') or {}).get('spdx_id'),stars_context_only=a['stargazers_count'],head=sha,commit_verified=b['commit']['verification']['verified'],releases=[dict(tag=r['tag_name'],published_at=r['published_at'],url=r['html_url'],prerelease=r['prerelease']) for r in rel if not r['draft']],source=base)
    if m:
        key(m)
        try:
            file=get('/contents/launch-proof.json?ref='+sha)
            if file.get('encoding')!='base64' or file.get('size',0)>65536:raise Problem('oversize or unsupported proof')
            z=json.loads(base64.b64decode(file['content']));o['repo_claim_matches']=(z.get('mint')==m and z.get('network')=='mainnet-beta' and z.get('state')=='published');o['proof_blob_sha']=file['sha']
        except (Problem,KeyError,TypeError,ValueError) as e:o['repo_claim_matches']=None;o['proof_gap']=str(e)
    o['interpretation']='A one-way repo claim, even if true, is not proof of approval by the original project. Inspect independent links, release tags and demo.';return o

def xget(path,q=None):
    url='https://api.x.com/2/'+path+('?' +parse.urlencode(q) if q else '');return readjson(url,headers={'Authorization':'Bearer '+envkey('X_BEARER_TOKEN')})[0]
def xuser(name,prev,followers):
    if not re.fullmatch(r'[A-Za-z0-9_]{1,15}',name):raise Problem('bad username')
    j=xget('users/by/username/'+name,{'user.fields':'created_at,public_metrics,protected'})['data']
    if j.get('protected'):raise Problem('public accounts only')
    n=j['public_metrics']['followers_count'];o=dict(id=j['id'],handle=j['username'],created_at=j['created_at'],followers=n,prior_snapshot=None,source='X user lookup');
    for row in reversed(prev):
        z=row['data'];
        if row['kind']=='x-user' and z.get('id')==j['id'] and 'followers' in z:o['prior_snapshot']=row['observed_at'];o['net_change']=n-z['followers'];break
    if followers:
        jj=xget('users/'+j['id']+'/followers',{'user.fields':'created_at','max_results':50});ages=[(time.time()-epoch(u['created_at']))/86400 for u in jj.get('data',[]) if u.get('created_at')];o['public_follower_age_sample']={'n':len(ages),'under_7d':sum(a<7 for a in ages),'median_age_days':round(statistics.median(ages),1) if ages else None,'warning':'single nonrandom API page; age is account age, NOT date followed'}
    return o

def xposts(m):
    j=xget('tweets/search/recent',{'query':f'"{key(m)}" -is:retweet','tweet.fields':'author_id,created_at','max_results':50});posts=[{'id':p['id'],'created_at':p.get('created_at'),'author_id':p.get('author_id')} for p in j.get('data',[]) if m in p.get('text','')];return {'mint':m,'public_posts':posts,'distinct_authors_in_page':len({p['author_id'] for p in posts if p['author_id']}),'source':'X recent search; single page, not a market-wide trend'}

def telegram(chats,prev):
    allowed={int(x) for x in chats.split(',')};token=envkey('TELEGRAM_BOT_TOKEN');bot=token.split(':',1)[0]
    if not bot.isdecimal() or not re.fullmatch(r'[0-9]+:[A-Za-z0-9_-]+',token):raise Problem('invalid dedicated bot credential')
    last=max((r['data'].get('last_update',0) for r in prev if r['kind']=='telegram' and r['data'].get('bot_id')==bot),default=0)
    q={'offset':last+1,'timeout':0,'limit':100,'allowed_updates':json.dumps(['channel_post','edited_channel_post'])};j,_=readjson('https://api.telegram.org/bot'+token+'/getUpdates?'+parse.urlencode(q));posts=[]
    if not j.get('ok'):raise Problem('Bot API rejected request')
    for u in j['result']:
        last=max(last,u['update_id']);typ='edited_channel_post' if 'edited_channel_post' in u else 'channel_post';z=u.get(typ) or {};chat=z.get('chat',{});
        if chat.get('type')!='channel' or chat.get('id') not in allowed:continue
        txt=z.get('text') or z.get('caption') or '';mints=[]
        for s in re.findall(r'(?<![A-Za-z0-9])['+ABC+r']{32,44}(?![A-Za-z0-9])',txt):
            try:mints.append(key(s))
            except Problem:pass
        posts.append(dict(channel_id=chat['id'],message_id=z['message_id'],original_at=utc(z['date']),edited_at=utc(z['edit_date']) if z.get('edit_date') else None,forwarded=bool(z.get('forward_origin')),update_type=typ,candidate_addresses=list(dict.fromkeys(mints)),body_sha256=hashlib.sha256(txt.encode()).hexdigest()))
    return dict(bot_id=bot,last_update=last,posts=posts,source='Telegram Bot API; authorized channel IDs only; public keys are candidates, not mints until verified')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',default='signals.jsonl');s=p.add_subparsers(dest='cmd',required=True);a=s.add_parser('repo');a.add_argument('repo');a.add_argument('--mint');a=s.add_parser('x-user');a.add_argument('handle');a.add_argument('--follower-sample',action='store_true');a=s.add_parser('x-posts');a.add_argument('mint');a=s.add_parser('x-trends');a.add_argument('woeid',type=int);a=s.add_parser('telegram');a.add_argument('--allow-channel-ids',required=True);a=s.add_parser('wallet');a.add_argument('address');a.add_argument('--limit',type=int,default=8);args=p.parse_args();out=Path(args.out);prev=[]
    if args.cmd in ('x-user','telegram') and out.exists():prev=[json.loads(s) for s in out.read_text().splitlines() if s.strip()]
    try:
        if args.cmd=='repo':d=gh(args.repo,args.mint)
        elif args.cmd=='x-user':d=xuser(args.handle,prev,args.follower_sample)
        elif args.cmd=='x-posts':d=xposts(args.mint)
        elif args.cmd=='x-trends':d={'woeid':args.woeid,'trends':xget('trends/by/woeid/'+str(args.woeid)).get('data',[]),'note':'topic name alone does not identify a mint'}
        elif args.cmd=='telegram':d=telegram(args.allow_channel_ids,prev)
        else:
            mainnet()
            if not 1<=args.limit<=30:raise Problem('limit must be 1..30')
            d=wallet_note(key(args.address),args.limit);recent={z['mint'] for z in d['prior_creations'] if time.time()-z['time']<3600};d['watch_alert']='repeated create activity in sample' if len(recent)>=2 else None
        status='OBSERVED'
    except (Problem,KeyError,ValueError,TypeError,OSError) as e:d={'reason':str(e)[:160]};status='UNKNOWN'
    rec=dict(observed_at=utc(),kind=args.cmd,status=status,data=d);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('a') as f:f.write(json.dumps(rec)+'\n')
    print(json.dumps(rec,indent=2));return 0 if status=='OBSERVED' else 2
if __name__=='__main__':sys.exit(main())
