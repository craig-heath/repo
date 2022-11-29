# **Red Canary Atomic Testing Guide**
These are my shorthand notes for getting this setup, full credit and more details can be found at: https://github.com/redcanaryco/atomic-red-team
Note to self:
- Ensure Detect only mode is configured
- Set-ExecutionPolicy Unrestricted

### Install execution framework and atomics
```
IEX (IWR 'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1' -UseBasicParsing); 
Install-AtomicRedTeam -getAtomics -Force
```

### Import the module (and add to profile)
```
Import-Module "C:\AtomicRedTeam\invoke-atomicredteam\Invoke-AtomicRedTeam.psd1" -Force
$PSDefaultParameterValues = @{"Invoke-AtomicTest:PathToAtomicsFolder"="C:\AtomicRedTeam\atomics"}
```

### List tests (All, or specific)
```
Invoke-AtomicTest All -ShowDetailsBrief
Invoke-AtomicTest T1003 -ShowDetailsBrief
Invoke-AtomicTest T1003 -ShowDetails 
```

### Check prereqs of specific technique 
```
Invoke-AtomicTest T1003 -CheckPrereqs
Invoke-AtomicTest T1003 -TestName "Windows Credential Editor" -CheckPrereqs
```

### Get pre-reqs
```
Invoke-AtomicTest T1003 -GetPrereqs
Invoke-AtomicTest T1003 -TestName "Windows Credential Editor" -GetPrereqs
```

### Execute tests
```
Invoke-AtomicTest T1218.010

//by test number
Invoke-AtomicTest T1218.010 -TestNumbers 1,2

// or using the short form ..

Invoke-AtomicTest T1218.010-1,2

//by name
Invoke-AtomicTest T1218.010 -TestNames "Regsvr32 remote COM scriptlet execution","Regsvr32 local DLL execution"

//interactively

Invoke-AtomicTest T1003 -Interactive

//All tests at once (not recommended)
Invoke-AtomicTest All
```

### Cleanup After Tests
```
Invoke-AtomicTest T1089 -TestNames "Uninstall Sysmon" -Cleanup
Invoke-AtomicTest T1089 -Cleanup
```

### Script that checks/installs pre-reqs and executes test for ALL
```
$techniques = gci C:\AtomicRedTeam\atomics\* -Recurse -Include T*.yaml | Get-AtomicTechnique

foreach ($technique in $techniques) {
    foreach ($atomic in $technique.atomic_tests) {
        if ($atomic.supported_platforms.contains("windows") -and ($atomic.executor -ne "manual")) {
            # Get Prereqs for test
            Invoke-AtomicTest $technique.attack_technique -TestGuids $atomic.auto_generated_guid -GetPrereqs
            # Invoke
            Invoke-AtomicTest $technique.attack_technique -TestGuids $atomic.auto_generated_guid
            # Sleep then cleanup
            Start-Sleep 3
            Invoke-AtomicTest  $technique.attack_technique -TestGuids $atomic.auto_generated_guid -Cleanup
        }
    }
}
```
