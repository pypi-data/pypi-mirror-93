"""
Module providing helpers to spawn an additional Docker daemon
"""

import asyncio
import os
import shutil
from subprocess import DEVNULL, Popen, run
import tempfile
from textwrap import dedent
from time import sleep
from typing import List

from .errors import DockerDaemonSetupError


class DockerDaemon:
    """
    Class managing a manually-started Docker daemon
    """

    def __init__(self):
        self.dockerd = None
        self.root_dir = tempfile.TemporaryDirectory(prefix="panza_").name
        self.network_brige_name = os.path.basename(self.root_dir).replace('_', '-')

    def launch(self, *, bridge_ip: str, dns: List[str] = None):
        """
        Launch the daemon

        :param bridge_ip:           the IP mask to use for the bridge
        :param dns:                 a list of servers IP addresses to use as DNS
        """
        dns = dns or []

        script = dedent(
            f"""
            set -e

            ip link add name {self.network_brige_name} type bridge
            ip addr add {bridge_ip} dev {self.network_brige_name}
            ip link set dev {self.network_brige_name} up
            """
        )
        result = run(["bash", "-c", script], capture_output=True)
        if result.returncode != 0:
            raise DockerDaemonSetupError(f"cannot configure a network bridge: {result.stderr.decode()}")
        command = dedent(
            f"""
            dockerd \
              --bridge={self.network_brige_name} \
              --data-root={self.root_dir}/data \
              --exec-root={self.root_dir}/exec \
              --host=unix://{self.root_dir}/docker.sock \
              --pidfile={self.root_dir}/docker.pid \
              {' '.join(f"--dns {ip}" for ip in dns)}
              """
        )
        self.dockerd = Popen(["bash", "-c", command], stdout=DEVNULL, stderr=DEVNULL)

    def is_ready(self) -> bool:
        return os.system(f"docker -H unix://{self.socket_path()} info >/dev/null 2>/dev/null") == 0

    READINESS_POLLING_DELAY = 0.5

    def wait_until_started(self, *, wait_for_seconds: float):
        """
        Wait until the daemon has finished starting

        :param wait_for_seconds:    the number of seconds to wait for
        """
        waited_for = 0
        while waited_for < wait_for_seconds:
            if self.is_ready():
                break
            sleep(self.READINESS_POLLING_DELAY)
            waited_for += self.READINESS_POLLING_DELAY
        else:
            raise DockerDaemonSetupError(f"timeout after waiting {waited_for} seconds for dockerd")

    async def wait_until_started_async(self, *, wait_for_seconds: float):
        waited_for = 0
        while waited_for < wait_for_seconds:
            if self.is_ready():
                break
            await asyncio.sleep(self.READINESS_POLLING_DELAY)
            waited_for += self.READINESS_POLLING_DELAY
        else:
            raise DockerDaemonSetupError(f"timeout after waiting {waited_for} seconds for dockerd")

    def stop(self):
        """
        Stop the daemon and cleanup the resources
        """
        if self.dockerd is not None:
            self.dockerd.terminate()
            self.dockerd.wait()
            shutil.rmtree(self.root_dir, ignore_errors=True)
            os.system(f"ip link set {self.network_brige_name} down")
            os.system(f"ip link delete {self.network_brige_name}")

    def socket_path(self) -> str:
        """
        Get the path to the Docker socket

        :return:                    the path to the Docker socket
        """
        return f"{self.root_dir}/docker.sock"
