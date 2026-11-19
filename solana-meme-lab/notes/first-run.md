# First run and troubleshooting

**Reading only?** Nothing to install. On GitHub, read the Markdown or visit the published Pages site. In the [offline HTML guide](../Field-Guide.html), use its file links to read the relevant material offline. To run anything, clone the repository or extract the **whole** release kit into a writable folder and open a terminal *in the folder containing* the [operator instructions](../README.md), [rules](../rules.json) and `tools/`. Do not run from inside the ZIP or from inside the `skills/` folder. The HTML preview does not run Python or connect to a wallet.

## 1. Test offline first

Use Python 3.10 or newer. No `pip install` is needed for the included Python tools. Depending on your installation use `python`, `python3` or Windows `py -3` consistently. This is the complete first command sequence:

```bash
python --version
python -m unittest discover -s tests -v
```

Expected for this version: **14 tests, final status OK**. An `EXIT_UNFILLED ... no sell route` line from a test fixture is expected; it is not a live transaction. To see actual previously recorded results without calling any service, [read the two sample runs](../examples/README.md).

## 2. Try one wallet-free mainnet scan

Internet, a working mainnet read RPC, correct local clock and data-provider access are needed. No wallet or real SOL is needed. Start in `flow`, with no social credentials:

```bash
python tools/lab.py --db paper.sqlite scan --limit 3 --profile flow
python tools/lab.py --db paper.sqlite report --out report-flow
```

`--limit 3` means **up to three recent signatures**, not three new mints or three trades. Previously seen mints, unsuccessful transactions or unsupported layouts may produce no new candidate. The generated `paper.sqlite` is the ledger. `report-flow` is **your output folder**. The [bundled CSV](../examples/new-launch/history.csv), [detailed events](../examples/new-launch/events.jsonl) and [summary](../examples/new-launch/summary.json) show their formats, not the results of your run. The CSV is a short index; inspect `DECISION.payload.gates` in the event stream for the actual reasons. The summary's realized result and cash floor are different measures.

## 3. Keep or stop the experiment deliberately

One call does not start a bot. Run `manage` periodically in the **same** ledger if you want to check due exits. The normal 120-second hold starts at the simulated buy; a command run too early does not close it. A late call gets later quotes, not a backdated two-minute fill. Example finite calls:

```bash
python tools/lab.py --db paper.sqlite manage
python tools/lab.py --db paper.sqlite scan --limit 3 --rechecks 2 --profile flow
python tools/lab.py --db paper.sqlite report --out report-flow
```

Run one worker at a time. Two automatic rechecks can revisit up to two old-enough WATCH candidates still inside the entry window, **not** REJECT cases or a guarantee of two candidates. To stop, stop scheduling calls. Open paper positions remain open when saved. Do not delete a ledger to hide an unfilled exit; use dated export folders to retain previous reports. To test another profile, follow the [profile-review handoff](profile-review.md). For a second calibration use a **fresh calibration ledger**: the current budget rule permits only one entry per mint per ledger.

## Common surprises

| Symptom | Meaning and next action |
|---|---|
| No new printout, or only WATCH / REJECT | Open the exported event stream. Check `SAMPLE_WINDOW`, actual `DISCOVERED` count and gate reasons. Do not manufacture a fill or lower a gate to make it trade. |
| `NOT_RUN` vs `UNKNOWN` | `NOT_RUN` means an earlier checkpoint stopped later work. `UNKNOWN` means evidence was missing or could not be interpreted. Neither is a pass. A known hard failure can still give REJECT when other data is missing. |
| HTTP 403/429, stale data or RPC problem | Check access, clock and provider limits; back off. A global RPC failure may stop the command; per-mint gaps may instead be recorded. Record the time missed. Do not invent a price or infer fraud from an unavailable provider. |
| `STOP: not Solana mainnet-beta` | You supplied the wrong network to the scanner. Keep the [devnet issuer rehearsal](devnet.md) separate; a devnet mint is not a mainnet paper candidate. |
| Missing review, wrong mint, stale timestamp | Follow the [profile-review handoff](profile-review.md). A fresh review is not a replacement for missing market evidence. |
| `STOP: empty ledger` or mode/policy mismatch | Use the original DB path and the original rules; `scan` or `calibrate` initializes a ledger. Never use a calibration DB for new-launch research. The sample exports are not SQLite files. |
| `EXIT_UNFILLED` | Read the recorded reason and preceding quote or `QUOTE_UNUSABLE` event if present. A quote over the 3% impact cap is not the same as no quote. Do not credit sale proceeds. |
| Lock/busy error | Another worker may be using the same ledger. Let it finish. Do not delete a lock or start several copies. |

A portfolio already holding a coin can cause later token checks to be skipped, so a WATCH may describe **your book**, not a bad coin. Use the [checkpoint judge](../skills/judge-checkpoints/SKILL.md) and [journal skill](../skills/trade-journal/SKILL.md) to interpret results.

**Stopped in the middle?** A discovery can be saved without a decision. See the [interrupted-scan checklist](technical-audit.md#4-resume-an-interrupted-scan-without-inventing-a-decision) before scheduling another run. A report inspects; a recheck can create a **new** paper decision and fill.
