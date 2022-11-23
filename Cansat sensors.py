import network
import time
from machine import I2C, Pin
import time
from bmp280 import *
from mpu9250 import MPU9250
import ntptime
import machine
import utime
from machine import ADC
from machine import Pin
import urequests

json_data = None
request = None

def sht20_temperature():
	i2c.writeto(0x40,b'\xf3')
	time.sleep_ms(70)
	t=i2c.readfrom(0x40, 2)
	return -46.86+175.72*(t[0]*256+t[1])/65535

def sht20_humidity():
	i2c.writeto(0x40,b'\xf5')
	time.sleep_ms(70)
	t=i2c.readfrom(0x40, 2)
	return -6+125*(t[0]*256+t[1])/65535

adc35=ADC(Pin(35))
adc35.atten(ADC.ATTN_11DB)
adc35.width(ADC.WIDTH_12BIT)

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()
sta_if.connect('Rede','Senha')
print("Waiting for Wifi connection")
while not sta_if.isconnected(): time.sleep(1)
print("Connected")
i2c=I2C(scl=Pin(22), sda=Pin(21))
bus=I2C(scl=Pin(22), sda=Pin(21))
bmp280 = BMP280(bus)
bmp280.use_case(BMP280_CASE_WEATHER)
bmp280.oversample(BMP280_OS_HIGH)
i2c=I2C(scl=Pin(22), sda=Pin(21))
mpu9250s = MPU9250(i2c)
while True:
  print('"data e hora":')
  # Uma aplicação de Network Time Protocol NTP.
  ntptime.settime()
  rtc = machine.RTC()
  utc_shift=(-3)
  tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
  tm = tm[0:3] + (0,) + tm[3:6] + (0,)
  rtc.datetime(tm)
  rtc.datetime()
  # Note que todos os dados dos sensores podem ser trabalhados previamente e ser enviados através de uma variável ou sub-rotina.
  json_data = ''.join([str(x) for x in ['"equipe":', 123, ', "bateria":' + str(adc35.read()), ', "temperatura":', sht20_temperature(), ', "pressao":', bmp280.pressure, ', "giroscopio":', mpu9250s.gyro, ', "acelerometro":', mpu9250s.acceleration]])
  request = urequests.post('http://ptsv2.com/t/bipes-test/post', json=json_data)

  print('HTTP Status = ' + str(request.status_code))
  print('HTTP Response = ' + str(str(request.content)))
  # Para o envio da sonda deverá ser 240 segundos.
  time.sleep(60)

'http://ptsv2.com/t/bipes-test/post'
