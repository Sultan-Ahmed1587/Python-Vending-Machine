import socket
import pickle
import csv

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# these like look for a connection from the client side and once found will state that the connection
#has been established meaning they are both connected to each other.

server.bind(('localhost', 9999))
server.listen(1)
print("Awaiting Cleint side to connect to server side")

socket_client,(host, port) = server.accept()
print(f'geting connection from {host} ({port})\n')
print(f'Connection sucsesful: {host}')

#opening and then reading the content within the csv file
f = open('Gapple_Stock.csv', 'r')
reader = csv.reader(f)


dictionary = {}
# replacing the csv and making it into a dictionary for manipulation of data.
for row in reader:
    dictionary[row[0]] = {'PrimaryKey':row[0], 'apple':row[1], 'price':float(row[2]), 'Quantity':int(row[3])}


while True:
    #these line show that the server is sending the Gapple.csv to the client side to be read from there.
    pickle_obj = pickle.dumps(dictionary)
    socket_client.send(pickle_obj)

    # getting customer transaction from the client side.
    recv_data2 = socket_client.recv(1024)
    pickle_customerpayment = pickle.loads(recv_data2)

    # this line stats that the server is getting updates to the stock from the client side.
    r_data = socket_client.recv(1024)
    pickle_obj = pickle.loads(r_data)


    new_list = []
    # reading throguht the pickled list.
    for i in pickle_obj:
        new_list.append(i)


    #upadteing the Gapple stock csv database.
    with open('Gapple_Stock.csv', 'w') as file:
        for i in new_list:
            pk = i.get('PrimaryKey')
            apple = i.get('apple')
            Pricing = i.get('Price')
            stockA = i.get('Quantity')
            file.write(f"{pk},{apple},{Pricing},{stockA}\n")


socket_client.close()