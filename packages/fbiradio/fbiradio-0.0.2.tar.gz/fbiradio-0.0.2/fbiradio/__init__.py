#!/usr/bin/env python
"""fbiradio

Show the currently playing track on FBi Radio."""

# fbiradio - Show the currently playing track on FBi Radio

# Copyright 2021, Christian Christiansen

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__author__ = "Christian Christiansen"
__copyright__ = "Copyright 2021, Christian Christiansen"
__license__ = "AGPL-3.0"
__version__ = "0.0.1"
__maintainer__ = "Christian Christiansen"
__email__ = "christian dot l dot christiansen at gmail dot com"
__status__ = "Development"

import requests
import re
import argparse

from bs4 import BeautifulSoup

def currently_playing(n=1):
    """Return the latest n tracks played on FBi Radio.'

    n: integer greater or equal to 1. n=0 returns all tracks in show.
    Default: return last track played."""

    class Track():
        def __init__(self, artist = None, track = None, played_at = None,
                     flags = None):
            self.artist = artist
            self.track = track
            self.played_at = played_at
            self.flags = flags.strip()

        def __is_flag(self, flag):
            if self.flags == flag:
                return True
            else:
                return False

        def is_NSW(self):
            return self.__is_flag("NSW")

        def is_Aus(self):
            return self.__is_flag("Aus")

        def __str__(self):
            if self.artist and self.track and self.played_at:
                output = f"{self.played_at}: {self.artist} - {self.track}"
            elif self.artist and self.track:
                output = f"          {self.artist} - {self.track}"

            if self.is_NSW():
                output += " (NSW)"
            if self.is_Aus():
                output += " (Aus)"

            return output

    r = requests.get("https://airnet.org.au/guide/grid.php?view=1118").text
    soup = BeautifulSoup(r, "html.parser")
    show_link = soup.find("td", {"class": "currentlyRunning"}).a.get('href')
    url = ("https://airnet.org.au/widget/widget.php?widget=444&url="+
        show_link.replace(":","%3A").replace("/","%2F"))
    r = requests.get(url).text
    soup = BeautifulSoup(r, "html.parser")
    tracks_raw = (
        soup.find_all(
            "div", attrs={"class": re.compile(r"has-info track.*")}))

    tracks = [
        Track(
            artist = track.find("h4", {"class": "trackArtist"}).text,
            track = track.find("h6", {"class": "trackName"}).text,
            played_at = track.find("div", {"class": "jumpToTrack_time"}).text,
            flags = track.find("div", {"class": "track-flags"}).text,
        ) for track in tracks_raw]

    return tracks[-min(len(tracks), int(abs(n))):]
