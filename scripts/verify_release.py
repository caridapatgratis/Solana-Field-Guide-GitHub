"""Verify the two prepared release downloads against this checkout. Offline, read-only, stdlib only."""
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import re
from zipfile import BadZipFile, ZipFile

REPO = Path(__file__).resolve().parents[1]
KIT = REPO / 'solana-meme-lab'
ZIP = 'Solana-Memecoin-Skills.zip'
HTML = 'Solana-Field-Guide.html'


def verify(condition, message):
    if not condition:
        raise ValueError(message)


def hashes(manifest):
    result = {}
    for line in manifest.read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        verify(match, 'Invalid SHA-256 line in ' + manifest.name)
        digest, name = match.groups()
        path = PurePosixPath(name)
        verify(not path.is_absolute() and name == path.as_posix() and name != '.' and '..' not in path.parts
               and '\\' not in name and ':' not in name and name not in result, 'Invalid or repeated manifest path')
        result[name] = digest
    return result


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, default=REPO.parent / 'release-assets',
                        help='Folder holding the three release assets (default: ../release-assets next to the repository)')
    assets = parser.parse_args().assets
    try:
        downloads = hashes(assets / 'SHA256SUMS.txt')
        verify(set(downloads) == {ZIP, HTML}, 'SHA256SUMS.txt must list the curated ZIP and standalone HTML')
        for name, digest in downloads.items():
            verify(sha(assets / name) == digest, 'Release asset checksum mismatch: ' + name)
        verify((assets / HTML).read_bytes() == (REPO / 'docs/index.html').read_bytes(), 'Standalone HTML differs from docs/index.html')
        sources = hashes(KIT / 'CHECKSUMS.sha256')
        for name, digest in sources.items():
            verify(sha(KIT / name) == digest, 'Kit source checksum mismatch: ' + name)
        kit_files = sorted(set(sources) | {'CHECKSUMS.sha256', 'Field-Guide.html'})
        expected = {'solana-meme-lab/' + n for n in kit_files}
        with ZipFile(assets / ZIP) as archive:
            entries = [i.filename for i in archive.infolist() if not i.is_dir()]
            verify(len(entries) == len(expected) and set(entries) == expected, 'Unexpected, missing or repeated kit files in ZIP')
            for name in kit_files:
                verify(archive.read('solana-meme-lab/' + name) == (KIT / name).read_bytes(), 'ZIP differs from kit: ' + name)
        print(f'OK: 2 release assets, {len(sources)} kit source hashes, {len(kit_files)} ZIP files; standalone reader matches docs/index.html.')
    except (OSError, KeyError, ValueError, BadZipFile) as exc:
        parser.exit(1, f'Verification failed: {exc}\n')


if __name__ == '__main__':
    main()
