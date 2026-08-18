function Get-CiscoSEToolSchema {
    [CmdletBinding()]
    param()
    return @(
        @{
            type     = 'function'
            function = @{
                name        = 'remember_fact'
                description = 'Store an episodic customer fact so it survives session restarts.'
                parameters  = @{
                    type       = 'object'
                    properties = @{
                        key   = @{ type = 'string'; description = 'Fact key' }
                        value = @{ type = 'string'; description = 'Fact value' }
                        ttl   = @{ type = 'string'; description = 'Optional TTL (stored, not swept)' }
                    }
                    required   = @('key', 'value')
                }
            }
        },
        @{
            type     = 'function'
            function = @{
                name        = 'recall_facts'
                description = 'Return all stored episodic facts.'
                parameters  = @{
                    type       = 'object'
                    properties = @{}
                }
            }
        },
        @{
            type     = 'function'
            function = @{
                name        = 'load_skill'
                description = 'Load a procedural SKILL.md by id (enterprise-networking, security, datacenter, collaboration, rfp-response, poc-plan, bom-draft).'
                parameters  = @{
                    type       = 'object'
                    properties = @{
                        id = @{ type = 'string'; description = 'Skill id' }
                    }
                    required   = @('id')
                }
            }
        },
        @{
            type     = 'function'
            function = @{
                name        = 'save_artifact'
                description = 'Save a design artifact. kind is HLD, LLD, BoM, PoC, RFP, or Discovery.'
                parameters  = @{
                    type       = 'object'
                    properties = @{
                        kind    = @{ type = 'string'; description = 'HLD LLD BoM PoC RFP Discovery' }
                        name    = @{ type = 'string'; description = 'Artifact name' }
                        body    = @{ type = 'string'; description = 'Markdown/text body' }
                        version = @{ type = 'string'; description = 'Optional version suffix' }
                    }
                    required   = @('kind', 'name', 'body')
                }
            }
        },
        @{
            type     = 'function'
            function = @{
                name        = 'build_bom_draft'
                description = 'After an LLD is saved, draft a BoM. Every price is [UNVERIFIED]. Never invent SKUs.'
                parameters  = @{
                    type       = 'object'
                    properties = @{
                        artifact_name = @{ type = 'string'; description = 'Saved LLD artifact name' }
                        vendor_scope  = @{ type = 'string'; description = 'Optional note only' }
                    }
                    required   = @('artifact_name')
                }
            }
        },
        @{
            type     = 'function'
            function = @{
                name        = 'park_for_approval'
                description = 'HITL gate: park customer-ready docs, final BoM, or live lab work.'
                parameters  = @{
                    type       = 'object'
                    properties = @{
                        artifact_name = @{ type = 'string' }
                        reason        = @{ type = 'string' }
                    }
                    required   = @('artifact_name', 'reason')
                }
            }
        }
    )
}

function Get-CiscoSEFactList {
    [CmdletBinding()]
    param()
    $path = Get-CiscoSEPath -Name facts
    $obj = Read-CiscoSEJsonFile -Path $path -Default @()
    $rows = @()
    foreach ($item in (ConvertTo-CiscoSEList -Value $obj)) {
        $rows += (ConvertTo-CiscoSETable -Value $item)
    }
    return (ConvertTo-CiscoSEList -Value $rows)
}

function Save-CiscoSEFactList {
    [CmdletBinding()]
    param($Facts)
    Initialize-CiscoSEHomeDirs
    Write-CiscoSEJsonFile -Path (Get-CiscoSEPath -Name facts) -Value (ConvertTo-CiscoSEList -Value $Facts)
}

function Invoke-CiscoSERememberFact {
    [CmdletBinding()]
    param($Arguments)
    $key = [string](Get-CiscoSEArg -Arguments $Arguments -Names @('key'))
    $value = [string](Get-CiscoSEArg -Arguments $Arguments -Names @('value'))
    $ttl = Get-CiscoSEArg -Arguments $Arguments -Names @('ttl')
    if ([string]::IsNullOrWhiteSpace($key)) {
        return (ConvertTo-CiscoSEJson -Value @{ error = 'key required' })
    }
    $facts = ConvertTo-CiscoSEList -Value (Get-CiscoSEFactList)
    $next = @()
    $replaced = $false
    foreach ($f in $facts) {
        if ([string]$f.key -eq $key) {
            $row = @{ key = $key; value = $value; at = (Get-Date).ToString('o') }
            if ($null -ne $ttl) { $row.ttl = [string]$ttl }
            $next += $row
            $replaced = $true
        }
        else {
            $next += $f
        }
    }
    if (-not $replaced) {
        $row = @{ key = $key; value = $value; at = (Get-Date).ToString('o') }
        if ($null -ne $ttl) { $row.ttl = [string]$ttl }
        $next += $row
    }
    Save-CiscoSEFactList -Facts $next
    return (ConvertTo-CiscoSEJson -Value @{ ok = $true; key = $key })
}

