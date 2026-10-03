import sys

from puild import Command, set_default_indent

from build import _frontend_build

set_default_indent("              ")

TEST_SUITES: dict[str, dict[str, object]] = {
    "unit": {
        "description": "Fast unit tests for models and business logic (pytest)",
        "command": [
            "uv",
            "run",
            "pytest",
            "--junitxml=build/test-results/junit-unit.xml",
            "tests/unit",
        ],
        "requires_frontend": False,
    },
    "smoke": {
        "description": "Smoke tests for critical API paths (robotcode)",
        "command": ["uv", "run", "robotcode", "robot", "-d", "build/test-results", "tests/smoke"],
        "requires_frontend": False,
    },
    "regression": {
        "description": "Regression tests covering edge cases and validation (robotcode)",
        "command": ["uv", "run", "robotcode", "robot", "-d", "build/test-results", "tests/regression"],
        "requires_frontend": False,
    },
    "e2e": {
        "description": "All end-to-end tests including workflows and browser UI (robotcode)",
        "command": ["uv", "run", "robotcode", "robot", "-d", "build/test-results", "tests/e2e"],
        "requires_frontend": True,
    },
    "ui": {
        "description": "Playwright browser UI automation tests (robotcode)",
        "command": ["uv", "run", "robotcode", "robot", "-d", "build/test-results", "tests/e2e/ui_tests.robot"],
        "requires_frontend": True,
    },
    "workflows": {
        "description": "End-to-end API workflows and schedule planning (robotcode)",
        "command": ["uv", "run", "robotcode", "robot", "-d", "build/test-results", "tests/e2e/e2e_workflows.robot"],
        "requires_frontend": False,
    },
}

ROBOT_SUITE_PATHS: dict[str, list[str]] = {
    "smoke": ["tests/smoke/smoke_tests.robot"],
    "regression": ["tests/regression/regression_tests.robot"],
    "e2e": ["tests/e2e/e2e_workflows.robot", "tests/e2e/ui_tests.robot"],
    "ui": ["tests/e2e/ui_tests.robot"],
    "workflows": ["tests/e2e/e2e_workflows.robot"],
}

ALL_SUITES = ["unit", "smoke", "regression", "e2e"]


def print_available_tests() -> None:
    print("Usage: uv run test <test_name> [test_name2 ...] or uv run test all\n")
    print("Available tests:")
    print("  all         - Run all test suites (unit, smoke, regression, e2e)")
    for name, info in TEST_SUITES.items():
        desc = info["description"]
        print(f"  {name:<11} - {desc}")


def run_tests(names: list[str]) -> None:
    from pathlib import Path

    if any(name == "all" for name in names):
        selected = ALL_SUITES
    else:
        invalid = [name for name in names if name not in TEST_SUITES]
        if invalid:
            print(f"Error: Unknown test(s): {', '.join(invalid)}\n")
            print_available_tests()
            sys.exit(1)
        selected = list(dict.fromkeys(names))

    Path("build/test-results").mkdir(parents=True, exist_ok=True)

    # 1. Run unit tests if selected
    if "unit" in selected:
        print("\n=== Running UNIT Tests (pytest) ===")
        unit_cmd = [
            "uv",
            "run",
            "pytest",
            "--junitxml=build/test-results/junit-unit.xml",
            "tests/unit",
        ]
        res = Command(*unit_cmd).run(capture=False)
        res.exit_for_error()

    # 2. Collect Robot test files
    robot_files: list[str] = []
    needs_frontend = False
    for name in selected:
        if name in ROBOT_SUITE_PATHS:
            for file_path in ROBOT_SUITE_PATHS[name]:
                if file_path not in robot_files:
                    robot_files.append(file_path)
            if name in ("e2e", "ui") or "all" in names:
                needs_frontend = True

    if robot_files:
        if needs_frontend:
            _frontend_build()

        suite_label = ", ".join(s for s in selected if s != "unit")
        print(f"\n=== Running Robot Framework Tests ({suite_label}) ===")
        robot_cmd = [
            "uv",
            "run",
            "robotcode",
            "robot",
            "-d",
            "build/test-results",
            "--name",
            "Todo Application Tests",
            *robot_files,
        ]
        res = Command(*robot_cmd).run(capture=False)
        res.exit_for_error()


def main() -> None:
    args = [arg.strip().lower() for arg in sys.argv[1:] if arg.strip()]
    if not args:
        print_available_tests()
        sys.exit(1)

    run_tests(args)


if __name__ == "__main__":
    main()
