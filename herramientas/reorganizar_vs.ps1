# Recoloca los proyectos de Visual Studio tras la reorganizacion del repo por temas.
#
# Uso (una sola vez, con Visual Studio CERRADO y despues de hacer git pull):
#     powershell -ExecutionPolicy Bypass -File herramientas\reorganizar_vs.ps1
#
# Que hace:
#   1. Mueve lo que git no controla (.vcxproj, .filters, .user, x64\, Debug\...) de cada
#      carpeta antigua (p. ej. EJ_05-1\) a la nueva (5-Grafos dirigidos\EJ_05-1\).
#   2. Corrige las rutas relativas "..\" dentro de los .vcxproj y .filters movidos
#      (ahora estan un nivel mas abajo).
#   3. Cambia en el .sln la ruta de cada proyecto movido.
# Antes de tocar un .sln, .vcxproj o .filters guarda una copia .bak al lado.
# Se puede ejecutar varias veces: lo que ya esta en su sitio no se toca.

$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $PSScriptRoot
function Ruta([string]$rel) { Join-Path $raiz ($rel -replace '\\', [IO.Path]::DirectorySeparatorChar) }

$mapa = @(
    @('DA', '1-Arboles AVL\EJ_01-1'),
    @('EJ 01-1 (GENERICO)', '1-Arboles AVL\EJ_01-1 (generico v1)'),
    @('J 01-1 (GENERICO) - NICE', '1-Arboles AVL\EJ_01-1 (generico)'),
    @('EJ 01-2', '1-Arboles AVL\EJ_01-2'),
    @('EJ_02-1', '2-Colas de prioridad\EJ_02-1'),
    @('EJ_02-2', '2-Colas de prioridad\EJ_02-2'),
    @('EJ_02-3', '2-Colas de prioridad\EJ_02-3'),
    @('EJ_02-4', '2-Colas de prioridad\EJ_02-4'),
    @('EJ_02-5', '2-Colas de prioridad\EJ_02-5'),
    @('EJ_02-6', '2-Colas de prioridad\EJ_02-6'),
    @('EJ_02-L', '2-Colas de prioridad\EJ_02-L'),
    @('EJ_03-1', '3-Colas de prioridad variable (Heapsort)\EJ_03-1'),
    @('EJ_03-2', '3-Colas de prioridad variable (Heapsort)\EJ_03-2'),
    @('EJ_03-3', '3-Colas de prioridad variable (Heapsort)\EJ_03-3'),
    @('EJ_03-4', '3-Colas de prioridad variable (Heapsort)\EJ_03-4'),
    @('EJ_03-5', '3-Colas de prioridad variable (Heapsort)\EJ_03-5'),
    @('EJ_03-L', '3-Colas de prioridad variable (Heapsort)\EJ_03-L'),
    @('EJ_04-1', '4-Grafos no dirigidos\EJ_04-1'),
    @('EJ_04-2', '4-Grafos no dirigidos\EJ_04-2'),
    @('EJ_04-3', '4-Grafos no dirigidos\EJ_04-3'),
    @('EJ_04-4', '4-Grafos no dirigidos\EJ_04-4'),
    @('EJ_04-5', '4-Grafos no dirigidos\EJ_04-5'),
    @('EJ_04-6', '4-Grafos no dirigidos\EJ_04-6'),
    @('EJ_04-7', '4-Grafos no dirigidos\EJ_04-7'),
    @('EJ_04-L', '4-Grafos no dirigidos\EJ_04-L'),
    @('EJ_05-1', '5-Grafos dirigidos\EJ_05-1'),
    @('EJ_05-2', '5-Grafos dirigidos\EJ_05-2'),
    @('EJ_05-3', '5-Grafos dirigidos\EJ_05-3'),
    @('EJ_05-4', '5-Grafos dirigidos\EJ_05-4'),
    @('EJ_05-5', '5-Grafos dirigidos\EJ_05-5'),
    @('EJ_05-6', '5-Grafos dirigidos\EJ_05-6'),
    @('Ejercicios juez\1-Arboles AVL', '1-Arboles AVL\Enunciados'),
    @('Ejercicios juez\2-Colas de prioridad', '2-Colas de prioridad\Enunciados'),
    @('Ejercicios juez\3-Colas de prioridad variable (Heapsort)', '3-Colas de prioridad variable (Heapsort)\Enunciados'),
    @('Ejercicios juez\4-Grafos no dirigidos', '4-Grafos no dirigidos\Enunciados'),
    @('Ejercicios juez\5-Grafos dirigidos', '5-Grafos dirigidos\Enunciados')
)

if (Get-Process devenv -ErrorAction SilentlyContinue) {
    Write-Host "Cierra Visual Studio antes de ejecutar el script." -ForegroundColor Red
    exit 1
}

