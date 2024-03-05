import time

from . import logger

class ColorSensor:
    ''' A color sensor connected to a hub block. '''
    
    def __init__(self, hub, port):
        '''
        Prepare hub for usage of a color sensor.
    
        :param Hub hub: [](#Hub) object the color sensor is connected to.
        :param str port:  Identifier of the hub port the sensor is connected to
                          (one of `'A'`, `'B'`, `'C'`, `'D'`, `'E'`, `'F'`).
        '''
        
        self.hub = hub
        port_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
        self.port = port_map[port]
        self.hub.cmd('import color_sensor')
        

    def get_raw_color(self):
        '''
        Read color and intensity without additional scaling.
        
        :return (int, int, int, int): Tuple `(R, G, B, intensity)` of ints in
                                      0-1023.
        '''
        
        ret = self.hub.cmd(f'color_sensor.rgbi({self.port})')
        logger.debug(
            f'color_sensor.rgbi in ColorSensor.get_raw_color returned {ret}'
        )
        
        return tuple(int(x) for x in ret[-1][1:-1].split(','))

    
    def get_color(self):
        '''
        Read color and intensity and scale values to 0-255.
        
        :return (int, int, int, int): Tuple `(R, G, B, intensity)` of ints in
                                      0-255.
        '''
        
        return tuple(int(x / 1024 * 255) for x in self.get_raw_color())
