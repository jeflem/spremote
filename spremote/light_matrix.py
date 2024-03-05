from . import logger

class LightMatrix:
    ''' The light matrix of a hub block. '''
    
    def __init__(self, hub):
        '''
        Prepare hub for light matrix usage.
    
        :param Hub hub: [](#Hub) object the light matrix belongs to.
        '''
        
        self.hub = hub

        self.clear()


    def clear(self):
        '''
        Clear light matrix (turn all pixels off).
        '''
        
        ret = self.hub.cmd('hub.light_matrix.clear()')
        logger.debug(f'hub.light_matrix.clear in LightMatrix.clear returned {ret}')
        

    def show_image(self, img):
        '''
        Show an image.
        
        :param str img: Image to show. The string has to contain 5 lines, each
                        with 5 characters. Allowed characters are 0-9 and X
                        corresponding to intensity levels 0%-90% and 100%,
                        respectively.
        '''
        
        value_map = {'0': 0, '1': 10, '2': 20, '3': 30, '4': 40, '5': 50, 
                     '6': 60, '7': 70, '8': 80, '9': 90, 'X': 100}
        
        img_list = [value_map[v] for v in img if v in value_map.keys()]
        if len(img_list) != 25:
            logger.debug(f'Invalid image: {img}.')
            return
        
        ret = self.hub.cmd(f'hub.light_matrix.show({str(img_list)})')
        logger.debug(f'hub.light_matrix.show in LightMatrix.show_image returned {ret}')


    def set_pixel(self, x, y, b):
        '''
        Set brightness of pixel.
        
        :param int x: x-position of pixel.
        :param int y: y-position of pixel.
        :param int b: brightness level (0-100).
        '''
        
        ret = self.hub.cmd(f'hub.light_matrix.set_pixel({x}, {y}, {b})')
        logger.debug(f'hub.light_matrix.set_pixel in LightMatrix.set_pixel returned {ret}')
        
