# **Red Canary Atomic Testing Guide**
These are my shorthand notes for getting this setup, full credit and more details can be found at: https://github.com/redcanaryco/atomic-red-team

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
