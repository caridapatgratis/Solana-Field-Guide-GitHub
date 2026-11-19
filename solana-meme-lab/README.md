# Operator guide: install and run the kit

**Start with the [field guide](FIELD-GUIDE.md)** for the two Good+ decisions, or the [first-run walkthrough](notes/first-run.md) for commands and expected outputs. This release packages the technical review and all linked resources together. Nothing starts when you open the guide. Use the [file index](FILES.md) to find any packaged resource.

## Set up an agent

1. Clone the repository or extract the full release ZIP. In either case, open the `solana-meme-lab` directory. Work from the directory containing [the rules](rules.json), `tools/`, `skills/` and `templates/`. Keep them together. The Python tools use the standard library; no wallet or package install is required. Use Python 3.10+. The separate human-run [devnet rehearsal](notes/devnet.md) does require the Solana CLIs and a disposable test signer.
2. Give your agent the [routing map](AGENTS.md). If it has a skill loader, register the individual skill directories listed there, not the whole ZIP as one skill. Each directory has its own linked instruction file and YAML frontmatter. Prefer using the in-place directories. If you must install copies in another directory, also give the agent the kit root; relative documentation links resolve in the **complete kit**, not in an isolated copied folder.
3. Run commands from the kit root. `SOLANA_LAB_ROOT` is an optional name for your agent's workspace path, **not** an environment variable that makes the Python CLI change directory. The scanner reads public mainnet data and writes a local ledger. Do not give it a private key, seed, signer or internal launch schedule.

Sample task: “Use [mint discovery](skills/discover-mints/SKILL.md), the [checkpoint judge](skills/judge-checkpoints/SKILL.md) and the [journal](skills/trade-journal/SKILL.md). Sample three recent signatures, manage any due paper exits, export all decisions and explain the skips.”

## One finite paper run

```bash
python -m unittest discover -s tests -v
python tools/lab.py --db paper.sqlite scan --limit 3 --profile flow
python tools/lab.py --db paper.sqlite manage
python tools/lab.py --db paper.sqlite report --out report-flow
```

`manage` can be silent when nothing is open or due. For an ongoing study, schedule short calls **serially**; for example, attempt `manage` every 10–15 s and `scan` every 30–60 s, if the provider budget allows. `scan` checks due exits first. `--rechecks 2` can revisit up to two prior WATCH decisions at least 60 s old while the mint is still within the 30-minute entry window; REJECT is not automatically revisited. A DB pins the run mode and [rules hash](rules.json), **not the entry profile**. Always pass `--profile builder` or `--profile social` and `--reviews reviews` on both `scan` and `recheck` for those experiments. See the [profile setup with exact commands](notes/profile-review.md).

Use `--db` **before** the subcommand, and `--out` **after** the `report` subcommand. One process per ledger; keep the DB and its rule version backed up. The rules hash does not identify the Python code; save the [release checksums](CHECKSUMS.sha256) and your chosen profile with each export. New modes or rule versions need a separate DB. A report export can replace files in its output directory; use a new directory for snapshots. Never overwrite the [supplied sample exports](examples/README.md).

## Optional data access

| Data | Access and limits |
|---|---|
| Solana and RugCheck | `SOLANA_RPC_URL` is optional. Use a trusted mainnet HTTPS RPC with finalized signatures, transactions (up to v1) and account queries. `SOLANA_INDEXED=1` optionally enables a mint-filtered full-account lookup when the initial list cannot reconcile. Provider limits can still leave ownership unknown. RugCheck is an additional public report, not a security certificate. |
| Jupiter | The tool can read `JUPITER_API_KEY` from the environment. The [V2 order reference](https://developers.jup.ag/docs/api-reference/swap/order) lists the API key header as required. Keyless reads worked for the **recorded sample**; do not assume that access today. An access error is a data gap, not evidence that no route exists. No taker, signing or execution. |
| GitHub | `GITHUB_TOKEN` is optional for approved public reads. Use [repo verification](skills/prove-repository/SKILL.md) before accepting affiliation. |
| X / Telegram | `X_BEARER_TOKEN` requires permitted X API access and may incur provider charges. `TELEGRAM_BOT_TOKEN` must belong to a dedicated bot permitted in the allowlisted channels. Use polling or webhook, not both. Polling advances the bot's update cursor. Neither authenticated feed was tested in the bundled examples. Without access, historical attention is unknown. |

Put secrets only in your local environment, not in a guide, exported history or shared review. `--out` for the **signal** tool goes **before** its subcommand. These are command patterns; replace capitalized placeholders and the illustrative channel ID with your approved inputs:

```bash
python tools/signals.py --out signals.jsonl repo OWNER/REPO --mint MINT
python tools/signals.py --out signals.jsonl wallet PUBLIC_ADDRESS --limit 8
python tools/signals.py --out signals.jsonl x-user HANDLE --follower-sample
python tools/signals.py --out signals.jsonl x-posts MINT
python tools/signals.py --out signals.jsonl x-trends 1
python tools/signals.py --out signals.jsonl telegram --allow-channel-ids=-1001234567890
```

Repeat follower snapshots into the same output file for the same numeric account. The [attention skill](skills/monitor-attention/SKILL.md) explains edited posts, location-specific trends and missing history. The signal file is supporting evidence; it is **not** imported into the paper ledger as a `PASS`. Use the [independent review workflow](notes/profile-review.md).

## What runs today

| Available | What it does not do |
|---|---|
| [Paper scanner](tools/lab.py): verified Pump creates, limited chain and wallet checks, real quote probes, simulated fills and exports. | Conventional active native-SOL Pump curve **entries** only. No guaranteed coverage of every mint or first-slot fill. No automated new AMM entries. |
| [Public signal collector](tools/signals.py): repo, wallet, X and Telegram observations with permitted access. | No real-person identification, private-channel scraping, automatic endorsement, or reliable prediction of a future mint. |
| [Creator skills](skills/launch-design/SKILL.md), [rehearsal runbook template](templates/launch-runbook.md) and [proof linter](tools/proof.py). | Lint checks disclosure shape, not truth. No automated mainnet mint, public posting or signing. |
| [GitHub cohort calculator](tools/cohort.py) for a completed, time-stamped cohort. | It does not collect the population or compute a buyer-attraction rate from a blank sheet. See the [study instructions](notes/study.md). |
| Two independent verdicts, size stress tests, detailed exit-reason reporting and follow-up on rejected tokens are described in the [technical review](FIELD-GUIDE.md#technical-review). | The [two-verdict worksheet](templates/independent-signoff.md) is manual. The proposed structured exit labels, multi-size trials and population follow-up are **not new CLI features**. |

**Calibration only:** `python tools/lab.py --db calibration.sqlite calibrate` uses an established BONK mint and a 12 s hold target, not the new-launch gates. One complete cycle ordinarily requests five live quotes. Use `manage` later if an exit is still open. Use a fresh calibration DB for a new independent trial; never pool it with the strategy. For the original arithmetic see the [calibration history](examples/calibration/history.csv) and [receipts](examples/calibration/events.jsonl).
