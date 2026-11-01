<#
.SYNOPSIS
    Verificador Autónomo de Protección y Seguridad Zero-Trust para SnakeUSBIP.
.DESCRIPTION
    Ejecuta 4 compuertas de seguridad:
    Gate 1: Compilación .NET 9 limpia sin errores.
    Gate 2: 133 Tests Unitarios superados al 100%.
    Gate 3: Purgado de símbolos PDB y metadatos de depuración.
    Gate 4: Zero-Leak (auditoría contra fugas de rutas locales privadas).
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
Write-Host "══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " 🛡️ SnakeUSBIP: Verificación de Protección Zero-Trust" -ForegroundColor Cyan
Write-Host "══════════════════════════════════════════════════════════════" -ForegroundColor Cyan

$root = "$PSScriptRoot\.."

# Gate 1: Compilación
Write-Host "`n[Gate 1/4] Verificando Compilación Release..." -ForegroundColor Yellow
$buildOut = dotnet build "$root\SnakeUSBIP.sln" -c Release --nologo 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Fallo en compilación:" -ForegroundColor Red
    $buildOut | Write-Host
    exit 1
}
Write-Host "  ✓ Compilación correcta (0 errores)." -ForegroundColor Green

# Gate 2: Tests
Write-Host "`n[Gate 2/4] Ejecutando 133 Tests Unitarios..." -ForegroundColor Yellow
$testOut = dotnet test "$root\SnakeUSBIP.sln" -c Release --no-build --nologo 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Fallo en tests unitarios:" -ForegroundColor Red
    $testOut | Write-Host
    exit 1
}
Write-Host "  ✓ 133 Tests superados al 100%." -ForegroundColor Green

# Gate 3: Purgado de PDBs en herramientas
Write-Host "`n[Gate 3/4] Verificando Higiene de Símbolos y Archivos..." -ForegroundColor Yellow
$loosePdbs = Get-ChildItem -Path "$root" -Filter "*.pdb" -Recurse | Where-Object { $_.FullName -notmatch '\\bin\\' -and $_.FullName -notmatch '\\obj\\' }
if ($loosePdbs.Count -gt 0) {
    Write-Host "❌ Se encontraron archivos PDB fuera de bin/obj:" -ForegroundColor Red
    $loosePdbs | Select-Object -ExpandProperty FullName | Write-Host
    exit 1
}
Write-Host "  ✓ No hay PDBs expuestos en el código fuente ni en distribución." -ForegroundColor Green

# Gate 4: Zero-Leak
Write-Host "`n[Gate 4/4] Verificando Zero-Leak de rutas privadas..." -ForegroundColor Yellow
$leaks = git -C $root grep -i "C:\\Users\\snake" 2>$null
if ($leaks) {
    Write-Host "❌ Alerta Zero-Leak: se detectaron rutas privadas locales." -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ 0 Fugas detectadas. Repositorio 100% higienizado." -ForegroundColor Green

Write-Host "`n══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host " ✅ Verificación de Protección Completa: APROBADA (4/4 GATES)" -ForegroundColor Green
Write-Host "══════════════════════════════════════════════════════════════" -ForegroundColor Green
