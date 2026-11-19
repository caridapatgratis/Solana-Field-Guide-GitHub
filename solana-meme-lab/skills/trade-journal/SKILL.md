---
name: trade-journal
description: Export the full decision and paper-trade history, reconcile cash and evaluate performance without removing losing, skipped or unsellable positions.
---

# Journal and review
**Input:** The paper SQLite file and original [rules.json](../../rules.json). Run `python tools/lab.py --db paper.sqlite report --out report`. For reproducibility keep the [release checksums](../../CHECKSUMS.sha256), mode, profile, code version and policy hash; a policy hash alone does not identify the code. For a changed policy, start a separate database; never edit old events to improve the result.

1. Export to **your own report folder**. In it, `events.jsonl` is the complete stream, including quotes, sample windows and decision details; `history.csv` is a short index that **omits `QUOTE` and `SAMPLE_WINDOW`**; `summary.json` shows cash, realized results, positions and mode. Compare the supplied [example events](../../examples/new-launch/events.jsonl), [example CSV](../../examples/new-launch/history.csv) and [example summary](../../examples/new-launch/summary.json). Preserve the complete JSONL, including failures and gaps. Join buys/sells by `position` and quotes by event ID. Wallet/source IDs may be public but do not attach private identities.
2. Reconcile cash in raw units: start − stakes − all modeled fees − rent reserves + sell proceeds + released rent. Reserve is not profit. Reconcile token balances separately. Never count a mark as spendable SOL. A position without an exit is still open; show units, age, last attempted exit, reason and conservative zero liquidation mark.
3. Daily report: all candidate signatures, confirmed new mints, `REJECT`/`WATCH` reasons, eligible signals, actual paper fills, unfilled exits, median signal-to-entry time. Report both closed win rate **with its denominator** and blocked/open share. For performance calculate net return on starting paper capital and drawdown including a zero-mark stress case, not just the hottest trade. The supplied summary covers counts/cash; derive per-profile diagnostics from the JSONL/CSV.
4. For comparisons, use separate shadow books with the same dates, capital, latency, sizing and exit rules. Compare no-trade cash, safety+flow, safety+flow+repo and safety+flow+social. An additional randomized entry control must use the same eligible universe and costs. Never remove delisted/failed tokens or pool calibration data with strategy data.
5. Review after several market regimes and a held-out time period. Run worse latency/fees and missing-quote stress. Track data gaps and provider changes. Pause if results depend on one day, one token, zero-fee fills or ignoring stranded capital. No automatic graduation to real trading. For a blocked exit or missing follow-up, see the [technical review](../../FIELD-GUIDE.md#technical-review).

**Output:** machine-readable ledger plus one-page count → decisions → fills → realized cash report. If the denominator is too small, write **not enough evidence**, not an annualized return.

**Kit location:** Run commands from the kit root, not this skill folder. See the [operator setup](../../README.md) and [agent routing map](../../AGENTS.md). `SOLANA_LAB_ROOT` is an optional agent convention; the Python tools do not read it.
