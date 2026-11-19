# A useful GitHub percentage: data contract
**Question A: How many buyers discovered my token through GitHub?** Use opt-in referral/survey data. Publish the denominator, number of unknowns and response rate. A tag measures a visit or recorded referral, not why someone chose to buy. Distinct first-buy wallets are a proxy for buyers, especially with bots. GitHub traffic is only available to people with the required repository access and has a short window; it does not identify wallet purchases. [2](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository)

**Question B: Are launches with a useful, verified repo more likely to attract buyers?** This is a different denominator: *tokens*, not people. Example of the arithmetic only, **not observed data**: if 30/100 verified-repo launches and 20/100 no-repo launches met the same buyer threshold, rates are 30% vs 20%, a **10 percentage-point** difference or **50% relative lift**. It does not mean GitHub caused 50% of buyers to buy. Bigger teams, paid promotion, venue and market conditions could explain the difference.

## Collector requirements
1. Pick the venue, time span, launch clock and exclusions before collecting. Enumerate all finalized successful creates, even if there were no subsequent trades. If sampling, use a documented random rule independent of outcome. Keep outages, dead tokens and migrations. Do not discard a launch for lacking a URL. The included latest-N scanner is a functional sample, not such a feed.
2. Freeze the original metadata, time-stamped first-party repo association, release and demo observations by t0 + 120 seconds. A repo found on day 5 is **unknown at cutoff** unless you can establish that the evidence was publicly observed by cutoff. Do not use today's follower counts for yesterday’s decisions. Use four classes: `none` (sources checked), `link-only` (including an unsubstantiated backlink), `verified`, `unknown`. Track verified conflicts separately.
3. Decode swaps by mint across the curve and migrated markets. Count each non-team buy wallet whose **first actual buy** of this mint is in (t0+120s, t0+1,800s]; exclude transfers, routers and the creator's own buys. Do not recount a wallet that also bought before minute two. Track funder clusters separately and repeat analysis with and without ambiguous groups. Wallets are not people. If a feed ends at migration, mark follow-up as a gap until covered elsewhere.
4. Use non-market outcomes too: 1d/7d returning app users and release use. If studying price, register separate outcomes (e.g. sellable fee-adjusted SOL return for fixed size at 30m, unsellable share). A pool peak or graduation is not the buyer outcome.

## CSV columns
| Column | Value |
|---|---|
| `mint`, `created_at` | Exact mainnet address, UTC creation timestamp (ISO 8601). One row per launch. |
| `evidence_at`, `repo_group` | Cutoff snapshot timestamp between creation and +120s; blank/late snapshots become `unknown`. Include pre-launch artifacts in this snapshot only if their identity was already bound to the mint by the cutoff. |
| `launchpad`, `opening_depth_band` | Predefined venue and comparable initial real depth bands in a common unit. Use the initial configuration, not a later liquidity peak. |
| `prelaunch_audience_band`, `paid_at_cutoff` | Freeze bands from pre-launch evidence and known paid exposure by cutoff. Unknown is not “unpaid”. Missing/unknown strata are excluded from the matched estimate, not the raw group counts. |
| `followup` | `complete` or `gap`; gaps reported separately. Include zero only if you actually observed the full window. |
| `outcome_through`, `new_buy_wallets` | ISO time through which trades are covered (at least +30m), nonnegative integer number of first-time buy wallets within the window only. |

Run `python tools/cohort.py path/to/cohort.csv`. It prints raw successes and denominators for all four groups. It compares `verified` with `none` **within common strata** (UTC day, venue, opening depth band, audience band, known sponsorship); each stratum weight is the smaller group size. It reports the standardized difference in percentage points and the relative lift over the standardized baseline. No overlap → no estimate. A zero baseline → no relative lift. At least 10 day blocks and 30 observations in each matched arm are needed even to display a 1,000-resample day-cluster interval; they do **not** guarantee useful precision. Report excluded unmatched mints, group-specific gaps and worst/best-case missing-outcome sensitivity. Bots or teams can span days; also split by time and creator, check clustering and power. Do not turn selection bias into a marketing claim.

The [included study CSV](../templates/study.csv) has headers and **no observations**. Make a separate working copy and add your own measured rows. **No GitHub buyer percentage has been estimated for this kit.**

[Measurement skill](../skills/measure-github/SKILL.md) · [Calculator source](../tools/cohort.py) · [Research notes](research.md). The calculator does not fetch events or fill in the CSV. No matched groups, no baseline successes or too little follow-up can yield `null`; that does not mean a 0% effect.

**Missing-outcome check (manual):** report the [worst/best-case bounds](technical-audit.md#study-check-can-missing-outcomes-reverse-the-conclusion) next to each complete-case rate. These are not confidence intervals. Do not publish a direction of effect when gaps alone could reverse it.
