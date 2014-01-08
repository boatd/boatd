some_hardware = {}

@boatd.do_something
def do_hardware(amount):
    some_hardware['something'] = amount
    return amount

print(do_hardware(4))
