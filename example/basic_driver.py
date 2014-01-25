some_hardware = {}

@boatd.heading
def heading():
    return 2.43

@boatd.wind
def get_wind():
    return 8.42

@boatd.position
def position():
    return (2.343443, None)

@boatd.rudder
def rudder(theta):
    return theta

@boatd.sail
def sail(theta):
    return theta
