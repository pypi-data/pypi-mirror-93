#https://bitstring.readthedocs.io/en/latest/constbitarray.html#bitstring.Bits
from bitstring import BitArray

adresse = BitArray(length=11)

adresse += 1

print(str(adresse))