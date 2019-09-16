from boatd import BasePlugin

import datetime
import time

gpx_trkpt_format = (
             '\t\t\t<trkpt '
             'lat="{lat:2.5f}" '
             'lon="{long:3.5f}">'
             
             '<time>{datetime}</time>'
             
             '<cmt>Rudder:{rudder:2.0f} Sail:{sail:2.0f} Wind:{wind_direction:2.0f} Heading:{heading:2.0f} Roll:{roll:2.0f} Pitch:{pitch:2.0f} Depth:{depth:4.2f}</cmt>'
             
             '</trkpt>'
             '\n'
             )
             
gpx_wpt_format = (
             '\t\t<wpt '
             'lat="{lat}" '
             'lon="{long}">'
             '</wpt>'
             '\n'
             )

class GPXLoggerPlugin(BasePlugin):
    def main(self):
        self.period = self.config.period
        self.filename = self.config.filename + time.strftime("_%Y-%m-%d_%H%M%SZ.gpx")
        
        self.startfile()
        
        self.trackpoints()
        
        self.waypoints()
            
        self.endfile()
            
    def startfile(self):
        
        with open(self.filename, 'a') as f:
                f.write('<?xml version="1.0"?> \n'
    '<gpx creator="boatd" xmlns="http://www.topografix.com/GPX/1/1"'
    ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation='
    '"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n')
                f.write("\t<name>Boatd Output Track</name>\n")
                
    def trackpoints(self):
        with open(self.filename, 'a') as f:
            f.write("\t<trk>\n\t\t<trkseg> \n")
        
            while self.running:
                boat_heading = self.boatd.boat.heading()
                boat_wind_direction = self.boatd.boat.wind_absolute()
                boat_lat, boat_lon = self.boatd.boat.position()
                boat_sail = self.boatd.boat.target_sail_angle
                boat_rudder = self.boatd.boat.target_rudder_angle
                boat_roll = self.boatd.boat.roll()
                boat_pitch = self.boatd.boat.pitch()
                boat_depth = self.boatd.boat.depth()
                boat_datetime = datetime.datetime.now().isoformat()

                log_line = gpx_trkpt_format.format(
                        lat=boat_lat,
                        long=boat_lon,
                        datetime=boat_datetime,
                        rudder=boat_rudder,
                        sail=boat_sail,
                        wind_direction=boat_wind_direction,
                        heading=boat_heading,
                        roll=boat_roll,
                        pitch=boat_pitch,
                        depth=boat_depth,
                )

                f.write(log_line)

                time.sleep(self.period)
            
            f.write("\t\t</trkseg>\n\t</trk>\n")
            
    def waypoints(self):
        with open(self.filename, 'a') as f:
            for mark in self.boatd.waypoint_manager.waypoints:
                mark_lat, mark_long = mark
            
                point_line = gpx_wpt_format.format(
                    lat=mark_lat,
                    long=mark_long,
                )
            
                f.write(point_line)
    
    def endfile(self):
        with open(self.filename, 'a') as f:
                f.write("</gpx>")

plugin = GPXLoggerPlugin
