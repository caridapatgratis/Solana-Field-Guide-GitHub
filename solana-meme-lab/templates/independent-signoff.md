# Independent sign-off — two verdicts, not a token grade

Use this worksheet with the [disclosure skill](../skills/launch-disclosure/SKILL.md) and [checkpoint judge](../skills/judge-checkpoints/SKILL.md). It is a human/agent review record, **not an input the CLI accepts**. For builder or social entry checks, follow the separate [profile-review handoff](../notes/profile-review.md).

## A. Creator: do the public facts match?

- Network; mint; test vs mainnet; reviewer who did not prepare the packet:
- Evidence cutoff (UTC); verified slot; creation transaction; venue stage:
- Issuer's claim → independent evidence → matches / contradicts / unknown:
- Check supply and decimals, mint/freeze/other powers, team and treasury allocations, vesting, costs, current withdrawal rights, and any claimed software affiliation.
- Verdict (choose one): **DEVNET REHEARSAL ONLY / VERIFIED AT SLOT / MISMATCH / UNKNOWN**.
- Limitations and next required check (migration, unlock, program change or corrected disclosure):

## B. Sniper: can the paper account take this position now?

- Network; exact mint; UTC decision time; policy version; profile; intended paper size:
- Current market stage; evidence IDs/slots; complete or incomplete owner coverage:
- Buy and full-size reverse quote times/amounts **if checked**; adverse findings:
- Record each gate as pass, fail, waiting, unknown or not run. Record cash/position limits separately.
- Copy the actual ledger verdict if there is one: **REJECT / WATCH / PAPER_ELIGIBLE**. If the CLI has not run, mark **NOT ASSESSED**, not eligible. A later fill needs a separate ledger event.
- Next observation time and reason; unresolved conflicts:

Never put private keys, API credentials or personal identities here. Never copy an issuer's assertions into an independent review as proof.

## Evidence limits to attach to either verdict

- Actual slot of each read (or unknown); do not imply one slot for separate reads.
- Mint freeze authority vs checked account states; frozen raw units and coverage if known. Keep the policy denominator unchanged.
- If quoted: route contains the curve / curve-only proven / split or unknown share. Signal reverse quantity vs delayed buy quantity vs actual exit quantity.
- Kit version and tool hashes, not only the rules hash; decision event ID and any fill event ID in the same ledger.

Use the [worked technical audit](../notes/technical-audit.md) for examples. If multiple slots were used, scope each “verified at slot” claim to the slot that actually supports it.
