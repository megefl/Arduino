import serial
import sys
import time
from serial.serialutil import SerialException

serialPort = serial.Serial()
serialPort.baudrate = 1000000
serialPort.port = '/dev/cu.usbmodem34B7DA657B442'
serialPort.parity = serial.PARITY_NONE
serialPort.stopbits = serial.STOPBITS_ONE
serialPort.bytesize = serial.EIGHTBITS
serialPort.timeout = 0.1  # ← TIMEOUT 100ms (CRUCIAL !)

try:
    serialPort.open()
except SerialException as serialException:
    print(serialException)
    sys.exit()

if not serialPort.isOpen():
    print('Serial port not opened')
    sys.exit()

try:
    print('Serial port opened. Write run character.')
    cmd = "r"
    serialPort.write(cmd.encode(encoding="ascii"))
    
    startTime = time.time()
    endTime = startTime
    
    # Durée d'acquisition : 10 secondes
    while (endTime - startTime < 10):
        if serialPort.in_waiting:  # Données disponibles
            line = serialPort.readline().decode('utf-8').strip()
            print(f"Temps écoulé: {line} s")
        
        endTime = time.time()
    
    print("Envoi du signal de redémarrage...")
    cmd = "s"
    serialPort.write(cmd.encode(encoding="ascii"))
    serialPort.close()
    print('Port closed')
    
except Exception as exception:
    print('Exception occurred')
    print(exception)
    serialPort.close()
    print('Port closed')


