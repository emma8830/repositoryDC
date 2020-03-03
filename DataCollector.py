import sys, os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
#sys.path.append('C:\\Python35-32\\Lib\\site-packages')
#sys.path.append('C:\\Python35-32\\Lib\\site-packages\\PyQt5\\Qt\\bin')

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
	
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit,   QTextEdit, QGridLayout, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from DeviceControl_new import Device
from TestWgtRunning_new import Tester


class Datacollector(QWidget):

    def __init__(self,parent=None):
        super(Datacollector,self).__init__(parent)
        self.input_cmd_collections = []
        self.dev = None
        self.tester = None
        self.PowerMeter = None
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        grid.setSpacing(15)

        self.setLayout(grid)

        self.setGeometry(200, 200, 1200, 300)
        self.setWindowTitle('DataCollector')

        # layout for commands input
        self.Cmd_label = QLabel('Input the commands you want to collect:')
        self.cmd_lineEdit_list = []
        for i in range(0, 14):
            self.cmd_lineEdit_list.append(QLineEdit())

        self.Empty_17 = QLabel()
        self.Empty_18 = QLabel()

        # set position
        grid.addWidget(self.Cmd_label, 0, 0, 1, 3)
        grid.addWidget(self.cmd_lineEdit_list[0], 1, 0, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[1], 1, 1, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[2], 1, 2, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[3], 1, 3, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[4], 1, 4, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[5], 1, 5, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[6], 1, 6, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[7], 2, 0, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[8], 2, 1, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[9], 2, 2, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[10], 2, 3, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[11], 2, 4, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[12], 2, 5, 1, 1)
        grid.addWidget(self.cmd_lineEdit_list[13], 2, 6, 1, 1)

        grid.addWidget(self.Empty_17, 3, 0, 1, 8)
        grid.addWidget(self.Empty_18, 11, 0, 1, 8)

        # layout for COMs
        self.COM1_Label = QLabel('COM')
        #self.PowerMeter_COM_Label = QLabel('PowerMeter COM')
        #self.PowerMeter_COM_No = QLineEdit()
        self.COM1_No = QLineEdit()
        self.COM1_Baud_Label = QLabel('Baudrate')
        self.COM1_Baud_ComboBox = QtWidgets.QComboBox()
        self.COM1_Baud_ComboBox.addItem('9600')
        self.COM1_Baud_ComboBox.addItem('19200')
        self.COM1_Bit_Label = QLabel('Bit')
        self.COM1_Bit_ComboBox = QtWidgets.QComboBox()
        self.COM1_Bit_ComboBox.addItem('8')
        self.COM1_Bit_ComboBox.addItem('7')
        self.COM1_Bit_ComboBox.addItem('6')
        self.COM1_Bit_ComboBox.addItem('5')
        self.COM1_Parity_Label = QLabel('Parity')
        self.COM1_Parity_ComboBox = QtWidgets.QComboBox()
        self.COM1_Parity_ComboBox.addItem('N')
        self.COM1_Parity_ComboBox.addItem('E')
        self.COM1_Parity_ComboBox.addItem('O')
        self.COM1_Parity_ComboBox.addItem('M')
        self.COM1_Parity_ComboBox.addItem('S')
        self.COM1_Stopbit_Label = QLabel('Stopbit')
        self.COM1_Stopbit_ComboBox = QtWidgets.QComboBox()
        self.COM1_Stopbit_ComboBox.addItem('1')
        self.COM1_Stopbit_ComboBox.addItem('1.5')
        self.COM1_Stopbit_ComboBox.addItem('2')

        # set position
        grid.addWidget(self.COM1_Label, 4, 0, 1, 1)
        #grid.addWidget(self.PowerMeter_COM_Label, 9, 0, 2, 1)
        #grid.addWidget(self.PowerMeter_COM_No, 9, 1, 2, 1)
        grid.addWidget(self.COM1_No, 4, 1, 1, 1)
        grid.addWidget(self.COM1_Baud_Label, 5, 0, 1, 1)
        grid.addWidget(self.COM1_Baud_ComboBox, 5, 1, 1, 1)
        grid.addWidget(self.COM1_Bit_Label, 6, 0, 1, 1)
        grid.addWidget(self.COM1_Bit_ComboBox, 6, 1, 1, 1)
        grid.addWidget(self.COM1_Parity_Label, 7, 0, 1, 1)
        grid.addWidget(self.COM1_Parity_ComboBox, 7, 1, 1, 1)
        grid.addWidget(self.COM1_Stopbit_Label, 8, 0, 1, 1)
        grid.addWidget(self.COM1_Stopbit_ComboBox, 8, 1, 1, 1)

        # layout for heating parameters
        HeatTemp_Label = QLabel('Heat temp[℃]:')
        self.HeatTemp_Line = QLineEdit()
        #HeatTempUnit_Label = QLabel('℃')
        HeatTime_Label = QLabel('Heat time[s]:')
        self.HeatTime_Line = QLineEdit()
        #HeatTimeUnit_Label = QLabel('seconds')
        HeatInterval_Label = QLabel('Heat interval[s]:')
        self.HeatInterval_Line = QLineEdit()

        WaitTime_Label = QLabel('Wait Time[s]:')
        self.WaitTime_Line = QLineEdit()
        CoolTime_Label = QLabel('Cool Time[s]:')
        self.CoolTime_Line = QLineEdit()
        Interval_Label = QLabel('Interval[s]:')
        self.Interval_Line = QLineEdit()

        self.StartTest_Button = QtWidgets.QPushButton('Start Test')
        self.StopHeat_Button = QtWidgets.QPushButton('Stop Heating')
        self.CmdConfirm_Button = QtWidgets.QPushButton('Confirm All Inputs')

        # set position
        grid.addWidget(HeatTemp_Label, 4, 3, 1, 1)
        grid.addWidget(self.HeatTemp_Line, 4, 4, 1, 1)
        #grid.addWidget(HeatTempUnit_Label, 4, 5, 1, 1)

        grid.addWidget(HeatTime_Label, 5, 3, 1, 1)
        grid.addWidget(self.HeatTime_Line, 5, 4, 1, 1)
        #grid.addWidget(HeatTimeUnit_Label, 5, 5, 1, 1)

        grid.addWidget(HeatInterval_Label, 6, 3, 1, 1)
        grid.addWidget(self.HeatInterval_Line, 6, 4, 1, 1)

        grid.addWidget(WaitTime_Label, 4, 5, 1, 1)
        grid.addWidget(self.WaitTime_Line, 4, 6, 1, 1)
        grid.addWidget(CoolTime_Label, 5, 5, 1, 1)
        grid.addWidget(self.CoolTime_Line, 5, 6, 1, 1)
        grid.addWidget(Interval_Label, 6, 5, 1, 1)
        grid.addWidget(self.Interval_Line, 6, 6, 1, 1)

        grid.addWidget(self.StartTest_Button, 8, 5, 1, 2)
        #grid.addWidget(self.StopHeat_Button, 10, 5, 1, 2)
        grid.addWidget(self.CmdConfirm_Button, 8, 3, 1, 2)

        self.CmdConfirm_Button.clicked.connect(self.SetPara)
        self.StartTest_Button.clicked.connect(self.StartTest)
        #self.StopHeat_Button.clicked.connect(self.StopHeat)

    #slot function for start heat button
    def StartTest(self):
        self.ConfiRunTest()
        #print('StartTest triggerd by clicking')

    def StopHeat(self):
        #print('Stop heating triggerd by clicking')
        Tester.stopHeat()

    def SetPara_PowerMeter(self):
        self.PowerMeter_COM_parameters = []
        self.PowerMeter_COM_parameters.append(self.PowerMeter_COM_No.text())
        return self.PowerMeter_COM_parameters

    #slot function for confirm button
    def SetPara(self):

        # generate cmd list
        self.input_cmd_collections = []
        for cmd_lineEdit in self.cmd_lineEdit_list:
            self.input_cmd_collections.append(cmd_lineEdit.text())
            #print(cmd_lineEdit.text())

        # generate com parameters
        self.COM_parameter_list = []
        self.COM_parameter_list.append(self.COM1_No.text())
        self.COM_parameter_list.append(self.COM1_Baud_ComboBox.currentText())
        self.COM_parameter_list.append(self.COM1_Bit_ComboBox.currentText())
        self.COM_parameter_list.append(self.COM1_Parity_ComboBox.currentText())
        self.COM_parameter_list.append(self.COM1_Stopbit_ComboBox.currentText())
        #for i in self.COM_parameter_list:
            #print(i)

        # generate heat parameters
        self.heat_parameter_list = []
        self.heat_parameter_list.append(self.HeatTemp_Line.text())  #0
        self.heat_parameter_list.append(self.HeatTime_Line.text())  #1
        self.heat_parameter_list.append(self.HeatInterval_Line.text()) #2
        self.heat_parameter_list.append(self.WaitTime_Line.text())  #3
        self.heat_parameter_list.append(self.CoolTime_Line.text())  #4
        self.heat_parameter_list.append(self.Interval_Line.text())  #5
        #for i in self.heat_parameter_list:
            #print(i)

        # return cmd list, com parameters, heat parameters
        return self.input_cmd_collections, self.COM_parameter_list, self.heat_parameter_list

    def ConfiRunTest(self):
        # Create device control object, the serial port device
        self.dev = Device()
        collect_cmds, com_parameters, test_parameters = self.SetPara()

        # Port setting
        self.dev.port_name = 'COM' + com_parameters[0]
        self.dev.baudrate = com_parameters[1]
        self.dev.bit = int(com_parameters[2])
        self.dev.parity = com_parameters[3]
        self.dev.stopbits = int(com_parameters[4])

        # #Permission command set, unlock all command before use them, no recording data
        self.dev.addPermission("XP0000 4712")
        self.dev.addPermission("XM0000 4713")
        self.dev.addPermission("ZZ00 4799")

        # create device object for Power Meter
        #self.PowerMeter = Device()
        #powerMeter_com = self.SetPara_PowerMeter()

        # Get serial Port no. for power meter
        #self.PowerMeter.port_name = 'COM' + powerMeter_com

        # Create the testing object
        self.tester = Tester()
        self.tester.addDevice(self.dev)
        #self.tester.addDevice(self.PowerMeter)
        self.tester.initalConnect()

        # Once Command, send & record reply data only once
        self.dev.addOnceCollectCommand("XP0304")
        self.dev.addOnceCollectCommand("XP0361")

        # set test parameters
        self.tester.waiting_time = float(test_parameters[3])
        self.tester.WaitCool_interval = float(test_parameters[5])
        self.tester.cooling_time = float(test_parameters[4])
        self.tester.heating_time = float(test_parameters[1])
        self.tester.heating_temp = test_parameters[0]
        self.tester.heating_interval = float(test_parameters[2])

        # Once Command, send & record reply data only once
        heat_command = "XM0028 1 " + self.tester.heating_temp + ' 0'
        self.dev.addStartCommand(heat_command)
        self.dev.addStopCommand("XM0028 0")

        # add all input collected commands
        for i in range(len(collect_cmds)):
            if collect_cmds[i] == '':
                continue
            else:
                self.dev.addCollectCommand(collect_cmds[i])

        import datetime
        nowtime = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        #self.tester.log_name = "WaitHeatCool_6Min_Results_" + nowtime + ".csv"
        self.tester.log_name = "Wait" + str(int(self.tester.waiting_time)) + "sec_Heat" + str(int(self.tester.heating_time)) + "sec_Cool" + str(int(self.tester.cooling_time)) + "sec_Results_" + nowtime + ".csv"

        self.tester.run()


if __name__ == "__main__":
        app = QApplication(sys.argv)
        DataCollector_1 = Datacollector()
        DataCollector_1.show()
        sys.exit(app.exec_())