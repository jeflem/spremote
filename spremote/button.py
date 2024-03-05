from . import logger

class Button:
    '''
    A button (power, bluetooth, left, right) of a hub block including button
    lights.
    '''
        
    def __init__(self, hub, which):
        '''
        Prepare hub for button usage.
    
        :param Hub hub: [](#Hub) object the button belongs to.
        'param str which: Button identifier (`'POWER'`, `'CONNECT'`, `'LEFT'`,
                          `'RIGHT`')
        '''
        
        self.hub = hub
        self.which = which
        self.hub.cmd('from hub import light')
        self.hub.cmd('from hub import button')
        
    
    def set_color(self, color):
        '''
        Set the button light's color.
        
        :param int color: 0 turns off the light. Values 1 to 10 select one of
                          the hub's predefined colors.
        '''
        
        ret = self.hub.cmd(f'light.color(light.{self.which}, {color})')
        logger.debug(
            f'light.color in Button.set_color returned {ret}'
        )
        
        
    def is_down(self):
        '''
        Returns number of milliseconds the button is down for.
        
        :return int: Button down time in milliseconds. If button isn't down, 0
                     is returned.
        '''
        
        ret = self.hub.cmd(f'button.pressed(button.{self.which})')
        logger.debug(
            f'button.pressed in Button.is_down returned {ret}'
        )
        
        return int(ret[-1])
