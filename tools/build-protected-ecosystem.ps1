[CmdletBinding()]
param(
    [string]$Version = "3.2.0",
    [string]$OutputDir = "$PSScriptRoot\..\dist"
)

$ErrorActionPreference = "Stop"
Write-Host "══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " 🐍 SnakeUSBIP: Workflow de Compilación Protegida (Coste 0 €)" -ForegroundColor Cyan
Write-Host "    Versión: $Version | Destino: $OutputDir" -ForegroundColor DarkGray
Write-Host "══════════════════════════════════════════════════════════════" -ForegroundColor Cyan

# Preparar salida limpia
if (Test-Path $OutputDir) { Remove-Item $OutputDir -Recurse -Force }
New-Item -ItemType Directory -Path "$OutputDir\portable\server" -Force | Out-Null
New-Item -ItemType Directory -Path "$OutputDir\installer" -Force | Out-Null

# 1. Server (.NET 9 ReadyToRun Single-File)
Write-Host "`n[1/4] Compilando Server con ReadyToRun (x64)..." -ForegroundColor Yellow
$serverProj = "$PSScriptRoot\..\server\src\SnakeUSBIP.Server\SnakeUSBIP.Server.csproj"
if (Test-Path $serverProj) {
    dotnet publish $serverProj -c Release -r win-x64 --self-contained `
        /p:PublishSingleFile=true `
        /p:PublishReadyToRun=true `
        /p:DebugType=none `
        /p:DebugSymbols=false `
        -o "$OutputDir\portable\server"
    Write-Host "  ✓ Servidor compilado a binario optimizado nativo." -ForegroundColor Green
}

# 2. Client WPF (ReadyToRun Single-File)
Write-Host "`n[2/4] Compilando Client WPF con ReadyToRun..." -ForegroundColor Yellow
$clientProj = "$PSScriptRoot\..\client\src\SnakeUSBIP\SnakeUSBIP.csproj"
if (Test-Path $clientProj) {
    dotnet publish $clientProj -c Release -r win-x64 --self-contained `
        /p:PublishSingleFile=true `
        /p:PublishReadyToRun=true `
        /p:DebugType=none `
        /p:DebugSymbols=false `
        -o "$OutputDir\portable"
    Write-Host "  ✓ Cliente visual protegido y empaquetado." -ForegroundColor Green
}

# 3. Integración de drivers y assets al paquete portable
Write-Host "`n[3/4] Integrando drivers y herramientas nativas..." -ForegroundColor Yellow
$clientPortable = "$PSScriptRoot\..\client\Portable"
if (Test-Path $clientPortable) {
    Copy-Item "$clientPortable\*" "$OutputDir\portable\" -Recurse -Force
}
$license = "$PSScriptRoot\..\LICENSE"
if (Test-Path $license) { Copy-Item $license "$OutputDir\portable\LICENSE" -Force }
$readme = "$PSScriptRoot\..\README.md"
if (Test-Path $readme) { Copy-Item $readme "$OutputDir\portable\README.md" -Force }

# Purgar archivos PDB residuales
Get-ChildItem -Path "$OutputDir\portable" -Filter "*.pdb" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force
Write-Host "  ✓ Símbolos de depuración purgados." -ForegroundColor Green

# 4. Inno Setup & Empaquetado
Write-Host "`n[4/4] Generando paquetes de distribución..." -ForegroundColor Yellow
$zipPath = "$OutputDir\installer\SnakeUSBIP_v$Version`_Portable_win-x64.zip"
Compress-Archive -Path "$OutputDir\portable\*" -DestinationPath $zipPath -Force
Write-Host "  ✓ Paquete Portable ZIP generado." -ForegroundColor Green

$innoScript = "$PSScriptRoot\..\client\installer\SnakeUSBIP.iss"
if (Test-Path $innoScript) {
    $iscc = Get-Command "iscc" -ErrorAction SilentlyContinue
    if (-not $iscc) {
        $paths = @(
            "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
            "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
        )
        foreach ($p in $paths) {
            if (Test-Path $p) { $iscc = $p; break }
        }
    }
    if ($iscc) {
        Write-Host "  Compilando instalador Inno Setup..." -ForegroundColor DarkGray
        & $iscc /DMyAppVersion=$Version /DSourceDir="$OutputDir\portable" /O"$OutputDir\installer" $innoScript | Out-Null
        Write-Host "  ✓ Instalador Inno Setup generado." -ForegroundColor Green
    }
}

# 5. Cálculo determinista de SHA256SUMS.txt
Write-Host "`nCalculando SHA256SUMS.txt para verificación oficial..." -ForegroundColor Yellow
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
