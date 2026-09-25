# DataHub on Windows — Setup Investigation

## Current objective

Set up **DataHub on Windows**, proceeding **one step at a time**, while keeping the installation clean and reversible.

The intended development model is:

```text
Windows
│
├── Python development
├── Database development
├── IDE / Git / normal tools
│
└── Docker Desktop
      │
      └── WSL 2 backend
            │
            ├── DataHub containers
            └── Future course / agentic-AI containers
```

Python and database development will remain on Windows. WSL 2 is not intended to become the primary Linux development environment.

---

## Current machine

```text
Dell Latitude 3420
Windows 11 Pro
Version: 25H2
OS Build: 26200
x64
RAM: ~16 GB
```

`systeminfo` explicitly confirms Windows 11 Pro.

A separate:

```powershell
(Get-ComputerInfo).WindowsProductName
```

returned `Windows 10 Pro`; this is treated as a legacy/internal reporting inconsistency because `systeminfo` confirms Windows 11 Pro.

---

## Current WSL status

The command:

```powershell
wsl --status
```

reported:

```text
The Windows Subsystem for Linux is not installed.
You can install by running 'wsl.exe --install'.
```

Therefore:

```text
WSL: NOT INSTALLED
```

No WSL installation has been performed.

---

## Current Hyper-V / virtualization feature status

From Administrator PowerShell:

```powershell
Get-WindowsOptionalFeature -Online |
    Where-Object {$_.FeatureName -match "Hyper-V|VirtualMachinePlatform|Microsoft-Windows-Subsystem-Linux"} |
    Select-Object FeatureName, State
```

returned:

```text
FeatureName                                State
-----------                                -----
VirtualMachinePlatform                     Disabled
Microsoft-Windows-Subsystem-Linux          Disabled
Microsoft-Hyper-V-All                      Disabled
Microsoft-Hyper-V                          Disabled
Microsoft-Hyper-V-Tools-All                Disabled
Microsoft-Hyper-V-Management-PowerShell    Disabled
Microsoft-Hyper-V-Hypervisor               Disabled
Microsoft-Hyper-V-Services                 Disabled
Microsoft-Hyper-V-Management-Clients       Disabled
```

Therefore:

```text
Hyper-V role:             Disabled
Virtual Machine Platform: Disabled
WSL:                      Disabled / not installed
```

---

## Why Windows nevertheless reports that a hypervisor is already present

This command:

```powershell
systeminfo | findstr /I "hypervisor"
```

returned:

```text
Hypervisor enforced Code Integrity
Hypervisor enforced Code Integrity
Hyper-V Requirements:
A hypervisor has been detected. Features required for Hyper-V will not be displayed.
```

And:

```powershell
Get-CimInstance Win32_ComputerSystem |
    Select-Object HypervisorPresent
```

returned:

```text
HypervisorPresent
-----------------
True
```

This does **not** mean the Hyper-V role is enabled.

Windows is already using the hypervisor infrastructure for virtualization-based security.

---

## Existing security virtualization

`systeminfo` reports:

```text
Virtualization-based security: Status: Running

Services Configured:
    Hypervisor enforced Code Integrity

Services Running:
    Hypervisor enforced Code Integrity
```

The registry check:

```powershell
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" -Name Enabled -ErrorAction SilentlyContinue
```

returned:

```text
Enabled : 1
```

Therefore:

> HVCI / Memory Integrity is enabled.

This explains why `HypervisorPresent` is `True` even though the Hyper-V Windows feature is disabled.

**Do not disable HVCI/Memory Integrity merely to install WSL 2, Docker, or DataHub.**

---

## WSL 2 vs Hyper-V decision

Both are technically capable of supporting the intended Docker/DataHub workload.

The current direction is:

> **Use WSL 2 as the Docker Desktop backend.**

Reasons:

- WSL 2 is Docker Desktop's current/default Windows path.
- It integrates well with Linux containers.
- It does not require moving Python/database development into WSL.
- It leaves Linux tooling available later if useful.
- It fits the planned future Docker-based agentic-AI work.

Hyper-V remains a technically valid alternative. The choice is not driven by DataHub functionality.

---

## RAM status

The machine currently has approximately 16 GB RAM.

Task Manager reports:

```text
Slots used: 1 of 2
```

PowerShell reports one module:

```text
Capacity:             16 GB
Speed:                3200
Configured speed:     3200
SMBIOSMemoryType:     26  (DDR4)
FormFactor:           12  (SODIMM)
DeviceLocator:        DIMM 1
PartNumber:           8ATF2G64HZ-3G2E2
```

Therefore:

```text
DIMM 1: 16 GB DDR4-3200 SODIMM
DIMM 2: EMPTY

TOTAL: 16 GB
```

The possibility of upgrading to 32 GB is being considered separately.

See:

`datahub_ram_upgrade_analysis.md`

---

## Why RAM matters

The planned workload may combine:

```text
Windows
+ browser
+ IDE
+ Python
+ databases
+ Docker
+ DataHub
+ Kafka
+ search/indexing
+ future agentic-AI containers
```

The earlier `systeminfo` measurement showed:

```text
Total Physical Memory:      16,123 MB
Available Physical Memory:   5,968 MB
Virtual Memory In Use:      13,728 MB
```

Therefore memory headroom may become important.

The preferred target is:

```text
16 GB → 32 GB
```

but the upgrade does not have to happen before testing DataHub.

---

## Remote DataHub — later option

There is no immediate requirement for DataHub to run continuously.

The current approach is:

```text
Local DataHub
      ↓
Learn and experiment
      ↓
Use DataHub only when needed
      ↓
If demonstration / persistent access / performance
becomes important:
      ↓
Move DataHub to a remote Docker server
```

A remote server could eventually provide more CPU/RAM and allow demonstrations without depending on the laptop's resources.

This is a later architectural option, not part of the initial installation.

---

## Clean rollback principle

The setup will be performed one change at a time:

```text
Inspect
  ↓
Make ONE change
  ↓
Verify
  ↓
Record state
  ↓
Proceed
```

Current baseline:

```text
Windows 11 Pro             Existing
HVCI / Memory Integrity    Existing + enabled
Hyper-V role               Disabled
Virtual Machine Platform   Disabled
WSL                        Not installed
Docker Desktop             Not installed
DataHub                    Not installed
RAM                        16 GB
```

No Docker, WSL, or DataHub installation has yet been performed.

The existing HVCI/security configuration should remain untouched.

---

## Next step

Before installing WSL 2 or Docker, the RAM purchase decision is being evaluated.

If the RAM upgrade is deferred, the next setup sequence will be:

```text
1. Install / enable WSL 2
2. Verify WSL 2
3. Install Docker Desktop
4. Verify Docker using WSL 2 backend
5. Run DataHub
6. Verify DataHub
```

Each step should be performed and verified independently.

The existing HVCI/security configuration should remain untouched.

---

# Current status summary

```text
Windows 11 Pro             ✓
x64                         ✓
HVCI / Memory Integrity     ✓ Running
Hyper-V feature             ✗ Disabled
Virtual Machine Platform    ✗ Disabled
WSL                         ✗ Not installed
Docker Desktop              ✗ Not installed
DataHub                     ✗ Not installed
RAM                         16 GB
RAM slots                   1 of 2 used

INTENDED ARCHITECTURE

Windows
  │
  └── Docker Desktop
        │
        └── WSL 2
              │
              ├── DataHub
              └── Future containerized services

Python / databases / IDE remain on Windows.
```