function Invoke-CiscoSERecallFacts {
    [CmdletBinding()]
    param()
    $facts = ConvertTo-CiscoSEList -Value (Get-CiscoSEFactList)
    $slim = @()
    foreach ($f in $facts) {
        $slim += @{ key = [string]$f.key; value = [string]$f.value }
    }
    return (ConvertTo-CiscoSEJson -Value @{ facts = $slim })
}

function Get-CiscoSESkillPath {
    [CmdletBinding()]
    param([string]$Id)
    $safe = Get-CiscoSESafeName -Name $Id
    $homeSkill = Join-Path (Get-CiscoSEPath -Name skills) ($safe + '.md')
    if (Test-Path -LiteralPath $homeSkill) { return $homeSkill }
    $modSkill = Join-Path (Join-Path $script:CiscoSEModuleRoot 'Skills') ($safe + '.md')
    if (Test-Path -LiteralPath $modSkill) { return $modSkill }
    return $null
}

function Get-CiscoSESkillCatalog {
    [CmdletBinding()]
    param()
    $ids = New-Object System.Collections.Generic.List[string]
    $dirs = @(
        (Join-Path $script:CiscoSEModuleRoot 'Skills'),
        (Get-CiscoSEPath -Name skills)
    )
    foreach ($dir in $dirs) {
        if (-not (Test-Path -LiteralPath $dir)) { continue }
        Get-ChildItem -Path $dir -Filter '*.md' | ForEach-Object {
            $id = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
            if (-not $ids.Contains($id)) { $ids.Add($id) }
        }
    }
    return $ids
}

function Invoke-CiscoSELoadSkill {
    [CmdletBinding()]
    param($Arguments)
    $id = [string](Get-CiscoSEArg -Arguments $Arguments -Names @('id', 'skill', 'name'))
    if ([string]::IsNullOrWhiteSpace($id)) {
        return (ConvertTo-CiscoSEJson -Value @{ error = 'id required'; loaded = $false })
    }
    $path = Get-CiscoSESkillPath -Id $id
    if ($null -eq $path) {
        return (ConvertTo-CiscoSEJson -Value @{ error = 'unknown skill'; id = $id; loaded = $false })
    }
    $body = [System.IO.File]::ReadAllText($path)
    return (ConvertTo-CiscoSEJson -Value @{ loaded = $true; id = $id; path = $path; body = $body })
}

function Find-CiscoSESkillTriggers {
    [CmdletBinding()]
    param([string]$UserText)
    $loaded = New-Object System.Collections.Generic.List[string]
    if ([string]::IsNullOrWhiteSpace($UserText)) { return @() }
    $text = $UserText.ToLowerInvariant()
    foreach ($id in @(Get-CiscoSESkillCatalog)) {
        $path = Get-CiscoSESkillPath -Id $id
        if ($null -eq $path) { continue }
        $body = [System.IO.File]::ReadAllText($path)
        $needles = New-Object System.Collections.Generic.List[string]
        $needles.Add($id.ToLowerInvariant())
        $needles.Add(($id -replace '-', ' ').ToLowerInvariant())
        if ($body -match '(?im)^\*\*Load when:\*\*\s*(.+)$') {
            foreach ($part in ($Matches[1] -split ',')) {
                $p = $part.Trim().ToLowerInvariant()
                if ($p) { $needles.Add($p) }
            }
        }
        foreach ($n in $needles) {
            if ($text.Contains($n)) {
                if (-not $loaded.Contains($id)) { $loaded.Add($id) }
                break
            }
        }
    }
    return @($loaded)
}

function Get-CiscoSEArtifactPath {
    [CmdletBinding()]
    param(
        [string]$Kind,
        [string]$Name
    )
    $safeKind = Get-CiscoSESafeName -Name $Kind
    $safeName = Get-CiscoSESafeName -Name $Name
    if ($safeName -notmatch '\.') { $safeName = $safeName + '.md' }
    return (Join-Path (Join-Path (Get-CiscoSEPath -Name artifacts) $safeKind) $safeName)
}

function Find-CiscoSEArtifact {
    [CmdletBinding()]
    param([string]$Name)
    $safe = Get-CiscoSESafeName -Name $Name
    $root = Get-CiscoSEPath -Name artifacts
    if (-not (Test-Path -LiteralPath $root)) { return $null }
    $candidates = @(
        $safe,
        ($safe + '.md'),
        ($safe + '.txt')
    )
    foreach ($item in @(Get-ChildItem -Path $root -Recurse -File -ErrorAction SilentlyContinue)) {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($item.Name)
        $file = $item.Name
        foreach ($c in $candidates) {
            if ($file -eq $c -or $base -eq $safe) {
                return $item
            }
        }
    }
    return $null
}

