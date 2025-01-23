# Check if the script is running with administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    # Relaunch the script with administrator privileges
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Add the new directory to the PATH
$newpath = $env:Path + ";C:\Users\DELL\Desktop\python cli+gui\pyhurtsmyarm\"
[Environment]::SetEnvironmentVariable("PATH", $newpath, [EnvironmentVariableTarget]::Machine)

# Verify the change
$newpath = $env:Path
Write-Output "New PATH: $newpath"
