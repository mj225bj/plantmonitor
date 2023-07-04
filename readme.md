# **Tutorial for plant monitoring**
By Mikael Johansson (mj225bj)

This is a tutorial on how to make a device for monitoring temperature, humidity and when to water your plant. 


## **Objective**
The objective was to make a device to monitor when you need to water your plant, the temperature and humidity surrounding the plant and connect it to a web dashboard to present the data.

I enjoy growing plants all year and vegetables, herbs and spices during the summer months. I like to keep track on when to water the plants and keep track of the climate on my built-in balcony where I usually keep my plants, that was my reasoning behind this project.


## **Material**

Here is a list of the components used in this project. Pricing and links where to buy them is also included.


|   Pictures        | Components            | Description | Cost |
| ---       |:------------------- | ----------- | ----- |
|  ![image alt](https://hackmd.io/_uploads/SJtCpzgY2.jpg "Raspberry Pi Pico W" =200x100)| Raspberry Pi Pico W | A microcontroller board with flexible digital interfaces. Includes on-board single-band 2.4GHz wireless interfaces (802.11n).         | €8.92  ([elektrokit.com](https://www.electrokit.com/produkt/raspberry-pi-pico-w/))  |
|     ![image alt](https://hackmd.io/_uploads/ByrYMXeKn.jpg "DHT11" =150x100)     | Sensor DHT 11 (3-pin model)       | A digital sensor for measuring temperature and humidity       | €4.46  ([elektrokit.com](https://www.electrokit.com/produkt/digital-temperatur-och-fuktsensor-dht11/))   |
|  ![](https://hackmd.io/_uploads/rJRZrXlKn.jpg "U019 Soil Moisture Sensor" =200x100)  | Earth unit (U019)         | A sensor for measuring soil moisture. Has an analog and a digital output.      | €3.88 ([elfa.se](https://www.elfa.se/sv/sensorenhet-foer-markfuktighet-m5stack-u019/p/30172529)) |
|![image alt](https://hackmd.io/_uploads/S1hbsMgF3.jpg "Breadboard" =200x100)     | Breadboard (full-size)          | A solderless breadboard with 840 connections. A smaller board could be used.        | €6.28 ([elektrokit.com](https://www.electrokit.com/produkt/kopplingsdack-840-anslutningar/))  |
|![](https://hackmd.io/_uploads/H1m5dmgYn.jpg "male/male jumper wires" =200x100) |  Jumper wires               | Wires to connect microcontroller and sensors, only male/male wires are needed for this project.        | €4.46 ([elektrokit.com](https://www.electrokit.com/en/product/jumper-wires-40-pin-30cm-male-male/))  |

You will also need a USB-A to micro-USB cable for programming and to power the Raspberry Pi Pico W.

I initially planned to get all components from elektrokit but the soil moisture sensors they sell were all out of stock so I looked around and decided to go with the Earth unit sensor and to order it from elfa. My reasoning behind picking elfa was that their shipping is known to be reliable and I wanted to make sure to get it in time. 





## **Computer setup**
The operating system I've been using during this project is Windows 11.
## **Code Platform**
The code platform that was recommended to use was [micropython](https://micropython.org/) so that's what I went with for this project. Micropython includes a subset of the standard Python library, optimized to be used on microcontrollers.



## **Chosen IDE**

I went with [Visual Studio Code](https://code.visualstudio.com/Download)(VScode) as IDE and I also used the Pymakr extension inside VScode. VScode is available for Windows, Linux and Mac.

Here are the steps I followed in order to get everything working:
1. Download and install [Node js](https://nodejs.org/en) (needed for plugin)
2. Download and install [VScode](https://code.visualstudio.com/Download)
3. Open VScode and then open the Extension Manager either by clicking the left panel icon or View > Extensions
4. Type in **pymakr** in the search window and install the main program, not the preview. (See image below)

![](https://hackmd.io/_uploads/Hkh4F5Ztn.png)

## **Raspberry Pi Pico W Firmware**
A firmware needs to be installed on the Raspberry Pi Pico W and it can be found [**here**](https://micropython.org/download/rp2-pico-w/). I suggest getting the latest release of the **uf2** and not any of the nightly builds. Follow the guide below in order to install the firmware onto the Pico.
1. Connect the micro-USB to the raspberry Pi Pico but be careful and make sure to hold onto the usb-slot so it doesnt bend.
2. While pressing the **BOOTSEL** key on the Pico board, plug the USB-A into your computer. Once connected you can release the **BOOTSEL** button.
3. A new drive named RPI-RP2 should show up in your file system, this is the storage for Raspberry Pi Pico. Copy/Paste the **uf2** firmware to this storage.
4. Wait for your Pico to disconnect from your computer and then wait for it to reconnect.

## **Putting everything together**
The Earth unit Soil moisture sensor analog out is connected to GP26 on the Pico board and the DHT out is connected to GP27. They are also connected to 3V3 Out and GND. Make sure you connect to the correct pins for your sensors and microcontroller.
Below is a diagram of how the sensors are connected to the Pico.
![](https://hackmd.io/_uploads/B1UJqTWY3.png)

## **Platform**
I'm using [Adafruit IO](https://io.adafruit.com/) as a cloud platform for this project.  The reasoning behind using Adafruit IO is that it looked like it would suit the project. I am using the free version of Adafruit IO. 



I am planning to add more sensors to be able to monitor more plants so the limitation to the amount of feeds that can be used with the free version of Adafruit IO will probably push me towards setting up a local installation of some sort but for now it will suffice.



## **The code**

The files for this project can be found in the [Github repository](https://github.com/mj225bj/plantmonitor).
The code for connecting to the WiFi is added to the boot file so that it will be connecting on every startup. I've also added a secrets file where you should put your SSID and Password. The main file runs after the boot and consists of the  initiations of sensors and creation of functions that sense and transmit data. I also have an mqtt library for using MQTT over WiFi.

I've calibrated the earth unit sensor by measuring a pot of dry soil and a fully saturated pot of wet soil. This gave me minimum and maximum values for the code shown below.
```
# Define the maximum and minimum sensor values based on calibration
max_sensor_value = 20000  # Replace with your maximum observed sensor value
min_sensor_value = 65535  # Replace with your minimum observed sensor value
```
I then decided to convert the values into percentages to get a value that is easier to read.
```
# Function to convert the sensor value to a percentage based on the range
def convert_to_percentage(sensor_value):
    percentage = (sensor_value - min_sensor_value) / (max_sensor_value - min_sensor_value) * 100
    return percentage
```
I've set my threshold when to water the plant at 30%, anything below that and it will tell me that it needs water. I used an analog moisture meter to help me get to this value. Below is an example of a plant before and after watering, with the the analog meter, I've also added the values shown in Adafruit IO.


| Before Watering | After watering |
| -------- | -------- |
| ![](https://hackmd.io/_uploads/H1s14kzF2.jpg )    |![](https://hackmd.io/_uploads/ByN6QJft3.jpg)    |




## **Transmitting the data / connectivity**
I'm using WiFi to connect the device to my LAN to get access to the internet and then connecting the Adafruit Feeds to be shown on the Dashboard.I've set up four different feeds. The data is transmitted from the Pico W over WiFi using the MQTT protocol. I currently have it set to sending data every 60 seconds to gather data, I'm probably gonna change that to a longer time for the soil moisture sensor. 
## **Presenting the data**
The four feeds, two for soil moisture and the other two for temperature and humidity, are shown on the dashboard.The soil moisture sensor is connected to GP26 and the dht11 sensor used to measure humidity and temperature is connected to GP27 on the Raspberry Pi Pico. Below is a screenshot of my current [Dashboard](https://io.adafruit.com/mj225bj/dashboards/lnu-project).

![](https://hackmd.io/_uploads/BJURXgfF2.png)


