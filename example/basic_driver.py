import boatd

some_hardware = object()

@boatd.do_hardware
def do_hardware(amount):
    some_hardware.something = amount
    return amount
