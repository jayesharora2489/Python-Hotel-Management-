
import string
from test.test_fileinput import LineReader


#----------global variables / lists----------#

confirmation_counter = 0
bedroom_list = ['101','202','303','404','505']
reservation_list = []
reserved_room_no=[]
reserved_room=[]

def line_reader():
    '''takes in one line of input and calls appropriate functions'''
    while(True):
        print("NR: New Reservation")
        print("DR: Delete Reservation")
        print("RG: Reservation Search by Guest Name")
        print("RL: Reservation Search by Room Number")
        print("EX : EXIT")
        
        command=raw_input("Enter the code : ")
        command=command.upper()
        if command == 'NR':
            new_reservation()
        elif command == 'DR':
            delete_reservation()
        elif command == 'RG':
            reservations_by_guest()
        elif command == 'RL':
            display_reservation_list()
        elif command == 'EX':
            break
        else:
            print('Invalid command')
    
def dashes():
    return '------------------------------------'

def display_bedroom_list():
    '''prints items in bedroom_list'''
    global bedroom_list
    print('Number of bedrooms in service:\t', len(bedroom_list))
    print(dashes())
    for bed in bedroom_list:
        print(bed)
        
def new_reservation():
    '''creates a new reservation and adds it to reservation_list'''
    global reservation_list,reserved_room
    global bedroom_list
    global confirmation_counter
    global Reservation
    global reserved_room_no
    #chop up input to get variables
    print(dashes())
    print("     |Enter customer details|    ")
    print(dashes())
    name=raw_input("Enter customer name       : ")
    address=raw_input("Enter City             : ")
    phoneno=raw_input("Enter Mobile no        : ")
    arrival =raw_input("Enter arrival date    : ")
    departure=raw_input("Enter departure date :")
    
    while(True):
        display_bedroom_list()
        room_no=raw_input("Enter Room no. : ")
        
        '''if (room_no in bedroom_list):'''
        if(room_no in bedroom_list ):
            confirmation_counter+=1
            reservation =[name, address, phoneno, arrival, departure, room_no]
            reservation_list.append(reservation)
            print reservation_list
            print('Reserving room '+str(room_no)+' for '+name+' -- Confirmation # ' + str(confirmation_counter))
            print('(arriving ' + arrival + ', departing ' + departure + ' )')
            bedroom_list.remove(room_no)
            reserved_room_no.append(room_no)
            reserved_room.append(reservation)
            print("Room reserved !! ")
            
            save()
            
            break
        
        elif(room_no in reserved_room_no):
            print("Sorry, can't reserve room ",room_no,'(',arrival,' to ',departure,"); \n it is already booked (conf # ",str(confirmation_counter))
        else:
            print("Sorry, can't reserve room", room_no,'; room not in service')
        

def delete_reservation():
    while(True):
        print("Rooms reserved are : ")
        print('\n'.join(reserved_room_no))
        room_no=raw_input("Enter Room no. : ")
        if(room_no in reserved_room_no):
            room=[]
            for i in range(len(reserved_room)):
                if(reserved_room[i][5]==room_no):
                    room=reserved_room[i]
                    break
            reserved_room.remove(room)
            bedroom_list.append(room_no)
            reserved_room_no.remove(room_no)
            save()
            return
        else:
            print("Sorry, no reserved room with number", room_no,'; room not in service')

def reservations_by_guest():
    name=raw_input("Enter guest name : ").lower()
    
    f=False
    for room in reserved_room:
        if(room[0].lower().find(name)!=-1):
            print_room_details(room)
            f=True
            
    if(not f):
        print('Not found.')

def display_reservation_list():
    print('\n'.join(reserved_room_no))
    room_no=raw_input("Enter Room number : ")
    
    f=False
    for room in reserved_room:
        if(room[5]==room_no):
            print_room_details(room)
            f=True

    if(not f):
        print('Not found.')

def print_room_details(room):
    print(dashes())
    print(
"""
Name:%s
Address:%s
Phone number:%s
Arrival date:%s
Departure date:%s
Room number:%s
"""%tuple(room)
        )
    print(dashes())

def save():
    global reserved_room
    
    fl=open('data.txt','w')
    
    for room in reserved_room:
        fl.write('\n'.join(room)+'\n')
    
    fl.close() 
        
def load_data():
    global reserved_room,bedroom_list,reserved_room_no
    fl=open('data.txt','r')
    data=fl.read().split('\n')
    
    room=[]
    for i in range(len(data)):
        line=data[i]
        if(line.strip()!=''):
            room.append(line)
            if(i%6==5):
                reserved_room.append(room)
                room=[]
                bedroom_list.remove(line)
                reserved_room_no.append(line)
                
        
    fl.close()

load_data()
line_reader()
    