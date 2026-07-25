"""Compile, test, and provide instant CS 210 Project One rubric feedback."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
GPP = shutil.which("g++")


def run(command: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=ROOT, input=input_text, text=True, capture_output=True
    )


def result(label: str, passed: bool, detail: str) -> bool:
    print(f"[{'PASS' if passed else 'NEEDS WORK'}] {label}: {detail}")
    return passed


def main() -> int:
    BUILD.mkdir(exist_ok=True)
    if not GPP:
        result("Compiler", False, "g++ was not found on PATH")
        return 1

    include = str(ROOT / "include")
    warnings = ["-std=c++17", "-Wall", "-Wextra", "-Wpedantic", "-Werror", f"-I{include}"]
    app = BUILD / "chada_clocks.exe"
    tests = BUILD / "clock_tests.exe"

    compile_app = run([GPP, *warnings, "src/main.cpp", "src/Clock.cpp", "-o", str(app)])
    if not result("Compiles cleanly", compile_app.returncode == 0,
                  compile_app.stderr.strip() or "no warnings or errors"):
        return 1

    compile_tests = run([GPP, *warnings, "tests/clock_tests.cpp", "src/Clock.cpp", "-o", str(tests)])
    if not result("Test suite builds", compile_tests.returncode == 0,
                  compile_tests.stderr.strip() or "test executable created"):
        return 1

    test_run = run([str(tests)])
    tests_ok = result("Responds to user input", test_run.returncode == 0,
                      (test_run.stdout + test_run.stderr).strip())

    demo = run([str(app)], input_text="23 59 59\n3\n2\n1\n4\n")
    display_ok = all(token in demo.stdout for token in
                     ("12-Hour Clock", "24-Hour Clock", "A M", "00:00:00"))
    result("Clock displays (15/15)", display_ok,
           "12-hour and 24-hour clocks render side by side")
    menu_ok = all(text in demo.stdout for text in
                  ("Add One Hour", "Add One Minute", "Add One Second", "Exit Program"))
    result("Menu functionality (20/20)", menu_ok, "all four required choices are present")

    main_source = (ROOT / "src" / "main.cpp").read_text(encoding="utf-8")
    implementation = (ROOT / "src" / "Clock.cpp").read_text(encoding="utf-8")
    main_body = re.search(r"int\s+main\s*\([^)]*\)\s*\{(.*?)\}", main_source, re.S)
    modular_ok = bool(main_body and "getInitialTime" in main_body.group(1)
                      and "runClockProgram" in main_body.group(1))
    result("Code modularization (20/20)", modular_ok,
           "main delegates the application workflow to functions")
    flow_ok = all(token in implementation for token in
                  ("getInitialTime", "displayClocks", "printMenu", "getMenuChoice", "switch", "while"))
    result("Flowchart sequence (10/10)", flow_ok,
           "display, menu, input, update, and exit loop are represented")
    style_ok = "Author:" in main_source and "//" in implementation and len(re.findall(r"[a-z][A-Z]", implementation)) > 10
    result("Best practices (up to 15/15)", style_ok,
           "file header, comments, descriptive camelCase names, and strict warnings")

    passed = all((tests_ok, display_ok, menu_ok, modular_ok, flow_ok, style_ok))
    print("\nEstimated rubric readiness: " + ("100/100 requirements covered" if passed else "review NEEDS WORK items"))
    print(f"Executable: {app}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
