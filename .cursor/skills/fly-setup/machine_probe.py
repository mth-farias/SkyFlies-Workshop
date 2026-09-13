#!/usr/bin/env python3
"""Host occupancy probe. JSON on stdout; one-line human summary on stderr.

Never opens credential files. TCP-only check for 127.0.0.1:9292 (no generate).
"""

from __future__ import annotations

import ctypes
import json
import os
import shutil
import socket
import subprocess
import sys
from typing import Any

NVIDIA_TIMEOUT_S = 2.0
TCP_TIMEOUT_S = 0.5
PORT_9292 = 9292
BUSY_UTIL_PCT = 15
NVIDIA_QUERY = [
    "--query-gpu=name,memory.total,utilization.gpu",
    "--format=csv,noheader,nounits",
]


def cpu_logical() -> int:
    return os.cpu_count() or 0


def ram_gb() -> float:
    if os.name == "nt":
        class MemoryStatusEx(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MemoryStatusEx()
        status.dwLength = ctypes.sizeof(MemoryStatusEx)
        ok = ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
        if ok:
            return round(status.ullTotalPhys / (1024 ** 3), 1)
        return 0.0
    try:
        with open("/proc/meminfo", encoding="ascii") as fh:
            for line in fh:
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    return round(kb / (1024 ** 2), 1)
    except OSError:
        pass
    return 0.0


def parse_nvidia_smi_csv(text: str) -> list[dict[str, Any]]:
    gpus: list[dict[str, Any]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 3:
            continue
        try:
            vram_mb = int(float(parts[1]))
        except ValueError:
            vram_mb = 0
        try:
            util_pct = int(float(parts[2]))
        except ValueError:
            continue
        gpus.append({"name": parts[0], "vram_mb": vram_mb, "util_pct": util_pct})
    return gpus


def run_nvidia_smi() -> list[dict[str, Any]] | None:
    exe = shutil.which("nvidia-smi")
    if not exe:
        return None
    try:
        proc = subprocess.run(
            [exe, *NVIDIA_QUERY],
            capture_output=True,
            text=True,
            timeout=NVIDIA_TIMEOUT_S,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return parse_nvidia_smi_csv(proc.stdout or "")


def probe_tcp(host: str, port: int, timeout: float = TCP_TIMEOUT_S) -> str:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "up"
    except TimeoutError:
        return "down"
    except OSError:
        return "down"
    except Exception:
        return "unknown"


def hint_from_gpus(gpus: list[dict[str, Any]] | None) -> str:
    if gpus is None:
        return "unknown"
    for gpu in gpus:
        util = gpu.get("util_pct")
        if isinstance(util, (int, float)) and util >= BUSY_UTIL_PCT:
            return "gpu_busy"
    return "gpu_free"


def collect() -> dict[str, Any]:
    gpus_or_none = run_nvidia_smi()
    gpus = gpus_or_none if gpus_or_none is not None else []
    return {
        "cpu_logical": cpu_logical(),
        "ram_gb": ram_gb(),
        "gpus": gpus,
        "port_9292": probe_tcp("127.0.0.1", PORT_9292),
        "hint": hint_from_gpus(gpus_or_none),
    }


def main() -> int:
    payload = collect()
    json.dump(payload, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    sys.stderr.write(
        "probe cpu={cpu} ram_gb={ram} gpus={n} port_9292={port} hint={hint}\n".format(
            cpu=payload["cpu_logical"],
            ram=payload["ram_gb"],
            n=len(payload["gpus"]),
            port=payload["port_9292"],
            hint=payload["hint"],
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
