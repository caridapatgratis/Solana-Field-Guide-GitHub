"""Set the two public links in README.md. Uses only local Git configuration; no network calls."""
import argparse
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BEGIN = '<!-- publication-links:start -->'
END = '<!-- publication-links:end -->'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', nargs='?', help='GitHub.com OWNER/REPO or clone URL; defaults to local remote origin')
    parser.add_argument('--pages-url', help='The exact HTTPS site URL for a custom Pages address')
    args = parser.parse_args()
    value = args.repository
    if value is None:
        try:
            value = subprocess.run(['git', '-C', str(ROOT), 'remote', 'get-url', 'origin'],
                                   capture_output=True, text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            parser.error('Set the Git remote origin first, or pass your actual GitHub OWNER/REPO.')
    name = value.strip()
    for prefix in ('https://github.com/', 'git@github.com:', 'ssh://git@github.com/'):
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    name = name.rstrip('/').removesuffix('.git')
    if not re.fullmatch(r'[A-Za-z0-9-]+/[A-Za-z0-9._-]+', name):
        parser.error('Use a GitHub.com OWNER/REPO or a clean clone URL, without embedded credentials.')
    owner, repo = name.split('/')
    if owner == 'YOUR-OWNER' or repo in {'.', '..'}:
        parser.error('Use your real GitHub owner and repository name, not the instructions placeholder.')
    site = f'https://{owner.lower()}.github.io/'
    if repo.lower() != owner.lower() + '.github.io':
        site += repo + '/'
    if args.pages_url:
        site = args.pages_url.strip().rstrip('/') + '/'
        u = urlsplit(site)
        if (u.scheme != 'https' or not u.hostname or u.username or u.password or u.netloc.lower() != u.hostname
                or u.query or u.fragment or not re.fullmatch(r'https://[A-Za-z0-9._~/%-]+/', site)):
            parser.error('--pages-url must be a clean HTTPS site URL, with no credentials, spaces, query, or fragment.')
    downloads = f'https://github.com/{name}/releases/latest/download/Solana-Memecoin-Skills.zip'
    block = '\n'.join([BEGIN, f'[Open the interactive reader]({site}) · [Read on GitHub](solana-meme-lab/FIELD-GUIDE.md) · [Browse all 27 Markdown files](solana-meme-lab/FILES.md) · [Download the kit]({downloads})', END])
    file = ROOT / 'README.md'
    text = file.read_text(encoding='utf-8')
    if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(BEGIN) >= text.index(END):
        parser.error('README publication markers are missing or out of order.')
    new = text[:text.index(BEGIN)] + block + text[text.index(END) + len(END):]
    if text != new:
        file.write_bytes(new.encode('utf-8'))
    print('Reader:', site, '\nKit:', downloads)
    print('README configured locally. These links go live after Pages and the named release asset are published.')


if __name__ == '__main__':
    main()
