# conan-or-tools

This is a conan recipe to download and install ortools (currently v8.0) from https://github.com/google/or-tools.

My ultimate goal is to build ortools without any dependencies, but pull them from conan-center.

I have not been able to build it this way without dependencies (`cmake.definitions['BUILD_DEPS'] = "OFF"`) and supplying the necessary dependencies via conan packages. Something always fails... :(

Any help is VERY welcome!