function Invoke-CiscoSESaveArtifact {
    [CmdletBinding()]
    param($Arguments)
    $kind = [string](Get-CiscoSEArg -Arguments $Arguments -Names @('kind'))
    $name = [string](Get-CiscoSEArg -Arguments $Arguments -Names @('name', 'artifact_id', 'artifact_name'))
    $body = [string](Get-CiscoSEArg -Arguments $Arguments -Names @('body'))
    $version = Get-CiscoSEArg -Arguments $Arguments -Names @('version')
    if ([string]::IsNullOrWhiteSpace($kind) -or [string]::IsNullOrWhiteSpace($name)) {
        return (ConvertTo-CiscoSEJson -Value @{ error = 'kind and name required' })
    }
    $known = $false
    foreach ($k in $script:CiscoSEArtifactKinds) {
        if ($k -eq $kind) { $known = $true }
    }
    if (-not $known) {
        return (ConvertTo-CiscoSEJson -Value @{ error = 'unknown kind'; kind = $kind })
    }
    if ($null -ne $version -and -not [string]::IsNullOrWhiteSpace([string]$version)) {
        $name = $name + '-v' + ([string]$version)
    }
    Initialize-CiscoSEHomeDirs
    $path = Get-CiscoSEArtifactPath -Kind $kind -Name $name
    $dir = Split-Path -Parent $path
    if (-not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    [System.IO.File]::WriteAllText($path, $body)
    return (ConvertTo-CiscoSEJson -Value @{ ok = $true; path = $path; kind = $kind; name = $name })
}

function Get-CiscoSELldRoles {
    [CmdletBinding()]
    param([string]$Body)
    $roles = New-Object System.Collections.Generic.List[string]
    if ([string]::IsNullOrWhiteSpace($Body)) { return @() }
    foreach ($line in ($Body -split '\r?\n')) {
        $t = $line.Trim()
        if ($t -match '(?i)^hostname\s+(\S+)') {
            $roles.Add(('hostname ' + $Matches[1]))
            continue
        }
        if ($t -match '(?i)^(?:device|role|node)\s*:\s*(.+)$') {
            $roles.Add($Matches[1].Trim())
            continue
        }
        if ($t -match '(?i)^[-*]\s+(?:device|role|switch|router|firewall|wlan|edge)\s*[:\-]\s*(.+)$') {
            $roles.Add($Matches[1].Trim())
            continue
        }
    }
    return @($roles)
}

function Invoke-CiscoSEBuildBomDraft {
    [CmdletBinding()]
    param($Arguments)
    $artifactName = [string](Get-CiscoSEArg -Arguments $Arguments -Names @('artifact_name', 'artifact_id', 'name'))
    $vendorScope = Get-CiscoSEArg -Arguments $Arguments -Names @('vendor_scope')
    if ([string]::IsNullOrWhiteSpace($artifactName)) {
        return (ConvertTo-CiscoSEJson -Value @{ error = 'artifact_name required' })
    }
    $file = Find-CiscoSEArtifact -Name $artifactName
    if ($null -eq $file) {
        $lldPath = Get-CiscoSEArtifactPath -Kind 'LLD' -Name $artifactName
        if (Test-Path -LiteralPath $lldPath) {
            $file = Get-Item -LiteralPath $lldPath
        }
    }
    if ($null -eq $file) {
        return (ConvertTo-CiscoSEJson -Value @{ error = 'LLD not found; save_artifact kind=LLD first'; artifact_name = $artifactName })
    }
    $parentKind = [System.IO.Path]::GetFileName($file.DirectoryName)
    if ($parentKind -ne 'LLD') {
        return (ConvertTo-CiscoSEJson -Value @{ error = 'build_bom_draft requires a saved LLD'; found_kind = $parentKind })
    }
    $lldBody = [System.IO.File]::ReadAllText($file.FullName)
    $roles = @(Get-CiscoSELldRoles -Body $lldBody)
    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add('# BoM draft')
    $lines.Add('')
    $lines.Add('Every list price is [UNVERIFIED]. No SKU is invented. Confirm via CCW/partner.')
    if ($null -ne $vendorScope -and -not [string]::IsNullOrWhiteSpace([string]$vendorScope)) {
        $lines.Add(('Vendor scope note: ' + [string]$vendorScope))
    }
    $lines.Add('')
    $lines.Add('| Group | Role | SKU | Qty | List price | Notes |')
    $lines.Add('|---|---|---|---|---|---|')
    if ($roles.Count -eq 0) {
        $lines.Add('| Cisco | (from LLD) | [UNVERIFIED – confirm via CCW/partner] | 1 | [UNVERIFIED] | Placeholder only. Human confirms SKU in CCW. |')
        $lines.Add('| Third-party | (none extracted) | [UNVERIFIED – confirm via CCW/partner] | 0 | [UNVERIFIED] | Inventory existing stack before quoting. |')
    }
    else {
        foreach ($role in $roles) {
            $safeRole = ($role -replace '\|', '/')
            $lines.Add("| Cisco | $safeRole | [UNVERIFIED – confirm via CCW/partner] | 1 | [UNVERIFIED] | Do not treat as a quote. |")
        }
    }
    $lines.Add('')
    $lines.Add('CCW is human-side. This file is a draft, not a commercial offer.')
    $body = ($lines -join "`n")
    $bomName = ([System.IO.Path]::GetFileNameWithoutExtension($file.Name) + '-bom')
    $saveArgs = @{ kind = 'BoM'; name = $bomName; body = $body }
    $saved = Invoke-CiscoSESaveArtifact -Arguments $saveArgs
    $savedTable = ConvertTo-CiscoSETable -Value ($saved | ConvertFrom-Json)
    return (ConvertTo-CiscoSEJson -Value @{
            ok   = $true
            path = $savedTable.path
            name = $bomName
            kind = 'BoM'
            body = $body
        })
}

function Invoke-CiscoSEParkForApproval {
    [CmdletBinding()]
    param($Arguments)
    $artifactName = [string](Get-CiscoSEArg -Arguments $Arguments -Names @('artifact_name', 'artifact_id', 'name'))
    $reason = [string](Get-CiscoSEArg -Arguments $Arguments -Names @('reason'))
    $sessionId = $script:CiscoSECurrentSessionId
    if ([string]::IsNullOrWhiteSpace($sessionId)) { $sessionId = 'default' }
    $session = Read-CiscoSESession -SessionId $sessionId
    $session.needs_hitl = $true
    $session.parked_artifact = $artifactName
    $session.park_reason = $reason
    $session.stop_reason = 'needs_hitl'
    $session.hitl_decision = $null
    Save-CiscoSESession -Session $session | Out-Null
    if ($session.job_id) {
        Set-CiscoSEJobStatus -JobId ([string]$session.job_id) -Status 'needs_hitl' -ProposedAction $reason | Out-Null
    }
    return (ConvertTo-CiscoSEJson -Value @{
            needs_hitl      = $true
            artifact_name   = $artifactName
            reason          = $reason
            session_id      = $sessionId
        })
}

function Invoke-CiscoSEHitlResume {
    [CmdletBinding()]
    param(
        [string]$SessionId = 'default',
        [bool]$Approved
    )
    $session = Read-CiscoSESession -SessionId $SessionId
    $decision = 'denied'
    $jobStatus = 'failed'
    if ($Approved) {
        $decision = 'approved'
        $jobStatus = 'done'
    }
    $session.needs_hitl = $false
    $session.hitl_decision = $decision
    $session.stop_reason = $decision
    $note = "Human $decision parked artifact '$($session.parked_artifact)'. Reason was: $($session.park_reason)."
    $session = Add-CiscoSESessionMessage -Session $session -Message @{ role = 'user'; content = $note }
    Save-CiscoSESession -Session $session | Out-Null
    if ($session.job_id) {
        Set-CiscoSEJobStatus -JobId ([string]$session.job_id) -Status $jobStatus -Result $decision | Out-Null
    }
    return $session
}

function Invoke-CiscoSETool {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        $Arguments
    )
    if ($script:CiscoSEAllowedTools -notcontains $Name) {
        return (ConvertTo-CiscoSEJson -Value @{ error = 'unknown tool'; name = $Name })
    }
    switch ($Name) {
        'remember_fact' { return (Invoke-CiscoSERememberFact -Arguments $Arguments) }
        'recall_facts' { return (Invoke-CiscoSERecallFacts) }
        'load_skill' { return (Invoke-CiscoSELoadSkill -Arguments $Arguments) }
        'save_artifact' { return (Invoke-CiscoSESaveArtifact -Arguments $Arguments) }
        'build_bom_draft' { return (Invoke-CiscoSEBuildBomDraft -Arguments $Arguments) }
        'park_for_approval' { return (Invoke-CiscoSEParkForApproval -Arguments $Arguments) }
        default { return (ConvertTo-CiscoSEJson -Value @{ error = 'unknown tool'; name = $Name }) }
    }
}
