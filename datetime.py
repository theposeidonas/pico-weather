import socket
import struct
import time
import network
from machine import RTC

def connect_ntp():
    ntp_host = "pool.ntp.org"
    port = 123
    ntp_query = bytearray(48)
    ntp_query[0] = 0x1B
    addr = socket.getaddrinfo(ntp_host, port)[0][-1]
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    s.sendto(ntp_query, addr)
    msg = s.recv(48)
    s.close()
    
    val = struct.unpack("!I", msg[40:44])[0]
    epoch = val - 2208988800
    return epoch

def set_rtc():
    try:
        t = connect_ntp() + 3 * 3600
        tm = time.localtime(t)
        rtc = RTC()
        rtc.datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))
    except:
        pass

def get_time():
    rtc = RTC()
    current_time = rtc.datetime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(current_time[0], current_time[1], current_time[2], current_time[4], current_time[5], current_time[6])
