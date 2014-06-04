def calculate_checksum(line):
    '''Return the NMEA checksum for a given line'''
    x = 0
    for c in line:
        x ^= ord(c)
    s = str(hex(x))[2:]
    return ('0' if len(s) < 2 else '') + s.upper()

def hdm(heading):
    '''Return a HDM nmea sentance from a given heading'''
    line = 'HDM,{0:.3g},M'.format(heading)
    checksum = calculate_checksum(line)
    return '$' + line + '*' + checksum
