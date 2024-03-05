# SPremote Python package

SPremote allows LEGO SPIKE Prime machines to be controlled remotely from a computer. With standard tools like [Lego Education SPIKE App](https://education.lego.com/en-us/downloads/spike-app/software/) or [Pybricks](https://pybricks.com/) all code runs on the hub block's microcontroller. With SPremote most of the code runs on your (fast) computer, only few commands for controlling motors and readings sensors have to be executed on the (slow) hub block. With SPremote you get
* much faster programs,
* programming in your favorite Python IDE,
* orchestration of multiple hub blocks,
* (relayed) communication between multiple hub blocks,
* seamless integration of other devices like cameras,

SPremote has been developed mainly for projects in deep reinforcement learning education. All the heavy code, neural network training, optimization algorithms and so on, runs on your powerful multi-core CPU (and maybe GPU), while the LEGO machine's microcontroller only has to execute some simple commands from time to time.

## Install

Install with `pip` from the GitHub repo:
```
pip install git+https://github.com/jeflem/spremote.git@main
```
or copy the `spremote` directory from the [repo](https://github.com/jeflem/spremote) into your project's directory.

On the hub block you have to install LEGO SPIKE Prime firmware via [Lego Education SPIKE App](https://education.lego.com/en-us/downloads/spike-app/software/) version 3.4.3. Other versions may work as well, but haven't been tested up to now.

## Usage

### Prerequisites

SPremote requires access to a serial connection to the hub block. Instructions for USB based serial connections are provided below. In principle, bluetooth connections should work, too. At least, they did with older firmware. With current 3.4.3 firmware we were not able to get a reliable connection.

SPremote has been tested on Linux only, but should work on other Unix-like systems, too. On Windows there's a good chance to get things running, if one is able to create a serial device and pass this device to [pyserial](https://github.com/pyserial/pyserial).

### Connect

To establish a serial USB connection to the hub block proceed as follows:
1. Connect the hub to your computer.
2. Press the hub's power button.
3. Run `dmesg` (or `sudo dmesg`) in a terminal. The last lines printed should contain information about a new USB device and it's name. Usually, it's `/dev/ttyACM0`.

### Test connection

Before you run SPremote based Python code you may want to test the connection:
1. Run `sudo screen /dev/ttyACM0` in a terminal.
2. Now you should see an empty terminal. Presse `Ctrl+C`.
3. Now you see the hub's Python interpreter waiting for input (`>>>`).
4. Write some commands, like `print('test')`.
5. Close `screen` with `Ctrl+a`, then `k`, then `y`.

### Permissions

To avoid using `sudo` you may have to modify permissions for device access. Choose one of the following (all tested on Debian 12):
* Run `sudo chmod 666 /dev/ttyACM0` (has to be rerun after each reconnect).
* Add your user to group `dialout`, then logout and login again (may cause troubles if software running as a different user wants to access the hub).
* Add a udev rule ([reference](https://askubuntu.com/questions/112568/how-do-i-allow-a-non-default-user-to-use-serial-device-ttyusb0), access for all users, survives reconnects and reboots):
  1. `sudo nano /etc/udev/rules.d/50-myusb.rules`,
  2. type `KERNEL=="ttyACM0",MODE="0666"`,
  3. close editor with `Ctrl+x`, then `y`, then `return`.

### Test SPremote

Here is some code for testing:

```python
import spremote

hub = spremote.Hub('/dev/ttyACM0')

print('light up one pixel')
lm = spremote.LightMatrix(hub)
lm.set_pixel(2, 2, 100)

print('change power button color')
power_button = spremote.Button(hub, 'POWER')
power_button.set_color(9)

hub.disconnect()
```

If you experience connection issues (device busy,...) power off the hub and power on again.

## How it works

SPremote stops the Python program running on the hub by default. For this purpose SPremote sends `b'\x03'`, which corresponds to pressing `Ctrl+c` in a terminal. Whenever you call an SPremote function, SPremote sends a string of Python code to the hub and waits for outputs until the hub's Python interpreter is ready for the next command.

Sending commands and retrieving outputs requires some fiddling with indentation, line breaks and other string processing issues. All this is done by the `Hub` class' methods. See [the doc's examples section](https://webspace.fh-zwickau.de/jef19jdw/spremote/examples.html) and [API documentation](https://webspace.fh-zwickau.de/jef19jdw/spremote/api.html) for more information.

## Documentation

Documentation is in the repo's `doc/src` directory (Markdown). [HTML documentation](https://webspace.fh-zwickau.de/jef19jdw/spremote) is available, too.

## Contributing

SPremote code lives on [github.com](https://github.com/jeflem/spremote).

File pull requests against `dev` branch. That branch contains the code from which the next release will be generated. The `main` branch contains the current stable release.
 
