import os
from conans import ConanFile, CMake, tools
from shutil import copyfile


class GORTConan(ConanFile):
    name = "ortools"
    version = "8.0"
    license = "Apache License 2.0"
    url = "https://github.com/google/or-tools/"
    description = "Google Optimization Tools"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_find_package"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "BUILD_DEPS": [True, False],
        "BUILD_ZLIB": [True, False],
        "BUILD_absl": [True, False],
        "BUILD_gflags": [True, False],
        "BUILD_glog": [True, False],
        "BUILD_Protobuf": [True, False],
        "USE_SCIP": [True, False],
        "BUILD_SCIP": [True, False],
        "USE_COINOR": [True, False],
        "BUILD_CoinUtils": [True, False],
        "BUILD_Osi": [True, False],
        "BUILD_Clp": [True, False],
        "BUILD_Cgl": [True, False],
        "BUILD_Cbc": [True, False],
        "BUILD_SAMPLES": [True, False],
        "BUILD_EXAMPLES": [True, False]
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        'BUILD_DEPS': False,
        'BUILD_ZLIB': False,
        'BUILD_absl': False,
        'BUILD_gflags': False,
        'BUILD_glog': False,
        'BUILD_Protobuf': True,
        'USE_SCIP': False,
        'BUILD_SCIP': False,
        'USE_COINOR': True,
        'BUILD_CoinUtils': False,
        'BUILD_Osi': False,
        'BUILD_Clp': False,
        'BUILD_Cgl': True,
        'BUILD_Cbc': True,
        'BUILD_SAMPLES': False,
        'BUILD_EXAMPLES': False
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.settings.compiler.cppstd != 17:
            raise ConanInvalidConfiguration(
                "c++17 is required to build or-tools")
        if self.settings.os == "Windows" and self.options.shared:
            raise ConanInvalidConfiguration(
                "Shared build is not supported on Windows by upstream")

    def requirements(self):
        if not self.options.BUILD_ZLIB:
            self.requires("zlib/1.2.11@")

        if not self.options.BUILD_gflags:
            self.requires("gflags/2.2.2@")

        if not self.options.BUILD_glog:
            self.requires("glog/0.4.0@")

        if not self.options.BUILD_absl:
            self.requires("abseil/20200923.2@")

        if not self.options.BUILD_CoinUtils:
            self.requires("coin-utils/2.11.4@")

        if not self.options.BUILD_Osi:
            self.requires("coin-osi/0.108.6@")

        if not self.options.BUILD_Clp:
            self.requires("coin-clp/1.17.6@")

    @property
    def _archive_url(self):
        return "https://github.com/google/or-tools/archive/v%s.tar.gz" % self.version

    @property
    def source_subfolder(self):
        return "or-tools"

    def source(self):
        if self.settings.os == "Windows":
            tools.get(self._archive_url)
            archive = "or-tools-{}".format(self.version)
            os.rename(archive, self.source_subfolder)
            # self.run("git clone https://github.com/google/or-tools")
            # self.run("cd or-tools && git checkout tags/v%s -b v%s" %
            #         (self.version, self.version))
        else:
            # from https://developers.google.com/optimization/install/cpp/linux
            url = "https://github.com/google/or-tools/releases/download/v%s/" % self.version
            zip_file_name = "or-tools_Ubuntu-20.04_v8.0.8283.tar.gz"
            tools.get(url + zip_file_name)
            os.rename("or-tools_Ubuntu-20.04-64bit_v8.0.8283", "or-tools")

    def build(self):
        if self.settings.os == "Windows":
            cmake = CMake(self)
            cmake.definitions['BUILD_DEPS'] = "ON" if self.options.BUILD_DEPS else "OFF"
            cmake.definitions['BUILD_ZLIB'] = "ON" if self.options.BUILD_ZLIB else "OFF"
            cmake.definitions['BUILD_absl'] = "ON" if self.options.BUILD_absl else "OFF"
            cmake.definitions['BUILD_gflags'] = "ON" if self.options.BUILD_gflags else "OFF"
            cmake.definitions['BUILD_glog'] = "ON" if self.options.BUILD_glog else "OFF"
            cmake.definitions['BUILD_Protobuf'] = "ON" if self.options.BUILD_Protobuf else "OFF"
            cmake.definitions['USE_SCIP'] = "ON" if self.options.USE_SCIP else "OFF"
            cmake.definitions['BUILD_SCIP'] = "ON" if self.options.BUILD_SCIP else "OFF"
            cmake.definitions['USE_COINOR'] = "ON" if self.options.USE_COINOR else "OFF"
            cmake.definitions['BUILD_CoinUtils'] = "ON" if self.options.BUILD_CoinUtils else "OFF"
            cmake.definitions['BUILD_Osi'] = "ON" if self.options.BUILD_Osi else "OFF"
            cmake.definitions['BUILD_Clp'] = "ON" if self.options.BUILD_Clp else "OFF"
            cmake.definitions['BUILD_Cgl'] = "ON" if self.options.BUILD_Cgl else "OFF"
            cmake.definitions['BUILD_Cbc'] = "ON" if self.options.BUILD_Cbc else "OFF"
            cmake.definitions['BUILD_SAMPLES'] = "ON" if self.options.BUILD_SAMPLES else "OFF"
            cmake.definitions['BUILD_EXAMPLES'] = "ON" if self.options.BUILD_EXAMPLES else "OFF"
            cmake.configure()
            cmake.build()
            cmake.install()
        else:  # assume Linux or compatible
            pass

    def package(self):
        if self.settings.os == "Windows":
            tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        else:  # assume Linux or compatible
            self.copy("LICENSE*", src="or-tools/", dst=".")
            self.copy("*", src="or-tools/include", dst="include")
            self.copy("*", src="or-tools/lib", dst="lib")

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.cxxflags = ["-DUSE_CBC",
                                      "-DUSE_CLP", "-DUSE_BOP", "-DUSE_GLOP"]
            self.cpp_info.cxxflags.append("/DNOMINMAX")
            common_libs = ["CbcSolver", "Cbc",
                           "OsiCbc", "Cgl", "ortools"]

            if self.options.BUILD_absl:
                common_libs.extend([
                    "absl_bad_any_cast_impl", "absl_bad_optional_access", "absl_bad_variant_access", "absl_base", "absl_city",
                    "absl_civil_time", "absl_cord", "absl_debugging_internal", "absl_demangle_internal",
                    "absl_examine_stack", "absl_exponential_biased", "absl_failure_signal_handler", "absl_flags", "absl_flags_config",
                    "absl_flags_internal", "absl_flags_marshalling", "absl_flags_parse", "absl_flags_program_name",
                    "absl_flags_usage", "absl_flags_usage_internal", "absl_graphcycles_internal", "absl_hash", "absl_hashtablez_sampler",
                    "absl_int128", "absl_leak_check", "absl_leak_check_disable", "absl_log_severity", "absl_malloc_internal",
                    "absl_random_distributions", "absl_random_internal_distribution_test_util", "absl_random_internal_pool_urbg",
                    "absl_random_internal_randen", "absl_random_internal_randen_hwaes", "absl_random_internal_randen_hwaes_impl",
                    "absl_random_internal_randen_slow", "absl_random_internal_seed_material", "absl_random_seed_gen_exception",
                    "absl_random_seed_sequences", "absl_raw_hash_set", "absl_raw_logging_internal", "absl_scoped_set_env",
                    "absl_spinlock_wait", "absl_stacktrace", "absl_status", "absl_str_format_internal", "absl_strings",
                    "absl_strings_internal", "absl_symbolize", "absl_synchronization", "absl_throw_delegate", "absl_time", "absl_time_zone"
                ])
            if self.options.BUILD_CoinUtils:
                common_libs.append("CoinUtils")

            if self.options.BUILD_Osi:
                common_libs.append("Osi")
                common_libs.append("OsiClp")

            if self.options.BUILD_Clp:
                common_libs.append("ClpSolver")
                common_libs.append("Clp")

            if self.options.BUILD_SCIP:
                common_libs.append("libscip")

            common_libs.append("shlwapi")
            common_libs.append("psapi")
            common_libs.append("ws2_32")

            self.cpp_info.release.libs = common_libs.copy()
            self.cpp_info.release.libs.extend([
                "libprotobuf", "libprotobuf-lite", "libprotoc"
            ])
            self.cpp_info.debug.libs = common_libs.copy()
            self.cpp_info.debug.libs.extend([
                "libprotobufd", "libprotobuf-lited", "libprotocd"
            ])

            if self.options.BUILD_gflags:
                self.cpp_info.release.libs.append("gflags_nothreads_static")
                self.cpp_info.debug.libs.append(
                    "gflags_nothreads_static_debug")

            if self.options.BUILD_glog:
                self.cpp_info.release.libs.append("glog")
                self.cpp_info.debug.libs.append("glogd")

            if self.options.BUILD_ZLIB:
                self.cpp_info.release.libs.append("zlib")
                self.cpp_info.debug.libs.append("zlibd")

            self.cpp_info.libs = self.cpp_info.debug.libs if self.settings.build_type == "Debug" else self.cpp_info.release.libs
        else:  # assume Linux or compatible
            self.cpp_info.cxxflags = ["-DUSE_CBC",
                                      "-DUSE_CLP", "-DUSE_BOP", "-DUSE_GLOP"]
            self.cpp_info.libs = ["CbcSolver", "Cbc", "OsiCbc", "Cgl", "ClpSolver", "Clp", "OsiClp", "Osi", "CoinUtils", "absl_bad_any_cast_impl", "absl_bad_optional_access", "absl_bad_variant_access", "absl_base", "absl_city", "absl_civil_time", "absl_debugging_internal", "absl_demangle_internal", "absl_examine_stack", "absl_failure_signal_handler",
                                  "absl_graphcycles_internal", "absl_hash", "absl_hashtablez_sampler", "absl_int128", "absl_leak_check", "absl_malloc_internal", "absl_raw_hash_set", "absl_spinlock_wait", "absl_stacktrace", "absl_str_format_internal", "absl_strings", "absl_strings_internal", "absl_symbolize", "absl_synchronization", "absl_throw_delegate", "absl_time", "absl_time_zone", "protobuf", "glog", "gflags", "ortools"]
