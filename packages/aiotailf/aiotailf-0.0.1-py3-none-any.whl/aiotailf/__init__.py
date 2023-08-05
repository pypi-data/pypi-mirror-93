import asyncio
import io
import os
import time
from typing import AsyncIterator

import aiofiles

LINE_BUFFER = 1


async def async_tail(
    filename: str,
    last_lines: int = 10,
    non_exist_max_secs: float = 30.0,
    fp_poll_secs: float = 0.125,
) -> AsyncIterator[str]:
    async def wait_exists() -> bool:
        bail_at: float = time.monotonic() + non_exist_max_secs
        while not os.path.exists(filename):
            if time.monotonic() >= bail_at:
                return False
            await asyncio.sleep(fp_poll_secs)
        return True

    async def check_rotate(_fp) -> io.TextIOBase:
        nonlocal fino
        if os.stat(filename).st_ino != fino:
            new_fp = await aiofiles.open(filename, "r")
            await _fp.close()
            await new_fp.seek(0, os.SEEK_SET)
            fino = os.fstat(new_fp.fileno()).st_ino
            return new_fp
        return _fp

    if not await wait_exists():
        return

    stat = os.stat(filename)

    fino: int = stat.st_ino
    size: int = stat.st_size
    blocksize: int = os.statvfs(filename).f_bsize

    fp = await aiofiles.open(filename, "r", LINE_BUFFER)

    if last_lines > 0:
        if stat.st_size <= blocksize:
            for line in (await fp.readlines())[-last_lines::]:
                yield line.rstrip()
        else:
            await fp.seek(os.stat(fp.fileno()).st_size - blocksize)
            for line in (await fp.readlines())[1:-1][-last_lines::]:
                yield line.rstrip()

    await fp.seek(0, os.SEEK_END)

    try:
        while True:
            if not os.path.exists(filename):
                if not await wait_exists():
                    return

            fp = await check_rotate(fp)
            n_stat = os.fstat(fp.fileno())
            n_size = n_stat.st_size

            if n_size == size:
                await asyncio.sleep(fp_poll_secs)
                continue

            if n_size < size:
                await fp.seek(0, os.SEEK_SET)

            size = n_size
            while True:
                chunk = await fp.read(blocksize)
                if chunk == "":
                    break
                yield chunk.rstrip()

    except IOError:
        await fp.close()


__version__ = "0.0.1"
__author__ = "nocilantro"
