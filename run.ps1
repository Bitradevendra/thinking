# Advanced Reasoning System - Quick Launch Script for Windows
# Save this as run.ps1 and execute with: powershell -ExecutionPolicy Bypass -File run.ps1

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " Advanced Reasoning System" -ForegroundColor Yellow
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if API key is set
if (-not $env:DEEPSEEK_API_KEY) {
    Write-Host "⚠️  WARNING: DEEPSEEK_API_KEY is not set!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please set your API key first:" -ForegroundColor White
    Write-Host "  `$env:DEEPSEEK_API_KEY = 'your-api-key-here'" -ForegroundColor Gray
    Write-Host ""
    
    $response = Read-Host "Continue anyway? (y/n)"
    if ($response -ne 'y') {
        exit
    }
}

# Show menu
Write-Host "Select an option:" -ForegroundColor Cyan
Write-Host "  1) Run setup script" -ForegroundColor White
Write-Host "  2) Quick test (10 iterations)" -ForegroundColor White
Write-Host "  3) Math example problem" -ForegroundColor White
Write-Host "  4) Code analysis example" -ForegroundColor White
Write-Host "  5) Custom problem" -ForegroundColor White
Write-Host "  6) Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-6)"

switch ($choice) {
    "1" {
        Write-Host "`nRunning setup script..." -ForegroundColor Green
        python setup.py
    }
    "2" {
        Write-Host "`nRunning quick test..." -ForegroundColor Green
        python main.py "What is 2 + 2? Verify the answer." --iterations 10
    }
    "3" {
        Write-Host "`nSolving math problem..." -ForegroundColor Green
        python main.py "Solve: x^2 - 4 = 0" --iterations 30
    }
    "4" {
        Write-Host "`nAnalyzing example code..." -ForegroundColor Green
        python main.py "Analyze this code for potential improvements" --files examples\example_code.py --iterations 40
    }
    "5" {
        $problem = Read-Host "`nEnter your problem"
        $iterations = Read-Host "Number of iterations (default: 50)"
        if (-not $iterations) { $iterations = 50 }
        
        $files = Read-Host "Files to attach (optional, space-separated)"
        
        if ($files) {
            Write-Host "`nRunning analysis..." -ForegroundColor Green
            python main.py "$problem" --iterations $iterations --files $files.Split(' ')
        } else {
            Write-Host "`nRunning analysis..." -ForegroundColor Green
            python main.py "$problem" --iterations $iterations
        }
    }
    "6" {
        Write-Host "`nGoodbye!" -ForegroundColor Green
        exit
    }
    default {
        Write-Host "`nInvalid choice!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Done! Check logs/ directory for results" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
