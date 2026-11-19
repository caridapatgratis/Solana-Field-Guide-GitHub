"""Offline unit tests; one explicitly labeled minimized real finalized create, otherwise synthetic fixtures."""
import base64,json,sys,tempfile,time,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import common,chain,lab,cohort,proof
from common import R,gate,Problem,b58
class Checks(unittest.TestCase):
    def test_real_program_event_matches_create(self):
        t=json.loads((common.ROOT/'tests/fixtures/finalized-create.json').read_text());z=chain.creations(t);self.assertEqual(len(z),1);self.assertEqual(z[0]['mint'],'E1MYV8hVJyqNEuBo8EjhhN8o7pLKDcn9uG6YRLJCpump');self.assertEqual(z[0]['finality'],'finalized');t['meta']['err']={'test':1};self.assertEqual(chain.creations(t),[])
    def test_counterfeit_program_is_not_create(self):
        t=json.loads((common.ROOT/'tests/fixtures/finalized-create.json').read_text());
        for i in common.ixlist(t):i['programId']=common.SOL
        self.assertEqual(chain.creations(t),[])
    def test_receipt_reconciliation(self):
        j=list(map(json.loads,(common.ROOT/'examples/calibration/events.jsonl').read_text().splitlines()));b=next(i['payload'] for i in j if i['kind']=='PAPER_BUY');s=next(i['payload'] for i in j if i['kind']=='PAPER_SELL');self.assertEqual(s['units'],b['units']);self.assertEqual(s['proceeds']-b['stake']-b['fee']-s['fee'],-115007);self.assertEqual(b['rent_reserve'],s['released_rent'])
    def test_no_score_override(self):
        for weak,state in [('FAIL','REJECT'),('UNKNOWN','WATCH'),('WAIT','WATCH'),('NOT_RUN','WATCH')]:self.assertEqual(lab.decide({'mint':gate(weak,'x'),'repo':gate('PASS','x')}),state)
        self.assertEqual(lab.decide({}),'WATCH')
    def test_mint_tlv(self):
        a=bytearray(166);a[45]=1;a[165]=1;a[36:44]=(100).to_bytes(8,'little')
        for typ,state in [(18,'PASS'),(19,'PASS'),(12,'FAIL'),(14,'FAIL'),(700,'UNKNOWN')]:
            d=bytes(a)+typ.to_bytes(2,'little')+bytes(2);m=chain.mint_info({'owner':common.T22,'data':[base64.b64encode(d).decode(),'base64']});self.assertEqual(chain.mint_gate(m,common.T22)['state'],state)
        a[46]=1;m=chain.mint_info({'owner':common.T22,'data':[base64.b64encode(a).decode(),'base64']});self.assertEqual(chain.mint_gate(m,common.T22)['state'],'FAIL')
    def test_mode_pin(self):
        with tempfile.TemporaryDirectory() as d:
            p=str(Path(d)/'book');lab.Ledger(p,'new-launch').d.close();self.assertRaises(Problem,lab.Ledger,p,'calibration-only')
    def test_book_and_stuck(self):
        l=lab.Ledger(':memory:','new-launch');self.addCleanup(l.d.close);m=common.BONK
        l.add('PAPER_BUY',m,position='p',mint=m,stake=10000000,units=1000,fee=15000,rent_reserve=3000000,entry_time=time.time()-200,due_at=0)
        with patch.object(lab,'qlog',side_effect=Problem('no sell route')):lab.manage(l)
        b=l.book();self.assertEqual(b['cash_lamports'],986985000);self.assertIn('p',b['open_positions']);self.assertEqual(b['closed_positions'],0);self.assertEqual(b['realized_net_lamports'],0);self.assertEqual(lab.budget(l,m)['state'],'WAIT');self.assertIsNotNone(l.last('EXIT_UNFILLED',m))
        l.add('PAPER_FAIL_FEE',m,fee=15000);l.add('PAPER_SELL',m,position='p',proceeds=9900000,fee=15000);b=l.book();self.assertEqual(b['cash_lamports'],999855000);self.assertEqual(b['realized_net_lamports'],-145000)
    def test_no_fill_with_missing_evidence(self):
        l=lab.Ledger(':memory:','new-launch');self.addCleanup(l.d.close);self.assertEqual(lab.paper_buy(l,common.BONK,{'mint':gate('UNKNOWN','no RPC')},time.time(),None,120,'flow'),'WATCH');self.assertEqual(l.book()['cash_lamports'],R['bankroll_lamports'])
    def test_fill_reprice_limit(self):
        l=lab.Ledger(':memory:','new-launch');self.addCleanup(l.d.close);t=time.time();g={'two_way':gate('PASS','ok',min_out=990,signal_time=t)}
        with patch.object(lab.time,'sleep'),patch.object(lab,'qlog',return_value=({'outAmount':'900','otherAmountThreshold':'890'},1,t)):
            self.assertEqual(lab.paper_buy(l,common.BONK,g,t,None,120,'flow'),'FAILED_LIMIT')
        self.assertFalse(l.book()['open_positions']);self.assertEqual(l.book()['realized_net_lamports'],-R['leg_fee_lamports'])
    def test_unknown_offchain(self):self.assertEqual(lab.review(common.BONK,'builder',None)['state'],'UNKNOWN')
    def test_known_conflict_cross_profile(self):
        with tempfile.TemporaryDirectory() as p:
            j={'mint':common.BONK,'role':'independent-reviewer','reviewer':'test','observed_at':common.utc(),'social':{'conflict':True,'references':['one','two']}};Path(p,common.BONK+'.json').write_text(json.dumps(j));self.assertEqual(lab.review(common.BONK,'flow',p)['state'],'FAIL')
    def test_study_missing_and_late(self):
        t=1700000000;rows=[]
        for k,(g,n,dt,complete) in enumerate([('verified',23,90,'complete'),('none',0,90,'complete'),('verified',99,200,'complete'),('none',0,30,'gap')],1):
            rows.append(dict(mint=b58(bytes([k])*32),created_at=common.utc(t),evidence_at=common.utc(t+dt),repo_group=g,launchpad='pump',opening_depth_band='native',prelaunch_audience_band='small',paid_at_cutoff='no',followup=complete,outcome_through=common.utc(t+1800),new_buy_wallets=n))
        j=cohort.analyze(rows);self.assertEqual(j['groups']['unknown']['complete'],1);self.assertEqual(j['groups']['none']['missing_followup'],1);self.assertEqual(j['matched_verified_vs_none']['difference_percentage_points'],100);self.assertIsNone(j['matched_verified_vs_none']['day_bootstrap_95pct_pp'])
    def test_template_not_proof(self):self.assertTrue(proof.check(json.loads((common.ROOT/'templates/launch-proof.json').read_text())))
    def test_pubkey_id(self):self.assertEqual(b58(common.un58(common.GENESIS)),common.GENESIS);self.assertEqual(len(common.un58(common.GENESIS)),32);self.assertRaises(Problem,common.key,'not a key')
if __name__=='__main__':unittest.main()
