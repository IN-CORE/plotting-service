# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [1.8.0] - 2021-02-07
### Changed
- Renamed master to main [#13](https://github.com/IN-CORE/plotting-service/issues/13)
- Reduced output container size [#17](https://github.com/IN-CORE/plotting-service/issues/17)
- Backward compatible with the dfr3 naming change [#19](https://github.com/IN-CORE/plotting-service/pull/19)

## [1.6.0] - 2021-10-27
### Added
- Add github action to build docker images [#2](https://github.com/IN-CORE/plotting-service/issues/2)
- 3D fragility plot and format the output correct for UI to consume [#1](https://github.com/IN-CORE/plotting-service/issues/1)

### Changed
- Update github action for automatic docker build [#4](https://github.com/IN-CORE/plotting-service/issues/4)

### Fixed
- Fix the cache.sqlite copy error in deployment [#7](https://github.com/IN-CORE/plotting-service/issues/7)


## [0.1.0] - not released
### Added
- Initial commit
- Generates sample points for plotting from fragility set JSON
- Supports 2D plots for both old and new formats of fragility
- Supports cache storage (sqlite3 database) for performance

