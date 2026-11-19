#!/usr/bin/env python3
"""Lint a public launch manifest. Passing validates disclosure shape, NOT truth or safety."""
import argparse,json,sys,re
from common import epoch,key,un58,Problem

def check(j):
    issues=[]
    def need(ok,msg):
        if not ok:issues.append(msg)
    need(j.get('schema')=='solana-launch-proof/1','schema mismatch'); need(j.get('state')=='published','not marked published');need(j.get('network')=='mainnet-beta','published public record must say mainnet-beta')
    for f in ('mint','creator_pubkey','create_user_pubkey','fee_payer_pubkey','launch_program','token_program'):
        try:key(j.get(f))
        except Problem:issues.append('supply a valid '+f)
    try:need(len(un58(j.get('create_tx')))==64,'creation signature length')
    except Problem:issues.append('creation signature missing/invalid')
    try:epoch(j['as_of_utc'])
    except (AttributeError,TypeError,ValueError,KeyError):issues.append('UTC evidence timestamp missing/invalid')
    need(isinstance(j.get('finalized_slot'),int) and j['finalized_slot']>0,'supply finalized slot');need(isinstance(j.get('decimals'),int) and 0<=j['decimals']<=255,'supply decimals');need(isinstance(j.get('supply_raw'),str) and j['supply_raw'].isdecimal() and int(j['supply_raw'])>0,'supply raw amount as positive integer string')
    a=j.get('supply_allocation_bps');need(isinstance(a,dict) and bool(a) and all(type(n) is int and 0<=n<=10000 for n in a.values()) and sum(a.values())==10000,'allocation must total exactly 10,000 basis points')
    for f in ('mint_authority','freeze_authority'):
        x=j.get(f) or {};ok=x.get('status') in ('revoked','not-set') and x.get('pubkey') is None
        if x.get('status')=='active':
            try:key(x.get('pubkey'));ok=True
            except Problem:pass
        need(ok,'document '+f+' status and key')
    need(j.get('extensions_verified') is True and isinstance(j.get('extensions'),list),'extensions not verified');v=j.get('venue') or {};need(v.get('stage') in ('curve','pool','migrating'),'missing venue stage');need(bool(v.get('curve_or_pool')) and bool(v.get('lp_withdrawal_rights')),'state address and liquidity rights, including not-applicable with reason')
    for f in ('display_name','canonical_site','risks','incident_contact','evidence_links','approver','fees_and_recipients'):need(bool(j.get(f)),f+' must be explicit')
    return issues
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('file');args=p.parse_args();issues=check(json.load(open(args.file)));print(json.dumps({'ready_for_independent_verification':not issues,'problems':issues,'not_a_security_audit':True},indent=2));sys.exit(bool(issues))
