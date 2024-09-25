#!/usr/bin/env python3
import argparse
import os
import sys
from time import sleep
import pymysql

import grpc
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../utils/'))
import p4runtime_lib.bmv2
import p4runtime_lib.helper
from p4runtime_lib.error_utils import printGrpcError
from p4runtime_lib.switch import ShutdownAllSwitchConnections

def printCounter(p4info_helper, sw, counter_name, index):
    """
    Reads the specified counter at the specified index from the switch. In our
    program, the index is the tunnel ID. If the index is 0, it will return all
    values from the counter.

    :param p4info_helper: the P4Info helper
    :param sw:  the switch connection
    :param counter_name: the name of the counter from the P4 program
    :param index: the counter index (in our case, the tunnel ID)
    """
    for response in sw.ReadCounters(p4info_helper.get_counters_id(counter_name), index):
        for entity in response.entities:
            counter = entity.counter_entry
            print("%s %s %d: %d packets (%d bytes)" % (
                sw.name, counter_name, index,
                counter.data.packet_count, counter.data.byte_count
            ))
    
    return counter.data.byte_count


def main(p4info_file_path, bmv2_file_path):
    # Instantiate a P4Runtime helper from the p4info file
    p4info_helper = p4runtime_lib.helper.P4InfoHelper(p4info_file_path)

    try:
        # Create a switch connection object for s1 and s2;
        # this is backed by a P4Runtime gRPC connection.
        # Also, dump all P4Runtime messages sent to switch to given txt files.
        s1 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s1',
            address='127.0.0.1:50051',
            device_id=0,
            proto_dump_file='logs/s1-p4runtime-requests.txt')
        s2 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s2',
            address='127.0.0.1:50052',
            device_id=1,
            proto_dump_file='logs/s2-p4runtime-requests.txt')
        s3 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s3',
            address='127.0.0.1:50053',
            device_id=2,
            proto_dump_file='logs/s3-p4runtime-requests.txt')
        s4 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s4',
            address='127.0.0.1:50054',
            device_id=3,
            proto_dump_file='logs/s4-p4runtime-requests.txt')
        s5 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s5',
            address='127.0.0.1:50055',
            device_id=4,
            proto_dump_file='logs/s5-p4runtime-requests.txt')
        s6 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s6',
            address='127.0.0.1:50056',
            device_id=5,
            proto_dump_file='logs/s6-p4runtime-requests.txt')

        # Send master arbitration update message to establish this controller as
        # master (required by P4Runtime before performing any other write operation)
        s1.MasterArbitrationUpdate()
        s2.MasterArbitrationUpdate()
        s3.MasterArbitrationUpdate()
        s4.MasterArbitrationUpdate()
        s5.MasterArbitrationUpdate()
        s6.MasterArbitrationUpdate()

        count1_ = 0
        count2_ = 0
        count3_ = 0
        count4_ = 0
        count5_ = 0
        count6_ = 0
        BW = 10.0
        while True:
            sleep(5)
            print('\n----- Reading tunnel counters -----')
            count1 = printCounter(p4info_helper, s1, "MyIngress.port_counter", 2)
            #Band1 = BW - float((count1 - count1_)*8)/5.0/1024.0  #Mb
            Band1 = band(count1, count1_, BW)
            count1_ = count1
            print("Band1:%f" % Band1)
            sql_insert(1, Band1)

            count2 = printCounter(p4info_helper, s2, "MyIngress.port_counter", 2)
            Band2 = band(count2, count2_, BW)
            count2_ = count2
            print("Band2:%f" % Band2)
            sql_insert(2, Band2)

            count3 = printCounter(p4info_helper, s3, "MyIngress.port_counter", 1)
            Band3 = band(count3, count3_, BW)
            count3_ = count3
            print("Band3:%f" % Band3)
            sql_insert(3, Band3)

            count4 = printCounter(p4info_helper, s4, "MyIngress.port_counter", 3)
            Band4 = band(count4, count4_, BW)
            count4_ = count4
            print("Band4:%f" % Band4)
            sql_insert(4, Band4)

            count5 = printCounter(p4info_helper, s5, "MyIngress.port_counter", 2)
            Band5 = band(count5, count5_, BW)
            count5_ = count5
            print("Band5:%f" % Band5)
            sql_insert(5, Band5)

            count6 = printCounter(p4info_helper, s6, "MyIngress.port_counter", 3)
            Band6 = band(count6, count6_, BW)
            count6_ = count6
            print("Band6:%f" % Band6)
            sql_insert(6, Band6)
        
   
    except KeyboardInterrupt:
        print(" Shutting down.")
    except grpc.RpcError as e:
        printGrpcError(e)
        
    ShutdownAllSwitchConnections()

def band(count, count_, BW):
    band = BW - float((count - count_)*8)/5.0/1024.0  #Mb
    return band

#mysql connection
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'INT_data'
}
connection = pymysql.connect(user=config['user'],
                                password=config['password'],
                                host=config['host'],
                                database=config['database'],
                                port=3306,
                                cursorclass=pymysql.cursors.DictCursor)




def sql_insert(swid, Band):
    try:
        with connection.cursor() as cursor:
            # insert
            add_data = ("INSERT INTO `INT_data`.`int_data` (`switch_id`, `Bandwidth`)"
                            " VALUES (%s, %s) "
                            " ON DUPLICATE KEY UPDATE "
                            " `Bandwidth` = VALUES(`Bandwidth`)")
            
            cursor.execute(add_data, (swid, Band))
        connection.commit()
        print("Successfully added sw_id INT data")

    except pymysql.MySQLError as e:
        print(e)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P4Runtime Controller')
    parser.add_argument('--p4info', help='p4info proto in text format from p4c',
                        type=str, action="store", required=False,
                        default='./build/INT.p4.p4info.txt')
    parser.add_argument('--bmv2-json', help='BMv2 JSON file from p4c',
                        type=str, action="store", required=False,
                        default='./build/INT.json')
    args = parser.parse_args()
    main(args.p4info, args.bmv2_json)

