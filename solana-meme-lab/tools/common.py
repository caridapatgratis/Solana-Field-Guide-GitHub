"""Read-only transport, public-key codec and versioned test policy. Python 3.10+."""
import base64, hashlib, json, os, time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib import request, error, parse
ROOT=Path(__file__).resolve().parents[1]
R=json.loads((ROOT/'rules.json').read_text())
POLICY=hashlib.sha256(json.dumps(R,sort_keys=True).encode()).hexdigest()[:16]
SOL='So11111111111111111111111111111111111111112'
BONK='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
PUMP='6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P'
AUTH='TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM'
SPL='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
T22='TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb'
ABC='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
RPC=os.environ.get('SOLANA_RPC_URL','https://api.mainnet-beta.solana.com')
GENESIS='5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d'
class Problem(Exception): pass
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPEN=request.build_opener(NoRedirect())
def utc(t=None):return datetime.fromtimestamp(time.time() if t is None else t,timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
def epoch(s):
    if not isinstance(s,str):raise ValueError('timestamp missing/not a string')
    d=datetime.fromisoformat(s.replace('Z','+00:00'))
    if d.tzinfo is None: raise ValueError('timezone missing')
    return d.timestamp()
def b58(b):
    n=int.from_bytes(b,'big'); s=''
    while n: n,i=divmod(n,58);s=ABC[i]+s
    return '1'*(len(b)-len(b.lstrip(b'\0')))+s
def un58(s):
    if not isinstance(s,str) or len(s)>6000:raise Problem('bad base58 length')
    n=0
    try:
        for c in s:n=n*58+ABC.index(c)
    except ValueError: raise Problem('bad base58') from None
    return bytes(len(s)-len(s.lstrip('1')))+n.to_bytes((n.bit_length()+7)//8,'big')
def key(s):
    if not isinstance(s,str) or not 32<=len(s)<=44 or len(un58(s))!=32:raise Problem('invalid Solana public address')
    return s
def raw(a):
    if not a:raise Problem('account missing')
    return base64.b64decode(a['data'][0],validate=True)
def readjson(url,payload=None,headers=None,max_bytes=4_000_000):
    if not url.startswith('https://'):raise Problem('HTTPS required')
    start=time.time(); hdr={'User-Agent':'SolanaEvidenceLab/1.0','Accept':'application/json','Cache-Control':'no-cache'}
    if payload is not None:hdr['Content-Type']='application/json'
    hdr.update(headers or {});data=None if payload is None else json.dumps(payload).encode()
    try:
        with OPEN.open(request.Request(url,data=data,headers=hdr),timeout=9) as res:
            body=res.read(max_bytes+1); dt=res.headers.get('Date'); age=res.headers.get('Age');end=time.time()
            if len(body)>max_bytes:raise Problem('response over byte budget')
            return json.loads(body),{'received_at':utc(end),'latency_ms':round(1000*(end-start)),'http_date':dt,'cache_age':age,'sha256':hashlib.sha256(body).hexdigest()}
    except error.HTTPError as e:raise Problem('HTTP '+str(e.code)+(' (back off)' if e.code==429 else '')) from None
    except (OSError,ValueError) as e:raise Problem('transport/JSON '+type(e).__name__) from None
RPC_METHODS={'getGenesisHash','getSignaturesForAddress','getTransaction','getMultipleAccounts','getTokenLargestAccounts','getProgramAccounts','getAccountInfo'}
def rpc(method,params):
    if method not in RPC_METHODS:raise Problem('not a read RPC')
    data,_=readjson(RPC,{'jsonrpc':'2.0','id':1,'method':method,'params':params})
    if not isinstance(data,dict) or 'result' not in data:raise Problem('RPC '+method+' '+str((data.get('error') or {}).get('code','unavailable')))
    return data['result']
def mainnet():
    if rpc('getGenesisHash',[])!=GENESIS: raise Problem('not Solana mainnet-beta')
def tx(sig):
    v=rpc('getTransaction',[sig,{'encoding':'jsonParsed','commitment':'finalized','maxSupportedTransactionVersion':1}]);
    if not v or not v.get('meta') or v['meta'].get('err') is not None:raise Problem('transaction absent/failed')
    return v
def signatures(addr,n):return rpc('getSignaturesForAddress',[key(addr),{'limit':n,'commitment':'finalized'}])
def ixlist(t):return t['transaction']['message']['instructions']+[i for g in t['meta'].get('innerInstructions') or [] for i in g['instructions']]
def gate(state,reason,**facts):return dict(state=state,reason=reason,**facts)
def safe(call,*args):
    try:return call(*args)
    except (Problem,KeyError,TypeError,ValueError,IndexError,OverflowError) as e:return gate('UNKNOWN',str(e)[:160])
def haircut(amount):return amount*(10000-R['execution_haircut_bps'])//10000
_last_quote=0.0
def quote(a,b,amount):
    global _last_quote
    if not 0<amount<2**64:raise Problem('invalid exact-in amount')
    params=dict(inputMint=key(a),outputMint=key(b),amount=str(amount),slippageBps=R['slippage_limit_bps'])
    url='https://api.jup.ag/swap/v2/order?'+parse.urlencode(params)
    time.sleep(max(0,2.1-(time.monotonic()-_last_quote))); _last_quote=time.monotonic()
    h={'x-api-key':os.environ['JUPITER_API_KEY']} if os.environ.get('JUPITER_API_KEY') else {}
    j,meta=readjson(url,headers=h); end=epoch(meta['received_at']); maxage=R['quote_max_age_seconds']
    if not isinstance(j,dict) or j.get('error') or j.get('errorCode') or j.get('transaction') or j.get('taker'):raise Problem('not a usable wallet-free quote')
    if (j.get('inputMint'),j.get('outputMint'),j.get('swapMode'),str(j.get('inAmount')))!=(a,b,'ExactIn',str(amount)):raise Problem('quote pair/size/mode mismatch')
    if meta['latency_ms']>maxage*1000 or float(meta['cache_age'] or 0)>maxage:raise Problem('stale response')
    if meta['http_date'] and abs(end-parsedate_to_datetime(meta['http_date']).timestamp())>maxage:raise Problem('stale HTTP date or local clock')
    if j.get('expireAt') and epoch(j['expireAt'])<=end:raise Problem('expired quote')
    if not j.get('routePlan') or not 0<int(j.get('otherAmountThreshold',0))<=int(j['outAmount']):raise Problem('no valid route/minimum')
    if int(j.get('slippageBps',-1))!=R['slippage_limit_bps']:raise Problem('slippage mismatch')
    return {'source':url,'transport':meta,'response':j}
