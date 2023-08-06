#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie EveLoop Team, all rights reserved

APPLICATION_VERSION = "0.1"
APPLICATION_AUTHORS = ["Tuxa", "Mo"]
APPLICATION_NAME = "Galaxie EveLoop"
APPLICATION_COPYRIGHT = "2016-2021 - Galaxie EveLoop Team all right reserved"
__all__ = [
    "EventList",
    "EventBus",
    "MainLoop",
]
from glxeveloop.event_list import EventList
from glxeveloop.event_bus import EventBus
from glxeveloop.main_loop import MainLoop
