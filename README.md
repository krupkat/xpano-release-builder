# xpano-release-builder
Release builder for the Xpano project

# Release process

## GitHub

- Push a commit titled "Release x.y.z" with changes to the following files:

```
CHANGELOG.md
misc/build/linux/cz.krupkat.Xpano.metainfo.xml
xpano/version.h
```

```
git tag vx.y.z
git push origin HEAD --tags
```

- Draft a new release on github: https://github.com/krupkat/xpano/releases/new with title "x.y.z - Feature name"

- Execute binary builder: https://github.com/krupkat/xpano-release-builder/actions/workflows/build.yml with the tag "vx.y.z" as the argument

## Microsoft Store

- Go to "Developer PowerShell for VS 2022" and build the Microsoft Store package:

```
.\misc\build\build-windows-latest.ps1
.\misc\build\windows-store\package.ps1 $(identity) $(publisher) $(password) x.y.z
```

- Launch "Windows App Cert Kit" and make sure the `Xpano.msixbundle` package passes all checks.

- Upload the package through the "Microsoft Partner Center"

## Flathub

- Update the flatpak definition: https://github.com/flathub/cz.krupkat.Xpano/blob/master/cz.krupkat.Xpano.yaml
- Change both xpano tag and commit to the latest release, commit message "Update Xpano to x.y.x"
- Create pull request
- Wait for bot build (manual trigger by commenting "bot, build cz.krupkat.Xpano")
- Test the build (bot gives command in comment)
- Merge

## Ubuntu

```
git checkout vx.y.x
./misc/build/linux/make_tar.sh x.y.z
```

modify `debian/changelog.in`
 - fill release date with `date -R`
 - commit with message "version x.y.x"

```
./package.sh 0.12.0 jammy
./package.sh 0.12.0 kinetic
./package.sh 0.12.0 lunar

cd packages jammy
dput ppa:krupkat/code xpano_0.12.0-0~ppa1~jammy_source.changes

cd packages kinetic
dput ppa:krupkat/code xpano_0.12.0-0~ppa1~kinetic_source.changes

cd packages lunar
dput ppa:krupkat/code xpano_0.12.0-0~ppa1~lunar_source.changes
```

## nixpkgs

- sync the nixpkgs fork: https://github.com/krupkat/nixpkgs
- Update the derivation: https://github.com/krupkat/nixpkgs/blob/master/pkgs/applications/graphics/xpano/default.nix
- get the new hash by running `nix-prefetch-github krupkat xpano --fetch-submodules --rev vx.y.z`
- build and test: `nix-build . -A xpano`
- commit with description e.g.: "xpano: 0.17.0 -> 0.18.0"
- open a PR to nixpkgs
