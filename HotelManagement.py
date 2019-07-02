from collections import namedtuple
import datetime
import string

Reservation = ('Reservation','room',' arr_date', 'dept_date','guest_name', 'confirmation_num')

#----------global variables / lists----------#

confirmation_counter = 0
bedroom_list = [101,202,303,404,505]
reservation_list = []

#main function
'''def Anteater_BandB (file_name):
    main function. reads a file named file_name
    infile = open(file_name, 'r')
    data = infile.readlines()
    infile.close()
    for line in data:
        line = line.strip()
        line_reader(line)'''

def line_reader():
    '''takes in one line of input and calls appropriate functions'''
    command=raw_input("Enter the code : ")
    command.upper()
    if command == '**':
        pass;
    elif command == 'BL':
        display_bedroom_list()
    elif command == 'PL':
        print_line(rest_of_input)
    elif command == 'BD':
        delete_bedroom(rest_of_input)
    elif command == 'NR':
        new_reservation(rest_of_input)
    elif command == 'RL':
        display_reservation_list()
    elif command == 'RD':
        delete_reservation(rest_of_input)
    elif command == 'RB':
        reservations_by_bedroom(rest_of_input)
    elif command == 'RC':
        reservations_by_guest(rest_of_input)
  
def dashes():
    return '------------------------------------'

#DL
def display_bedroom_list():
    '''prints items in bedroom_list'''
    global bedroom_list
    print('Number of bedrooms in service:\t', len(bedroom_list))
    print(dashes())
    for bed in bedroom_list:
        print(bed)


#BD

def delete_bedroom(room):
    '''deletes specified room from the list. print error message if
    room isn't on the list'''
    global bedroom_list
    if room in bedroom_list:
        bedroom_list.remove(room)
        cancel_room_reservations(room)
    else:
        print('Sorry, can\'t delete room '+room+'; it is not in service now')


def new_reservation():
    '''creates a new reservation namedtuple and adds it to reservation_list'''
    global reservation_list
    global bedroom_list
    global confirmation_counter
    #chop up input to get variables
    
    room_request = raw_input("Enter the room no to allot : ") 
    if (room_request in bedroom_list) and (allow_reservation(arrival, departure)) and room_not_taken(room_request) :
        confirmation_counter+=1
        reservation = Reservation(room_request, arrival, departure, name, confirmation_counter)
        reservation_list.append(reservation)
        print('Reserving room '+room_request+' for '+name+' -- Confirmation # ' + str(confirmation_counter))





#RL

def display_reservation_list():
    global reservation_list
    print('Number of reservations:\t' + str(len(reservation_list)))
    print('{:>3}{:>4}{:>11}{:>11}{}{}'.format('No.','Rm.','Arrive','Depart',' ','Guest'))
    print(dashes())
    for r in reservation_list:
        print('{:>3}{:>4}{:>11}{:>11}{}{}'.format(
            str(r.confirmation_num),r.room,r.arr_date,r.dept_date,' ',r.guest_name))

#RD
def delete_reservation(num):
    '''takes in a confirmation number and deletes the reservation with that confirmation number'''
    global reservation_list
    #reservation_list.sort(key = conf_num, reverse=False)
    confirmation_list = []
    for r in reservation_list:
        confirmation_list.append(r.confirmation_num)
    if (int(num) in confirmation_list):
        reservation_index = confirmation_list.index(int(num)) #find where the reservation is in the list
        reservation_list.remove(reservation_list[reservation_index]) #delete the reservation with that index
    else:
        print("Sorry, can't cancel reservation; no confirmation number " + num)


#First: reject if arrival of guest A is later than departure date of guest A

def allow_reservation(arr,dept):
    '''takes in two dates as strings, converts them to dates to compare them,
    and determines whether, based on the arr and dept date, the reservation is valid
    '''
    if date(arr)>=date(dept):
        #print('can\'t leave before you arrive')
        return False
    return True

#Second: check conflicts with existing reservations

