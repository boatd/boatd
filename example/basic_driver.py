some_hardware = {}

@boatd.do_something
def do_hardware(amount):
    some_hardware['something'] = amount
    return amount * 2

@boatd.heading
def heading():
    return 2.43

@boatd.wind
def get_wind():
    return 0.42
