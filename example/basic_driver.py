from boatd import Driver
driver = Driver()

some_hardware = {}

@driver.heading
def heading():
    return 2.43

@driver.wind_direction
def get_wind():
    return 8.42

@driver.wind_speed
def get_wind_speed():
    return 25

@driver.position
def position():
    return (2.343443, None)

@driver.rudder
def rudder(theta):
    return theta

@driver.sail
def sail(theta):
    return theta
