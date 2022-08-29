# Project One - WaterHealth

As a student Multimedia & Creative technology in Howest Kortrijk, I had to make my own IoT project. This would combine all of the modules followed in the first year into one big project. at home we have a pool and i thought it might be a great idea to make a system to check up on all the different values our pool has such as ph and temperature. I also added an ldr to see how much sunlight we get daily.

Installing Python packages

Before we try to run anything, we need to install some packages for python first. Head into the terminal of your RPi and type the following commands:

- pip3 install mysql-connector-python

- pip3 install flask-socketio

- pip3 install flask-cors

Raspi-config

We will have to enable different interfaces and to do that we first have to typ following code:

sudo raspi-config

The things we need to enable are in the interfacing section. We need to enable following interfaces:

- Serial

- SPI

- i2c

- Serial Port

-1-Wire

check out https://www.instructables.com/Waterhealth-MCT-Howest/ for a more in depth guide
