# Launch rehearsal runbook — fill in a working copy

Use with the [rehearsal skill](../skills/launch-rehearsal/SKILL.md) and [devnet instructions](../notes/devnet.md). This is a **plan**, not a mainnet deployment command. Do not put secrets, signer paths or nonpublic launch times in any copy shared with the scanner.

| Decision | Record before rehearsal |
|---|---|
| Scope | Project, test network, date (UTC), operator, independent reviewer. |
| Market route | Launchpad-created mint and curve **or** plain mint plus separately seeded pool. Name program, tested version/mode, quote asset and limits of the test environment. |
| Supply | Decimals, initial supply in whole tokens **and** raw units, allocation percentages totaling 100%, team purchases, vesting and unlocks. |
| Control | Expected mint, freeze and metadata authorities; extensions; program upgrade authority if applicable. State who can change what. |
| Money and liquidity | Budget ceiling, fee recipients and rights. For a curve: real reserve vs virtual reserve and migration rule. For a pool: both vaults, LP/position owner, amount locked, expiry and withdrawal rights. |
| Approval | Explicit stop conditions, irreversible actions, who approves each step, how a mistake will be disclosed. |

## Evidence from the test network

| Test | Expected | Observed: network, address, signature/slot, UTC | PASS / FAIL / NOT TESTED |
|---|---|---|---|
| Create and identify the test mint | | | |
| Reconcile supply and permissions | | | |
| Check distribution and venue custody | | | |
| Test a buy and a sell on the supported test venue | | | |
| Re-read from an independent source | | | |

Record discrepancies, what was not possible on devnet, and who must resolve it. **Rehearsal verdict:** ready for independent review / wait / stop. A devnet receipt is not evidence that the corresponding mainnet launch exists or is tradable.

**Handoff:** prepare the [launch proof template](launch-proof.json). After a real mainnet creation, have an independent reviewer complete the [two-verdict worksheet](independent-signoff.md) with fresh public facts. No token is deployed by this template.
