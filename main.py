import time
import ubinascii #Converts between binary and ascii
import machine
import micropython
from machine import Pin
import dht
from mqtt import MQTTClient

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "your_aio_user_name" #Replace with your aio username
AIO_KEY = "your aio_key"        #Replace with your aio key
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_SOIL_FEED = "your/feed/name" #Replace with your feed name
AIO_TEMPERATURE_FEED = "your/feed/name" #Replace with your feed name
AIO_HUMIDITY_FEED = "your/feed/name" #Replace with your feed name

# Define the GPIO pin connected to the temperature and humidity sensor's OUT pin
dht_sensor = dht.DHT11(machine.Pin(27))

# Define the GPIO pin connected to the soil moisture sensor's OUT pin
moisture_pin = machine.ADC(26)

# Define the threshold moisture level as a percentage
threshold_percentage = 30

# Define the maximum and minimum sensor values based on calibration
max_sensor_value = 20000  # Replace with your maximum observed sensor value
min_sensor_value = 65535  # Replace with your minimum observed sensor value

# Function to check if watering is needed based on soil moisture
def is_water_needed():
    moisture_value = moisture_pin.read_u16()
    moisture_percentage = convert_to_percentage(moisture_value)
    print("Moisture percentage:", moisture_percentage) #Prints to console, can be removed after testing.
    client.publish(AIO_MOISTURE_FEED, str(moisture_percentage))  # Publish moisture percentage to the moisture feed
    return moisture_percentage < threshold_percentage

# Function to convert the sensor value to a percentage based on the range
def convert_to_percentage(sensor_value):
    percentage = (sensor_value - min_sensor_value) / (max_sensor_value - min_sensor_value) * 100
    return percentage

# Use the MQTT protocol to connect to Adafruit IO
client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)

# Subscribed messages will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))

client.set_callback(sub_cb)
client.connect()
client.subscribe(AIO_TEMPERATURE_FEED)
print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, AIO_TEMPERATURE_FEED))

try:
    while True:
        client.check_msg()
        if is_water_needed():
            print("Water is needed.") #Prints to console, can be removed after testing.
            # Publish soil moisture data to Adafruit IO
            moisture_value = moisture_pin.read_u16()
            moisture_percentage = convert_to_percentage(moisture_value)
            client.publish(AIO_SOIL_FEED, "Water is Needed")
        else:
            print("No watering required.") #Prints to console, can be removed after testing.
            # Publish soil moisture data to Adafruit IO
            client.publish(AIO_SOIL_FEED, "No watering required")
        time.sleep(3600) #Set this to whatever time you want to update the soil moisture feed
        
        # Read temperature and humidity from DHT11 sensor
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        # Publish temperature and humidity data to Adafruit IO
        client.publish(AIO_TEMPERATURE_FEED, str(temperature))
        client.publish(AIO_HUMIDITY_FEED, str(humidity))
        time.sleep(900) #Set this to whatever time you want to update the temperature and humidity feeds
        
except Exception as e:
    print("Error:", str(e))