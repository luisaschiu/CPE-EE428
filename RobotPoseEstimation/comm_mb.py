import bluetooth

microbit_address = "D6:AC:8A:B9:DB:70" 
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((microbit_address, 1)) # channel 1 (should be default)
while True:
    command = "mf#\n" # the # is for the delimiter in makecode bluetooth stuff
    sock.send(command)
    sleep(1)

sock.close()