def room_not_taken(room_req):
    '''return true if room is taken'''

    #based on whether bedroom is free
    global reservation_list
    reserved_rooms = []
    for r in reservation_list:
        reserved_rooms.append(r.room) #list of strings of taken rooms
    if (room_req not in reserved_rooms):
        return True
    return False

def reservations_conflict(r1,r2):
    '''takes two reservations and compares them. return true if they conflict'''
    if (date(r1.arr_date)>=date(r2.arr_date) and date(r1.arr_date)<date(r2.dept_date)) or (date(r1.dept_date)>=date(r2.arr_date) and date(r1.dept_date)<date(r2.dept_date)):
            print('Sorry, can\'t reserve room '+room_request+'\t('+arrival+' to '+departure+');')
            print('it\'s already been booked')
            return True
    return False

#Finally, if user deletes bedroom, all reservations for that room are cancelled
def cancel_room_reservations(room):
    for r in reservation_list:
        if r.room == room:
            print('Deleting room',room,'forces cancellation of this reservation:')
            print('\t',r.guest_name,'arriving',r.arr_date,'and departing',r.dept_date,'(Conf. #',r.confirmation_num,')')
            delete_reservation(r.confirmation_num)


#RB
def reservations_by_bedroom(line):
    global reservation_list
    bedroom_reserve_list= []
    bedroom_num = line
    for r in reservation_list:
        if r.room == bedroom_num:
            bedroom_reserve_list.append(r)
    print("Reservations for room " + line +':')
    for re in bedroom_reserve_list:
        print(re.arr_date,' to ',re.dept_date, re.guest_name)
#RC
def reservations_by_guest(line):
    guest_reserve_list = []
    guest_name = line
    print('Reservation for',guest_name)
    for r in reservation_list:
        if r.guest_name == guest_name:
            print(r.arr_date + ' to ' + r.dept_date + ': room ' + r.room)

def display_guest(rl):
    '''takes in a reservation list and prints out guest name as well as room number
    '''
    for r in rl:
        print(r.guest_name+ '(room '+ r.room + ')')

def reserved_rooms(rl):
    '''takes in a list of reservations and returns a list of reserved rooms''' 
    reserved = []
    for r in rl:
        reserved.append(str(r.room))
    return reserved

#LA
def list_arrivals(line):
    guest_arrival_list = []
    guest_arrival = date(line)
    for r in reservation_list:
        if guest_arrival == date(r.arr_date):
            guest_arrival_list.append(r)
    print('Guests arriving on '+ line+ ':')
    display_guest(guest_arrival_list)

#LD
def list_departures(line):
    guest_departure_list = []
    guest_departure = date(line)
    for r in reservation_list:
        if guest_departure == date(r.dept_date):
            guest_departure_list.append(r)
    print('Guests departing on '+ line+ ':')
    display_guest(guest_departure_list)

#LF
def list_free_beds(line):
    global bedroom_list
    bedroom_requests = []
    two_dates = line.split()
    arr_date = two_dates[0]
    dept_date = two_dates[1]
    print('Bedrooms free between ' + arr_date + ' to ' + dept_date + ':')
    for r in reservation_list:
        if (date(dept_date)<=date(r.arr_date)) or (date(arr_date)>=date(r.dept_date)):
            bedroom_requests.append(str(r.room))
    for b in bedroom_list:
        if str(b) not in reserved_rooms(reservation_list):
            bedroom_requests.append(str(b))
    bedroom_requests = list(set(bedroom_requests))
    for beds in bedroom_requests:
        print(beds)

#LO
def list_occupied(line):
    global bedroom_list
    bedroom_requests = []
    two_dates = line[2:].split()
    arr_date = two_dates[0]
    dept_date = two_dates[1]
    print('Bedrooms occupied between ' + arr_date + ' to ' + dept_date + ':')
    for r in reservation_list:
        if not (date(dept_date)<=date(r.arr_date)) or (date(arr_date)>=date(r.dept_date)):
            bedroom_requests.append(str(r.room))
    bedroom_requests = list(set(bedroom_requests))
    for beds in bedroom_requests:
        print(beds)

