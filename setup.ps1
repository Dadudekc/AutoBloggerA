# Define the base directory for the project
$projectBase = "C:\Auto_Blogger"

# Create directories for the project structure
$directories = @(
    "$projectBase",
    "$projectBase\Scripts",
    "$projectBase\BlogPosts",
    "$projectBase\Logs",
    "$projectBase\Configs"
)

# Create the directories if they don't exist
foreach ($dir in $directories) {
    if (-not (Test-Path -Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir
        Write-Output "Created directory: $dir"
    } else {
        Write-Output "Directory already exists: $dir"
    }
}

# Output the project structure
Write-Output "Project structure created at ${projectBase}:"
Get-ChildItem -Path $projectBase -Recurse | Format-List
