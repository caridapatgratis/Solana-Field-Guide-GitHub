# Hand off a builder or social review

Use this when a scanner should require a real software project or independent public attention **in addition to**, not instead of, its market checks. One database per profile keeps experiments apart, but the database name does **not** select the profile.

1. First discover a real mainnet mint with the chosen profile. Use the exact mint printed by the scanner or recorded in `DISCOVERED`. Do not use a ticker, test mint or an address from a post alone.
2. Keep the original [review template](../templates/review.json) blank. Make a `reviews` folder under the kit root. Save a **working copy** there named exactly the mint address followed by `.json`. This per-mint file is created by **you or your independent reviewer**; it does not ship in the kit.
3. Set `role` to `independent-reviewer`; enter a nonempty reviewer label, the matching mint, and `observed_at` as an ISO 8601 timestamp with timezone. The current rules check that the **review timestamp** is at most **600 seconds** old and not in the future. They do not check when each underlying source was published, whether it is still available, or whether the sources are independent. Preserve its publication time and your own first-seen time. A months-old release can still be usable if freshly verified; a late sighting cannot justify an earlier decision. Do not renew old evidence merely by changing its timestamp.
4. For `builder`, use the [repo verification skill](../skills/prove-repository/SKILL.md): confirm the exact mint from the original maintainer, the shipped release and a usable demo. For `social`, use the [attention skill](../skills/monitor-attention/SKILL.md): verify dated growth, independent mint-specific sources and separation of paid activity. Record distinct source references (at least two) and any verified conflict. Unknown stays `null`. Set a check to `true`, or `conflict` to `false`, only after actually checking. The program checks fields, time and the presence of references; it **does not independently open and authenticate those references**.
5. Run from the kit root. Below, replace `ACTUAL_MINT` with an address already discovered **in this same ledger**. The `scan` line is an initial discovery step; `recheck` is the follow-up after the reviewer saves the matching file. Both are paper only.

```bash
python tools/lab.py --db builder.sqlite scan --limit 3 --profile builder --reviews reviews
python tools/lab.py --db builder.sqlite recheck ACTUAL_MINT --profile builder --reviews reviews
python tools/lab.py --db builder.sqlite report --out report-builder
```

For the social experiment, use a **separate** `social.sqlite` and explicitly pass `--profile social --reviews reviews` on every `scan` and `recheck`. The default when `--profile` is omitted is `flow`, **even in a database named builder or social**. In `flow`, the reviews folder is optional; supply it if the flow judge should consider a documented public conflict. An unsupplied or stale review is not automatically checked elsewhere. A supplied stale review cannot clear an entry.

`manage` and `report` take `--db` before the subcommand and need no profile argument. A fresh profile review never overrides unsafe controls, inadequate market evidence or the portfolio limit. A review can be complete and still produce only WATCH or REJECT. For a fair study, compare profiles against the same captured launches, not two unrelated live samples. See [research design](study.md).
