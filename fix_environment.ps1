
Write-Host "Checking environment..." -ForegroundColor ConsoleColor.Cyan

# 1. Check if python is available
try {
    $py = Get-Command python -ErrorAction Stop
    Write-Host "Found Python: $($py.Source)" -ForegroundColor Green
} catch {
    try {
        $py = Get-Command py -ErrorAction Stop
        Write-Host "Found Python Launcher (py): $($py.Source)" -ForegroundColor Green
        $python_cmd = "py"
    } catch {
        Write-Host "ERROR: Python is not found in your PATH. Please install Python from python.org or the Microsoft Store." -ForegroundColor Red
        exit 1
    }
}

if (-not $python_cmd) { $python_cmd = "python" }

# 2. Reset .venv if it exists (it seems broken)
if (Test-Path ".venv") {
    Write-Host "Removing existing (potentially broken) .venv..." -ForegroundColor Yellow
    Remove-Item -Path ".venv" -Recurse -Force
}

# 3. Create new venv
Write-Host "Creating new virtual environment..." -ForegroundColor Cyan
& $python_cmd -m venv .venv

if (-not (Test-Path ".venv")) {
    Write-Host "Failed to create .venv!" -ForegroundColor Red
    exit 1
}

# 4. Install requirements
Write-Host "Installing dependencies..." -ForegroundColor Cyan
./.venv/Scripts/pip install -r requirements.txt

# 5. Run Debug
Write-Host "Running debug test..." -ForegroundColor Cyan
./.venv/Scripts/python debug_client.py

Write-Host "Done! You can now run the client using: .\.venv\Scripts\python main_client.py" -ForegroundColor Green
pause
