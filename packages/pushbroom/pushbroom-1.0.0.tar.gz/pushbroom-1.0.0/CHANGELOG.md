# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2021-01.27
### Changes
- Update minimum Python version to 3.6

## [0.3.2] - 2020-01-27
### Changes
- More bug fixes regarding incompatibility of Python 3.5 system calls with
  pathlib

## [0.3.1] - 2020-01-27
### Changes
- Use `Path.open()` instead of `open(Path)`, as the latter does not work in
  Python 3.5 (but does in 3.6 and on)
- Look for configuration in `/etc/pushbroom/pushbroom.conf` if not found in
  `$XDG_CONFIG_HOME`

## [0.3.0] - 2020-01-16
### Added
- Empty subdirectories are automatically removed from monitored directories.
  This can be changed with the new `RemoveEmpty` option.
### Changes
- Create `Trash` directory if it doesn't exist

## [0.2.1] - 2019-11-16
### Changes
- Coerce `Shred` option into a boolean

## [0.2.0] - 2019-11-16
### Added
- New `Shred` configuration option
- py.test dependency
- Unit tests

### Changed
- Update minimum Python version to 3.5
- `sweep()` no longer has optional arguments
- Make the ignore and match parameters use `re.compile()` instead of `r""`
- Use `pathlib` instead of `os.path`

## [0.1.5] - 2019-06-20
### Added
- `Match` configuration parameter

### Changed
- Logging output

## [0.1.4] - 2019-06-18
### Added
- Systemd service
- Add instructions in README for automating Pushbroom

## [0.1.3] - 2019-06-18
### Changed
- Update documentation

## [0.1.2] - 2019-06-18
### Added
- `CHANGELOG.md` to log changes
- Command line flag to print version information (`-V`)

## [0.1.1] - 2019-06-18
### Added
- `bin` directory containing an executable script

## [0.1.0] - 2019-06-18
- Initial Python release

[Unreleased]: https://github.com/gpanders/pushbroom/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/gpanders/pushbroom/compare/v0.3.2...v1.0.0
[0.3.2]: https://github.com/gpanders/pushbroom/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/gpanders/pushbroom/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/gpanders/pushbroom/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/gpanders/pushbroom/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/gpanders/pushbroom/compare/v0.1.5...v0.2.0
[0.1.5]: https://github.com/gpanders/pushbroom/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/gpanders/pushbroom/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/gpanders/pushbroom/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/gpanders/pushbroom/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/gpanders/pushbroom/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/gpanders/pushbroom/releases/tag/v0.1.0
