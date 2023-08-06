import asyncio
import os
import select
import time
from typing import AsyncIterator, Iterator, IO


class PipeStream:
    def __init__(self, stream: IO[bytes]):
        self.stream = stream

    def _iter_lines(self):
        for line in self.stream:
            yield line.decode()

    def _iter_lines_with_timeout(self, with_timeout: float):
        """
        Obtain a generator that reads the pipe's output line-by-line

        :param with_timeout:            the time (in seconds) to wait before bailing out

        :raise                          TimeoutError
        """
        buf = b""
        timeout_limit = time.monotonic() + with_timeout
        did_timeout = time.monotonic() > timeout_limit
        while not did_timeout:
            read_ready, *_ = select.select([self.stream.fileno()], [], [], 0.5)
            if read_ready:
                data = os.read(self.stream.fileno(), 4096)
                if not data:
                    break
                buf += data
                newline = buf.find(b"\n")
                while newline != -1:
                    line = buf[:newline]
                    buf = buf[newline + 1:]
                    yield line.decode()
                    newline = buf.find(b"\n")
            did_timeout = time.monotonic() > timeout_limit
        if buf:
            yield buf.decode()
        if did_timeout:
            raise TimeoutError

    def iter_lines(self, with_timeout: float = None) -> Iterator[str]:
        """
        Obtain a generator that reads the pipe's output line-by-line

        :param with_timeout:            the time (in seconds) to wait before bailing out

        :raise                          TimeoutError
        """
        if with_timeout is None:
            return self._iter_lines()
        return self._iter_lines_with_timeout(with_timeout)


class AsyncPipeStream:
    def __init__(self, stream: asyncio.StreamReader):
        self.stream = stream

    async def _iter_lines(self):
        while True:
            line = await self.stream.readline()
            if not line:
                break
            yield line.decode()

    async def _iter_lines_with_timeout(self, with_timeout: float):
        end_time = time.monotonic() + with_timeout
        while True:
            rem_time = end_time - time.monotonic()
            if rem_time <= 0:
                raise asyncio.TimeoutError
            line = await asyncio.wait_for(self.stream.readline(), rem_time)
            if not line:
                break
            yield line.decode()

    def iter_lines(self, with_timeout: float = None) -> AsyncIterator[str]:
        """
        Obtain a generator that reads the pipe's output line-by-line

        :param with_timeout:            the time (in seconds) to wait before bailing out

        :raise                          asyncio.TimeoutError
        """

        if with_timeout is None:
            return self._iter_lines()
        return self._iter_lines_with_timeout(with_timeout)
