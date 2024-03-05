import time

from . import logger

class DistanceSensor:
    ''' A distance sensor connected to a hub block. '''
    
    def __init__(self, hub, port):
        '''
        Prepare hub for usage of a distance sensor.
    
        :param Hub hub: [](#Hub) object the distance sensor is connected to.
        :param str port:  Identifier of the hub port the sensor is connected to
                          (one of `'A'`, `'B'`, `'C'`, `'D'`, `'E'`, `'F'`).
        '''
        
        self.hub = hub
        port_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
        self.port = port_map[port]
        self.hub.cmd('import distance_sensor')
        self.lights_off()
        
    
    def lights_off(self):
        '''
        Turn all lights of the sensor off.
        '''
        
        ret = self.hub.cmd(f'distance_sensor.clear({self.port})')
        logger.debug(
            f'distance_sensor.clear in DistanceSensor.lights_off returned {ret}'
        )
        

    def get_distance(self):
        '''
        Read distance in millimeters.
    
        :return int: Distance in millimeters. -1 indicates an invalid
                     measurement.
        '''
        
        ret = self.hub.cmd(f'distance_sensor.distance({self.port})')
        logger.debug(
            f'distance_sensor.distance in DistanceSensor.get_distance returned {ret}'
        )
        
        return int(ret[-1])

    
    def set_pixel(self, pos, intensity):
        '''
        Set intensity of a distance sensor's light.

        Each of the four lights is indentified by an int in 0...3:
        * 0 is left top,
        * 1 is left botton,
        * 2 is right top,
        * 3 is right bottom.

        :param int pos: Identifier of the light (0...3).
        :param int intensity: Intensity of the light (0...100).
        '''
        
        ret = self.hub.cmd(f'distance_sensor.set_pixel({self.port}, {pos // 2}, {pos % 2}, {intensity})')
        logger.debug(
            f'distance_sensor.set_pixel in DistanceSensor.set_pixel returned {ret}'
        )
 