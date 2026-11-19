---
name: launch-rehearsal
description: Prepare and test a Solana mint, supply, permissions and launch venue on devnet; produce a human approval packet, not a mainnet transaction.
---

# Rehearse creation and disclose control
**Input:** An approved [launch brief](../../templates/launch-brief.md), supply and decimals, allocation table, launch venue, budget in SOL, custody plan and named human approvals. No seed phrases, private keys or funded agent wallet.

1. Pick **one** route. For the included scanner use a conventional SOL-quoted Pump curve. Inspect the current official creation interface and fee schedule; the lab decoder is pinned, not a promise about future upgrades. Or use the standard SPL mint + separately seeded pool path. A mint alone does not create a market. Raydium/other venues need their own checker.
2. Prepare a **working copy** of [templates/launch-proof.json](../../templates/launch-proof.json) as `draft`. A devnet rehearsal must remain labeled as such; the mainnet linter is not a test for this draft. Set integer base units (`UI supply × 10^decimals`), allocations totaling 10,000 bps, team and treasury addresses, first buys, vesting addresses/unlocks, metadata control, mint/freeze controls, each extension and every fee/recipient. List who can change each. Distinguish original supply allocation from a later secondary-market purchase.
3. Rehearse with a separate disposable **devnet** wallet. For a plain SPL mint, have the operator select devnet explicitly on every command. See the [devnet instructions](../../notes/devnet.md) for the mint → token account → issue supply → revoke mint → verify sequence. For a launchpad, use its supported test environment, not that SPL sequence on a live curve. If no test deployment exists for a feature, stop or use an isolated validator; do not substitute mainnet.
4. Verify from a second read RPC: right program, decimals, actual supply and authority values. For a curve identify the real base/quote vaults, protocol roles, graduation and migration behavior. For a pool show quote capital, LP withdrawal rights, exact % locked and unlock time or permanent proof. Test a small buy and sell only on the test network. Record what was **not** tested. Do not claim a lock before it exists.
5. Final gates: rights, legal/promotion review, treasury custody (e.g. independently controlled multisig), loss budget, explicit disclosure of incentives, supply reconciliation, rollback limits. Revoking a key or permanently locking LP can be irreversible. A failed dry run, wrong network or undisclosed privilege means **STOP**.

**Output:** your own runbook, copied from [templates/launch-runbook.md](../../templates/launch-runbook.md), with selected program/version, expected changes, test receipts, required fees/rent, risks and named approvers. Mainnet launch and public posting require separate human authorization outside this kit. Hand resulting confirmed public facts to [Launch disclosure](../launch-disclosure/SKILL.md).

**Kit location:** Run commands from the kit root, not this skill folder. See the [operator setup](../../README.md) and [agent routing map](../../AGENTS.md). `SOLANA_LAB_ROOT` is an optional agent convention; the Python tools do not read it.
