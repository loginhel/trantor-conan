from conans import ConanFile, CMake, tools
import os


class TrantorConan(ConanFile):
    name = "trantor"
    version = "1.0.0"
    license = "unknown"
    author = "An Tao antao2002@gmail.com"
    url = "https://github.com/an-tao/trantor"
    description = "A non-blocking I/O based TCP network library, using C++14/17."
    topics = ("conan", "trantor", "TCP-lib", "cross-platform")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "build_testing": [True, False]
    }
    default_options = {
        "shared": False,
        "build_testing": False
    }
    generators = "cmake"

    _cmake = None


    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        minimal_cpp_standard = "14"
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, minimal_cpp_standard)
    
    def configure(self):
        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           tools.Version(self.settings.compiler.version) < "17":
           raise ConanInvalidConfiguration("drogon requires Visual Studio 17 or later.")

    def source(self):
        self.run("git clone https://github.com/an-tao/trantor.git")


    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)

        self._cmake.definitions["FAIL_ON_WARNINGS"] = False
        self._cmake.definitions["BUILD_TESTING"] = self.options.build_testing
        self._cmake.definitions["BUILD_TRANTOR_SHARED"] = self.options.shared

        #self._cmake.configure(build_folder=self._build_subfolder)
        self._cmake.configure(source_folder="trantor")
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def requirements(self):
        self.requires("openssl/1.1.1c")
        self.requires("c-ares/1.14.0")
        if self.options.build_testing:
            self.requires("gtest/1.10.0")

    def package(self):
        self.copy("LICENSE", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        #self.cpp_info.libs.append("trantor")
        self.cpp_info.libs.sort(reverse=True)

        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread"]
        if self.settings.os == "Windows":
            self.cpp_info.system_libs.append("ws2_32")
            self.cpp_info.system_libs.append("Rpcrt4")
        
