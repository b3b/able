import os
import sys
from configparser import ConfigParser
from pathlib import Path


def requirement_name(requirement: str) -> str:
    for separator in ("==", ">=", "<=", "~=", "!=", ">", "<"):
        if separator in requirement:
            return requirement.split(separator, 1)[0].strip()

    return requirement.strip()


def read_requirements(spec_path: Path) -> list[str]:
    config = ConfigParser()
    config.optionxform = str

    with spec_path.open(encoding="utf-8") as spec_file:
        config.read_file(spec_file)

    return [
        requirement.strip()
        for requirement in config.get("app", "requirements").split(",")
        if requirement.strip()
    ]


def replace_requirement(
    requirements: list[str],
    package_name: str,
    replacement: str,
) -> list[str]:
    replaced = False
    result = []

    for requirement in requirements:
        if requirement_name(requirement) == package_name:
            result.append(replacement)
            replaced = True
        else:
            result.append(requirement)

    if not replaced:
        raise ValueError(f"Could not find {package_name!r} in requirements")

    return result


def write_github_output(name: str, value: str) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")

    if not github_output:
        print(f"{name}={value}")
        return

    with Path(github_output).open("a", encoding="utf-8") as output_file:
        output_file.write(f"{name}={value}\n")


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(
            "Usage: replace_buildozer_requirement.py BUILDOZER_SPEC PACKAGE_NAME REPLACEMENT"
        )

    spec_path = Path(sys.argv[1])
    package_name = sys.argv[2]
    replacement = sys.argv[3]

    requirements = replace_requirement(
        read_requirements(spec_path),
        package_name,
        replacement,
    )

    write_github_output("requirements", ",".join(requirements))


if __name__ == "__main__":
    main()
