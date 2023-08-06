# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

#
# SimplyPrint
# Copyright (C) 2020-2021  SimplyPrint ApS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
This file checks for updates for OctoPrint and all OctoPrint plugins, and lets SimplyPrint know if there are any
"""
import json
from base import octoprint_api_req, log, website_ping_update, url_quote


def run_check():
    # Important 'True' last!
    check = octoprint_api_req("plugin/softwareupdate/check", None, False, None, False, False, True)
    has_updates = False
    available_updates = []

    if check is not None:
        if "information" in check:
            for plugin in check["information"]:
                if "updateAvailable" in check["information"][plugin]:
                    if check["information"][plugin]["updateAvailable"]:
                        has_updates = True
                        release_notes = check["information"][plugin]["releaseNotes"]
                        new_version = check["information"][plugin]["information"]["remote"]["name"]

                        available_updates.append({
                            "plugin": plugin,
                            "version": new_version,
                            "release_notes": release_notes
                        })

    if has_updates:
        # Tell server!
        log("OctoPrint or plugin(s) has an update available!")
        website_ping_update("&updates_available=" + url_quote(json.dumps(available_updates)))