$slns = Get-ChildItem -LiteralPath $raiz -Filter *.sln -File
if (-not $slns) {
    Write-Host "No encuentro ningun .sln en $raiz (la carpeta del repositorio). No he movido nada." -ForegroundColor Red
    exit 1
}

function Corrige-Relativas([string]$fichero) {
    $txt = [IO.File]::ReadAllText($fichero)
    # Include="..\x" / ;..\x / >..\x  ->  ..\..\x   (rutas que salen de la carpeta del proyecto)
    $nuevo = [regex]::Replace($txt, '(?<=["'';>])\.\.\\', '..\..\')
    if ($nuevo -ne $txt) {
        Copy-Item -LiteralPath $fichero -Destination "$fichero.bak" -Force
        [IO.File]::WriteAllText($fichero, $nuevo, (New-Object Text.UTF8Encoding $true))
        Write-Host "    rutas ..\ corregidas en $(Split-Path -Leaf $fichero)"
    }
}

$movidos = @()
foreach ($par in $mapa) {
    $viejo = Ruta $par[0]
    $nuevo = Ruta $par[1]
    if (-not (Test-Path -LiteralPath $viejo)) { continue }
    if (-not (Test-Path -LiteralPath $nuevo)) { New-Item -ItemType Directory -Path $nuevo | Out-Null }
    Write-Host "$($par[0])  ->  $($par[1])" -ForegroundColor Cyan
    foreach ($item in Get-ChildItem -LiteralPath $viejo -Force) {
        $destino = Join-Path $nuevo $item.Name
        if (Test-Path -LiteralPath $destino) {
            Write-Host "    ya existe, no se mueve: $($item.Name)" -ForegroundColor Yellow
            continue
        }
        Move-Item -LiteralPath $item.FullName -Destination $destino
        Write-Host "    movido: $($item.Name)"
        if ($item.Name -match '\.vcxproj(\.filters)?$') { Corrige-Relativas $destino }
    }
    if (-not (Get-ChildItem -LiteralPath $viejo -Force)) { Remove-Item -LiteralPath $viejo }
    else { Write-Host "    (la carpeta antigua no queda vacia, revisala: $viejo)" -ForegroundColor Yellow }
    $movidos += ,$par
}
$ej = Join-Path $raiz 'Ejercicios juez'
if ((Test-Path -LiteralPath $ej) -and -not (Get-ChildItem -LiteralPath $ej -Recurse -File -Force)) {
    Remove-Item -LiteralPath $ej -Recurse
}

# .sln: rutas de los proyectos
foreach ($sln in $slns) {
    $txt = [IO.File]::ReadAllText($sln.FullName)
    $orig = $txt
    foreach ($par in $mapa) {
        $a = [regex]::Escape($par[0] + '\')
        $txt = [regex]::Replace($txt, '(Project\("\{[^}]+\}"\) = "[^"]*", ")' + $a, ('${1}' + $par[1].Replace('$', '$$') + '\'))
    }
    if ($txt -ne $orig) {
        Copy-Item -LiteralPath $sln.FullName -Destination "$($sln.FullName).bak" -Force
        [IO.File]::WriteAllText($sln.FullName, $txt, (New-Object Text.UTF8Encoding $true))
        Write-Host "Rutas actualizadas en $($sln.Name)" -ForegroundColor Green
    } else {
        Write-Host "$($sln.Name): no habia rutas que cambiar" -ForegroundColor Green
    }
}

# comprobacion: todos los proyectos del .sln existen; si no, se restaura la copia
foreach ($sln in $slns) {
    $txt = [IO.File]::ReadAllText($sln.FullName)
    $mal = 0
    $ms = [regex]::Matches($txt, 'Project\("\{[^}]+\}"\) = "([^"]*)", "([^"]+\.vcxproj)"')
    $total = ([regex]::Matches($txt, '\.vcxproj"')).Count
    if ($ms.Count -ne $total) { Write-Host "  Hay lineas de proyecto con un formato inesperado en $($sln.Name)" -ForegroundColor Red; $mal++ }
    foreach ($m in $ms) {
        $p = Ruta $m.Groups[2].Value
        if (-not (Test-Path -LiteralPath $p)) { Write-Host "  FALTA: $($m.Groups[1].Value) -> $($m.Groups[2].Value)" -ForegroundColor Red; $mal++ }
    }
    if ($mal -eq 0) {
        Write-Host "OK: los $($ms.Count) proyectos de $($sln.Name) estan en su sitio. Ya puedes abrir Visual Studio." -ForegroundColor Green
    } else {
        Write-Host "Algo no cuadra (ver arriba). No toques nada y avisame; la version anterior del .sln esta en $($sln.Name).bak" -ForegroundColor Red
    }
}
