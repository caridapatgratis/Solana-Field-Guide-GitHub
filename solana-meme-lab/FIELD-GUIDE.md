# Solana memecoin field guide

**Version 1.3 · 18 November 2026 · Documentation update**

A creator needs to show **what is true about this mint**. A paper trader needs to know **whether this position can be entered and exited at its size**. Those are different questions. A verified launch can still be unsuitable for the paper account.

## Start here

| I want to… | Start with | What I should have at the end |
|---|---|---|
| Design or rehearse a launch | [Creator workflow](#creator-workflow) → [launch brief template](templates/launch-brief.md) | A testable idea, then a rehearsal record. A devnet receipt is not a mainnet launch. |
| Run the paper scanner | [First run and troubleshooting](notes/first-run.md) → [paper checkpoints](#paper-scanner) | A local paper ledger and an explanation of each decision, even if there are no fills. No wallet needed. |
| Give these tasks to an AI agent | [Agent routing map](AGENTS.md) → [operator setup](README.md) | The right skill for each task, with the issuer and the scanner kept separate. |
| Check the results or a GitHub claim | [Read the evidence](#read-the-evidence) or [GitHub study](#github-study) | Dated receipts or a study design, not a profitability claim. |

**Reading vs running.** The [offline kit reader](Field-Guide.html) includes the local documents, forms, examples and tool sources. Use the [file index](FILES.md) for direct file links, including every Markdown document. Read one skill on its own or keep the whole folder for its related files. The HTML reader also includes the exact Markdown text for offline use. On GitHub, read the Markdown directly or use the published GitHub Pages site for the interactive reader. External websites need internet. To **run** the tools, clone the repository or extract the full release ZIP, then work in `solana-meme-lab`, the directory containing the [operator guide](README.md). To **edit** a form, copy the template in that folder. A project’s published manifest, a reviewer’s per-mint JSON and your new reports are **outputs you create**, not missing downloads.

**New in 1.3:** the [technical audit](notes/technical-audit.md) uses saved event IDs to explain mixed-slot reads, frozen balances, route splits, and how to recover after an interrupted paper scan. It also shows how missing study outcomes can reverse an apparent result. No trading rule changed.

**Status key:** **In the kit** means the current files support it. **Review by hand** means an operator or independent agent must verify it. **Research proposal** means it is not implemented. **Recorded example** means a dated observation, not a new test or a forecast. “Good+” is a working label here, not a vendor rating or a buy signal.

## Common mistakes

| Easy mistake | What to do instead |
|---|---|
| Treat a GitHub link, star count or fee destination as an endorsement. | Verify the exact mainnet mint with the original maintainer. Check a usable release and demo. A pure meme does not need a repo. See [repo verification](skills/prove-repository/SKILL.md) and the [fake-stars study](https://cmustrudel.github.io/papers/icse2026fakestars.pdf). |
| Treat a paid boost, forwarded call or fast follower count as independent demand. | Record the first source, time and exact mint. Separate paid, copied and unknown activity. A DEX Screener boost affects **its** score; it is not an organic X trend. See [attention checks](skills/monitor-attention/SKILL.md) and [DEX Screener's explanation](https://docs.dexscreener.com/boosting). |
| Call a green RugCheck report “safe.” | Read its named findings. Verify supply controls, extensions, concentration and withdrawal rights on chain; test the full-size reverse quote. See [chain inspection](skills/inspect-chain/SKILL.md). |
| Call the payer the founder, or a same-slot buy a bundle. | Keep fee payer, create-user and recorded creator separate. A transfer proves money moved; neither one exchange funder nor one shared slot proves common ownership. See [wallet tracing](skills/trace-wallets/SKILL.md) and [Jito's bundle definition](https://docs.jito.wtf/lowlatencytxnsend/). |
| Estimate a strategy's chances from trending or graduated coins. | Sample at creation and keep quiet coins, outages and missing exits. In one large study, 68.67% of **traded** Pump.fun launches had their last **recorded curve trade** on launch day. Zero-trade mints and post-migration trades were excluded; that is not a universal failure rate. See [study and limits](https://www.coingecko.com/research/publications/average-lifespan-of-pumpfun-tokens) and [research notes](notes/research.md). |
| Count a quoted price or a due exit as cash. | Record a simulated fill only after a fresh, acceptable full-size quote. Keep unsold tokens open and report the cash tied up. See [paper execution](skills/paper-trade/SKILL.md) and [the journal](skills/trade-journal/SKILL.md). |

## Creator workflow

**A Good+ launch is checkable, not engineered to pass a scanner.** Someone can identify the real mint, see who can change supply or remove liquidity, and tell what the project offers without trusting a ticker. A practical first project is a browser meme-remix tool: licensed art, one example someone can export without connecting a wallet, and a dated release. Test whether people return **before** deciding to issue a token. An honest community meme is better than an invented software claim.

| Step | Do this | Use this resource |
|---|---|---|
| 1 · Design | Choose one audience, record what exists today, disclose rights, budget, token role, team purchases and unlocks. Choose a reason to postpone. | [Launch design skill](skills/launch-design/SKILL.md) · [launch brief template](templates/launch-brief.md) |
| 2 · Rehearse | Choose a launchpad-created mint and curve **or** a plain mint plus a separately seeded pool. The included SPL devnet exercise creates a **test mint only**; it does not create a Pump curve or liquidity. Record “not tested” where appropriate. | [Launch rehearsal skill](skills/launch-rehearsal/SKILL.md) · [devnet steps](notes/devnet.md) · [runbook template](templates/launch-runbook.md) |
| 3 · Disclose | After a human-approved real launch, use the finalized transaction, exact mint, supply, roles, fees and custody. Before migration there is no pool LP token to lock on an active Pump curve. Publish the same facts to everyone. | [Launch disclosure skill](skills/launch-disclosure/SKILL.md) · [issuer proof template](templates/launch-proof.json) · [address card and corrections](templates/address-card.md) |
| 4 · Verify independently | Someone other than the packet’s author checks the public evidence. A creator verdict is “verified at this slot,” “mismatch,” or “unknown”; a devnet verdict is **rehearsal only**. Renew after a migration, authority change, upgrade or unlock. | [Two-verdict worksheet](templates/independent-signoff.md) · [technical review](#technical-review) |

**Creator check:** an absent freeze authority is a fact about the mint, not a transfer test for every existing account. Record the [account-state checks](notes/technical-audit.md#1-a-frozen-balance-can-still-be-counted) before claiming all balances can move.

**Which JSON goes where?** The [issuer proof template](templates/launch-proof.json) is deliberately blank. For a repo-backed project, the issuer’s completed public `launch-proof.json` belongs at the root of the **project’s** repo. The [proof linter](tools/proof.py) expects `state: published` and `network: mainnet-beta`; it checks the shape of selected fields. A truthful disclosure of an active authority can pass that lint and **still fail the paper policy**. Do not relabel a devnet draft just to get a pass. The scanner’s analyst instead works from the finalized transaction and a separate [independent review template](templates/review.json).

**What each audience can check:** fast traders need real quote-side reserves, known fees, first buys and a full-size route out. Rug-screen readers need authorities, extensions, allocation, and who can withdraw liquidity. Builders need maintainer confirmation and usable software. Narrative traders need original posts with paid placements labeled. Holders need a reason to return, public treasury reports and an unlock calendar. Day-7 and day-30 retention are **later evidence**, not launch-day badges. If marketing in Indonesia, get current local advice; [the OJK context and limits](notes/research.md) are not permission to promote.

## Paper scanner

**First run:** clone the repository or extract the kit, open a terminal in `solana-meme-lab` and follow the [walkthrough](notes/first-run.md). [Operator setup](README.md) covers Python, data-provider access, scheduling and CLI options. The scanner reads mainnet and simulates both sides. Do not connect a wallet or give it a signing key.

```bash
python -m unittest discover -s tests -v
python tools/lab.py --db paper.sqlite scan --limit 3 --profile flow
python tools/lab.py --db paper.sqlite manage
python tools/lab.py --db paper.sqlite report --out report-flow
```

`--limit 3` samples **up to three recent finalized signatures**, not three mints, decisions or trades. `scan` and `manage` run once, then stop. `manage` may have nothing due; run it later on the **same DB** if a position is open. Put `--db` **before** the subcommand. `--profile` and `--reviews` go **after** `scan` or `recheck`, not after `manage` or `report`. For builder/social use a separate ledger per profile **and** specify the profile on every assessment: an omitted profile defaults to `flow`. See the [per-mint review instructions](notes/profile-review.md).

### What must pass for a new-launch paper entry?

| Check | Current baseline, not a market law |
|---|---|
| Creation and market | Matching finalized Pump creation event, age ≤30 min, conventional active native-SOL curve, supported mode and ≥2 real SOL. No direct-pool or post-migration **new entry** adapter. [Mint discovery](skills/discover-mints/SKILL.md) |
| Supply and permissions | No mint or freeze authority; only supported extensions. Reconcile all supply and remove only the verified curve vault. Of the remainder: largest owner ≤15%, top ten together ≤60%, recorded creator + create-user (deduplicated) ≤10%. This is not a claim about every insider. [Inspect chain](skills/inspect-chain/SKILL.md) |
| Public checks and activity | Read named RugCheck findings, check pre-launch role history and, when reached, observe ≥5 non-role buy wallets, ≥2 sell wallets and ≥3 trade slots in the bounded sample. Wallets are not people. [Trace wallets](skills/trace-wallets/SKILL.md) · [checkpoint judge](skills/judge-checkpoints/SKILL.md) |
| Optional profile, never a bonus | `builder` adds independent exact-mint binding, a verified release **and** a verified demo. `social` adds mint binding, dated growth, independent sources and paid/organic separation. Require a matching, independent, fresh review with at least two distinct references. A reviewer’s `true` is not automatic verification of a source. [Profile handoff](notes/profile-review.md) |
| Size, time and account | Start with 1 virtual SOL; stake 0.01 SOL; at most one open position and one entry per mint. At signal time, probe the buy and reverse the expected net tokens. Both route plans must **include** the verified curve; its share need not be 100%. Require a modeled return ≥0.0095 SOL after costs, then wait ≥2 s and re-quote the buy. The delayed fill can have a different quantity. [Route and size audit](notes/technical-audit.md#3-check-the-route-and-the-amount-being-reversed). Keep the 0.03 SOL UTC-day net loss cap. A portfolio limit can stop later token checks from running. [Rules](rules.json) · [paper-trade skill](skills/paper-trade/SKILL.md) |

**How to read a decision.** A known `FAIL` gives `REJECT` under this policy, not “scam.” Otherwise any unresolved or waiting gate gives `WATCH`; `NOT_RUN` means the check wasn't performed. Only `PAPER_ELIGIBLE` allows an attempted entry; only `PAPER_BUY` records a simulated purchase. A provider problem can stop discovery (`STOP` or `DATA_GAP`), block a decision, produce `NO_FILL` on delayed entry, or leave an exit `EXIT_UNFILLED`. It does **not** always become WATCH. Automatic retries are off by default. With `scan --rechecks N`, only prior WATCH decisions at least 60 s old and still inside the mint age window can be selected.

**How to read an exit.** The normal exit is **due** at 120 s; it is not guaranteed to fill then. The full-balance sale still needs a usable quote within the absolute 3% impact cap, a delay and a fresh acceptable sell quote. A real 8%-impact quote rejected by policy is not proof that there was no route. With no fill, keep the position open. A zero stress value is **not** an observed sell price, spendable cash or a realized loss. See the [exit and reporting review](#technical-review) and [journal skill](skills/trade-journal/SKILL.md).

## Read the evidence

These are the **existing observations from 18 November 2026**, not new trades performed for this guide. Start with the [explanation of the two runs](examples/README.md). Keep their denominators separate.

| Recorded run | What happened | Open the actual export |
|---|---|---|
| New launches · about 08:12 UTC / 15:12 WIB | Four signatures: one failed transaction, three verified mints. All three passed the basic authority check; all three were **WATCH**. Two used Mayhem mode and the third used a non-SOL quote. **Zero simulated entries**, 1 virtual SOL unchanged. | [History CSV](examples/new-launch/history.csv) · [event details](examples/new-launch/events.jsonl) · [cash and counts](examples/new-launch/summary.json) |
| BONK · separate accounting check | Five wallet-free quotes on an established token. Simulated proceeds 0.009914993 SOL − 0.010000000 stake − 0.000030000 fees = **−0.000115007 SOL**. Rent reserve was returned, not counted as profit. This tests the arithmetic, not the new-launch strategy. | [History CSV](examples/calibration/history.csv) · [quote and fill receipts](examples/calibration/events.jsonl) · [cash and counts](examples/calibration/summary.json) |

**Trace one WATCH yourself.** Open the [new-launch history](examples/new-launch/history.csv). Its first `DECISION` is event **3**. Open [the corresponding events](examples/new-launch/events.jsonl) and inspect `payload.gates` for that ID. The market check cites a nonstandard mode; the distribution check could not reconcile supply. The flow and two-way quote checks say `NOT_RUN`. The log does **not** say that an exit was attempted and failed.

**Your files vs these files:** `report --out report-flow` writes *your* `history.csv`, `events.jsonl` and `summary.json` inside `report-flow`. The history CSV omits raw quote and sample-window rows; use the event file for those. An exported example is not a SQLite database and cannot be passed to `--db`. Use the [first-run steps](notes/first-run.md) to create a new ledger; don’t write over the examples.

## GitHub study

**What percentage of early buyers bought because of GitHub? Unknown.** The studies reviewed do not establish that percentage for Solana memecoins. Research on shared developers and correlated crypto returns is not research on why a particular buyer bought. [Study text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7744071/) · [research notes and other sources](notes/research.md).

1. **Own-project referrals, denominator = first buyers.** With consent, count attributable GitHub-referred first buyers divided by all first buyers in the same period. Report counts, response rate and unknowns; clicks are not purchases, and a referral is not proof of motivation.
2. **Market comparison, denominator = launches.** Class each launch by minute two: `none`, `link-only`, `verified`, or `unknown`. Compare the share reaching ≥20 new non-team buy wallets in minutes **(2,30]**, matching day, venue, opening depth, audience and paid exposure. Include quiet launches and keep missing follow-up separate from zero. This estimates association, not causation.

If many outcomes are missing, even the direction of the comparison can change. See the [worked example with 10 missing launches](notes/technical-audit.md#study-check-can-missing-outcomes-reverse-the-conclusion).

**To do the study:** read the [measurement skill](skills/measure-github/SKILL.md), use the [study protocol and column definitions](notes/study.md), then fill a copy of the [blank cohort CSV](templates/study.csv). Run the [calculator](tools/cohort.py) on your populated file: `python tools/cohort.py my-cohort.csv` from the kit root. `my-cohort.csv` is the name of **your copy**. Running it on the blank template shows zero launches and no estimate. The sampled launches above do not constitute a study.

**Project ideas to test, not rank:** a wallet-free meme remix tool, a small game with one replayable round, a treasury dashboard with checkable addresses, or an agent plugin with a working example. Measure use without a purchase and later retention. No repo genre has a demonstrated buyer multiplier in this guide.

## Skill map

These are **12 separate agent skills**. Each link opens the actual instructions for that job. Start with the [agent routing map](AGENTS.md) if more than one agent is involved.

| Work | Open the skill files |
|---|---|
| Create and maintain | [Launch design](skills/launch-design/SKILL.md) → [Launch rehearsal](skills/launch-rehearsal/SKILL.md) → [Launch disclosure](skills/launch-disclosure/SKILL.md) |
| Find and check | [Discover mints](skills/discover-mints/SKILL.md) → [Inspect chain](skills/inspect-chain/SKILL.md) + [Trace wallets](skills/trace-wallets/SKILL.md) |
| Verify off-chain claims | [Prove repository](skills/prove-repository/SKILL.md) and [Monitor attention](skills/monitor-attention/SKILL.md) |
| Decide and keep records | [Judge checkpoints](skills/judge-checkpoints/SKILL.md) → [Paper trade](skills/paper-trade/SKILL.md) → [Trade journal](skills/trade-journal/SKILL.md) |
| Measure instead of guessing | [Measure GitHub](skills/measure-github/SKILL.md) |

## Technical review

Read the [1.3 technical audit](notes/technical-audit.md) for concrete receipts, manual actions and proposed tests. The design review below remains applicable.

**Two sign-offs, not one Good+ score.** The [worksheet](templates/independent-signoff.md) makes this a review procedure today. The [scanner implementation](tools/lab.py) and [policy](rules.json) are unchanged. Do not treat the reporting and research proposals below as implemented switches.

### 1. Renew the creator verdict; date the trader verdict

An independent creator reviewer checks the finalized mint, supply, permissions, first buys, fees, vesting and venue custody. Record the slot and evidence. A day-seven holder result needs a defined day-one group and balance rule; later returning app users are a separate metric. For the paper verdict, record the mint, stage, size, time and token evidence, then report the portfolio's capacity **separately**. If it stopped later checks, those checks are not passed.

After migration or a change in rights, recheck the mint/pool, vaults and usable liquidity. In a concentrated-liquidity pool, recorded locked value is not necessarily active at today's price. For an upgradeable program, note its program ID, latest deployment slot and upgrade authority; a venue's upgrade key is not the issuer’s mint key. These are reviewer tasks. [Solana deployment docs](https://solana.com/docs/programs/deploying) · [Raydium active liquidity](https://docs.raydium.io/products/clmm/ticks-and-positions).

### 2. Show the denominator before judging concentration

Publish raw supply, the excluded vault and its balance, remaining balance, and number of positive-balance owners. Report both % of total supply and % **outside that vault**. Example: 4% of total with 80% held by the curve means 4/20 = **20% outside**. Outside does not mean freely unlocked.

With 16 outside owners even an equal split puts 10/16 = **62.5%** in the top ten. At least **17** are needed for a 60% cap to be possible; 17 wallets still need not be 17 people. A verified cap breach is `REJECT`. Automatic rechecks select `WATCH` only. If you study an initially rejected coin later, take a new dated observation; never rewrite the first decision.

### 3. Separate event time from when the agent knew

For each important fact save the mint/network, source and ID, event time or slot, first-seen UTC, decision UTC and policy/decoder version. A 12:01 release first seen at 12:08 cannot justify a 12:03 decision. Preserve edited calls and contradictory evidence without backdating a pass.

**Proposed coverage improvement:** a continuous collector would need a persisted cursor, finalized backfill, deduplication and explicit gaps after disconnects. The latest-N sampler does not provide that. An old mint found during a backfill is not a timely entry. Continue observing exits even if new entries must pause. [Signature ordering](https://solana.com/docs/rpc/http/getsignaturesforaddress) · [Solana RPC](https://solana.com/docs/rpc).

### 4. Distinguish unavailable exits from unacceptable prices

**In the kit:** the timed exit and 3% absolute impact cap can leave an open position. Inspect actual quote receipts and reasons; the `EXIT_UNFILLED` label alone is insufficient. A quote without a wallet is not proof of settlement. [Jupiter order reference](https://developers.jup.ag/docs/api-reference/swap/order).

**Proposed report labels:** explicit `NO_ROUTE_FROM_PROVIDER`, `DATA_UNKNOWN` for ambiguous errors, `QUOTED_BUT_OVER_CAP`, `LIMIT_MISSED`, `PAPER_FILLED`. Report the age and size of the last usable quote separately from a zero stress mark and realized cash. **Proposed size stress:** alongside 0.01 SOL, obtain 0.005 and 0.02 SOL probes when allowed. Reverse the **net token quantity at each size**. A half-size quote cannot fill a full-sized exit, and sequential observations are not simultaneous.

### 5. Separate a repo reference from maintainer consent

A repo link, a fee destination, original-maintainer confirmation of the exact mainnet mint, and a working pre-decision release are four distinct facts. Pump.fun announced fees could be assigned to **any GitHub account**; routing fees there is not that account's endorsement. For the builder profile the [reviewer](notes/profile-review.md) must also verify the demo. Two copies of one announcement are not two independent sources. [Pump.fun announcement](https://x.com/Pumpfun/status/2022029057869947173).

### 6. Follow tokens the scanner declined

**Research proposal:** before seeing outcomes, preselect a reproducible sample across `WATCH`, `REJECT` and eligible mints. Observe all groups at the same horizons, size and venues, without creating trades. Compare flow, builder and social policies on the **same** launches. At 30 minutes report the sampled count, complete follow-ups, share with a full-size sell quote, and blocked or missing exits. Show closed profit beside open positions and time cash was locked. A missing historical quote is not reconstructible as a fill. For pre-launch alerts, also count expiries, false alarms and coverage gaps.

**Three checks on interpretation:** ten outside owners can mean *verified creator facts, rejected paper entry*; an 8% sell quote can mean *route observed, policy refused it*; missing X history or maintainer confirmation arriving tomorrow means *no evidence for yesterday's pass*. These are examples of reasoning, not live results.
