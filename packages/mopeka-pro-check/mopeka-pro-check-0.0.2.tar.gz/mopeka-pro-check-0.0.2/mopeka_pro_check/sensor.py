"""Module that represents a Mopeka Pro Check sensor.

Sensors can hold multiple readings (advertisements) but the
sensor provides access to the latest information.

Copyright (c) 2021 Sean Brogan

SPDX-License-Identifier: MIT

"""
import logging
from enum import Enum
from collections import deque

from bleson import BDAddress

from .advertisement import MopekaAdvertisement

_LOGGER = logging.getLogger(__name__)

class MopekaSensor(object):
  """ Sensor Object """

  packet_list: deque
  _mac: str
  _bdaddress: BDAddress

  def __init__(self, mac_address:str ):
    self._mac = mac_address
    self._bdaddress = BDAddress(mac_address)
    self.packet_list = deque(maxlen=3)  #use deque so we get only the most recent

  def AddReading(self, reading_data: MopekaAdvertisement):
    self.packet_list.append(reading_data)

  def __str__(self) -> str:
    return "{MopekaSensor - MAC ADDRESS: " + str(self._mac) + " Advertisements: " + str(len(self.packet_list)) + "}"

  def Clear(self):
    """ clear the saved advertisement list """
    self.packet_list.clear()

  def Dump(self):
    print(f"MopekaSensor:")
    print(f"  - MAC: {self._mac}")
    print(f"  - Advertisements ({len(self.packet_list)})")
    for ad in self.packet_list:
      ad.Dump()
    print()