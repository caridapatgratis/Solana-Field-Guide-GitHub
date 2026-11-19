# Creation rehearsal — operator only, no real SOL
Use this to learn the **plain-token** path. It does not launch a Pump curve, make a listing, or create liquidity. It is not used by the paper trader. No mint or public post was created for this kit.

**Before you start:** install the official Solana and `spl-token` CLIs, check versions/`--help`, and use a separately funded *devnet-only* signer controlled locally by the human. Never paste its seed or key into an agent. Use free test SOL. Check that the CLI and explorer both show devnet. The official SPL quickstart covers creating a mint, token account and supply. [1](https://solana.com/docs/tokens/quickstart)

This exercise is for the **plain-mint route only**. It creates an actual test mint using devnet funds. Keep the [runbook template](../templates/launch-runbook.md) open to record the network and receipts. The mainnet scanner deliberately rejects devnet RPCs. Do not run the next steps unless a human has approved a devnet exercise.

**Step A — identify the new test mint.** In a local Bash-compatible shell with a disposable devnet signer already configured in `DEVNET_ONLY_SIGNER`:

```bash
NET=https://api.devnet.solana.com
: "${DEVNET_ONLY_SIGNER:?set your local devnet-only signer path}"
unset MINT
st() { spl-token --url "$NET" --program-id TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA --owner "$DEVNET_ONLY_SIGNER" --fee-payer "$DEVNET_ONLY_SIGNER" "$@"; }
st create-token --decimals 6
```

**Step B — issue the test supply.** Stay in the **same shell**. Copy the exact newly printed devnet mint address into `MINT` when prompted. A ticker or an old environment variable is not a substitute. Stop if any command fails.

```bash
read -r -p 'Paste the NEW devnet mint from step A: ' MINT
: "${MINT:?new devnet mint required}"
st display "$MINT"
st create-account "$MINT"
st mint "$MINT" 1000
st supply "$MINT"
st display "$MINT"
```

**Step C — optional and irreversible.** Verify 1,000 whole test tokens = 1,000,000,000 raw units at six decimals. Only if the network, address and full supply match the approved test plan, the operator may revoke mint authority for that devnet mint. Do not run this merely to test a CLI installation.

```bash
st authorize "$MINT" mint --disable
st display "$MINT"
```

Record signatures, program ID, decimals, actual supply and the **observed** authority values. After a successful step C the mint authority should be absent; if you skipped step C it should still be present. Verify freeze authority independently (this example did not request one) and, if using metadata, check its update rights separately. Verify from an independent devnet read RPC; a screenshot is not evidence. A zero mint authority is not the same thing as a zero freeze or metadata authority. [1](https://solana.com/docs/tokens/basics/set-authority)

**Next, pick a market path, not both.**
- **Launchpad curve (compatible concept for the supplied scanner):** the program creates its own mint/curve. Do **not** pre-mint a separate SPL token and present it as the Pump mint. Select the simple native-SOL quote path, review mode/fees, creation roles, actual initial buy, real and virtual reserves, and what happens at migration. Use the current verified venue documentation. [1](https://github.com/pump-fun/pump-public-docs)
- **Direct pool:** budget real quote-side capital, calculate the implied opening exchange rate and real exit proceeds at multiple sizes. Show who owns the LP tokens or position, how much can be removed, what was locked and who can claim fees. A permanent lock is irreversible. The starter scanner cannot verify direct-pool launches. [1](https://docs.raydium.io/user-flows/burn-and-earn)

For either path, price a budget on the actual day (rent, base/priority fees, venue/creator fees, hosting, liquidity capital where applicable, maintenance). Never call locked capital a guaranteed recoverable expense. No mainnet publishing or signing is automated here.
