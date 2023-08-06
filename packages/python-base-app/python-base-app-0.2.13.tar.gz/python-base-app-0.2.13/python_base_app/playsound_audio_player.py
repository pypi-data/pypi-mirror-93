# -*- coding: utf-8 -*-

# Copyright (C) 2019  Marcus Rickert
#
# See https://github.com/marcus67/python_base_app
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from python_base_app import configuration
from python_base_app import base_audio_player

class PlaysoundAudioPlayer(base_audio_player.BaseAudioPlayer):


    def __init__(self):

        super().__init__()
        self._player = None

        try:
            import playsound
            self._play_command = playsound.playsound

        except:
            fmt = "Cannot load module 'playsound'"
            self._logger.error(fmt)
            raise configuration.ConfigurationException(fmt)

        self._logger.info("audio player 'playsound' loaded")


    def play_audio_file(self, p_audio_filename):  # pragma: no cover
        self._play_command(p_audio_filename)

