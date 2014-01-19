some_hardware = {}

@boatd.do_something
def do_hardware(amount):
    some_hardware['something'] = amount
    return amount * 2

@boatd.heading
def heading():
    return 2.43
