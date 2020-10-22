# conan-or-tools

This is a conan recipe to download and install ortools (currently v8.0) from https://github.com/google/or-tools.

My ultimate goal is to build ortools without any dependencies, but pull them from conan-center.

I have not been able to build it this way without dependencies (`cmake.definitions['BUILD_DEPS'] = "OFF"`) and supplying the necessary dependencies via conan packages. Something always fails... :(

Any help is VERY welcome!

## conan workflow

1. conan install . -pr vs2019_debug
2. conan source . (or, alternatively: cd or-tools; git clean -fd; cd ..)
3. copy Find\* to or-tools/cmake folder (make sure to overwrite existing ones there, e.g. Findglog.cmake)
4. conan build .
5. conan package .
6. conan export-pkg . user/testing --package-folder=package -pr vs2019_debug --force
7. conan test test_package ortools/8.0@user/testing -pr vs2019_debug

## CHANGELOG

## [Unreleased]

## [0.1.0] - 2020-10-22

### Added

- merger of my previos conanfile.py and the one provided by @Talkless [here](https://gist.github.com/Talkless/a2eda9abfb005bd314c92140e72c3b2b)
- all cmake build options for or-tools as options for conan (all untested)

[unreleased]: https://github.com/philsuess/conan-or-tools
[0.1.0]: https://github.com/philsuess/conan-or-tools/tags/v0.1.0
