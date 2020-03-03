import serial
import time

class Device:

    def __init__(self):

        # default parameters for RS232
        self.port_name = "COM3"
        self.baudrate  = 9600
        self.bit = 8
        self.parity    = 'N'
        self.stopbits  = 1


        # COM is an RS322 object
        self.com = None
        
        self.permissions = []
        self.collect_cmd_once = []
        self.collect_cmd = []
        self.start_cmd = []
        self.stop_cmd = []
        
    def __del__(self):
        self.disconnect()


    # use this function to set RS232 port parameters
    def setSerial(self, port_name, baudrate, parity, stopbits):
        self.port_name = port_name
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
    
    def addPermission(self, command):
        self.permissions.append(command)

    # mark 1 as always collect command
    def addCollectCommand(self, command):
        result = self.sendString(command)
        self.collect_cmd.append((command, result[1], 1))

    def delCollectCommand(self):
        self.collect_cmd.pop()

    # mark 2 as Once collect command
    def addOnceCollectCommand(self, command):
        result = self.sendString(command)
        self.collect_cmd_once.append((command, result[1], 2))
        
    def addStartCommand(self, command):
        self.start_cmd.append(command)

    def addStopCommand(self, command):
        self.stop_cmd.append(command)

    # connect serial port
    def connect(self):
        self.com = serial.Serial(timeout=0.1)
        self.com.port = self.port_name
        self.com.baudrate = self.baudrate
        #self.com.bytesize = self.bit
        self.com.parity = self.parity
        self.com.stopbits = self.stopbits
        self.com.open()
        return self.com.is_open

    # send cmd and return the received feedback
    def sendString(self, command):
        if not self.com.is_open:
            print("COM is not open")
            return ""
        if command == "":
            return ""
        command = command + "\r\n"
        self.com.write(command.encode('utf-8'))
        ret = self.com.readline().decode()  #'XP0126 A 28.67113203' -> ['XP0126 A 28.67113203', 1]  ['XP0139 A 0.02202246 0.44781586 0.44781586', 3]
        if ret == "ES\r\n":
            print('Error Command for Device: ' + command)
            return ""
        if ret == "EL\r\n":
            print('Error Command in format: ' + command)
            return ""
        if len(ret) == 0:
            print(self.port_name + ' cannot get data')

        parameterNo = ret.count(' ')-1
        ret = [ret, parameterNo]
        return ret

    def collectPreCond(self):
        ret = []
        for cmd, parameterNo, ctype in self.collect_cmd_once:
            result = self.sendString(cmd)
            if len(result) == 0:
                continue
            result = result[0][:6] + result[0][8:-1]
            #result = result.split(' ')[parameterNo - 1]
            ret.append(result)
        return ret

    # collect date time and corresponding received data
    def collectData(self, basetime):
        ret = []
        if float(time.time() - basetime) < 0.2:
            import datetime
            # starting time like 2019.09.30-10:41:07
            ret.append(datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
        else:
            # offset time from the starting time
            ret.append(round((time.time() - basetime),1))
            #ret.append((time.time() - basetime))
        for cmd, parameterNo, ctype in self.collect_cmd:
            #if ctype == 2 and float(time.time() - basetime) > 0.2:
                #ret.append("")
                #continue

            '''
            _parent.Connection.Send(_terminal1, "POWER");
            _parent.Connection.Receive(_terminal1, out  received, true);
            LampPower = GetParameter(received, 3);

            _parent.Connection.Send(_terminal2, ":NUMERIC:NORMAL:VALUE? 3");
            _parent.Connection.Receive(_terminal2, out  received, true);
            InputPower = GetParameter(received, 1);
            
            '''

            result = self.sendString(cmd)  # ['XP0126 A 28.67113203', 1], ['XP0139 A 0.02202246 0.44781586 0.44781586', 3]
            if len(result) == 0:
                continue
            if result[1] == 1:
                result1 = (result[0][:-2]).split(' ')[2]
                ret.append(result1)
            else:
                for i in range(0, result[1]):
                    result1 = (result[0][:-2]).split(' ')
                    ret.append(result1[i+2])
        return ret

    # get permission for commands like XP, XM
    def getPermission(self):
        for cmd in self.permissions:
            self.sendString(cmd)

    # send start cmd
    def getStartAction(self):
        for cmd in self.start_cmd:
            self.sendString(cmd)

    # send stop cmd
    def getStopAction(self):
        for cmd in self.stop_cmd:
            self.sendString(cmd)

    # close the port
    def disconnect(self):
        if self.com != None and self.com.is_open == True:
            self.com.close()