---
name: trace-wallets
description: Trace public creator, payer and funding roles; flag possible preparation or related-wallet activity without identifying real people.
---

# Follow public money, not personal identity
**Input:** Confirmed creation facts, bounded public wallet history, early trade events and a local list of known infrastructure hubs. Use only project-relevant public accounts; never seek names, addresses or private accounts.

1. Report three separate roles: transaction fee payer, create-user/signer (or program-authorized role), and creator recorded in the instruction. Also record fee recipient and metadata/treasury authority if independently proven. Do not infer control of all these roles by the same person.
2. `python tools/signals.py wallet PUBLIC_KEY --limit 8` records direct native system transfers and earlier decoded creates in a bounded recent sample. In the [paper scanner](../../tools/lab.py) only history **before the launch slot** counts for the pre-launch funding check. Save source, destination, amount, slot and transaction signature. A transfer is a fact; common control is a hypothesis. A missing history window cannot establish that a wallet is new.
3. For deeper review, follow at most two public funding hops and a fixed time budget. Stop at exchange withdrawals, bridge, relayer, router, airdrop distributor, unknown high-volume service or ambiguous custody; label `unresolved`. A common exchange funder alone is **not** a cluster. Compare same-source funding with independent evidence such as repeated joint exits across dated launches, or an explicitly disclosed project wallet. Note potential false positives such as fee sponsorship or a payroll batch.
4. For a pre-launch watch, compare the known public project wallet to its own prior activity: e.g. multiple recent creates plus a time-stamped public launch announcement. Save both events, alternative explanations and a 30-minute expiry. Funding alone, a normal authority change or one social post = weak watch only. Never predict the exact future mint or act on private order flow.
5. Label **observed** (signature/role), **possible** (shared pattern), **unknown** (hub/missing evidence). No claim about the “real founder” without a voluntary, publicly verifiable declaration; even then report exactly what was attested. A signed challenge proves key control, not legal identity.

**Output:** public roles, a short edge table, sample completeness, flags, competing explanations, confidence level and expiry. Hand material warnings to [Judge checkpoints](../judge-checkpoints/SKILL.md). Do not publish accusations or contact address owners.

**Kit location:** Run commands from the kit root, not this skill folder. See the [operator setup](../../README.md) and [agent routing map](../../AGENTS.md). `SOLANA_LAB_ROOT` is an optional agent convention; the Python tools do not read it.
