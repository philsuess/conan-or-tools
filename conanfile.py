import os
from conans import ConanFile, CMake, tools
from shutil import copyfile


class GORTConan(ConanFile):
    name = "ortools"
    version = "8.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_find_package"

    def source(self):
        if self.settings.os == "Windows":
            self.run("git clone https://github.com/google/or-tools")
            self.run("cd or-tools && git checkout tags/v%s -b v%s" %
                     (self.version, self.version))
        else:
            # from https://developers.google.com/optimization/install/cpp/linux
            url = "https://github.com/google/or-tools/releases/download/v%s/" % self.version
            zip_file_name = "or-tools_Ubuntu-20.04_v8.0.8283.tar.gz"
            tools.get(url + zip_file_name)
            os.rename("or-tools_Ubuntu-20.04-64bit_v8.0.8283", "or-tools")

    def build(self):
        if self.settings.os == "Windows":
            cmake = CMake(self)
            cmake.definitions['CMAKE_INSTALL_PREFIX'] = self.package_folder
            cmake.definitions['BUILD_DEPS'] = "ON"

            cmake.definitions['USE_SCIP'] = "OFF"
            cmake.definitions['BUILD_SCIP'] = "OFF"
            cmake.definitions['USE_COINOR'] = "ON"
            cmake.definitions['BUILD_CoinUtils'] = "ON"
            cmake.definitions['BUILD_Osi'] = "ON"
            cmake.definitions['BUILD_Clp'] = "ON"
            cmake.definitions['BUILD_Cgl'] = "ON"
            cmake.definitions['BUILD_Cbc'] = "ON"
            cmake.definitions['BUILD_SAMPLES'] = "OFF"
            cmake.definitions['BUILD_EXAMPLES'] = "OFF"
            cmake_source_folder = self.source_folder + "/or-tools"
            cmake_build_folder = self.source_folder + "/or-tools"
            cmake.configure(source_dir=cmake_source_folder,
                            build_dir=cmake_build_folder)
            cmake.build(target='install')
        else:  # assume Linux or compatible
            pass

    def package(self):
        if self.settings.os == "Windows":
            pass
        else:  # assume Linux or compatible
            self.copy("LICENSE*", src="or-tools/", dst=".")
            self.copy("*", src="or-tools/include", dst="include")
            self.copy("*", src="or-tools/lib", dst="lib")

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.cxxflags = ["-DUSE_CBC",
                                      "-DUSE_CLP", "-DUSE_BOP", "-DUSE_GLOP"]
            self.cpp_info.cxxflags.append("/DNOMINMAX")
            common_libs = ["CbcSolver", "Cbc", "OsiCbc", "Cgl", "ClpSolver", "Clp", "OsiClp", "Osi", "CoinUtils",
                           # "libscip",
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
                           "absl_strings_internal", "absl_symbolize", "absl_synchronization", "absl_throw_delegate", "absl_time", "absl_time_zone",
                           "ortools"]
            common_libs.append("shlwapi")
            common_libs.append("psapi")
            common_libs.append("ws2_32")

            self.cpp_info.release.libs = common_libs.copy()
            self.cpp_info.release.libs.extend([
                "libprotobuf", "libprotobuf-lite", "libprotoc", "glog", "gflags_nothreads_static", "zlib"
            ])

            self.cpp_info.debug.libs = common_libs.copy()
            self.cpp_info.debug.libs.extend([
                "libprotobufd", "libprotobuf-lited", "libprotocd", "glogd", "gflags_nothreads_static_debug", "zlibd"
            ])
            self.cpp_info.libs = self.cpp_info.debug.libs if self.settings.build_type == "Debug" else self.cpp_info.release.libs
        else:  # assume Linux or compatible
            self.cpp_info.cxxflags = ["-DUSE_CBC",
                                      "-DUSE_CLP", "-DUSE_BOP", "-DUSE_GLOP"]
            self.cpp_info.libs = ["CbcSolver", "Cbc", "OsiCbc", "Cgl", "ClpSolver", "Clp", "OsiClp", "Osi", "CoinUtils", "absl_bad_any_cast_impl", "absl_bad_optional_access", "absl_bad_variant_access", "absl_base", "absl_city", "absl_civil_time", "absl_debugging_internal", "absl_demangle_internal", "absl_examine_stack", "absl_failure_signal_handler",
                                  "absl_graphcycles_internal", "absl_hash", "absl_hashtablez_sampler", "absl_int128", "absl_leak_check", "absl_malloc_internal", "absl_raw_hash_set", "absl_spinlock_wait", "absl_stacktrace", "absl_str_format_internal", "absl_strings", "absl_strings_internal", "absl_symbolize", "absl_synchronization", "absl_throw_delegate", "absl_time", "absl_time_zone", "protobuf", "glog", "gflags", "ortools"]
