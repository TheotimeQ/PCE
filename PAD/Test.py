# import serial

# ser = serial.Serial("COM4",timeout=1) //Le port utilisé est ici COM4
# print(ser)
# while 1:
#  code=input("Code à envoyer à l'Arduino: ")
#  ser.write(code.encode('utf-8'))

import serial
ser = serial.Serial("COM5",timeout=1)
print (ser)

# while 1:
#     donnee=str(ser.readline())
#     print(donnee)

while 1:
  code=input("Code à envoyer à l'Arduino: ")
  ser.write(code.encode('utf-8'))