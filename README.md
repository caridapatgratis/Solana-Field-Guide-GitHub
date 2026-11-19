# Solana-Field-Guide-GitHub

**First public release: v1.0.0** · Solana Memecoin Field Guide, edition **1.3** · [Release notes](releases/v1.0.0.md)

An independent guide to two different questions: **What can a creator prove about a mint?** And **what evidence would a paper trader need before counting an entry or an exit?** The kit includes 12 agent skills, copyable templates, dated examples, and a wallet-free Python paper lab. This is not a token launch, a live trading service, or an endorsement of any mint.

<!-- publication-links:start -->
[Open the interactive reader](https://caridapatgratis.github.io/Solana-Field-Guide-GitHub/) · [Read on GitHub](solana-meme-lab/FIELD-GUIDE.md) · [Browse all 27 Markdown files](solana-meme-lab/FILES.md) · [Download the kit](https://github.com/caridapatgratis/Solana-Field-Guide-GitHub/releases/latest/download/Solana-Memecoin-Skills.zip)
<!-- publication-links:end -->

| If you are here to… | Start with |
| --- | --- |
| Plan a launch or document what happened | [Creator workflow](solana-meme-lab/FIELD-GUIDE.md#creator-workflow) and [devnet rehearsal](solana-meme-lab/notes/devnet.md) |
| Understand the paper scanner before running it | [First run](solana-meme-lab/notes/first-run.md) and [recorded results](solana-meme-lab/examples/README.md) |
| Give an agent one bounded task | [Agent routing map](solana-meme-lab/AGENTS.md) |
| Inspect the assumptions, not just the conclusions | [Technical review](solana-meme-lab/FIELD-GUIDE.md#technical-review) and [independent sign-off worksheet](solana-meme-lab/templates/independent-signoff.md) |

## Interactive reader

Open the **Website** link under this repository’s **About** panel if the maintainer has published it. The website runs the guide’s search and navigation. Its **.md** links download the original Markdown text. To read the files on GitHub instead, use the [kit index](solana-meme-lab/FILES.md).

**Offline fallback:** open the [portable HTML file](docs/index.html) in the repository, choose **Download raw file**, then open the saved `.html` file in your browser. The GitHub file viewer itself does not run the reader. No account, wallet, or installation is needed for reading.

## Download the kit

Open **Releases** on this repository and choose **`Solana-Memecoin-Skills.zip`** under **Assets**. Extract it once; it contains `solana-meme-lab/`. The separate **`Solana-Field-Guide.html`** release asset is for reading without extraction. **`SHA256SUMS.txt`** covers both assets.

If no release is published yet, use **Code → Download ZIP** or clone the repository. Open the `solana-meme-lab/` directory inside that checkout or source archive. GitHub’s automatic *Source code (zip)* is a snapshot of the whole repository, not the curated release ZIP.

## Try the kit without using the network

From the repository root (Python 3.10+):

```bash
cd solana-meme-lab
python -B -m unittest discover -s tests -v
```

Expected: **14 tests, OK**. These tests do not connect a wallet or place trades. The optional live **read-only** commands are in the [operator manual](solana-meme-lab/README.md); they can depend on network and data-provider access. Do not put API credentials, signing keys, private reviews, or a paper ledger in a public repository.

**Versioning:** [VERSION](VERSION) tracks the GitHub release. The guide, readers and dated evidence retain their edition 1.3 labels. The [examples](solana-meme-lab/examples/README.md) are dated observations, not forecasts. The publishing changes affect how the guide is opened and downloaded, not the Python tools, rules, or recorded results.
