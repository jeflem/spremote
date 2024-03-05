import time

from . import logger

class ForceSensor:
    ''' A force sensor connected to a hub block. '''
    
    def __init__(self, hub, port):
        '''
        Prepare hub for usage of a force sensor.
    
        :param Hub hub: [](#Hub) object the force sensor is connected to.
        :param str port:  Identifier of the hub port the sensor is connected to
                          (one of `'A'`, `'B'`, `'C'`, `'D'`, `'E'`, `'F'`).
        '''
        
        self.hub = hub
        port_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
        self.port = port_map[port]
        self.hub.cmd('import force_sensor')
        
    
    def get_raw(self):
        '''
        Read raw data.
    
        :return int: Force read from sensor.
        '''
        
        ret = self.hub.cmd(f'force_sensor.raw({self.port})')
        logger.debug(
            f'force_sensor.raw in ForceSensor.get_raw returned {ret}'
        )
        
        return int(ret[-1])
