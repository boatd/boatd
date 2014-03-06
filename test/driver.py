import boatd
driver = boatd.Driver()

some_hardware = {}

@driver.heading
def heading():
    return 2.43

@driver.handler('pony')
def something():
    return 'magic'
