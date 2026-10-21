# Instala (una sola vez) un hook de git para que, despues de cada "git pull" que traiga ejercicios
# nuevos, se anadan solos a tu .sln de Visual Studio (herramientas\anadir_ejercicios_vs.ps1 -Auto).
#
# Uso, desde la carpeta del repositorio:
#     powershell -ExecutionPolicy Bypass -File herramientas\instalar_auto_vs.ps1
#
# - El hook (.git/hooks/post-merge) es local: no se sube al repo ni afecta a nadie mas.
# - Si Visual Studio esta abierto durante el pull, no toca nada y te avisa; entonces ejecuta
#   herramientas\anadir_ejercicios_vs.ps1 cuando lo cierres.
# - Para quitarlo: borra el fichero .git\hooks\post-merge.

$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $PSScriptRoot
$hooks = Join-Path $raiz '.git\hooks'
if (-not (Test-Path -LiteralPath $hooks)) {
    Write-Host "No encuentro $hooks. Ejecuta el script desde un clon del repositorio." -ForegroundColor Red
    exit 1
}
$hook = Join-Path $hooks 'post-merge'
$marca = '# anadir-ejercicios-vs'
$contenido = @"
#!/bin/sh
$marca
raiz=`$(git rev-parse --show-toplevel)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "`$raiz/herramientas/anadir_ejercicios_vs.ps1" -Auto || true
"@
$contenido = $contenido -replace "`r`n", "`n"

if ((Test-Path -LiteralPath $hook) -and -not ([IO.File]::ReadAllText($hook) -match [regex]::Escape($marca))) {
    Write-Host "Ya existe un hook post-merge tuyo; no lo piso. Anade esta linea al final a mano:" -ForegroundColor Yellow
    Write-Host "  powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"`$(git rev-parse --show-toplevel)/herramientas/anadir_ejercicios_vs.ps1`" -Auto || true"
    exit 1
}
[IO.File]::WriteAllText($hook, $contenido, (New-Object Text.UTF8Encoding $false))
Write-Host "Hook instalado: $hook" -ForegroundColor Green
Write-Host "A partir de ahora, cada git pull anade los ejercicios nuevos a tu .sln (con Visual Studio cerrado)."
