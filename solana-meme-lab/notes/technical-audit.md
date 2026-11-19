# Technical audit: what the evidence actually proves

**Edition 1.3 · 18 November 2026 · Documentation review, not a new market run.** This audit compares the shipped code with the two saved runs. It does not change eligibility rules. Use the [independent sign-off worksheet](../templates/independent-signoff.md) for extra observations; never rewrite an original decision.

## 1. A frozen balance can still be counted

**What runs now:** the [mint gate and account decoder](../tools/chain.py) check whether the mint has a freeze authority. But `acct_token` accepts both initialized and frozen token accounts and returns the owner and amount, not the freeze state. A holder total can reconcile even when part of it cannot move. This is a limitation, not a finding that any sampled account was frozen.

**Creator and reviewer action:** record two facts separately: “freeze authority absent at slot S” and “these named token accounts were checked for frozen state at slot T.” Check the exact venue vault and material team/treasury accounts. For an ordinary SPL mint a frozen account retains its balance and cannot transfer normally until thawed; ordinary thawing needs the mint's freeze authority. Revoking that authority is **not** a thaw. If a broader claim matters, state how much supply you actually checked and what is unknown. Do not drop frozen balances from the existing concentration denominator to make a token pass. Solana: freeze [1](https://solana.com/docs/tokens/basics/freeze-account) and thaw [2](https://solana.com/docs/tokens/basics/thaw-account).

**Proposed test, not an existing gate:** a fixture with no current freeze key and a positive frozen balance should report the two facts separately. An authority `PASS` must never be displayed as “all balances transferable.”

## 2. Finalized reads can describe different slots

**Recorded example:** in new-launch [event 3](../examples/new-launch/events.jsonl), the creation slot was **470863420**, the authority read was at **470863440**, and the distribution read was at **470863454**. These are genuine observations, not one snapshot of the launch slot. Distribution was `UNKNOWN` because balances did not reconcile; the slot difference alone does **not** explain why.

**What runs now:** the [chain reader](../tools/chain.py) batches mint, curve and vault, then makes a separate holder read. `minContextSlot` is a lower bound, not a request for state at exactly that slot. The optional indexed fallback can compare an earlier supply value with balances from a later slot. A token burn between reads is one possible source of mismatch, not a diagnosis. See [Solana's batch-read response](https://solana.com/docs/rpc/http/getmultipleaccounts) and the minimum-slot explanation [2](https://docs.triton.one/project-yellowstone/cloudbreak-custom-indexes).

**Reviewer action:** put a source and actual slot beside each claim. Batch related addresses in one response where practical. If a mismatch matters, take a new coherent read or use an explicitly slot-addressable historical source. If neither is possible, leave it unresolved. Don't stamp every check with the creation slot or invent an exact-slot replay. No new slot-gap threshold is imposed by this guide.

## 3. Check the route and the amount being reversed

**What runs now:** in [`qlog` and `roundtrip`](../tools/lab.py), an entry or reverse probe passes the venue-membership check if **any** route leg has the verified curve's `ammKey`. That is not proof that 100% of the trade used that curve. A quote can have split paths and several hops; adding percentages across sequential hops is not a valid curve share. Inspect the mints, raw amounts and pool key on the relevant branches. If you cannot attribute the share, say **“curve present; share unknown.”** Exits can use a different route. [Jupiter V2 route fields](https://developers.jup.ag/docs/api-reference/swap/order).

**Recorded example, BONK calibration only:** [quote 2](../examples/calibration/events.jsonl) tested a reverse sale of **31,318,946,695** raw token units. The delayed paper buy recorded **31,324,460,123** units in event 5; the exit quotes used that actual balance. The first reverse probe covered the **expected** quantity, not the later fill. BONK calibration did not require a Pump curve. This example proves the amount distinction, not curve routing or profitability.

**Proposed test:** record signal quantity, delayed quantity, actual exit quantity and curve share when it can be established. A split route must not be labeled “curve only.” If researching a second reverse quote at the delayed size, timestamp it separately: the extra request changes latency. The shipped entry does not make that second reverse check before recording a buy.

## 4. Resume an interrupted scan without inventing a decision

**What runs now:** the [ledger](../tools/lab.py) commits `DISCOVERED` before assessment. If a run stops between those steps, a later scan skips the already discovered mint, and automatic retries look for a previous `WATCH` decision. A discovery without **any** decision can therefore remain unassessed. Likewise, an eligible decision is not a purchase without `PAPER_BUY`.

**Operator action:** first export the **same** ledger to a new folder with `report`. In its event file, group by exact mint: find `DISCOVERED` with no `DECISION`; separately match entries to `PAPER_BUY` by decision ID. If you only want to inspect, stop there. If you want a **new paper assessment now**, after the old worker stops, use the original ledger and profile. Example for a builder ledger (replace `ACTUAL_MINT` with the discovered address):

```bash
python tools/lab.py --db builder.sqlite report --out report-after-stop
python tools/lab.py --db builder.sqlite recheck ACTUAL_MINT --profile builder --reviews reviews
```

`recheck` can manage due exits and attempt a paper entry. It is not a replay or a read-only report. Use `--profile flow` for a flow experiment or `--profile social --reviews reviews` for social; preserve the experiment's review directory if one was used. If the mint is now outside the entry window, keep the original decision missing; a new age-window `WATCH` is a later observation. Do not delete the DB, edit old events or manufacture a fill.

## 5. Keep the rules hash and the code version separate

**What runs now:** the [policy hash](../tools/common.py) covers the parsed [rule values](../rules.json). The database pins that hash and the mode, not the Python implementation, profile, or data-provider behavior. Two runs can share a policy hash but use different decoders or entry logic.

**Operator action:** with each report retain the UTC range, ledger mode, explicit profile, rule hash, exact kit release and the hashes of the tool files used. The [release checksums](../CHECKSUMS.sha256) cover the Markdown, tools, policy, templates and saved evidence. From the kit root, `sha256sum -c CHECKSUMS.sha256` checks them on systems with that utility. Check before editing; use working copies for filled-in forms. A matching hash shows unchanged bytes against this list, **not** a trusted publisher, safe code or an accurate disclosure. Never include API keys in a run note.

## Study check: can missing outcomes reverse the conclusion?

For each GitHub group, show a simple range beside the complete-case rate. If `s` launches succeeded, `c` have complete follow-up and `g` have gaps, the lowest possible raw rate is `s / (c + g)`; the highest is `(s + g) / (c + g)`. If `c + g = 0`, report **no estimate**. The two endpoints assume all missing outcomes failed or all succeeded. These are bounds for that sampled group, **not** confidence intervals, matched effects, or shares of buyers.

**Illustration only:** verified projects with 6 successes among 10 complete and 10 missing look like 60% on complete cases, but the full group could be **30–80%**. A no-repo group at 5/10 with no gaps is **50%**. The raw difference can therefore be **−20 to +30 percentage points**; even the direction is not established. The [calculator](../tools/cohort.py) already outputs successes, complete counts and gaps; it does not compute these bounds. The [study protocol](study.md) still requires matching and a defined cohort. No new buyers or launches were measured here.
