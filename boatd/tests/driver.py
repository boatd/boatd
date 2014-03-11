import boatd
driver = boatd.Driver()

driver.some_hardware = {}

@driver.heading
def heading():
    return 2.43

@driver.rudder
def move_rudder(angle):
    driver.some_hardware['rudder'] = angle

@driver.handler('pony')
def horse():
    return 'magic'
