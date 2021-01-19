import lib.crc as crc

def runtest():
    data = b"10011101" #data to be sent
    mesg = crc.chksum(data)

    print("Message:   %s" % data)
    print("After CRC: %s" % mesg)

    corrupt_data = mesg.replace(b'0',b'',1) #data received

    print("Corrupted: %s" % corrupt_data)
    print("Verification:", crc.verify(corrupt_data) == False
     and "Bad transmission as expected."
     or  "Something unexpected happened, verify returns True.")
