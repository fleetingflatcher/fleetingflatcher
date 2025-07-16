param (
    [string]$RootDir = "$PWD",              # Root folder to search
    [string]$Author = $(git config user.name), # Defaults to current git user
    [string]$Since = "2024-04-01",          # Start date (inclusive)
    [string]$Until = "2024-08-01"           # End date (inclusive)
)

# Find all git repos (folders with a .git directory)
$possibleRepos = Get-ChildItem -Path $RootDir -Recurse -Directory
$gitRepos =  $possibleRepos | Where-Object { Test-Path "$($_.FullName)\.git" }

Write-Host "Found directories: $possibleRepos"
Write-Host "Found repositories: $gitRepos"

foreach ($repo in $gitRepos) {
    Write-Host "`n`n===== $($repo.FullName) =====" -ForegroundColor Cyan
    Push-Location $repo.FullName

    $commits = git log --oneline --author="$Author" --since="$Since" --until="$Until"

    if ($commits) {
        $commits
    } else {
        Write-Host "No commits in this range." -ForegroundColor DarkGray
    }

    Pop-Location
}
