from . import logger

class MotionSensor:
    ''' Motion sensor integrated into a hub block. '''
        
    def __init__(self, hub, up='BUTTONS'):
        '''
        Prepare hub for using the motion sensor.
    
        :param Hub hub: [](#Hub) object the motion sensor belongs to.
        :param str up: Side of hub block facing upwards (used for relative angle
                       measurements, see [](#reset) for details).
        '''
        
        self.hub = hub
        self.hub.cmd('from hub import motion_sensor')
        self.reset(up)
        
    
    def reset(self, up='BUTTONS'):
        '''
        Tell the motion sensor which side of the hub block faces upwards and
        that current yaw angle is zero. Yaw, pitch, role angles returned by
        [](#get_orientation) will be relative to these settings.
        
        :param str up: Side of hub block to be considered facing upwards. One of
                       `'BUTTONS'`, `'BATTERY'`, `'USB'`, `'SPEAKER'`, `'ACE'`,
                       `'BDF'`, each referring to one side of the hub block.
        '''
        
        up_dict = {
            'BUTTONS': 'TOP',
            'USB': 'BACK',
            'ACE': 'LEFT',
            'BDF': 'RIGHT',
            'SPEAKER': 'FRONT',
            'BATTERY': 'BOTTOM'
        }
        ret = self.hub.cmd(f'motion_sensor.set_yaw_face(motion_sensor.{up_dict[up]})')
        logger.debug(
            f'motion_sensor.set_yaw_face in MotionSensor.reset returned {ret}'
        )
        ret = self.hub.cmd(f'motion_sensor.reset_yaw(0)')
        logger.debug(
            f'motion_sensor.reset_yaw in MotionSensor.reset returned {ret}'
        )
        
        
    def get_orientation(self):
        '''
        Read yaw, pitch and role angles of hub block in 3d space.

        :return (float, float, float): yaw, pitch and role angles in degrees
                                       from -180 to 180.
        
        To make clear how angles are to be interpreted, assume the hub block
        rests on a table with the side defined as facing upwards (cf.
        [](#reset)) facing upwards. Further assume you are sitting at the table
        looking at the following side of the hub block:
        * speaker side, if buttons side or battery side or ACE side or BDF side
          faces upwards,
        * buttons side, if USB side faces upwards,
        * battery side, if speaker side faces upwards.
        
        We introduce the following coordinate system:
        * One axis is normal to the hub's upward facing side and points upwards.
          This is the yaw axis.
        * One axis lies in the table plan and points to the left from your point
          of view. This is the pitch axis.
        * One axis lies in the table plan and points away from you. This is the
          role axis.
        
        Note that is constitudes a left-handed coordinate system with axis
        sequence yaw, pitch, role.
    
        Take two instances of the coordinate system. One is fixed to the hub
        (axis labels y, p, r) and one is fixed to the table (axis labels Y, P,
        R). Initially both coordinate systems coincide. After rotating the hub
        in arbitrary directions the relation between both coordinate systems can
        be described (up to translations) by three angles:
        * The yaw angle is the angle between R-axis and projection of the r-axis
        onto the P-R-plane. Alternatively, we may say that yaw is rotation
        around the Y-axis. Looking in opposite direction of the Y-axis (that is,
        looking down onto the table) counterclockwise rotation yields positive
        angles.
        * The pitch angle is the angle between P-R-plan and r-axis.
          Alternatively, we may say that pitch is rotation around the p-axis.
          Looking along the p-axis clockwise rotation yields positive angle.
        * The role angle is the angle between P-R-plan and p-axis.
          Alternatively, we may say that role is rotation around the r-axis.
          Looking along the r-axis clockwise rotation yields positive angle.
        '''
        
        ret = self.hub.cmd(f'motion_sensor.tilt_angles()')
        logger.debug(
            f'motion_sensor.tilt_angles in MotionSensor.orientation returned {ret}'
        )
        
        return tuple(int(x) / 10 for x in ret[-1][1:-1].split(','))


    def get_angular_velocity(self):
        '''
        Read angular velocity.
        
        For interpretation of angles take the coordinate system y, p, r defined
        in [](#get_orientation) for buttons side facing upwards. Angular
        velocities are positive if angles described there increase.
        
        :return (float, float, float): Angular velocity for rotation around axes
                                       r, p, y in degrees per second.
        '''
        
        ret = self.hub.cmd(f'motion_sensor.angular_velocity(True)')
        logger.debug(
            f'motion_sensor.angular_velocity in MotionSensor.get_angular_velocity returned {ret}'
        )
        
        return tuple(int(x) / 10 for x in ret[-1][1:-1].split(','))


    def get_acceleration(self):
        '''
        Read acceleration.

        For interpretation of accelerations take the coordinate system y, p, r
        defined in [](#get_orientation) for buttons side facing upwards.
        Accelerations are positive in direction of the axes.
        
        :return (float, float, float): Acceleration in r, p, y direction in G.
                                       Note that even if the hub doesn't move,
                                       values aren't all zero due to
                                       gravitation.
        '''
        
        ret = self.hub.cmd(f'motion_sensor.acceleration(True)')
        logger.debug(
            f'motion_sensor.acceleration in MotionSensor.get_acceleration returned {ret}'
        )
        
        return tuple(int(x) / 1000 for x in ret[-1][1:-1].split(','))

