import ast
import os
import re
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.install import install

try:
    from setuptools.command.bdist_wheel import bdist_wheel
except ModuleNotFoundError:
    from wheel.bdist_wheel import bdist_wheel


PACKAGE_ROOT = Path(__file__).parent
JAVA_SOURCE_DIR = PACKAGE_ROOT / "able" / "src" / "org" / "able"


def read_package_version():
    version_path = PACKAGE_ROOT / "able" / "version.py"
    tree = ast.parse(version_path.read_text())

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue

        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "__version__":
                return ast.literal_eval(node.value)

    raise RuntimeError(f"Cannot find __version__ in {version_path}")


def is_android_build():
    return "ANDROIDAPI" in os.environ


def debug_p4a_context(stage):
    if not is_android_build():
        return

    print(f"[able] ===== {stage} =====")

    for key in (
        "ANDROIDAPI",
        "ARCH",
        "P4A_ARCH",
        "CPPFLAGS",
        "LDFLAGS",
    ):
        value = os.environ.get(key)
        if value:
            print(f"[able] {key}={value}")

    print(f"[able] ===== end {stage} =====")


class P4APathParser:
    @property
    def cppflags(self):
        return os.environ.get("CPPFLAGS", "")

    @property
    def ldflags(self):
        return os.environ.get("LDFLAGS", "")

    @property
    def python_path(self):
        match = re.search(
            r"-I(/[^\s]+/build/python-installs/[^/\s]+/)",
            self.cppflags,
        )
        if match:
            return Path(match.group(1))

        match = re.search(
            r"-I(/[^\s]+/build/python-installs/[^/\s]+/[^/\s]+/"
            r"include/python[0-9.]+)",
            self.cppflags,
        )
        if match:
            return Path(match.group(1)).parents[2]

        match = re.search(
            r"-I(/[^\s]+/build/other_builds/python3/[^/\s]+/python3/"
            r"android-build/android-root/include/python[0-9.]+)",
            self.cppflags,
        )
        if match:
            return Path(match.group(1))

        raise RuntimeError(
            "Cannot find p4a Python path in CPPFLAGS: "
            f"{self.cppflags}"
        )

    @property
    def python_installs_dir(self):
        path = self.python_path

        while path.name != "python-installs":
            if path.parent == path:
                raise RuntimeError("Cannot find python-installs directory")
            path = path.parent

        return path

    @property
    def build_dir(self):
        path = self.python_path

        for parent in (path, *path.parents):
            if parent.name == "other_builds":
                return parent.parent

        return self.python_installs_dir.parent

    @property
    def javaclass_collection_dir(self):
        match = re.search(
            r"(?:^|\s)-L(/[^\s]+/build/libs_collections/[^/\s]+/[^/\s]+)",
            self.ldflags,
        )
        if match:
            dist_name = Path(match.group(1)).parent.name
            return self.build_dir / "javaclasses" / dist_name

        return self.build_dir / "javaclasses" / self.distribution_name

    @property
    def distribution_name(self):
        path = self.python_path

        while path.parent.name != "python-installs":
            if path.parent == path:
                raise RuntimeError(
                    "Cannot find distribution name. Set LDFLAGS with p4a "
                    "libs_collections path or include a python-installs path in "
                    "CPPFLAGS."
                )
            path = path.parent

        return path.name

    @property
    def javaclass_dir(self):
        base = self.build_dir / "javaclasses"
        if not base.exists():
            raise RuntimeError(
                "Java classes directory was not found. "
                "Please report this at https://github.com/b3b/able/issues"
            )

        target = self.javaclass_collection_dir
        target.mkdir(parents=True, exist_ok=True)
        return target


def install_able_java_classes():
    paths = P4APathParser()
    javaclass_dir = paths.javaclass_dir

    print(f"[able] p4a build dir: {paths.build_dir}")
    print(f"[able] p4a javaclass dir: {javaclass_dir}")

    java_files = sorted(JAVA_SOURCE_DIR.glob("*.java"))

    if not java_files:
        raise RuntimeError(f"No Able Java files found in {JAVA_SOURCE_DIR}")

    for src in java_files:
        dst = javaclass_dir / src.name
        shutil.copy(src, dst)
        print(f"[able] installed {src} -> {dst}")


def maybe_install_able_java_classes(stage):
    debug_p4a_context(stage)

    if is_android_build():
        install_able_java_classes()


class InstallAble(install):
    def run(self):
        if not is_android_build():
            raise RuntimeError(
                "able_recipe works only inside a Buildozer/python-for-android "
                "Android build. Add it to buildozer.spec requirements instead "
                "of installing it on desktop."
            )

        maybe_install_able_java_classes("install.run")

        super().run()


class BDistWheelAble(bdist_wheel):
    def run(self):
        maybe_install_able_java_classes("bdist_wheel.run")
        super().run()


def main():
    setup(
        name="able_recipe",
        version=read_package_version(),
        install_requires=[],
        cmdclass={
            "bdist_wheel": BDistWheelAble,
            "install": InstallAble,
        },
        options={
            "bdist_wheel": {
                # Keep p4a from reusing a cached wheel and skipping Java copy hooks.
                "plat_name": "unused-nocache",
            },
        },
    )


if __name__ == "__main__":
    main()
