import serial
import time
import sched
import xlwt

class Tester:
    
    def __init__(self):
        self.devices = []
        self.heating_temp = 160
        self.heating_time = 5
        self.heating_interval = 2
        self.heating_counts = 10
        self.waiting_time = 5
        self.waiting_counts = 10
        self.cooling_time = 5
        self.WaitCool_interval = 10
        self.cooling_counts = 10
        self.all_datas = []
        self.log_name = 'result.csv'
        
        self.if_start = False
        self.basetime = 0
        self.count = 0
        self.writeLine = 0
    
    def addDevice(self, dev):
        self.devices.append(dev)

    # return True if all added devices are connected, return false if finding one device is not connected.
    def connect(self):
        for dev in self.devices:
            if not dev.connect():
                return False
        return True

    # collect data and write into log file
    def collectAllDevice(self):
        if not self.if_start:
            self.base_time = time.time()
            self.if_start = True

        # read text
        ret = []

        for dev in self.devices:
            # temporary data
            tmp = dev.collectData(self.base_time)
            ret.append(tmp)
        
        #print(ret)
        with open(self.log_name, 'a+') as myFile:
            # matrix array used for >1 devices, each line stores received data for each device
            myFile.write(str(ret[0][0]))
            for tmp in ret:
                for i in range(1, len(tmp)):
                    myFile.write(','+tmp[i])
            myFile.write('\n')

    def collectPreCondition(self):
        # read text
        ret = []

        for dev in self.devices:
            # temporary data
            tmp = dev.collectPreCond()
            ret.append(tmp)

        #print(ret)
        with open(self.log_name, 'w') as myFile:
            # matrix array used for >1 devices, each line stores received data for each device
            for tmp in ret:
                for i in range(0, len(tmp)):
                    myFile.write(tmp[i])

    def initalConnect(self):
        # connect
        print("Connect")

        for dev in self.devices:
            try:
                dev.connect()
            except:
                print("Connect Error: " + dev.port_name)
                return

        # permission command
        print("Get Permission")
        for dev in self.devices:
            dev.getPermission()

    def stopHeat(self):
        print("stop heating")
        for dev in self.devices:
            dev.getStopAction()

    # define the procedure for whole test
    def run(self):

        self.collectPreCondition()

        #write header
        with open(self.log_name,'a+') as myFile:
            myFile.write('\n')
            myFile.write("Time[s]")
            for dev in self.devices:
                for cmd in dev.collect_cmd:
                    # judge if more than 1 parameters received, if yes, split cmd like XP0139_0, XP0139_1, XP0139_2
                    # <class 'list'>: [('XP0146', 1, 1), ('XP0139', 3, 1)]
                    if cmd[1] == 1:
                        myFile.write(','+cmd[0])
                    else:
                        for i in range(0, cmd[1]):
                            myFile.write(','+cmd[0]+'_' + str(i))
            myFile.write('\n')

        #set waiting timer, just collect all results
        #interval = self.waiting_time / self.waiting_counts
        self.waiting_counts = int(self.waiting_time/self.WaitCool_interval)
        self.heating_counts = int(self.heating_time/self.heating_interval)
        self.cooling_counts = int(self.cooling_time/self.WaitCool_interval)

        schedule = sched.scheduler(time.time, time.sleep)

        #print("start waiting")

        for i in range(self.waiting_counts):
            schedule.enter(i*self.WaitCool_interval, 0, self.collectAllDevice)
        schedule.run()
        self.if_start = False
        
        #set heating timer, start heating and collect all results
        #interval = self.heating_time / self.heating_counts
        schedule = sched.scheduler(time.time, time.sleep)

        #sleepTime = float(self.WaitCool_interval)
        #time.sleep(sleepTime)

        #print("start heating")
        for dev in self.devices:
            dev.getStartAction()

        for i in range(self.heating_counts):
            schedule.enter(i*self.heating_interval, 0, self.collectAllDevice)
        schedule.run()
        self.if_start = False
        
        #set cooling timer, stop heating and collect all results
        #interval = self.cooling_time / self.cooling_counts
        schedule = sched.scheduler(time.time, time.sleep)
        
        #print("stop heating")
        for dev in self.devices:
            dev.getStopAction()

        #sleepTime = 0.8 + self.WaitCool_interval
        #time.sleep(sleepTime)

        for i in range(self.cooling_counts):
            schedule.enter(i*self.WaitCool_interval, 0, self.collectAllDevice)
        schedule.run()

    def stopHeat(self):
        print("stop heating")
        for dev in self.devices:
            dev.getStopAction()
