from pathlib import Path

import pytest
from setuptools.dist import Distribution

import setup


def make_fake_p4a_build(tmp_path):
    build_dir = tmp_path / "build"
    include_dir = (
        build_dir
        / "python-installs"
        / "demo"
        / "arm64-v8a"
        / "include"
        / "python3.14"
    )
    javaclasses_dir = build_dir / "javaclasses"
    include_dir.mkdir(parents=True)
    javaclasses_dir.mkdir()

    return build_dir, include_dir


@pytest.mark.parametrize(
    ("cppflags", "expected"),
    [
        (
            "-I/media/able/examples/alert/.buildozer/android/platform/"
            "build-arm64-v8a_armeabi-v7a/build/python-installs/alert_mi/",
            "/media/able/examples/alert/.buildozer/android/platform/"
            "build-arm64-v8a_armeabi-v7a/build/javaclasses/alert_mi",
        ),
        (
            "-DANDROID -I/home/user/.buildozer/android/platform/android-ndk-r25b/"
            "toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include "
            "-I/media/able/examples/alert/.buildozer/android/platform/"
            "build-arm64-v8a_armeabi-v7a/build/python-installs/alert_mi/"
            "arm64-v8a/include/python3.14",
            "/media/able/examples/alert/.buildozer/android/platform/"
            "build-arm64-v8a_armeabi-v7a/build/javaclasses/alert_mi",
        ),
    ],
)
def test_javaclass_dir_found(monkeypatch, cppflags, expected):
    monkeypatch.setenv("CPPFLAGS", cppflags)
    monkeypatch.setattr(
        "pathlib.Path.exists",
        lambda path: path.name == "javaclasses",
    )
    monkeypatch.setattr("pathlib.Path.mkdir", lambda *args, **kwargs: None)

    assert setup.P4APathParser().javaclass_dir == Path(expected)


def test_p4a_path_parser_handles_other_builds_python_layout(tmp_path, monkeypatch):
    build_dir = tmp_path / "build-arm64-v8a_armeabi-v7a_x86_64" / "build"
    include_dir = (
        build_dir
        / "other_builds"
        / "python3"
        / "armeabi-v7a__ndk_target_22"
        / "python3"
        / "android-build"
        / "android-root"
        / "include"
        / "python3.14"
    )
    libs_arch_dir = build_dir / "libs_collections" / "demo" / "armeabi-v7a"
    javaclasses_dir = build_dir / "javaclasses"
    include_dir.mkdir(parents=True)
    libs_arch_dir.mkdir(parents=True)
    javaclasses_dir.mkdir()

    monkeypatch.setenv("CPPFLAGS", f"-DANDROID -I{include_dir}")
    monkeypatch.setenv("LDFLAGS", f"-lm -L{libs_arch_dir}")

    paths = setup.P4APathParser()

    assert paths.build_dir == build_dir
    assert paths.javaclass_dir == build_dir / "javaclasses" / "demo"


def test_install_able_java_classes_copies_sources(tmp_path, monkeypatch):
    build_dir, include_dir = make_fake_p4a_build(tmp_path)
    monkeypatch.setenv("CPPFLAGS", f"-I{include_dir}")

    setup.install_able_java_classes()

    copied = sorted(
        path.name for path in (build_dir / "javaclasses" / "demo").glob("*.java")
    )

    assert copied == [
        "BLE.java",
        "BLEAdvertiser.java",
        "PythonBluetooth.java",
        "PythonBluetoothAdvertiser.java",
    ]


def test_android_build_detection(monkeypatch):
    monkeypatch.delenv("ANDROIDAPI", raising=False)
    assert not setup.is_android_build()

    monkeypatch.setenv("ANDROIDAPI", "35")
    assert setup.is_android_build()


def test_direct_install_outside_android_is_blocked(monkeypatch):
    monkeypatch.delenv("ANDROIDAPI", raising=False)
    monkeypatch.setattr(
        setup.install,
        "run",
        lambda command: pytest.fail("unexpected base install"),
    )

    command = setup.InstallAble(Distribution())

    with pytest.raises(RuntimeError, match="buildozer.spec requirements"):
        command.run()


def test_bdist_wheel_runs_android_hook(monkeypatch):
    calls = []

    def fake_hook(stage):
        calls.append(stage)

    def fake_bdist_wheel_run(command):
        calls.append("base bdist_wheel")

    monkeypatch.setattr(setup, "maybe_install_able_java_classes", fake_hook)
    monkeypatch.setattr(setup.bdist_wheel, "run", fake_bdist_wheel_run)

    command = setup.BDistWheelAble(Distribution())
    command.run()

    assert calls == ["bdist_wheel.run", "base bdist_wheel"]


def test_maybe_install_able_java_classes_is_quiet_outside_android(monkeypatch, capsys):
    monkeypatch.delenv("ANDROIDAPI", raising=False)
    monkeypatch.setattr(
        setup,
        "install_able_java_classes",
        lambda: pytest.fail("unexpected Android Java install"),
    )

    setup.maybe_install_able_java_classes("test")

    assert capsys.readouterr().out == ""


def test_debug_p4a_context_prints_android_environment(monkeypatch, capsys):
    monkeypatch.setenv("ANDROIDAPI", "35")
    monkeypatch.setenv("P4A_ARCH", "arm64-v8a")

    setup.debug_p4a_context("test")

    output = capsys.readouterr().out

    assert "[able] ===== test =====" in output
    assert "[able] ANDROIDAPI=35" in output
    assert "[able] P4A_ARCH=arm64-v8a" in output
    assert "[able] ===== end test =====" in output


def test_debug_p4a_context_is_quiet_outside_android(monkeypatch, capsys):
    monkeypatch.delenv("ANDROIDAPI", raising=False)

    setup.debug_p4a_context("test")

    assert capsys.readouterr().out == ""
