# Kit file index

Each path below is a direct link to a supplied file. All 27 Markdown files are listed, including this index. In the HTML reader, use the document title for the reading view or the adjacent **.md file** link for Markdown. On GitHub, each Markdown path below opens the file in the repository. If a preview blocks downloads, use this index or copy the exact source from the reader. Your database, finished manifest, per-mint reviews and report folders are not on this list: you create them.

## Getting started
| File | Use it for |
|---|---|
| [`FILES.md`](FILES.md) | **This file index.** Direct paths for human readers and agents. |
| [`FIELD-GUIDE.md`](FIELD-GUIDE.md) | **Field guide.** Workflows, evidence and the technical review. |
| [`Field-Guide.html`](Field-Guide.html) | **Offline HTML reader.** Navigable copy of the kit in a single file. |
| [`README.md`](README.md) | **Operator setup.** Installation, access and command syntax. |
| [`AGENTS.md`](AGENTS.md) | **Agent routing map.** Assign each task to a separate skill. |
| [`notes/first-run.md`](notes/first-run.md) | **First run and troubleshooting.** Try offline tests, scan once, then read your report. |
| [`notes/profile-review.md`](notes/profile-review.md) | **Profile-review handoff.** Prepare an independent per-mint review for the right ledger. |

## Agent skills
| File | Use it for |
|---|---|
| [`skills/launch-design/SKILL.md`](skills/launch-design/SKILL.md) | **Launch design.** Test the idea before the token. |
| [`skills/launch-rehearsal/SKILL.md`](skills/launch-rehearsal/SKILL.md) | **Launch rehearsal.** Plan and verify a test-network exercise. |
| [`skills/launch-disclosure/SKILL.md`](skills/launch-disclosure/SKILL.md) | **Launch disclosure.** Publish public facts and maintain corrections. |
| [`skills/discover-mints/SKILL.md`](skills/discover-mints/SKILL.md) | **Discover mints.** Verify a real creation, not a ticker. |
| [`skills/inspect-chain/SKILL.md`](skills/inspect-chain/SKILL.md) | **Inspect chain.** Check control, reserves and concentration. |
| [`skills/trace-wallets/SKILL.md`](skills/trace-wallets/SKILL.md) | **Trace wallets.** Separate public roles and funding evidence. |
| [`skills/prove-repository/SKILL.md`](skills/prove-repository/SKILL.md) | **Prove repository.** Verify mint affiliation, release and demo. |
| [`skills/monitor-attention/SKILL.md`](skills/monitor-attention/SKILL.md) | **Monitor attention.** Check source, time, growth and sponsorship. |
| [`skills/judge-checkpoints/SKILL.md`](skills/judge-checkpoints/SKILL.md) | **Judge checkpoints.** Read a REJECT, WATCH or PAPER_ELIGIBLE decision. |
| [`skills/paper-trade/SKILL.md`](skills/paper-trade/SKILL.md) | **Paper trade.** Understand quotes, delayed fills and exits. |
| [`skills/trade-journal/SKILL.md`](skills/trade-journal/SKILL.md) | **Trade journal.** Reconcile the simulated account. |
| [`skills/measure-github/SKILL.md`](skills/measure-github/SKILL.md) | **Measure GitHub.** Study referrals separately from market association. |

## Templates to copy
| File | Use it for |
|---|---|
| [`templates/launch-brief.md`](templates/launch-brief.md) | **Launch brief.** Starting idea, audience, economics and approval. |
| [`templates/launch-runbook.md`](templates/launch-runbook.md) | **Launch runbook.** Test plan, devnet receipts and stop conditions. |
| [`templates/launch-proof.json`](templates/launch-proof.json) | **Issuer proof template.** Draft disclosure; not a valid published mainnet manifest. |
| [`templates/address-card.md`](templates/address-card.md) | **Address card and corrections.** Share verified public facts after human approval. |
| [`templates/independent-signoff.md`](templates/independent-signoff.md) | **Independent sign-off worksheet.** Two verdicts for a reviewer; not a CLI input. |
| [`templates/review.json`](templates/review.json) | **Independent profile review.** Blank input to copy for a specific discovered mint. |
| [`templates/study.csv`](templates/study.csv) | **GitHub cohort CSV.** Headers only; add your own rows to a working copy. |

## Background and methods
| File | Use it for |
|---|---|
| [`notes/technical-audit.md`](notes/technical-audit.md) | **Technical audit.** Frozen balances, mixed slots, route and size checks, interruptions, code versions and study gaps. |
| [`notes/devnet.md`](notes/devnet.md) | **Devnet SPL rehearsal.** Human-operated plain-mint exercise; does not make a Pump curve. |
| [`notes/study.md`](notes/study.md) | **GitHub study protocol.** Cohort definition, columns, denominators and uncertainty. |
| [`notes/research.md`](notes/research.md) | **Research and primary sources.** What the evidence supports and what it does not. |

## Dated paper evidence
| File | Use it for |
|---|---|
| [`examples/README.md`](examples/README.md) | **Read the two recorded runs.** 18 November 2026: new-launch decisions vs a separate calibration. |
| [`examples/new-launch/history.csv`](examples/new-launch/history.csv) | **New-launch history.** Short index of discoveries, decisions and the failed signature. |
| [`examples/new-launch/events.jsonl`](examples/new-launch/events.jsonl) | **New-launch events.** Full receipts, gate reasons and skipped checks. |
| [`examples/new-launch/summary.json`](examples/new-launch/summary.json) | **New-launch summary.** Counts, no fills and unchanged cash. |
| [`examples/calibration/history.csv`](examples/calibration/history.csv) | **BONK calibration history.** One simulated buy and sell, not a new launch. |
| [`examples/calibration/events.jsonl`](examples/calibration/events.jsonl) | **BONK calibration receipts.** Five quotes and the paper-accounting events. |
| [`examples/calibration/summary.json`](examples/calibration/summary.json) | **BONK calibration summary.** Closed result, cash and open-position count. |

## Tools and tests
| File | Use it for |
|---|---|
| [`CHECKSUMS.sha256`](CHECKSUMS.sha256) | **Release checksums.** Compare the bytes of the source, docs and saved data with this edition. |
| [`rules.json`](rules.json) | **Paper policy.** The exact frozen thresholds the scanner reads. |
| [`tools/lab.py`](tools/lab.py) | **Paper scanner and ledger.** Finite commands, checkpoints, quotes, fills and exports. |
| [`tools/chain.py`](tools/chain.py) | **Chain evidence adapter.** Pinned Pump decoder, ownership, flow and wallet checks. |
| [`tools/common.py`](tools/common.py) | **Data access and settings.** Read-only transport, quote validation and policy hash. |
| [`tools/signals.py`](tools/signals.py) | **Public signal collector.** Repo, wallet, X and authorized Telegram observations. |
| [`tools/proof.py`](tools/proof.py) | **Issuer proof linter.** Checks selected published mainnet disclosure fields, not truth. |
| [`tools/cohort.py`](tools/cohort.py) | **GitHub cohort calculator.** Summarizes a supplied dataset; does not collect one. |
| [`tests/test_lab.py`](tests/test_lab.py) | **Offline test suite.** Tests include synthetic cases and a recorded receipt check. |
| [`tests/fixtures/finalized-create.json`](tests/fixtures/finalized-create.json) | **Minimized finalized creation.** The recorded transaction fixture used by the decoder test. |
