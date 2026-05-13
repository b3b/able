from pathlib import Path

import pytest

from scripts.release.replace_buildozer_requirement import (
    read_requirements,
    replace_requirement,
    requirement_name,
)


def write_spec(path: Path, requirements: str) -> None:
    path.write_text(
        "\n".join(
            [
                "[app]",
                "title = Demo",
                "requirements =",
                requirements,
                "",
            ]
        ),
        encoding="utf-8",
    )


def test_read_requirements_from_multiline_buildozer_spec(tmp_path):
    spec = tmp_path / "buildozer.spec"
    write_spec(
        spec,
        "\n".join(
            [
                "             python3==3.14.2,",
                "             hostpython3==3.14.2,",
                "             kivy==2.3.1,",
                "             filetype,",
                "             able_recipe,",
            ]
        ),
    )

    assert read_requirements(spec) == [
        "python3==3.14.2",
        "hostpython3==3.14.2",
        "kivy==2.3.1",
        "filetype",
        "able_recipe",
    ]


def test_replace_named_requirement_preserves_other_requirements():
    requirements = [
        "python3==3.14.2",
        "hostpython3==3.14.2",
        "kivy==2.3.1",
        "filetype",
        "able_recipe",
    ]

    result = replace_requirement(
        requirements,
        "able_recipe",
        "https://github.com/b3b/able/archive/abc123.zip",
    )

    assert result == [
        "python3==3.14.2",
        "hostpython3==3.14.2",
        "kivy==2.3.1",
        "filetype",
        "https://github.com/b3b/able/archive/abc123.zip",
    ]


def test_replace_requirement_fails_when_able_recipe_is_missing():
    with pytest.raises(ValueError, match="Could not find 'able_recipe'"):
        replace_requirement(["python3", "kivy"], "able_recipe", "replacement")


def test_replace_requirement_can_target_other_packages():
    assert replace_requirement(
        ["python3", "kivy", "example-package"],
        "example-package",
        "https://example.test/archive.zip",
    ) == ["python3", "kivy", "https://example.test/archive.zip"]


def test_replace_requirement_matches_pinned_requirement_name():
    assert replace_requirement(
        ["python3==3.14.2", "hostpython3==3.14.2", "kivy==2.3.1"],
        "hostpython3",
        "hostpython3==1.2.3",
    ) == ["python3==3.14.2", "hostpython3==1.2.3", "kivy==2.3.1"]


@pytest.mark.parametrize(
    ("requirement", "name"),
    [
        ("hostpython3==3.14.2", "hostpython3"),
        ("kivy>=2.3", "kivy"),
        ("filetype", "filetype"),
    ],
)
def test_requirement_name(requirement, name):
    assert requirement_name(requirement) == name
