$ErrorActionPreference = 'Stop'
$python = 'C:\Users\garza\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'

if (-not (Test-Path -LiteralPath $python)) {
    $python = (Get-Command python -ErrorAction Stop).Source
}

& $python "$PSScriptRoot\tools\rubric_check.py"
exit $LASTEXITCODE
