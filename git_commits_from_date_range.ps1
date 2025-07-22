param (
    [string]$RootDir = "$PWD",              # Root folder to search
    [string]$Author = $(git config user.name), # Defaults to current git user
    [string]$Since = "2023-03-01",          # Start date (inclusive)
    [string]$Until = "2025-08-01"           # End date (inclusive)
)

function RefreshIndex {
    Write-Host "Refreshing git repository index..."

    # Find all possible repositories.
    Write-Host "Storing all possible directories..."
    $possibleRepos = Get-ChildItem -Path $RootDir -Recurse -Directory

    # Find all git repos (folders with a .git directory)
    Write-Host "Filtering $($possibleRepos.Count) directories for those containing git repositories..."
    $gitRepos =  $possibleRepos | Where-Object { Test-Path "$($_.FullName)\.git" }

    Write-Host "Found $($gitRepos.Count) repositories:"
    foreach($repo in $gitRepos) {
        Write-Host "    $($repo.FullName)"
    }
    Write-Host "Saving refreshed index..."

    # Remove existing gitrepos index.
    if (Test-Path '.gitrepos') { Remove-Item '.gitrepos' }

    # Save new index.
    foreach($repo in $gitRepos)
    {
        Out-File -InputObject "$($repo.FullName)" -Append '.gitrepos'
    }
}


function PrintCommits {
    $gitRepos = Get-Content '.gitrepos'
    foreach ($repo in $gitRepos) {
	$repo_item = Get-Item $repo
        Write-Host "`n`n===== $($repo_item.FullName) =====" -ForegroundColor Cyan
        Push-Location $repo_item.FullName

        $commits = git log --format="%h %ad %s" --date=short --author="$Author" --since="$Since" --until="$Until"

        if ($commits) {
            $commits
        } else {
            Write-Host "No commits in this range." -ForegroundColor DarkGray
        }

        Pop-Location
    }
}

if (!(Test-Path '.gitrepos')) {
    $response = Read-Host "No repository index cache found. Create one? [Y/n] "

    switch ($response.ToLower()) {
        'n' { }
        default {
    	    RefreshIndex
        }
    }
} 
else {
    $response = Read-Host "Do you want to refresh the index? [y/N]"

    switch ($response.ToLower()) {
        'y' { RefreshIndex }
    }
}

Write-Host "Printing commits in date range: $Since -- $Until"
PrintCommits
    
Write-Host "Exiting..."
