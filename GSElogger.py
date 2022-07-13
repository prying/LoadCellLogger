from asyncore import write
import csv
from datetime import datetime
import sys
import time

EMULATE_HX711 = False
referenceUnit = -15.98649219577974

if not EMULATE_HX711:
	import RPi.GPIO as GPIO
	from hx711 import HX711
else:
	from emulated_hx711 import HX711

def cleanAndExit():
	print("Cleaning...")

	if not EMULATE_HX711:
		GPIO.cleanup()
		
	print("Done!")
	sys.exit()


now = datetime.now()
timeStr = now.strftime("%H%M%S")

header = ['time', 'raw data', 'weight (g)']

# Setup load cell
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("Tare done!")

# Open log file
with open(f"logs/LoadCell{timeStr}.csv", 'w') as file:
	writer = csv.writer(file)

	writer.writerow(header)

	offset = hx.get_offset()

	# Write to file
	while True:
		try:
			now = datetime.now().time()
			val_raw = hx.get_value(3)
			val = val_raw/referenceUnit
			row = [now, val_raw, val]

			write.writerow(row)
			time.sleep(0.1)

			# Pretty sure you dont need ot do this 
			#hx.power_down()
			#hx.power_up()

		except (KeyboardInterrupt, SystemExit):
			cleanAndExit();