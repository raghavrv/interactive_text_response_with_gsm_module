import serial
import math
import binascii
from time import sleep
from datetime import datetime
from datetime import date
from selenium import webdriver

global pnostr
pnostr  = '1822219771'
errcnt = 0
Date_Today = (date.today()).isoformat()
unicode_flag=0
EXT = 0
browser=webdriver.Firefox()
logfile = open('D:\\Programming\\RV SMS InteGrate\\Log Files\\' + Date_Today + '.txt','w+')
GSM_SET=[0x0040,0x00A3,0x0024,0x00A5,0x00E8,0x00E9,0x00F9,0x00EC,0x00F2,0x00E7,0x000A,0x00D8,0x00F8,0x000D,0x00C5,0x00E5,0x0394,0x005F,0x03A6,0x0393,0x039B,0x03A9,0x03A0,0x03A8,0x03A3,0x0398,0x039E,0x00A0,0x00C6,0x00E6,0x00DF,0x00C9,0x0020,0x0021,0x0022,0x0023,0x00A4,0x0025,0x0026,0x0027,0x0028,0x0029,0x002A,0x002B,0x002C,0x002D,0x002E,0x002F,0x0030,0x0031,0x0032,0x0033,0x0034,0x0035,0x0036,0x0037,0x0038,0x0039,0x003A,0x003B,0x003C,0x003D,0x003E,0x003F,0x00A1,0x0041,0x0042,0x0043,0x0044,0x0045,0x0046,0x0047,0x0048,0x0049,0x004A,0x004B,0x004C,0x004D,0x004E,0x004F,0x0050,0x0051,0x0052,0x0053,0x0054,0x0055,0x0056,0x0057,0x0058,0x0059,0x005A,0x00C4,0x00D6,0x00D1,0x00DC,0x00A7,0x00BF,0x0061,0x0062,0x0063,0x0064,0x0065,0x0066,0x0067,0x0068,0x0069,0x006A,0x006B,0x006C,0x006D,0x006E,0x006F,0x0070,0x0071,0x0072,0x0073,0x0074,0x0075,0x0076,0x0077,0x0078,0x0079,0x007A,0x00E4,0x00F6,0x00F1,0x00FC,0x00E0]

class logger(object):
	'''Contains methods to maintain a log of events'''
	def __init__(self, logFile = None):
		if logFile not None:
			self.logFile = logFile
		else:
			self.logActive = False
		
		
		

