import subprocess
from sense_hat import SenseHat
from flask import Flask, render_template

app = Flask(__name__)
sense = SenseHat()

old_temp = 0.0

@app.route('/')
def index():
	temp = sense.get_temperature()
	hum_temp = sense.get_temperature_from_humidity()
	pres_temp = sense.get_temperature_from_pressure()

	avg = (hum_temp+pres_temp)/2

	rpi_temp = subprocess.run('/usr/bin/vcgencmd measure_temp', shell=True, stdout=subprocess.PIPE)
	rpi_temp = rpi_temp.stdout[5:9].decode('utf-8')

	calc_temp = avg - ((float(rpi_temp) - avg) / 2)
	calc_temp = '%.2f' % calc_temp

	global old_temp
	old_temp_string = str(old_temp)
	old_temp = calc_temp

	tempDiff = 0.0
	tempDiff = float(calc_temp) - float(old_temp)
	if calc_temp > old_temp:
		tempDiff = float(calc_temp) - float(old_temp_string)
	else:
		tempDiff = float(old_temp_string) - float(calc_temp)

	tempDiff = '%.2f' % abs(tempDiff)
	#return str('%0.2f&deg;C' % calc_temp)
	#return str('It is %0.2f&deg;C right now. The humidity sensor says %0.2f&deg;C while the pressure sensor says %0.2f&deg;C.\n\nThe average is %0.2f&deg;C.' % (temp, hum_temp, pres_temp, avg))
	return render_template('index.html', temperature=calc_temp, oldTemp = old_temp_string, tempDiff=tempDiff)

if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0', port='9001')
