# wiki_preview.ps1 — Build and serve the Star Atlas Lore Wiki locally
# Usage: .\tools\wiki_preview.ps1 [-Port 8001] [-Watch]
param(
    [int]$Port = 8001,
    [switch]$Watch
)

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent

Write-Host "`n=== Star Atlas Lore Wiki — Local Preview ===" -ForegroundColor Cyan
Write-Host "Root: $root" -ForegroundColor DarkGray

# Step 1: Sync canon → docs
Write-Host "`n[1/3] Syncing canon -> docs..." -ForegroundColor Yellow
$synced = 0
@("factions", "species") | ForEach-Object {
    $category = $_
    Get-ChildItem -Path "$root\canon\$category\*.md" -ErrorAction SilentlyContinue | ForEach-Object {
        [System.IO.File]::Copy($_.FullName, "$root\docs\$category\$($_.Name)", $true)
        $synced++
    }
}
Get-ChildItem -Path "$root\canon\geography\sectors\*.md" -ErrorAction SilentlyContinue | ForEach-Object {
    [System.IO.File]::Copy($_.FullName, "$root\docs\geography\sectors\$($_.Name)", $true)
    $synced++
}
Write-Host "  Synced $synced files" -ForegroundColor Green

# Step 2: Build
Write-Host "`n[2/3] Building site..." -ForegroundColor Yellow
Push-Location $root
Remove-Item -Path "site" -Recurse -Force -ErrorAction SilentlyContinue
mkdocs build --clean 2>&1 | ForEach-Object {
    if ($_ -match "Documentation built") { Write-Host "  $_" -ForegroundColor Green }
}
Pop-Location

# Step 3: Serve
Write-Host "`n[3/3] Serving on http://127.0.0.1:$Port/star-atlas-lore/" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor DarkGray

# Serve with proper base path handling
python -c @"
import http.server, socketserver, os, sys
os.chdir(r'$root\site')

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Only log actual page requests, not assets
        if not any(ext in str(args[0]) for ext in ['.js', '.css', '.png', '.svg', '.woff']):
            super().log_message(format, *args)

try:
    with socketserver.TCPServer(('127.0.0.1', $Port), Handler) as httpd:
        print(f'Wiki live at http://127.0.0.1:$Port/')
        print(f'Open: http://127.0.0.1:$Port/star-atlas-lore/')
        httpd.serve_forever()
except KeyboardInterrupt:
    print('\nStopped.')
except OSError as e:
    print(f'Port $Port in use. Try: .\\tools\\wiki_preview.ps1 -Port 8002')
    sys.exit(1)
"@
