# "0013 fff5 0022 002d 00 0000 0000 0000 0000 00 0003 fff3 000d 002c 0000 0000 0000 0000 00 0d0a"
# "A    B    C    D    E  A1   B1   C1   D1   E1 F    G    H    I    F1   G1   H1   I1   J"

bytelist = '0013fff50022002d000000000000000000000003fff3000d002c000000000000000000'

print('A:', bytelist[0:4])
print('B:', bytelist[4:8])
print('C:', bytelist[8:12])
print('D:', bytelist[12:16])
print('E:', bytelist[16:18])
print('A1:', bytelist[18:22])
print('B1:', bytelist[22:26])
print('C1:', bytelist[26:30])
print('D1:', bytelist[30:34])
print('E1:', bytelist[34:36])
print('J:', bytelist[-2:])
