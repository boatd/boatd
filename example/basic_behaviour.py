import time

for i in range(5):
    boat.heading()
    boat.get_wind()
    boat.position()
    boat.rudder(0)
    boat.rudder(-1)
    boat.rudder(3)

    boat.sail(0)
