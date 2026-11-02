[CmdletBinding()]
param(
    [string]$Version = "1.0.0",
    [string]$OutputDir = "$PSScriptRoot\..\dist"
)

$ErrorActionPreference = "Stop"
# Resolver ruta absoluta contra la raiz del repositorio para evitar ambigüedades en Inno Setup
if (-not [System.IO.Path]::IsPathRooted($OutputDir)) {
    $OutputDir = Join-Path "$PSScriptRoot\.." $OutputDir
}
$OutputDir = [System.IO.Path]::GetFullPath($OutputDir)

Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host " 🐍 SnakeUSBIP: Workflow de Compilacion Protegida (Coste 0 €)" -ForegroundColor Cyan
Write-Host "    Version: $Version | Destino: $OutputDir" -ForegroundColor DarkGray
Write-Host "==============================================================" -ForegroundColor Cyan

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
        /p:Version=$Version /p:AssemblyVersion=$($Version).0 /p:FileVersion=$($Version).0 /p:InformationalVersion=$Version `
        /p:DebugType=none `
        /p:DebugSymbols=false `
        -o "$OutputDir\portable\server"
    Write-Host "  [OK] Servidor compilado a binario optimizado nativo." -ForegroundColor Green
}

# 2. Client WPF (ReadyToRun Single-File)
Write-Host "`n[2/4] Compilando Client WPF con ReadyToRun..." -ForegroundColor Yellow
$clientProj = "$PSScriptRoot\..\client\src\SnakeUSBIP\SnakeUSBIP.csproj"
if (Test-Path $clientProj) {
    dotnet publish $clientProj -c Release -r win-x64 --self-contained `
        /p:PublishSingleFile=true `
        /p:PublishReadyToRun=true `
        /p:Version=$Version /p:AssemblyVersion=$($Version).0 /p:FileVersion=$($Version).0 /p:InformationalVersion=$Version `
        /p:DebugType=none `
        /p:DebugSymbols=false `
        -o "$OutputDir\portable"
    Write-Host "  [OK] Cliente visual protegido y empaquetado." -ForegroundColor Green
}

# 3. Integracion de drivers y assets al paquete portable
Write-Host "`n[3/4] Integrando drivers y herramientas nativas..." -ForegroundColor Yellow
$clientPortable = "$PSScriptRoot\..\client\Portable"
if (Test-Path $clientPortable) {
    Copy-Item "$clientPortable\*" "$OutputDir\portable\" -Recurse -Force
}
$serverDrivers = "$PSScriptRoot\..\server\portable\drivers"
if (-not (Test-Path $serverDrivers)) { $serverDrivers = "$PSScriptRoot\..\server\Portable\drivers" }
if (Test-Path $serverDrivers) {
    Copy-Item "$serverDrivers\*" "$OutputDir\portable\server\drivers" -Recurse -Force -ErrorAction SilentlyContinue
}

$license = "$PSScriptRoot\..\LICENSE"
if (Test-Path $license) {
    Copy-Item $license "$OutputDir\portable\LICENSE" -Force
    Copy-Item $license "$OutputDir\portable\server\LICENSE" -Force
}
$readme = "$PSScriptRoot\..\README.md"
if (Test-Path $readme) {
    Copy-Item $readme "$OutputDir\portable\README.md" -Force
    Copy-Item $readme "$OutputDir\portable\server\README.md" -Force
}

# Purgar archivos PDB residuales
Get-ChildItem -Path "$OutputDir\portable" -Filter "*.pdb" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force
Write-Host "  [OK] Simbolos de depuracion purgados." -ForegroundColor Green

# 4. Inno Setup & Empaquetado
Write-Host "`n[4/4] Generando paquetes de distribucion..." -ForegroundColor Yellow
$zipPath = "$OutputDir\installer\SnakeUSBIP_v$Version`_Portable_win-x64.zip"
Compress-Archive -Path "$OutputDir\portable\*" -DestinationPath $zipPath -Force
Write-Host "  [OK] Paquete Portable ZIP generado." -ForegroundColor Green

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
        Write-Host "  Compilando instalador Inno Setup Cliente..." -ForegroundColor DarkGray
        $portableDir = "$OutputDir\portable"
        $installerDir = "$OutputDir\installer"
        & $iscc "/DMyAppVersion=$Version" "/DSourceDir=$portableDir" "/O$installerDir" $innoScript
        if ($LASTEXITCODE -ne 0) {
            throw "Compilacion de Inno Setup Cliente fallo con codigo $LASTEXITCODE"
        }
        Write-Host "  [OK] Instalador Cliente Inno Setup generado." -ForegroundColor Green

        # Servidor Inno Setup
        $serverInnoScript = "$PSScriptRoot\..\server\installer\SnakeUSBIP-Server.iss"
        if (Test-Path $serverInnoScript) {
            Write-Host "  Compilando instalador Inno Setup Servidor..." -ForegroundColor DarkGray
            $serverPortableDir = "$OutputDir\portable\server"
            & $iscc "/DMyAppVersion=$Version" "/DSourceDir=$serverPortableDir" "/O$installerDir" $serverInnoScript
            if ($LASTEXITCODE -ne 0) {
                Write-Warning "Compilacion de Inno Setup Servidor finalizo con codigo $LASTEXITCODE"
            } else {
                Write-Host "  [OK] Instalador Servidor Inno Setup generado." -ForegroundColor Green
            }
        }
    }
}

# 5. Calculo determinista de SHA256SUMS.txt
Write-Host "`nCalculando SHA256SUMS.txt para verificacion oficial..." -ForegroundColor Yellow
$hashFile = "$OutputDir\installer\SHA256SUMS.txt"
if (Test-Path $hashFile) { Remove-Item $hashFile -Force }

Get-ChildItem -Path "$OutputDir\installer" -File | Where-Object { $_.Name -ne "SHA256SUMS.txt" } | ForEach-Object {
    $hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower()
    $line = "$hash  $($_.Name)"
    Add-Content -Path $hashFile -Value $line
    Write-Host "  SHA256: $line" -ForegroundColor DarkGray
}

Write-Host "`n==============================================================" -ForegroundColor Green
Write-Host " ✅ Workflow de Proteccion Completado con Éxito" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green
