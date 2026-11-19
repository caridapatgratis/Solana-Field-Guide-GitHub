# Observed on 18 November 2026 — no real trade or token creation
**Discovery sample:** at approximately **15:12 WIB / 08:12 UTC**, sampled four most recent finalized signatures mentioning the Pump mint-authority PDA via a public mainnet RPC. One failed on chain. Three were verified creations; all three were WATCH. Each passed the narrowly defined mint/freeze/extension gate but did not clear other checkpoints. Two used Mayhem mode; the third used a non-SOL quote. The holder samples for two did not cover all supply, and the other had no outside-curve float at the snapshot. Named vendor alerts are stored as third-party reports, not our accusations. No rule was relaxed. No hypothetical entry price was assigned. These are **three observations**, not a market statistic or a blacklist.

To independently inspect one creation, see the [finalized transaction](https://explorer.solana.com/tx/5kFK93RzDV7epSAm9oHPMFYuHQUTrZaoksExTwRu5yiY52U1ApYUsk5qA4KcxGsJWnNxAnbW7k7ghvn4cxFUM7nt). The [new-launch event file](new-launch/events.jsonl) holds the exact mints, signatures, slot, time, risks, coverage and decisions; current token state may have changed.

**Separate quote/accounting calibration:** five live wallet-free Jupiter quotes on the established BONK mint. Simulated entry 08:11:27.429 UTC; simulated exit 08:11:42.003 UTC. Exact input 10,000,000 lamports; modeled position 31,324,460,123 raw token units. Sell output after haircut 9,914,993 lamports. Fees 15,000 + 15,000; rent reserve 3,000,000 released in full. Net = 9,914,993 − 10,000,000 − 30,000 = **−115,007 lamports = −0.000115007 SOL** (about −1.15% of the paper stake). The 30 bp per-side haircuts are already in these outputs. The quote timestamps, size, routes, fees and hashes are in [calibration event receipts](calibration/events.jsonl). It tests the math and network adapters, **not** the early-coin strategy or actual execution quality.

| Recorded run | Human-readable ledger | Decision / quote detail | Counts and cash |
|---|---|---|---|
| New mints: no simulated fill | [New-launch history](new-launch/history.csv) | [New-launch events](new-launch/events.jsonl) | [New-launch summary](new-launch/summary.json) |
| BONK: accounting only | [Calibration history](calibration/history.csv) | [Calibration events](calibration/events.jsonl) | [Calibration summary](calibration/summary.json) |

The unit tests include synthetic cases, one minimized real creation fixture and a check of the recorded calibration arithmetic. Synthetic test events are not mixed into these ledgers. The files above are **exports**, not a database to open with `--db`. The [first-run walkthrough](../notes/first-run.md) shows how to make your own DB and export to a different folder.

**Read the exact numbers:** the [technical audit](../notes/technical-audit.md) traces slots in new-launch decision 3 and the expected vs filled token units in BONK events 2 and 5. These are two separate ledgers; event IDs are local to each one.
