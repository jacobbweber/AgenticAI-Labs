function Invoke-CiscoSEHttp {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Uri,
        [string]$Body,
        [int]$TimeoutSec = 300
    )
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
    $params = @{
        Uri             = $Uri
        Method          = 'POST'
        Body            = $bytes
        ContentType     = 'application/json; charset=utf-8'
        TimeoutSec      = $TimeoutSec
        UseBasicParsing = $true
    }
    $iwr = Get-Command Invoke-WebRequest -ErrorAction Stop
    if ($iwr.Parameters.ContainsKey('SkipHttpErrorCheck')) {
        $params.SkipHttpErrorCheck = $true
    }
    try {
        $resp = Invoke-WebRequest @params
        return @{
            StatusCode = [int]$resp.StatusCode
            Content    = [string]$resp.Content
        }
    }
    catch [System.Net.WebException] {
        $ex = $_.Exception
        $code = 0
        $content = $ex.Message
        if ($ex.Response) {
            $code = [int]$ex.Response.StatusCode
            try {
                $stream = $ex.Response.GetResponseStream()
                $reader = New-Object System.IO.StreamReader($stream)
                $content = $reader.ReadToEnd()
                $reader.Close()
            }
            catch {
                $content = $ex.Message
            }
        }
        return @{
            StatusCode = $code
            Content    = $content
            Error      = $ex.Message
        }
    }
    catch {
        $code = 0
        $msg = $_.Exception.Message
        if ($_.Exception.Response) {
            try { $code = [int]$_.Exception.Response.StatusCode } catch { $code = 0 }
        }
        if ($msg -match '\((\d{3})\)') {
            $code = [int]$Matches[1]
        }
        return @{
            StatusCode = $code
            Content    = $msg
            Error      = $msg
        }
    }
}

function Get-CiscoSEBackoffSeconds {
    [CmdletBinding()]
    param([int]$Attempt)
    if ($null -ne $script:CiscoSEBackoffSeconds) {
        return [double]$script:CiscoSEBackoffSeconds
    }
    $exp = [Math]::Pow(2, [Math]::Max(0, $Attempt - 1))
    return [double]$exp
}

function Invoke-OllamaChat {
    [CmdletBinding()]
    param(
        $Messages,
        $Tools,
        $Config
    )
    $cfg = Merge-CiscoSEConfig -FileConfig $Config
    if ($null -ne $Config) {
        $incoming = ConvertTo-CiscoSETable -Value $Config
        foreach ($k in $incoming.Keys) { $cfg[$k] = $incoming[$k] }
        $cfg.host = ([string]$cfg.host).TrimEnd('/')
    }
    $uri = $cfg.host.TrimEnd('/') + '/api/chat'
    $payload = @{
        model    = $cfg.model
        messages = ConvertTo-CiscoSEList -Value $Messages
        stream   = $false
        think    = $false
        options  = @{ temperature = 0.2 }
    }
    if ($null -ne $Tools) {
        $payload.tools = ConvertTo-CiscoSEList -Value $Tools
    }
    $body = ConvertTo-CiscoSEJson -Value $payload
    $maxAttempts = 1 + [int]$cfg.max_retries
    $last = $null
    for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
        $last = Invoke-CiscoSEHttp -Uri $uri -Body $body -TimeoutSec ([int]$cfg.timeout_sec)
        $code = 0
        if ($null -ne $last.StatusCode) { $code = [int]$last.StatusCode }
        $retryable = ($code -ge 500 -or $code -eq 429 -or $code -eq 0)
        if ($code -ge 200 -and $code -lt 300) {
            $obj = $last.Content | ConvertFrom-Json
            $eval = 0
            $promptEval = 0
            if ($obj.PSObject.Properties['eval_count']) { $eval = [int]$obj.eval_count }
            if ($obj.PSObject.Properties['prompt_eval_count']) { $promptEval = [int]$obj.prompt_eval_count }
            return @{
                message           = $obj.message
                eval_count        = $eval
                prompt_eval_count = $promptEval
                raw               = $obj
                StatusCode        = $code
            }
        }
        if ($retryable -and $attempt -lt $maxAttempts) {
            $sleep = Get-CiscoSEBackoffSeconds -Attempt $attempt
            if ($sleep -gt 0) {
                Start-Sleep -Seconds $sleep
            }
            continue
        }
        throw "Ollama chat failed (HTTP $code): $($last.Content)"
    }
    throw "Ollama chat failed after $maxAttempts attempts: $($last.Content)"
}
