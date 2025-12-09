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
serialPort.timeout = 0.1

try:
    serialPort.open()
except SerialException as serialException:
    print(serialException)
    sys.exit()

if not serialPort.isOpen():
    print('Serial port not opened')
    sys.exit()

try:
    cmd = "r"
    serialPort.write(cmd.encode(encoding="ascii"))
    serialPort.flush()
    
    startTime = time.time()
    endTime = startTime
    
    times = []
    distances = []
    
    while (endTime - startTime < 10):
        if serialPort.in_waiting:
            line = serialPort.readline().decode('utf-8').strip()
            
            if line and ':' in line:
                try:
                    time_us, distance_cm = line.split(':')
                    times.append(float(time_us) / 1000000.0)
                    distances.append(float(distance_cm))
                    print(f"Temps: {times[-1]:.3f}s, Distance: {distances[-1]:.1f}cm")
                except ValueError:
                    pass
        
        endTime = time.time()
    
    print(f"\n=== RÉSULTATS STEP 5 ===")
    print(f"Nombre de mesures: {len(times)}")
    print(f"Durée totale: {times[-1]:.2f}s")
    print(f"Distance finale: {distances[-1]:.1f}cm")
    print(f"Distances moyennes: {sum(distances)/len(distances):.1f}cm")
    print(f"Min/Max distance: {min(distances):.1f}/{max(distances):.1f}cm")
    
    cmd = "s"
    serialPort.write(cmd.encode(encoding="ascii"))
    serialPort.flush()
    
    serialPort.close()
    print('Port closed')
    
except Exception as exception:
    print('Exception occurred')
    print(exception)
    serialPort.close()
    print('Port closed')
