[CmdletBinding()]
param(
    [string]$Version = "3.0.0",
    [string]$OutputDir = "$PSScriptRoot\..\dist"
)

$ErrorActionPreference = "Stop"
Write-Host "══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " 🐍 SnakeUSBIP: Workflow de Compilación Protegida (Coste 0 €)" -ForegroundColor Cyan
Write-Host "    Versión: $Version | Destino: $OutputDir" -ForegroundColor DarkGray
Write-Host "══════════════════════════════════════════════════════════════" -ForegroundColor Cyan

# Preparar salida
if (Test-Path $OutputDir) { Remove-Item $OutputDir -Recurse -Force }
New-Item -ItemType Directory -Path "$OutputDir\portable" -Force | Out-Null
New-Item -ItemType Directory -Path "$OutputDir\installer" -Force | Out-Null

# 1. Server (.NET 9 Native AOT)
Write-Host "`n[1/4] Compilando Server con Native AOT (x64)..." -ForegroundColor Yellow
$serverProj = "$PSScriptRoot\..\server\src\SnakeUSBIP.Server\SnakeUSBIP.Server.csproj"
if (Test-Path $serverProj) {
    dotnet publish $serverProj -c Release -r win-x64 --self-contained `
        /p:PublishAot=true `
        /p:StripSymbols=true `
        /p:OptimizationPreference=Speed `
        -o "$OutputDir\portable\server"
    Write-Host "  ✓ Servidor compilado a código máquina nativo puro." -ForegroundColor Green
}

# 2. Client WPF (ReadyToRun + Single-File)
Write-Host "`n[2/4] Compilando Client WPF con ReadyToRun..." -ForegroundColor Yellow
$clientProj = "$PSScriptRoot\..\client\src\SnakeUSBIP\SnakeUSBIP.csproj"
if (Test-Path $clientProj) {
    dotnet publish $clientProj -c Release -r win-x64 --self-contained `
        /p:PublishSingleFile=true `
        /p:PublishReadyToRun=true `
        /p:PublishReadyToRunComposite=true `
        /p:PublishTrimmed=true `
        /p:TrimMode=partial `
        /p:DebugType=none `
        /p:DebugSymbols=false `
        -o "$OutputDir\portable"
    Write-Host "  ✓ Cliente visual protegido y empaquetado." -ForegroundColor Green
}

# 3. Purgar PDBs
Write-Host "`n[3/4] Purgando archivos PDB..." -ForegroundColor Yellow
Get-ChildItem -Path "$OutputDir\portable" -Filter "*.pdb" -Recurse | Remove-Item -Force
Write-Host "  ✓ Símbolos eliminados." -ForegroundColor Green

# 4. Empaquetar y Hash SHA-256
Write-Host "`n[4/4] Empaquetando y calculando SHA256SUMS.txt..." -ForegroundColor Yellow
$zipPath = "$OutputDir\installer\SnakeUSBIP_v$Version`_Portable_win-x64.zip"
Compress-Archive -Path "$OutputDir\portable\*" -DestinationPath $zipPath -Force

$hashFile = "$OutputDir\installer\SHA256SUMS.txt"
if (Test-Path $hashFile) { Remove-Item $hashFile -Force }

Get-ChildItem -Path "$OutputDir\installer" -File | Where-Object { $_.Name -ne "SHA256SUMS.txt" } | ForEach-Object {
    $hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower()
    $line = "$hash  $($_.Name)"
    Add-Content -Path $hashFile -Value $line
    Write-Host "  SHA256: $line" -ForegroundColor DarkGray
}

Write-Host "`n══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host " ✅ Workflow de Protección Completado con Éxito" -ForegroundColor Green
Write-Host "══════════════════════════════════════════════════════════════" -ForegroundColor Green
