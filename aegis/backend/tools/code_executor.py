from __future__ import annotations

import asyncio
import sys


class CodeExecutor:
    name = "code_executor"

    async def run_python(self, code: str, timeout: float = 3.0) -> dict[str, str | int]:
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-c",
            code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            process.kill()
            return {"returncode": 124, "stdout": "", "stderr": "Execution timed out"}

        return {
            "returncode": process.returncode or 0,
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
        }
