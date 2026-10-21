# Anade a la solucion de Visual Studio los ejercicios que todavia no estan en ella.
#
# Por que hace falta: el .sln y los .vcxproj estan en el .gitignore (son de cada uno), asi que
# al hacer git pull llegan las carpetas nuevas (EJ_06-1, EJ_07-1, ...) con su .cpp y sus .h,
# pero Visual Studio no sabe que existen hasta que tienen un proyecto dentro de tu .sln.
#
# Uso (con Visual Studio CERRADO y despues de hacer git pull):
#     powershell -ExecutionPolicy Bypass -File herramientas\anadir_ejercicios_vs.ps1
#
# Que hace:
#   1. Recorre las carpetas de tema (1-..., 2-..., ...) y, dentro, las carpetas EJ* que tengan .cpp.
#   2. Si una carpeta no tiene .vcxproj, lo crea copiando uno de tu repo (para conservar tu
#      PlatformToolset y tu estandar de C++); si no hay ninguno, usa una plantilla propia (C++17).
#      Incluye en el proyecto el .cpp, las cabeceras .h y el README.md.
#   3. Anade al .sln los proyectos que falten, dentro de la carpeta de solucion de su tema
#      (si no existe, la crea), con las mismas configuraciones (Debug/Release, x86/x64) que el resto.
# Antes de tocar el .sln guarda una copia .bak-ejercicios al lado.
# Se puede ejecutar varias veces: lo que ya esta en el .sln no se toca.
#
# -Auto: modo silencioso para el hook de git (ver instalar_auto_vs.ps1). Si Visual Studio esta abierto
# o no hay .sln, no hace nada y no falla (para no estropear el git pull); avisa de que lo ejecutes a mano.
param([switch]$Auto)

$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $PSScriptRoot
$tipoCpp = '8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942'
$tipoCarpeta = '2150E333-8FDC-42A3-9474-1A3956D46DE8'
$utf8bom = New-Object Text.UTF8Encoding $true

if (Get-Process devenv -ErrorAction SilentlyContinue) {
    if ($Auto) {
        Write-Host "[ejercicios] Visual Studio esta abierto: no toco el .sln. Cuando lo cierres ejecuta herramientas\anadir_ejercicios_vs.ps1" -ForegroundColor Yellow
        exit 0
    }
    Write-Host "Cierra Visual Studio antes de ejecutar el script." -ForegroundColor Red
    exit 1
}

$slns = @(Get-ChildItem -LiteralPath $raiz -Filter *.sln -File)
if ($slns.Count -eq 0) {
    if ($Auto) { exit 0 }
    Write-Host "No encuentro ningun .sln en $raiz (la carpeta del repositorio). No he cambiado nada." -ForegroundColor Red
    exit 1
}

# ---------------------------------------------------------------- ejercicios del repo
$ejercicios = @()
$temas = Get-ChildItem -LiteralPath $raiz -Directory | Where-Object { $_.Name -match '^\d+-' } | Sort-Object Name
foreach ($tema in $temas) {
    $dirs = Get-ChildItem -LiteralPath $tema.FullName -Directory | Where-Object { $_.Name -like 'EJ*' } | Sort-Object Name
    foreach ($ej in $dirs) {
        $cpps = @(Get-ChildItem -LiteralPath $ej.FullName -Filter *.cpp -File)
        if ($cpps.Count -eq 0) { continue }
        $ejercicios += [pscustomobject]@{ Tema = $tema.Name; Nombre = $ej.Name; Dir = $ej.FullName }
    }
}
Write-Host "Ejercicios con codigo en el repo: $($ejercicios.Count)"

# ---------------------------------------------------------------- plantilla de .vcxproj
function Nueva-Guid { return ([guid]::NewGuid().ToString().ToUpper()) }

$plantilla = $null
foreach ($e in $ejercicios) {
    $p = @(Get-ChildItem -LiteralPath $e.Dir -Filter *.vcxproj -File)
    if ($p.Count -gt 0) {
        if ($null -eq $plantilla -or $p[0].Name -like 'EJ_05-1*') { $plantilla = [IO.File]::ReadAllText($p[0].FullName) }
    }
}
if ($null -ne $plantilla) { Write-Host "Plantilla: uno de tus .vcxproj (se conservan tu toolset y tu estandar de C++)." }

