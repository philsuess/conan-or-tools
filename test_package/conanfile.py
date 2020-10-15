from conans import ConanFile, CMake, tools
import os


class ORToolsTestConan(ConanFile):
    # TBD settings = "os", "compiler", "build_type", "arch", "os_build", "arch_build"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake_find_package_multi"
    #generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.verbose = True
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            if self.settings.os == "Windows":
                if self.settings.build_type == "Release":
                    os.chdir("Release")
                if self.settings.build_type == "Debug":
                    os.chdir("Debug")
            self.run(".%stest_or_tools" % os.sep)
