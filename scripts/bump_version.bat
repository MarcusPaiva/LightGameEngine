@echo off
rem Bump LightGameEngine's patch version (X.Y.Z -> X.Y.(Z+1)) in
rem pyproject.toml, then commit and tag that change.
rem
rem Usage:
rem   scripts\bump_version.bat            bump, commit, and tag
rem   scripts\bump_version.bat --force    bump even with other uncommitted changes in the tree
rem
rem Only the new version number is printed on stdout (the last line);
rem everything else goes to stderr. This lets other scripts capture the
rem version cleanly.
rem
rem This does NOT push the commit or the tag - review them, then push
rem yourself (git push && git push --tags) when you're ready.

setlocal enabledelayedexpansion

cd /d "%~dp0.."

set "FORCE=0"
if "%~1"=="" goto args_done
if /i "%~1"=="--force" (set "FORCE=1") else (
    echo Unknown option: %~1 1>&2
    echo Usage: %~nx0 [--force] 1>&2
    exit /b 1
)
:args_done

if "%FORCE%"=="0" (
    for /f "delims=" %%s in ('git status --porcelain') do (
        echo Working tree has uncommitted changes - refusing to bump the version. 1>&2
        echo Commit or stash your changes first, or re-run with --force. 1>&2
        exit /b 1
    )
)

set "RAWVERSION="
for /f "usebackq tokens=2 delims==" %%v in (`findstr /b "version" pyproject.toml`) do (
    set "RAWVERSION=%%v"
)
if "%RAWVERSION%"=="" (
    echo Could not read the version from pyproject.toml. 1>&2
    exit /b 1
)
set "CURRENT_VERSION=%RAWVERSION:"=%"
set "CURRENT_VERSION=%CURRENT_VERSION: =%"

for /f "tokens=1,2,3 delims=." %%a in ("%CURRENT_VERSION%") do (
    set "MAJOR=%%a"
    set "MINOR=%%b"
    set "PATCH=%%c"
)
if "%MAJOR%%MINOR%%PATCH%"=="" (
    echo Could not parse version "%CURRENT_VERSION%" as MAJOR.MINOR.PATCH. 1>&2
    exit /b 1
)

set /a NEWPATCH=%PATCH%+1
set "NEW_VERSION=%MAJOR%.%MINOR%.%NEWPATCH%"

powershell -NoProfile -Command "(Get-Content 'pyproject.toml') -replace 'version\s*=\s*\"%CURRENT_VERSION%\"', 'version = \"%NEW_VERSION%\"' | Set-Content 'pyproject.toml'"
if errorlevel 1 (
    echo Failed to write the new version into pyproject.toml. 1>&2
    exit /b 1
)

git add pyproject.toml
if errorlevel 1 exit /b 1
rem [skip ci] stops this commit from re-triggering the deploy workflow -
rem both when pushed by CI itself and when pushed manually after a
rem local deploy (see .github\workflows\deploy-pypi.yml).
git commit --quiet -m "chore: bump version to %NEW_VERSION% [skip ci]"
if errorlevel 1 exit /b 1
git tag "v%NEW_VERSION%"
if errorlevel 1 exit /b 1

echo Bumped version: %CURRENT_VERSION% -^> %NEW_VERSION% 1>&2
echo %NEW_VERSION%

endlocal
