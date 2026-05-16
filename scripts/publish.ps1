# Publish local commits to GitHub (main + master for GitHub Pages).
param(
    [Parameter(Mandatory = $true)]
    [string]$Message
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

git add -A
$status = git status --porcelain
if (-not $status) {
    Write-Host "Nothing to commit."
    exit 0
}

git commit -m $Message
git push origin main
git push origin main:master
Write-Host "Pushed to origin/main and origin/master."