$primerSln = [IO.File]::ReadAllText($slns[0].FullName)
$toolset = 'v143'
if ($primerSln -match '# Visual Studio Version (\d+)') {
    if ($Matches[1] -eq '16') { $toolset = 'v142' } elseif ($Matches[1] -eq '15') { $toolset = 'v141' }
}

function Plantilla-Propia([string]$nombre, [string]$guid, [string]$items) {
    $cfgs = @(@('Debug', 'Win32'), @('Release', 'Win32'), @('Debug', 'x64'), @('Release', 'x64'))
    $sb = New-Object Text.StringBuilder
    [void]$sb.AppendLine('<?xml version="1.0" encoding="utf-8"?>')
    [void]$sb.AppendLine('<Project DefaultTargets="Build" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">')
    [void]$sb.AppendLine('  <ItemGroup Label="ProjectConfigurations">')
    foreach ($c in $cfgs) {
        [void]$sb.AppendLine("    <ProjectConfiguration Include=`"$($c[0])|$($c[1])`">")
        [void]$sb.AppendLine("      <Configuration>$($c[0])</Configuration>")
        [void]$sb.AppendLine("      <Platform>$($c[1])</Platform>")
        [void]$sb.AppendLine('    </ProjectConfiguration>')
    }
    [void]$sb.AppendLine('  </ItemGroup>')
    [void]$sb.AppendLine('  <PropertyGroup Label="Globals">')
    [void]$sb.AppendLine('    <VCProjectVersion>17.0</VCProjectVersion>')
    [void]$sb.AppendLine('    <Keyword>Win32Proj</Keyword>')
    [void]$sb.AppendLine("    <ProjectGuid>{$guid}</ProjectGuid>")
    [void]$sb.AppendLine("    <RootNamespace>$nombre</RootNamespace>")
    [void]$sb.AppendLine('    <WindowsTargetPlatformVersion>10.0</WindowsTargetPlatformVersion>')
    [void]$sb.AppendLine('  </PropertyGroup>')
    [void]$sb.AppendLine('  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />')
    foreach ($c in $cfgs) {
        $dbg = ($c[0] -eq 'Debug').ToString().ToLower()
        [void]$sb.AppendLine("  <PropertyGroup Condition=`"'`$(Configuration)|`$(Platform)'=='$($c[0])|$($c[1])'`" Label=`"Configuration`">")
        [void]$sb.AppendLine('    <ConfigurationType>Application</ConfigurationType>')
        [void]$sb.AppendLine("    <UseDebugLibraries>$dbg</UseDebugLibraries>")
        [void]$sb.AppendLine("    <PlatformToolset>$toolset</PlatformToolset>")
        if ($c[0] -eq 'Release') { [void]$sb.AppendLine('    <WholeProgramOptimization>true</WholeProgramOptimization>') }
        [void]$sb.AppendLine('    <CharacterSet>Unicode</CharacterSet>')
        [void]$sb.AppendLine('  </PropertyGroup>')
    }
    [void]$sb.AppendLine('  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />')
    [void]$sb.AppendLine('  <ImportGroup Label="ExtensionSettings">')
    [void]$sb.AppendLine('  </ImportGroup>')
    [void]$sb.AppendLine('  <ImportGroup Label="Shared">')
    [void]$sb.AppendLine('  </ImportGroup>')
    foreach ($c in $cfgs) {
        [void]$sb.AppendLine("  <ImportGroup Label=`"PropertySheets`" Condition=`"'`$(Configuration)|`$(Platform)'=='$($c[0])|$($c[1])'`">")
        [void]$sb.AppendLine('    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists(''$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props'')" Label="LocalAppDataPlatform" />')
        [void]$sb.AppendLine('  </ImportGroup>')
    }
    [void]$sb.AppendLine('  <PropertyGroup Label="UserMacros" />')
    foreach ($c in $cfgs) {
        $defs = if ($c[0] -eq 'Debug') { '_DEBUG;_CONSOLE;%(PreprocessorDefinitions)' } else { 'NDEBUG;_CONSOLE;%(PreprocessorDefinitions)' }
        [void]$sb.AppendLine("  <ItemDefinitionGroup Condition=`"'`$(Configuration)|`$(Platform)'=='$($c[0])|$($c[1])'`">")
        [void]$sb.AppendLine('    <ClCompile>')
        [void]$sb.AppendLine('      <WarningLevel>Level3</WarningLevel>')
        if ($c[0] -eq 'Release') {
            [void]$sb.AppendLine('      <FunctionLevelLinking>true</FunctionLevelLinking>')
            [void]$sb.AppendLine('      <IntrinsicFunctions>true</IntrinsicFunctions>')
        }
        [void]$sb.AppendLine('      <SDLCheck>true</SDLCheck>')
        [void]$sb.AppendLine("      <PreprocessorDefinitions>$defs</PreprocessorDefinitions>")
        [void]$sb.AppendLine('      <ConformanceMode>true</ConformanceMode>')
        [void]$sb.AppendLine('      <LanguageStandard>stdcpp17</LanguageStandard>')
        [void]$sb.AppendLine('    </ClCompile>')
        [void]$sb.AppendLine('    <Link>')
        [void]$sb.AppendLine('      <SubSystem>Console</SubSystem>')
        if ($c[0] -eq 'Release') {
            [void]$sb.AppendLine('      <EnableCOMDATFolding>true</EnableCOMDATFolding>')
            [void]$sb.AppendLine('      <OptimizeReferences>true</OptimizeReferences>')
        }
        [void]$sb.AppendLine('      <GenerateDebugInformation>true</GenerateDebugInformation>')
        [void]$sb.AppendLine('    </Link>')
        [void]$sb.AppendLine('  </ItemDefinitionGroup>')
    }
    [void]$sb.Append($items)
    [void]$sb.AppendLine('  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />')
    [void]$sb.AppendLine('  <ImportGroup Label="ExtensionTargets">')
    [void]$sb.AppendLine('  </ImportGroup>')
    [void]$sb.AppendLine('</Project>')
    return $sb.ToString()
}

function Items-Del-Ejercicio([string]$dir) {
    $s = New-Object Text.StringBuilder
    $cpps = @(Get-ChildItem -LiteralPath $dir -Filter *.cpp -File | Sort-Object Name)
    $hs = @(Get-ChildItem -LiteralPath $dir -File | Where-Object { $_.Extension -in '.h', '.hpp' } | Sort-Object Name)
    $rd = @(Get-ChildItem -LiteralPath $dir -Filter README.md -File)
    [void]$s.AppendLine('  <ItemGroup>')
    foreach ($f in $cpps) { [void]$s.AppendLine("    <ClCompile Include=`"$($f.Name)`" />") }
    [void]$s.AppendLine('  </ItemGroup>')
    if ($hs.Count -gt 0) {
        [void]$s.AppendLine('  <ItemGroup>')
        foreach ($f in $hs) { [void]$s.AppendLine("    <ClInclude Include=`"$($f.Name)`" />") }
        [void]$s.AppendLine('  </ItemGroup>')
    }
    if ($rd.Count -gt 0) {
        [void]$s.AppendLine('  <ItemGroup>')
        [void]$s.AppendLine('    <None Include="README.md" />')
        [void]$s.AppendLine('  </ItemGroup>')
    }
    return $s.ToString()
}

function Crea-Vcxproj($ej) {
    $nombre = $ej.Nombre -replace '[^A-Za-z0-9_\-\.]', '_'
    $guid = Nueva-Guid
    $items = Items-Del-Ejercicio $ej.Dir
    if ($null -ne $plantilla) {
        $t = $plantilla
        $t = [regex]::Replace($t, '<ProjectGuid>[^<]*</ProjectGuid>', "<ProjectGuid>{$guid}</ProjectGuid>")
        $t = [regex]::Replace($t, '<RootNamespace>[^<]*</RootNamespace>', "<RootNamespace>$nombre</RootNamespace>")
        $t = [regex]::Replace($t, '<ProjectName>[^<]*</ProjectName>', "<ProjectName>$nombre</ProjectName>")
        # fuera los ItemGroup de ficheros de la plantilla (los que no tienen Label) y dentro los nuestros
        $t = [regex]::Replace($t, '(?s)[ \t]*<ItemGroup>.*?</ItemGroup>\r?\n?', '')
        $marca = '<Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />'
        $pos = $t.IndexOf($marca)
        if ($pos -lt 0) { $t = $null } else {
            $ini = $t.LastIndexOf("`n", $pos) + 1
            $t = $t.Substring(0, $ini) + $items + $t.Substring($ini)
        }
    } else { $t = $null }
    if ($null -eq $t) { $t = Plantilla-Propia $nombre $guid $items }
    $t = $t -replace "`r?`n", "`r`n"
    $ruta = Join-Path $ej.Dir ($nombre + '.vcxproj')
    [IO.File]::WriteAllText($ruta, $t, $utf8bom)
    return $ruta
}

# ---------------------------------------------------------------- 1. un .vcxproj por ejercicio
foreach ($e in $ejercicios) {
    $p = @(Get-ChildItem -LiteralPath $e.Dir -Filter *.vcxproj -File)
    if ($p.Count -eq 0) {
        $ruta = Crea-Vcxproj $e
        Write-Host "  creado: $($e.Tema)\$($e.Nombre)\$(Split-Path -Leaf $ruta)" -ForegroundColor Cyan
    }
    $p = @(Get-ChildItem -LiteralPath $e.Dir -Filter *.vcxproj -File)
    $e | Add-Member -NotePropertyName Vcxproj -NotePropertyValue $p[0] -Force
}

# ---------------------------------------------------------------- 2. el .sln
function Inserta-En-Seccion([string]$txt, [string]$nombre, [string]$modo, [string[]]$lineas, [string]$nl) {
    $ini = $txt.IndexOf("GlobalSection($nombre)")
    if ($ini -lt 0) {
        $ms = [regex]::Matches($txt, '(?m)^EndGlobal[ \t]*\r?$')
        if ($ms.Count -eq 0) { throw "El .sln no tiene 'EndGlobal'; no lo toco." }
        $pos = $ms[$ms.Count - 1].Index
        $bloque = "`tGlobalSection($nombre) = $modo$nl" + (($lineas | ForEach-Object { "`t`t$_" }) -join $nl) + "$nl`tEndGlobalSection$nl"
        return $txt.Substring(0, $pos) + $bloque + $txt.Substring($pos)
    }
    $fin = $txt.IndexOf('EndGlobalSection', $ini)
    $lineStart = $txt.LastIndexOf("`n", $fin) + 1
    $bloque = (($lineas | ForEach-Object { "`t`t$_" }) -join $nl) + $nl
    return $txt.Substring(0, $lineStart) + $bloque + $txt.Substring($lineStart)
}

foreach ($sln in $slns) {
    $txt = [IO.File]::ReadAllText($sln.FullName)
    $orig = $txt
    $nl = if ($txt.Contains("`r`n")) { "`r`n" } else { "`n" }

    # configuraciones de la solucion (Debug|x64 = Debug|x64 ...)
    $cfgSol = @()
    $m = [regex]::Match($txt, '(?s)GlobalSection\(SolutionConfigurationPlatforms\) = preSolution(.*?)EndGlobalSection')
    if ($m.Success) {
        foreach ($l in [regex]::Matches($m.Groups[1].Value, '(?m)^\s*([^=\r\n]+?)\s*=\s*[^\r\n]+$')) { $cfgSol += $l.Groups[1].Value.Trim() }
    }
    if ($cfgSol.Count -eq 0) { $cfgSol = @('Debug|x64', 'Debug|x86', 'Release|x64', 'Release|x86') }

    $anadidos = 0
    foreach ($e in $ejercicios) {
        $nombreProy = [IO.Path]::GetFileNameWithoutExtension($e.Vcxproj.Name)
        $rel = "$($e.Tema)\$($e.Nombre)\$($e.Vcxproj.Name)"
        if ($txt.IndexOf($rel, [StringComparison]::OrdinalIgnoreCase) -ge 0) { continue }

        $vc = [IO.File]::ReadAllText($e.Vcxproj.FullName)
        $g = [regex]::Match($vc, '<ProjectGuid>\{?([0-9A-Fa-f-]+)\}?</ProjectGuid>')
        if (-not $g.Success) { Write-Host "  sin ProjectGuid, me lo salto: $rel" -ForegroundColor Yellow; continue }
        $guid = $g.Groups[1].Value.ToUpper()
        if ($txt.IndexOf($guid, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
            Write-Host "  el .sln ya tiene el GUID de $rel con otra ruta; me lo salto (revisalo a mano)" -ForegroundColor Yellow
            continue
        }

        # carpeta de solucion del tema (se crea si no existe)
        $cf = [regex]::Match($txt, 'Project\("\{' + $tipoCarpeta + '\}"\) = "' + [regex]::Escape($e.Tema) + '", "[^"]*", "\{([^}]+)\}"')
        $nuevoTexto = ''
        if ($cf.Success) { $guidCarpeta = $cf.Groups[1].Value.ToUpper() } else {
            $guidCarpeta = Nueva-Guid
            $nuevoTexto += "Project(`"{$tipoCarpeta}`") = `"$($e.Tema)`", `"$($e.Tema)`", `"{$guidCarpeta}`"$($nl)EndProject$nl"
            Write-Host "  carpeta de solucion nueva: $($e.Tema)" -ForegroundColor Cyan
        }
        $nuevoTexto += "Project(`"{$tipoCpp}`") = `"$nombreProy`", `"$rel`", `"{$guid}`"$($nl)EndProject$nl"

        # despues del ultimo EndProject (o antes de Global)
        $ms = [regex]::Matches($txt, '(?m)^EndProject[ \t]*\r?$')
        if ($ms.Count -gt 0) {
            $u = $ms[$ms.Count - 1]
            $pos = $u.Index + $u.Length
            if ($pos -lt $txt.Length -and $txt[$pos] -eq "`n") { $pos++ }
        } else {
            $pos = $txt.IndexOf('Global')
            if ($pos -lt 0) { throw "El .sln no tiene 'Global'; no lo toco." }
        }
        $txt = $txt.Substring(0, $pos) + $nuevoTexto + $txt.Substring($pos)

        # configuraciones del proyecto
        $lin = @()
        foreach ($c in $cfgSol) {
            $partes = $c.Split('|')
            $plat = $partes[1]
            if ($plat -eq 'x86') { $platProy = 'Win32' } elseif ($plat -eq 'Any CPU') { $platProy = 'x64' } else { $platProy = $plat }
            $lin += "{$guid}.$c.ActiveCfg = $($partes[0])|$platProy"
            $lin += "{$guid}.$c.Build.0 = $($partes[0])|$platProy"
        }
        $txt = Inserta-En-Seccion $txt 'ProjectConfigurationPlatforms' 'postSolution' $lin $nl
        $txt = Inserta-En-Seccion $txt 'NestedProjects' 'preSolution' @("{$guid} = {$guidCarpeta}") $nl

        Write-Host "  anadido a $($sln.Name): $rel" -ForegroundColor Green
        $anadidos++
    }

    if ($txt -ne $orig) {
        Copy-Item -LiteralPath $sln.FullName -Destination "$($sln.FullName).bak-ejercicios" -Force
        [IO.File]::WriteAllText($sln.FullName, $txt, $utf8bom)
        Write-Host "$($sln.Name): $anadidos proyecto(s) anadido(s). Copia anterior en $($sln.Name).bak-ejercicios" -ForegroundColor Green
    } else {
        Write-Host "$($sln.Name): ya tenia todos los ejercicios, no he cambiado nada." -ForegroundColor Green
    }

    # comprobacion: todos los proyectos del .sln existen
    $txt = [IO.File]::ReadAllText($sln.FullName)
    $mal = 0
    $ms = [regex]::Matches($txt, 'Project\("\{[^}]+\}"\) = "([^"]*)", "([^"]+\.vcxproj)"')
    foreach ($mm in $ms) {
        $p = Join-Path $raiz ($mm.Groups[2].Value -replace '\\', [IO.Path]::DirectorySeparatorChar)
        if (-not (Test-Path -LiteralPath $p)) { Write-Host "  FALTA: $($mm.Groups[1].Value) -> $($mm.Groups[2].Value)" -ForegroundColor Red; $mal++ }
    }
    if ($mal -eq 0) { Write-Host "OK: los $($ms.Count) proyectos de $($sln.Name) existen. Ya puedes abrir Visual Studio." -ForegroundColor Green }
    else { Write-Host "Hay proyectos del .sln cuya ruta no existe (ver arriba)." -ForegroundColor Red }
}
