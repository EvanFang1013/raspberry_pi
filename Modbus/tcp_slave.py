import sys
import modbus_tk
import modbus_tk.modbus as modbus
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import configparser
import logging
import threading
import datetime
import Adafruit_ADS1x15
import time

reader_flag=1


class Senreader_Thread(threading.Thread):
    def __init__(self,threadID,name,_server):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.name=name
        self.server=_server
    def Stop(self):
        print('stop value reader')
        reader_flag=0
        self.server._do_exit()
    def run(self):
        global reader_flag
        GAIN=2/3
        curtime=datetime.datetime.now()
        print('sensor value start reading...'+str(curtime)+"\n")
        try:
            
            while(reader_flag):
                ads_adr=71
                channel=0
                list=([])           
                for i in range (0,4):
                    ads_adr+=1
                    channel=0
                    adrs=0
                    adc=Adafruit_ADS1x15.ADS1115(ads_adr)
                #print(ads_adr)
                    for chanel in range (0,4):
                        sen_value=0
                        sen_value=adc.read_adc(int(channel),gain=GAIN)
                        channel=channel+1
                        adrs=channel+i*4
                        #list.append(sen_value)
                #time.sleep(1)
                #print(list)
                        
                        slaveread = self.server.get_slave(1)
                        slaveread.set_values('0', adrs, sen_value)
                        
                    
        except KeyboardInterrupt:
            reader_flag=0
            #self.server.stop()
##            self.server._do_exit()
            
                
        
class slave():
    def _init_(self):
        pass
    def sercreate(self,_slaveid,_localip,_port,_fuc):
         try:
        #Create the server
            
            #server = modbus_tcp.TcpServer(address=_localip,port=_port)
            server = modbus_tcp.TcpServer()
            
            logger.info("running...")
            #logger.info("enter 'quit' for closing the server")
                  
            server.start()
            print ('server start..')
            slave_1 = server.add_slave(_slaveid)
            print(_slaveid)
            #slave_1.add_block('0', cst.HOLDING_REGISTERS, 0, 100)
            slave_1.add_block('0', _fuc, 0, 100)
            senreader=Senreader_Thread(1,"Thread-1",server)
            senreader.start()
         except: 
            print('server create fail')
            #server.stop()
            #server._do_exit()
            
            
            
 
 

if __name__ == "__main__":
    
    slave1=slave()
    logger=modbus_tk.utils.create_logger(name="console",record_format="%(message)s")
    cfg=configparser.ConfigParser()
    cfg.read("/home/pi/Desktop/modbus_slave/config/modbus_slave.conf")
    localip=cfg.get("SLAVE","IP")
    port=cfg.get("SLAVE","PORT")
    slaveid=cfg.getint("SLAVE","SLAVEID")
    funcode=cfg.getint("SLAVE","FUNCTION")
    print(slaveid)
    slave1.sercreate(slaveid,localip,port,funcode)
    #senreader=Senreader_Thread(1,"Thread-1",60)
    print('ok')
    #senreader.start()

    
   
            
        
