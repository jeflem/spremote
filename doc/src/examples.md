# Examples

```{contents}
---
depth: 1
local: True
---
```

## Sending commands directly to the hub

```{hint}
SPremote provides a `Hub` class for communicating with the hub's Python interpreter. In addition, there are classes for all devices (motors, sensors,...). Depending on your needs, either work with the Hub class only (and send command strings to the hub) or use SPremote's device classes (simpler and cleaner code).
```

```python
import spremote

hub = spremote.Hub('/dev/ttyACM0')

hub.cmd('import hub')
dev_id = hub.cmd('hub.device_uuid()')

print(f'Hub\'s device ID: {dev_id}')

hub.disconnect()
```

Everything you send to the hub with `cmd` will be executed on the hub! So `import hub` imports LEGO's `hub` module into the Python session running on the hub.

Note that the `cmd` method returns a list of strings. Each item contains one line of output from the hub's Python interpreter. To get the pure return value of the `device_uuid` method in the code above add something like
```python
dev_id = dev_id[0][1:-1]
```
This way you get rid of the list and of additional quotation marks originating from simply copying the output of the hub's Python interpreter.

## Motors and buttons

Connect a motor to port A before you run the code below.

```python
import spremote
import time

print('Press left button to reduce speed, right button to increase speed, ' + \
      'both buttons to stop the program.')

hub = spremote.Hub('/dev/ttyACM0')
lb = spremote.Button(hub, 'LEFT')
rb = spremote.Button(hub, 'RIGHT')
m = spremote.Motor(hub, 'A')

speed = 0
new_speed = 0
while not (lb.is_down() and rb.is_down()):
    if rb.is_down():
        new_speed = min([speed + 10, 100])
    elif lb.is_down():
        new_speed = max([speed - 10, 0])
    if new_speed != speed:
        speed = new_speed
        if speed == 0:
            m.stop()
        else:
            m.start(speed=speed)
    time.sleep(0.2)
m.stop()

hub.disconnect()
```

## Listing devices

Connect a distance sensor to some port of the hub before you run the code below.

```python
import spremote

dev = 62  ## ID of distance sensors

hub = spremote.Hub('/dev/ttyACM0')

devs = hub.list_devices()
for p, d in devs.items():
    if d == dev:
        print(f'distance sensor connected to port {p}')

hub.disconnect()
```

## Polling sensors

The following program detects movement of the hub.

```python
import spremote
import time

print('Press left button on hub to stop.')

hub = spremote.Hub('/dev/ttyACM0')
b = spremote.Button(hub, 'LEFT')
ms = spremote.MotionSensor(hub)

acc = ms.get_acceleration()
while not b.is_down():
    new_acc = ms.get_acceleration()
    if max([abs(old - new) for old, new in zip(acc, new_acc)]) > 0.01:
        print('hub moved')
        time.sleep(0.5)
        new_acc = ms.get_acceleration()  # avoid counting twice (accelerate, decelerate)
    acc = new_acc

hub.disconnect()
```

## Debugging and logging

SPremote uses Python's `logging` module for logging output of a hub's Python interpreter. This is especially useful for debugging exceptions in the hub's Python interpreter not handled by SPremote.

Connect a distance sensor to port A of the hub before running the code below.

```python
import logging
import spremote

logging.basicConfig(
    filename='test.log',
    format='%(levelname)s %(asctime)s %(name)s %(filename)s:' \
           '%(lineno)d: %(message)s',
    level=logging.DEBUG
)

hub = spremote.Hub('/dev/ttyACM0')

ds = spremote.DistanceSensor(hub, 'A')
print(ds.get_distance())

hub.disconnect()
```

## Projects using SPremote

* [Pasta machine](https://webspace.fh-zwickau.de/jef19jdw/codedata/pasta.html): motor control based on processing of camera images.


TODO: logging
TODO: list_devices zur automatischen erkennung des ports
