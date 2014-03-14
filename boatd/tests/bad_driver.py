import boatd
driver = boatd.Driver()

driver.some_hardware = {}

@driver.heading
def heading():
    some invalid syntax
    return 2.43
