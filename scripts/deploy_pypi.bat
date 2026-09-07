@echo off
rem Build and publish LightGameEngine to PyPI (or TestPyPI).
rem
rem Usage:
rem   scripts\deploy_pypi.bat                bump patch version, run tests, build, confirm, upload to PyPI
rem   scripts\deploy_pypi.bat --test         upload to https://test.pypi.org instead
rem   scripts\deploy_pypi.bat --skip-tests   skip running the test suite first
rem   scripts\deploy_pypi.bat --no-bump      deploy the version already in pyproject.toml, unchanged
rem   scripts\deploy_pypi.bat --yes          don't ask for confirmation before uploading
rem
rem You can combine flags, e.g.: scripts\deploy_pypi.bat --test --yes
rem
rem Every run bumps the patch version (via bump_version.bat) and
rem commits + tags that change locally, unless --no-bump is given.
rem That commit and tag are not pushed automatically - push them
rem yourself once you're happy with the release (git push && git push
rem --tags).
rem
rem Credentials:
rem   twine reads them from %USERPROFILE%\.pypirc, or from the
rem   TWINE_USERNAME / TWINE_PASSWORD environment variables. PyPI wants
rem   an API token, not a normal password:
rem       set TWINE_USERNAME=__token__
rem       set TWINE_PASSWORD=pypi-xxxxxxxx...
rem   Use a token starting with "pypi-" for PyPI, or the token from
rem   https://test.pypi.org/manage/account/ for TestPyPI (--test).
rem   If neither %USERPROFILE%\.pypirc nor the env vars are set, twine
rem   will ask for them interactively when it uploads.

setlocal enabledelayedexpansion

cd /d "%~dp0.."

set "REPOSITORY=pypi"
set "SKIP_TESTS=0"
set "ASSUME_YES=0"
set "SKIP_BUMP=0"

:parse_args
if "%~1"=="" goto args_done
if /i "%~1"=="--test" (set "REPOSITORY=testpypi" & shift & goto parse_args)
if /i "%~1"=="--skip-tests" (set "SKIP_TESTS=1" & shift & goto parse_args)
if /i "%~1"=="--no-bump" (set "SKIP_BUMP=1" & shift & goto parse_args)
if /i "%~1"=="--yes" (set "ASSUME_YES=1" & shift & goto parse_args)
if /i "%~1"=="-y" (set "ASSUME_YES=1" & shift & goto parse_args)
echo Unknown option: %~1
echo Usage: %~nx0 [--test] [--skip-tests] [--no-bump] [--yes]
exit /b 1

:args_done

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else (
    set "PYTHON=python"
)

echo ==^> Using Python:
"%PYTHON%" --version || exit /b 1

if "%SKIP_BUMP%"=="0" (
    echo ==^> Bumping the package version...
    set "BUMP_OUTPUT=%TEMP%\lge_bump_output_%RANDOM%.tmp"
    call "%~dp0bump_version.bat" > "!BUMP_OUTPUT!"
    if errorlevel 1 (
        type "!BUMP_OUTPUT!"
        del "!BUMP_OUTPUT!" 2>nul
        exit /b 1
    )
    set /p VERSION=<"!BUMP_OUTPUT!"
    del "!BUMP_OUTPUT!" 2>nul
) else (
    echo ==^> Skipping version bump ^(--no-bump given^).
    set "RAWVERSION="
    for /f "usebackq tokens=2 delims==" %%v in (`findstr /b "version" pyproject.toml`) do (
        set "RAWVERSION=%%v"
    )
    if "!RAWVERSION!"=="" (
        echo Could not read the version from pyproject.toml.
        exit /b 1
    )
    set "VERSION=!RAWVERSION:"=!"
    set "VERSION=!VERSION: =!"
)

echo ==^> Package version: %VERSION%
echo ==^> Target repository: %REPOSITORY%

echo ==^> Making sure build and twine are installed...
"%PYTHON%" -m pip install --quiet --upgrade build twine
if errorlevel 1 exit /b 1

if "%SKIP_TESTS%"=="0" (
    echo ==^> Running the test suite...
    "%PYTHON%" -m pytest -q
    if errorlevel 1 exit /b 1
) else (
    echo ==^> Skipping tests ^(--skip-tests given^).
)

echo ==^> Cleaning old build artifacts...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
for /d %%d in (*.egg-info) do rmdir /s /q "%%d"

echo ==^> Building the sdist and wheel...
"%PYTHON%" -m build
if errorlevel 1 exit /b 1

echo ==^> Checking the built distribution...
"%PYTHON%" -m twine check dist\*
if errorlevel 1 exit /b 1

if "%ASSUME_YES%"=="0" (
    set /p CONFIRM="Upload LightGameEngine %VERSION% to %REPOSITORY%? [y/N] "
    if /i not "!CONFIRM!"=="y" if /i not "!CONFIRM!"=="yes" (
        echo Aborted.
        exit /b 1
    )
)

if "%REPOSITORY%"=="testpypi" (
    "%PYTHON%" -m twine upload --repository testpypi dist\*
) else (
    "%PYTHON%" -m twine upload dist\*
)
if errorlevel 1 exit /b 1

echo ==^> Done. Published version %VERSION% to %REPOSITORY%.

endlocal
