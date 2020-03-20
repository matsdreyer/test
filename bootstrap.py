#!/usr/bin/env python3
from platform import system
from pathlib import Path

_basedir = Path.cwd()
_home = Path.home()
_dotfiles = Path(_home, '.dotfiles')
_config = _basedir / 'config'
_is_mac = system() == 'Darwin'


def source():
    return Path.glob(_basedir, '**/*.symlink')


def destination(src):
    if 'config' in src.parts:
        return _home / '.config' / src.parent.relative_to(_config) / src.stem
    else:
        return _home / f'.{src.stem}'


def backup(dst):
    d = destination(dst)

    if d.is_symlink():
        d.unlink()
        print('[ removed symlink ]', d)
    elif d.is_file() or d.is_dir():
        d.rename(Path(f'{d}.bak'))
        print(f'[ moved file to ] {d}.bak')


def link_files(src, dst):
    if src.is_file():
        print('[ linked file ]', dst, '->', src)
    elif src.is_dir():
        print('[ linked dir ]', dst, '->', src)

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.symlink_to(src)


def macos():
    # TODO: macOS spesific shit
    pass


def install_dotfiles():
    # TODO: this is where shit happans
    src = source
    dst = destination
    # dst = destination

    print('')

    if _is_mac:
        print('Installing dotfiles on macOS\n')
    else:
        print('Installing dotfiles on Linux\n')

    print('Doing backups')
    for s in src():
        backup(s)

    print('')

    print('Linking files')
    for s in src():
        link_files(s, dst(s))


if __name__ == '__main__':
    install_dotfiles()
