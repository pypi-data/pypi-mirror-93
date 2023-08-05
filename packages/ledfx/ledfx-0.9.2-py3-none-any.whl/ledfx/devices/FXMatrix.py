import logging
import socket

import numpy as np
import voluptuous as vol

from ledfx.devices import Device
from ledfx.utils import resolve_destination

_LOGGER = logging.getLogger(__name__)


class FXMatrix(Device):
    """FXMatrix device support"""

    CONFIG_SCHEMA = vol.Schema(
        {
            vol.Required(
                "ip_address",
                description="Hostname or IP address of the device",
            ): str,
            vol.Required(
                "port", description="Port for the UDP device"
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535)),
            vol.Required(
                "width", description="Number of pixels width"
            ): vol.All(vol.Coerce(int), vol.Range(min=1)),
            vol.Required(
                "height", description="Number of pixels height"
            ): vol.All(vol.Coerce(int), vol.Range(min=1)),
            # vol.Required('pixel_count', description='Number of individual
            # pixels'): vol.All(vol.Coerce(int), vol.Range(min=1)),
        }
    )

    def activate(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._config["pixel_count"] = int(
            self._config["width"] * self._config["height"]
        )
        # check if ip/hostname resolves okay
        self.resolved_dest = resolve_destination(self._config["ip_address"])
        if not self.resolved_dest:
            _LOGGER.warning(
                f"Cannot resolve destination {self._config['ip_address']}, aborting device {self.name} activation. Make sure the IP/hostname is correct and device is online."
            )
            return

        super().activate()

    def deactivate(self):
        super().deactivate()
        self._sock = None

    @property
    def pixel_count(self):
        return int(self._config["width"] * self._config["height"])

    def flush(self, data):
        udpData = bytearray()
        byteData = data.astype(np.dtype("B"))
        # Append all of the pixel data
        udpData.extend(byteData.flatten().tobytes())

        self._sock.sendto(
            bytes(udpData),
            (self.resolved_dest, self._config["port"]),
        )