class modem(object):
	'''Contains the various methods to interface with the Serial port corresponding to the modem'''
	def __init__(self, port = '/dev/rfcomm0', logFile = None):
		'''Initializes the port for the modem interface.'''
		s = serial.Serial()
		s.port = port
		s.open()
		s.flushInput()
		s.flushOutput()
		s.writeTimeout=10
		s.write('at\r\n'.encode('UTF-8'))
		sleep(1)
		if s.read(s.inWaiting())==('at\r\n\r\nOK\r\n'.encode('UTF-8')):
			status = 'Success - Connected to modem at \'%s\''%(s.port)
			self.serialport = s
			self.connected = True
		else:
			status = 'Failure - Unable to connect to modem at \'%s\''%(s.port)
			s.close()
			self.serialport = None
			self.connected = False
		print status
		if logFile not None:
			self.logFile = logFile
		self.log = logger(logFile)
		log.write(status)
	def refreshPort(self, port = '/dev/rfcomm0')
		'''Refreshes the serial port'''
		self.serialport.close()
		self.connected = False
		self.__init__()
	def flushIO(self, FlushInput = True, FlushOutput = True, TwoPass = False):
		'''Flushes the input and output buffers of the serial port'''
		if self.connected == True:
			if FlushInput == True:
				self.serialport.flushInput()
			if FlushOutput == True:
				self.serialport.flushOutput()
		if TwoPass == True:
			sleep(10)
			flushIO()
		
	def write(self, atcommand = ''):
		'''Write a line of at+ command to the modem and returns its response'''
		sleep(1)
		self.flushIO()
		self.serialport.write(atcommand.encode('UTF-8'))
		self.serialport.write('\r\n'.encode('UTF-8'))
		status = 'AT Command Written to Modem : ' + atcommand + '\r\n'
		print(status)
		log.write( 
		
		
		



def log(logdata):
    global Date_Today
    global logfile
    if (date.today()).isoformat() != Date_Today:
        logfile.close()
        Date_Today = (date.today()).isoformat()
        logfile = open('D:\\Programming\\RV SMS InteGrate\\Log Files\\' + Date_Today + '.txt','w+')
        log(logdata)
    else:
        logfile.write('\n['+str(datetime.now())[11:16]+'] - '+logdata)

def sendsms_textmode(text, en = 0):
        global modem
        text = str(text)
        modem.write( 'at+cmgf=1\r\n'.encode('UTF-8') )
        sleep(0.5)
        modem.write( 'at+cmgs="+918122127917"\r\n'.encode('UTF-8') )
        sleep(0.5)
        modem.write( text.encode('UTF-8') )
        modem.write(chr(26).encode('UTF-8'))
        sleep(10)
        modem.write('at+cmgf=0\r\n'.encode('UTF-8'))
        sleep(0.5)
        log('MODEM_ACTIVITY_SENDSMS_TEXT : ' + modem.read(modem.inWaiting()).encode('utf-8','replace'))

def numtohexstr(num):
        hexnum = hex(num)
        return ( ('0' + hexnum[-1]) if (len(hexnum)==3) else hexnum[-2:] )

def txttohexstr(unicode_str):
    res = ''
    ii = 0
    for i in range(0, len(unicode_str)):
        if (unicode_str[ii:ii+2] !='\\\\') & (ii<len(unicode_str)):
            res += '00'
            #print(repr(unicode_str[ii]))
            #res += repr(unicode_str[ii].encode('hex'))[2:-1]
            res += repr(binascii.b2a_hex(binascii.a2b_qp(unicode_str[ii])))[2:-1]
        elif (unicode_str[ii:ii+2] =='\\\\') & (ii<len(unicode_str)):
            ii += 2
            for k in range (4):
                ii += 1
                res += unicode_str[ii]
    ii += 1
    return res


def sendsms_pdumode(text):
        global modem
        text = (repr(text)[2:-1]).replace('\\x','\\u00')
        hextext = txttohexstr(text)
        modem.close()
        sleep(1)
        modem.open()
        modem.write('at+cmgf=0\r\n'.encode('UTF-8'))
        sleep(0.5)
        print('in pdu mode')
        l = len(hextext)
        smsindexfile = open('D:\\Programming\\RV SMS InteGrate\\Log Files\\sms_index.txt','r+')
        sms_index=int(str(smsindexfile.readline()))
        smsindexfile.close()
        sms_index = 0 if (sms_index>255) else (sms_index+1)
        smsindexfile = open('D:\\Programming\\RV SMS InteGrate\\Log Files\\sms_index.txt','w+')
        smsindexfile.write(str(sms_index))
        smsindexfile.close()
        if(l>280):
            j = (l//268)+1
            k = 0
            for i in range (0,l,268):
                print('in concat of pdu mode')
                length = len(hextext[i:i+268]) // 2
                k += 1
                pdu = '0041000C9119'+pnostr+'0008'+numtohexstr(length+6)+'050003'+numtohexstr(sms_index)+numtohexstr(j)+numtohexstr(k)+ hextext[i:i+268]
                modem.write(('at+cmgs='+str((len(pdu)-2)//2)+'\r\n').encode('utf-8'))
                sleep(0.5)
                modem.write(pdu.encode('utf-8'))
                sleep(0.5)
                modem.write(chr(26).encode('utf-8'))
                sleep(10)
        else:
                length = len(hextext[0:280]) // 2
                pdu = '0001000C9119'+pnostr+numtohexstr(length)+hextext[0:280]
                modem.write(('at+cmgs='+str(len(pdu)-2)+'\r\n').encode('utf-8'))
                sleep(0.5)
                modem.write(pdu.encode('utf-8'))
                sleep(0.5)
                modem.write(chr(26).encode('utf-8'))
                sleep(10)
        log('MODEM_ACTIVITY_SENDSMS_PDU : ' + str(modem.read(modem.inWaiting())))
        
def MeaningEnglish(Word):
    browser.get('http://www.google.com/search?q=define%20'+Word)
    s = browser.page_source
    s = s.replace('\\xa0',' ')
    s = s.replace('\\xb7','.')
    s = s.replace('\\u02cc',',')
    s = s.replace('\\u02c8',"'")
    #s = s.encode('unicode_escape') #-- returns error for s.find()
    i = s.find('vk_ans vk_bk')
    j = s.find('>More info<')
    if i == -1:
        mean = "No Definition Found."
    else:
        mean = ''
        for k in range (0,j-i-1):
            if (s[i:j])[k] == '>':
                k += 1;
                while ( ((s[i:j])[k] != '<') & (k<(j-i-1)) ):
                    mean += (s[i:j])[k]
                    k += 1;
    return mean.encode('unicode_escape')

def slen(sms):
    smslenstr='0';
    for i in range(13,len(sms)):
        if(sms[i] == '\\'):
            break;
        else:
            smslenstr = smslenstr + sms[i]
    return int(smslenstr);


def d_gsm(data):
    j = 0
    smsdata = ''
    carry = 0
    for  i in range (0,len(data), 2):
        j = j % 7
        if(j ==0):
            carry = 0;
        j = j + 1
        t = int(data[i:i+2],16)
        t2 = t
        t = (t<<j) & 0xFF
        t = t>>j
        smsdata += chr(GSM_SET[ ( ( (t << (j-1)) + carry) ) ]);
        carry = t2 - t
        carry = carry>>(8-j)
        if(j ==7):
            smsdata += chr(GSM_SET[carry])
    return smsdata



def decod(sms):
    print(sms.find('+CMT'))
    print(sms.find('1822219771'))
    if(sms.find('+CMT')>0) and ((sms.find('1822219771')>0) or (sms.find('8904171961')>0)):
        log("Auth SMS Received : " + sms)
        sms_start = sms.find('07')
        sms_chr_len = int(sms[sms_start+52:sms_start+54],16)
        print('len of sms received : ' + str(sms_chr_len))
        sms_dat_len = int(math.ceil(float(sms_chr_len*7)/float(8)))
        sms_data_end = sms[sms_start:].find('\\') + sms_start
        sms_data_start = sms_data_end - sms_dat_len*2
        global pnostr
        pnostr = str(sms[sms_start+24:sms_start+34])
        print('sms from :' + pnostr)
        if sms[sms_start+16] == '4':
            sms_data_start += 12
        smsdata = ''
        if sms[sms_start+36:sms_start+38] == '08':
            log('#Encoding Type: UTF-8')
            for  ptr in range (sms_data_start, sms_data_end, 4):
                smsdata += chr(int(sms[ptr:ptr+4],16))
        elif sms[sms_start+36:sms_start+38] == '00':
            log('#Encoding Type: GSM')
            print(sms[sms_data_start:sms_data_end])
            smsdata = d_gsm(sms[sms_data_start:sms_data_end])
        else:
            smsdata = 'Decoding Error - Unknown Encoding' + sms[sms_start+36:sms_start+38]
        log('#SMS Data: ' + smsdata)
        return smsdata
    else:
        log("UnAuth SMS Received : " + sms)
    return 'error'

def parse(sms):
        decodedsms = decod(sms)
        print(decodedsms)
        if(decodedsms[0:4] == 'MENG'):
            sendsms_pdumode( MeaningEnglish(decodedsms[5:]) )
                
                
modem = set_comport()
print(str(modem))
while(EXT!=1):
    try:
        if(modem.inWaiting()>0):
            sleep(5)
            SMS = modem.read(modem.inWaiting())
            errcnt = 0
            SMS = repr(SMS)[2:-1]
            print(SMS)
            parse(SMS)
    except serial.SerialException:
        log("Ran into Serial Exception Error")
        sleep(5)
        modem.close()
        while(~init_modem()):
                if errcnt == 10:
                    EXT = 1
                    log('Max Error Count Reached -- Exiting.')
                    break
                else:
                        errcnt = errcnt + 1
                        log('INIT MODEM Failure -- Retrying after 1 min')
                        sleep(60)

print ("\nDefinition is : " + mean  )

browser.quit()
log.close()
