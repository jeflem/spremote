import serial

from . import logger

class Hub:
    ''' Connection related functionality of a hub block (no sensors, buttons,
        light matrix aso.). '''
    
    def __init__(self, port):
        '''
        Connect host to the hub's Python interpreter.
    
        :param str port: Device name of the hub at the host machine (e.g.
                         `/dev/ttyACM0`).
        '''
        
        # connect
        logger.debug(f'Trying to connect to {port}.')
        self.connection = serial.Serial(port, 115200, timeout=0.1)
        if not self.connection.is_open:
            self.connection.open()
        
        # stop runloop by Ctrl+D (yields full control over Python interpreter)
        self.connection.write(b'\x03')

        # check Python interpreter's greeting message
        greeting = self.connection.readlines()
        logger.debug(f'Python interpreter greeting: {greeting}')
        if greeting[-1] != b'>>> ':
            logger.warning('Python interpreter does not show >>>.')
        
        # prepare for device listing
        self.cmd('import device')
        

    def disconnect(self):
        '''
        Close serial connection to hub.
        '''
        
        self.connection.close()
        

    def write(self, text):
        '''
        Send one or multiple lines of text to the hub's Python interpreter
        (almost) as is.
        
        :param str text: String to send to the hub.
        
        If text does not end with `'\\n'`, then `'\\n'` will be appended before
        sending. In addition, the hub's interactive Python interpreter uses
        `'\\r\\n'` for line breaks. Thus, `'\\n'` is replaced by `'\\r\\n'`
        before sending.
        
        ```{note}
        Due to the interpreter's autoindentation feature this method is not
        suitable for sending code blocks with identation. Instead, use [](#cmd)
        to send code blocks.
        ```
        '''
        
        if not text.endswith('\n'):
            text += '\n'
        self.connection.write(text.replace('\n', '\r\n').encode())
        
        
    def readline(self):
        '''
        Read one line from the hub's Python interpreter.
        
        :return str: Text read from hub without trailing line break.
        '''
        
        raw = self.connection.readline()
        if raw[-2:] == b'\r\n':
            text = raw[:-2].decode()
        else:
            text = raw.decode()
        
        return text

    
    def readlines(self):
        '''
        Read all available lines from hub.
        
        Hub line breaks (`'\\r\\n'`) are replaced by `'\\n'`.

        :return str: Text read from hub.
        '''
        
        raw = self.connection.readlines()
        text = ''
        for raw_line in raw:
            if raw_line[-2:] == b'\r\n':
                text += raw_line[:-2].decode() + '\n'
            else:
                text += raw_line.decode()
        
        return text


    def cmd(self, code):
        '''
        Send Python code to the hub.
        
        Waits until interpreter asks for next command and returns output
        shown by the interpreter.
        
        :param str code: Python code to execute on the hub.
        :return [str]: All outputs produced by the code (list of lines).
        '''
        
        marker = '<<<done>>>'
        
        # insert line breaks to cope with the interpreter's autoindentation
        lines = code.split('\n')
        for i in range(len(lines) - 1):
            if lines[i + 1].startswith(' ') or lines[i].startswith(' '):
                lines[i] += '\n\n'
        if lines[-1].startswith(' '):
            lines[-1] += '\n\n'
        lines[-1] += '\n'
            
        # send code
        self.write('\n'.join(lines))
        self.write('#' + marker)
        
        # wait till executed and collect outputs
        output = []
        while True:
            line = self.readline()
            if line == '':
                continue
            if line.find(marker) > -1:
                break
            if line[:3] != '>>>' and line[:3] != '...':
                output.append(line)
                
        return output


    def list_devices(self):
        '''
        List IDs of devices connected to the hub.
        
        Each device type has a unique ID. With this method the port a device is
        connected to can be identified at runtime.
        
        :return dict(str=int): Dictionary with keys `'A'`, `'B'`, `'C'`, `'D'`,
                            `'E'`, `'F'` and integer values representing device
                            IDs. 0 indicates that no device is connect to the
                            port.
        '''
        
        devices = {}
        for num, port in enumerate(['A', 'B', 'C', 'D', 'E', 'F']):
            devices[port] = int(self.cmd(f'try:\n    print(device.id({num}))\nexcept:\n    print(0)\n')[0])
        
        return devices
