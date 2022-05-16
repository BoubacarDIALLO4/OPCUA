import random
import time
from glob import glob, iglob
import os
from itertools import cycle

from opcua import Server

# list_barcode_index = ['36','37','38','44','49'] # '013', '021', '022', '023', '031', '041', '042', '052', '082', '111', '122', '280',
#                       #'373', '380', '430', '440', '450']
# production_line_index = "05J"

def get_barcode_from_fake_images() -> list:
    
    #fake_images_path = os.getenv('FAKE_IMAGES_DIR')
    fake_images_path="D:\AIVI_FCM\Test\etupes\left_fake_images\*"
    files = []
    barcode_list = []
    without_empty_strings = []


    for path in sorted(list(iglob(fake_images_path))):
        barcode = os.path.basename(path).split("_")[1]
        #print(f'path : {barcode}')
        barcode_list.append(barcode)
        #without_empty_strings = [string for string in barcode_list if string != ""]
        without_empty_strings = ' '.join(barcode_list).split()
    return without_empty_strings

p = get_barcode_from_fake_images()
print(p)
# the_list_of_barcode = get_barcode_from_fake_images()

# def generate_random_barcode() -> str:
#     barcode_index = random.choice(list_barcode_index)
#     code_head = '22328'
#     code_tail = '200123231307'
#     return code_head + barcode_index + production_line_index + code_tail


def change_tag_value(opcua_variable, tag_value):
    opcua_variable.set_value(tag_value)
    print(f'tag value changed for {opcua_variable}: {tag_value}')


def create_opcua_variable(objects, idx, value, snum, line, station, barcode_type='str'):
    if barcode_type == 'byte':
        value = list(map(ord, value))
    line_object = objects.add_object(idx, line)
    station_object = line_object.add_object(idx, station)
    barcode_variable = station_object.add_variable(idx, "barcodeVariable", value)
    trigger_variable = station_object.add_variable(idx, "triggerVariable", snum)
    return [barcode_variable, trigger_variable]


def get_tag_id(idx, opcua_variable):
    opcua_tag_id = f'ns={idx};i={opcua_variable.nodeid.Identifier}'
    return opcua_tag_id


def main():
    # setup our opcua_qualif
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/dsf/qualif/")

    # setup our own namespace, not really necessary but should as spec
    namespace = "qualif_environment_opcua_server"

    idx = server.register_namespace(namespace)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # variable for line 1
    barcode_value_line1_station1_init = []
    barcode_value_line1_station1_init += get_barcode_from_fake_images()
    line1 = "line1"
    station1 = "station1"
    station2 = "station2"
    serial_number_go = True
    serial_number_not_go =  False

    # Init opcua variables (serial number value = 0 and a random barcode value) for line 1 station 1
    opcuaVariables_l1_s1 = create_opcua_variable(objects, idx, barcode_value_line1_station1_init,
                                                 serial_number_not_go, line1, station1)

    # process barcode tag id and trigger tag id for line1 station1
    barcode_tag_id_l1_s1 = get_tag_id(idx, opcuaVariables_l1_s1[0])
    trigger_tag_id_l1_s1 = get_tag_id(idx, opcuaVariables_l1_s1[1])
    print('line1 station1 barcode', opcuaVariables_l1_s1[0], barcode_tag_id_l1_s1)
    print('line1 station1 trigger', opcuaVariables_l1_s1[1], trigger_tag_id_l1_s1)

    # line 1 station 2
    barcode_value_line1_station2_init = get_barcode_from_fake_images()
    opcuaVariables_l1_s2 = create_opcua_variable(objects, idx, barcode_value_line1_station2_init,
                                                 serial_number_not_go, line1, station2)

    # process barcode tag id and trigger tag id for line1 station1
    barcode_tag_id_l1s2 = get_tag_id(idx, opcuaVariables_l1_s2[0])
    trigger_tag_id_l1s2 = get_tag_id(idx, opcuaVariables_l1_s2[1])
    print('line1 station1 barcode', opcuaVariables_l1_s2[0], barcode_tag_id_l1s2)
    print('line1 station1 trigger', opcuaVariables_l1_s2[1], trigger_tag_id_l1s2)

    server.start()
    count = 0
    #time.sleep(60)
    for count in cycle(range(len(barcode_value_line1_station1_init))):
    #while True:
        # Get new barcode for line 1 station 1 and update barcode variable
        barcode_value_line1_station1 = barcode_value_line1_station1_init[count]
        print(f'New barcode on station 1: {barcode_value_line1_station1}')
        change_tag_value(opcuaVariables_l1_s1[0], barcode_value_line1_station1)
        time.sleep(1)
        # Trigger pipeline by changing sequence number
        change_tag_value(opcuaVariables_l1_s1[1], serial_number_go)
        time.sleep(2)
        change_tag_value(opcuaVariables_l1_s1[1], serial_number_not_go)
        time.sleep(3)
    

        # Update station 2 with barcode of station 1
      #  change_tag_value(opcuaVariables_l1_s2[0], barcode_value_line1_station1)
       # time.sleep(3)
       # change_tag_value(opcuaVariables_l1_s2[1], serial_number_go)
       # change_tag_value(opcuaVariables_l1_s2[1], serial_number_not_go)
       # time.sleep(14)
    #time.sleep(3600)


if __name__ == "__main__":
    main()    
