# CS 210 Project One - Chada Tech Clocks

This self-contained C++17 project implements the required simultaneous 12-hour
and 24-hour clocks, four-option menu, rollover behavior, secure input recovery,
and flowchart-style application loop.

Open `ChadaTechClocks.sln` in Visual Studio 2022 to build and run the project.

## Instant feedback

From PowerShell, run:

```powershell
cd "C:\Users\garza\Videos\DNA-Synthesis Tokenizer Pipline photosynthisis\cs210_project_one"
.\check.ps1
```

The checker compiles with strict warnings, runs unit and interactive tests, and
maps the results to all six rubric criteria. The compiled program is written to
`build\chada_clocks.exe`.

## Run the clock

```powershell
.\build\chada_clocks.exe
```

## Submission preparation

1. Replace the author name in the file headers if needed.
2. Review the AI acknowledgement against the course AI-usage policy.
3. Run `check.ps1` and confirm every line reports `PASS`.
4. Zip `include`, `src`, and the project files your instructor expects. Build
   outputs and the local tests do not need to be submitted unless requested.

## Rubric coverage

- Flowchart: display clocks, print menu, get input, update, repeat, exit.
- Modularization: `main()` contains only the program delegation and return.
- Displays: correct padded 12-hour/24-hour formats shown side by side.
- Menu: add hour, minute, second, and exit options.
- Input: invalid input recovery plus correct midnight rollover.
- Best practices: file headers, focused comments, descriptive names, headers,
  const-correctness where applicable, and warning-free C++17 compilation.
