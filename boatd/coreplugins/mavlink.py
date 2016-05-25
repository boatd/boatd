import serial
import time

from boatd import BasePlugin
import boatd.coreplugins.mavlink_common as mv


class MavlinkPlugin(BasePlugin):

    def send_heartbeat(self):
        self.ml.heartbeat_send(
            mv.MAV_TYPE_SURFACE_BOAT,
            mv.MAV_AUTOPILOT_GENERIC,
            mv.MAV_MODE_FLAG_GUIDED_ENABLED,
            0,
            mv.MAV_STATE_ACTIVE,
            3
        )

    def send_position(self):
        self.ml.global_position_int_send(
            int(time.time()),
            int(52.41389 * 1e7),
            int(-4.09098 * 1e7),
            25000,
            25000,
            1,1,1,180)

        self.ml.gps_raw_int_send(
            int(time.time()*100),
            3,
            int(52.41389 * 1e7),
            int(-4.09098 * 1e7),
            25000,
            0xFFFF,
            0xFFFF,
            0xFFFF,
            0xFFFF,
            5
        )

    def main(self):
        #period = self.config.period
        #filename = self.config.filename

        # FIXME: make serial port name and baud rate configurable
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
        self.ml = mv.MAVLink(self.ser)

        while self.running:
            self.send_heartbeat()
            self.send_position()

            lat, lon = self.boatd.boat.position()

            buf = self.ser.read(18)
            messages = self.ml.parse_buffer(buf)
            if messages:
                for message in messages:
                    name = message.get_type()
                    print(name)

            time.sleep(0.01) 


plugin = MavlinkPlugin
