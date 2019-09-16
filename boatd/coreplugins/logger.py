# This file is part of boatd, the Robotic Sailing Boat Daemon.
#
# Copyright (C) 2013-2017 Louis Taylor <louis@kragniz.eu>
#
# boatd is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# boatd is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from boatd import BasePlugin

import datetime
import time


wrsc_log_format = (
             '{time}, '
             #'bhead={head} '
             #'wind={wind} '
             '{lat}, '
             '{long}, '
             '{depth:4.2f}, '
             #'nwlat={wpn} '
             #'nwlon={wpe} '
             #'nwn={num} '
             #'spos={sail} '
             #'rpos={rudder} '
             #'whead={waypoint_heading} '
             #'distance={waypoint_distance} '
             #'speed={speed} '
             '\n'
             )


sensible_log_format = (
             '{time}, '
             #'bhead={head} '
             #'wind={wind} '
             '{lat:2.7f}, '
             '{long:3.8f}, '
             '{depth:4.2f}, '
             #'nwlat={wpn} '
             #'nwlon={wpe} '
             #'nwn={num} '
             #'spos={sail} '
             #'rpos={rudder} '
             #'whead={waypoint_heading} '
             #'distance={waypoint_distance} '
             #'speed={speed} '
             '\n'
             )


class LoggerPlugin(BasePlugin):
    def main(self):
        period = self.config.period

        #filename for WRSC style logs
        filename_wrsc = self.config.filename + time.strftime("_%Y-%m-%d_%H%M%SZ_wrsc.csv")

        #filename for sensibly formatted logs with decimal lat/lon
        filename = self.config.filename + time.strftime("_%Y-%m-%d_%H%M%SZ.csv")

        with open(filename, 'a') as f:
            f.write("time,lat,lon,depth\n")

        while self.running:
            heading = self.boatd.boat.heading()
            wind_direction = self.boatd.boat.wind_absolute()
            lat, lon = self.boatd.boat.position()
            depth = self.boatd.boat.depth()

            ts = time.time()

            log_line = wrsc_log_format.format(
                    time=time.strftime("%H%M%S%d"),
                    #head=heading,
                    #wind=wind_direction,
                    lat=str(lat*(10**7)).split(".",1)[0],
                    long=str(lon*(10**7)).split(".",1)[0],
                    depth=depth,
            )

            with open(filename_wrsc, 'a') as f:
                f.write(log_line)


            log_line = sensible_log_format.format(
                    time=time.strftime("%H%M%S%d"),
                    #head=heading,
                    #wind=wind_direction,
                    lat=lat,
                    long=lon,
                    depth=depth,
            )

            with open(filename, 'a') as f:
                f.write(log_line)

            time.sleep(period)

plugin = LoggerPlugin
