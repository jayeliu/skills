#!/usr/bin/env python3
"""
System Information Script
Retrieves OS and shell information using only Python standard library.
Supports Windows, Linux, and macOS (Darwin).
"""

import os
import platform
import subprocess


def get_os_info():
    """Get operating system information."""
    info = {}

    system = platform.system()
    info["system"] = system
    info["node"] = platform.node()
    info["release"] = platform.release()
    info["machine"] = platform.machine()
    info["version"] = platform.version()

    if system == "Darwin":
        # macOS - use sw_vers
        try:
            result = subprocess.run(
                ["sw_vers"], capture_output=True, text=True, timeout=5, shell=False
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key_lower = key.strip().lower().replace(" ", "_")
                        info[key_lower] = value.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError, PermissionError):
            pass

    elif system == "Linux":
        # Linux - read /etc/os-release
        try:
            result = subprocess.run(
                ["cat", "/etc/os-release"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False,
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        if key in (
                            "NAME",
                            "VERSION",
                            "VERSION_ID",
                            "ID",
                            "PRETTY_NAME",
                        ):
                            info[key.lower()] = value.strip('"').strip("'")
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError, PermissionError):
            pass

        # Fallback: try lsb_release
        if "name" not in info:
            try:
                result = subprocess.run(
                    ["lsb_release", "-a"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    shell=False,
                )
                if result.returncode == 0:
                    for line in result.stdout.strip().split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key_lower = key.strip().lower()
                            if key_lower in (
                                "distributor id",
                                "description",
                                "release",
                            ):
                                info[key_lower.replace(" ", "_")] = value.strip()
            except (
                subprocess.TimeoutExpired,
                FileNotFoundError,
                OSError,
                PermissionError,
            ):
                pass

    elif system == "Windows":
        # Windows - use platform module
        win_ver = platform.win32_ver()
        info["win_name"] = win_ver[0]  # e.g., '10'
        info["win_version"] = win_ver[1]  # e.g., '10.0.19041'
        info["win_sp"] = win_ver[2]  # service pack
        info["win_type"] = win_ver[3]  # e.g., 'Multiprocessor Free'

        # Try to get more detailed Windows info
        try:
            result = subprocess.run(
                ["cmd", "/c", "ver"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False,
            )
            if result.returncode == 0:
                info["win_ver_output"] = result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError, PermissionError):
            pass

    return info


def get_shell_info():
    """Get shell information for Windows, Linux, and macOS."""
    info = {}

    system = platform.system()

    if system == "Windows":
        # Windows shell detection
        # Check for PowerShell
        if "PSModulePath" in os.environ:
            info["name"] = "powershell"
            # Try to get PowerShell version
            try:
                result = subprocess.run(
                    ["powershell", "-Command", "$PSVersionTable.PSVersion.ToString()"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    shell=False,
                )
                if result.returncode == 0:
                    info["version"] = result.stdout.strip()
            except (
                subprocess.TimeoutExpired,
                FileNotFoundError,
                OSError,
                PermissionError,
            ):
                pass
            info["path"] = "powershell"
        else:
            # Command Prompt (cmd)
            info["name"] = "cmd"
            try:
                result = subprocess.run(
                    ["cmd", "/c", "echo %COMSPEC%"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    shell=False,
                )
                if result.returncode == 0:
                    info["path"] = result.stdout.strip()
            except (
                subprocess.TimeoutExpired,
                FileNotFoundError,
                OSError,
                PermissionError,
            ):
                info["path"] = os.environ.get("COMSPEC", "cmd.exe")

        # Check if running in specific terminal
        info["terminal"] = os.environ.get("WT_SESSION", "") or os.environ.get(
            "TERM_PROGRAM", ""
        )

    else:
        # Unix-like systems (Linux, macOS/Darwin)
        shell_path = os.environ.get("SHELL", "")
        info["path"] = shell_path if shell_path else "Unknown"

        # Detect shell from environment variables
        if "ZSH_VERSION" in os.environ:
            info["name"] = "zsh"
            info["version"] = os.environ.get("ZSH_VERSION", "")
        elif "BASH_VERSION" in os.environ:
            info["name"] = "bash"
            info["version"] = os.environ.get("BASH_VERSION", "")
        elif "FISH_VERSION" in os.environ:
            info["name"] = "fish"
            info["version"] = os.environ.get("FISH_VERSION", "")
        elif shell_path:
            info["name"] = os.path.basename(shell_path)
        else:
            info["name"] = "Unknown"

        # Get shell version if not already detected
        if not info.get("version") and shell_path and shell_path != "Unknown":
            try:
                result = subprocess.run(
                    [shell_path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    shell=False,
                )
                if result.returncode == 0 and result.stdout:
                    info["version"] = result.stdout.strip().split("\n")[0]
                elif result.stderr:
                    # Some shells output version to stderr
                    info["version"] = result.stderr.strip().split("\n")[0]
            except (
                subprocess.TimeoutExpired,
                FileNotFoundError,
                OSError,
                PermissionError,
            ):
                pass

    return info


def print_report():
    """Print formatted system information report."""
    os_info = get_os_info()
    shell_info = get_shell_info()
    system = os_info.get("system", "Unknown")

    print("=" * 50)
    print("SYSTEM INFORMATION")
    print("=" * 50)

    # OS Section
    print("\n## Operating System")
    print(f"  Platform:     {system}")
    print(f"  Hostname:     {os_info.get('node', 'Unknown')}")
    print(f"  Release:      {os_info.get('release', 'Unknown')}")
    print(f"  Architecture: {os_info.get('machine', 'Unknown')}")

    if system == "Darwin":
        print(f"  Name:         {os_info.get('productname', 'macOS')}")
        print(f"  Version:      {os_info.get('productversion', 'Unknown')}")
        if os_info.get("buildversion"):
            print(f"  Build:        {os_info.get('buildversion', '')}")

    elif system == "Linux":
        if os_info.get("pretty_name"):
            print(f"  Distribution: {os_info.get('pretty_name', '')}")
        elif os_info.get("name"):
            print(f"  Distribution: {os_info.get('name', '')}")
        if os_info.get("version"):
            print(f"  Version:      {os_info.get('version', '')}")
        elif os_info.get("version_id"):
            print(f"  Version:      {os_info.get('version_id', '')}")

    elif system == "Windows":
        print(f"  Name:         Windows {os_info.get('win_name', '')}")
        print(f"  Version:      {os_info.get('win_version', '')}")
        if os_info.get("win_sp"):
            print(f"  SP:           {os_info.get('win_sp', '')}")

    # Shell Section
    print("\n## Shell")
    print(f"  Name:    {shell_info.get('name', 'Unknown')}")
    print(f"  Path:    {shell_info.get('path', 'Unknown')}")
    if shell_info.get("version"):
        print(f"  Version: {shell_info.get('version', '')}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    print_report()
