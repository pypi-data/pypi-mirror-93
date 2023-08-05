'''
Created on 2021年1月8日

@author: Administrator
'''
from zp_pycrc import *
def test_crc32():
    datas=b'\x01\x02\x03\x04\x05'
    r=cal_crc32_classcial(datas, 0xffffffff, 0x04c11db7, True, True, 0xffffffff)
    print(hex(r))
def test_crc16():   
    datas=b'\x01\x02\x03\x04\x05'
    print(len(datas),datas)
    crc=crc16_ccitt()
    print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
    crc=crc16_ccitt_false()
    print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
    crc=crc16_xmodem()
    print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
    crc=crc16_x25()
    print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
    crc=crc16_ibm()
    print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
    crc=crc16_usb()
    print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
    crc=crc16_maxim()
    print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
    crc=crc16_modbus()
    print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
    crc=crc16_dnp()
    print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))       
    crc=crc16( 0,0x8005, True, True, 0)
    print(crc.__class__.__name__,"%04X"%(crc.cal(datas)))
    crc=crc16_ibm()
    print("crc16_ibm __call__",hex(crc(datas)))
    b=cal_crc16_classcial(datas, 0,0x8005, True, True, 0)
    print("cal_crc16_classcial",hex(b))
    print('*******crc  ibm table*****')
    print([hex(i) for i in crc.crc_table])
def test_detect_crc16_algorithm ():
    data=b'\x01\x02\x03\x04\x05\x22\xec'
    results=[int('22ec',16),int('ec22',16)]
    print(results)
    r=detect_crc16_algorithm(data[0:-2],results)
    print(r)
if __name__ == '__main__':
    test_crc16()
    #test_crc32()
    test_detect_crc16_algorithm ()