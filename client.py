import socket
import pickle
from tkinter import *
from tkinter import messagebox

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))

# this code states that teh client is has recived the stock
r_data = client.recv(1024)
r_obj = pickle.loads(r_data)

client_dictionary = {}

gapple = []
# reading throught the gapple stocks and placing it into a dictionary
for key in r_obj:
    client_dictionary.update({key: r_obj[key]})

# reading throguh the dictionary and making it into a list for later use.
for i in client_dictionary:
    gapple.append(client_dictionary[i])

# apple store

applestore = Tk()

applestore.geometry('565x745')


applestore.config(background='black')


appleStore_frame = Label(applestore, relief=RAISED, background='black')
appleStore_frame.pack(pady=20, padx=20)

# Iphone13
Iphone13_frame = LabelFrame(appleStore_frame, text="iphone13", relief=RAISED, background='black', fg='white')
Iphone13_frame.grid(column=0, row=0)

Iphone13_price = Label(Iphone13_frame, text='£1,000.00')
Iphone13_price.grid(column=0, row=1)

# Iphone12
Iphone12_frame = LabelFrame(appleStore_frame, text="iphone13", relief=RAISED, background='black', fg='white')
Iphone12_frame.grid(column=1, row=0)

Iphone12_price = Label(Iphone12_frame, text='£800.00')
Iphone12_price.grid(column=0, row=1)

# Iphone11
Iphone11_frame = LabelFrame(appleStore_frame, text="iphone11", relief=RAISED, background='black', fg='white')
Iphone11_frame.grid(column=2, row=0)

Iphone11_price = Label(Iphone11_frame, text='£600.00')
Iphone11_price.grid(column=0, row=1)

# Iphone10
Iphone10_frame = LabelFrame(appleStore_frame, text="iphone10", relief=RAISED, background='black', fg='white')
Iphone10_frame.grid(column=3, row=0)

Iphone10_price = Label(Iphone10_frame, text='£500.00')
Iphone10_price.grid(column=0, row=1)



# These code allowsd the customer to enter what item they wish to buy
INPUT = LabelFrame(applestore, text="Enter the item you wish to purchase!", relief=RAISED, background='black', fg='white')
INPUT.pack()

Entry1 = Entry(INPUT, borderwidth=4, width=31)
Entry1.pack()

stockbox = LabelFrame(applestore, text="Available Stock Items", relief=RAISED, background='black', fg='white')
stockbox.pack(side=LEFT)


order_list = []

# this is the basket label where the customer will be able to see what they placed in the basket for purchase.
basket = LabelFrame(applestore, text='Basket', relief=RAISED, background='black', fg='white')
basket.pack(side=RIGHT)

Answer2 = Text(basket)
Answer2.pack()
Answer2.config(height=4, width=14)

costbx = LabelFrame(applestore, text='Total-Cost', relief=RAISED, background='black', fg='white')
costbx.pack(side=BOTTOM)

totalbx = Text(costbx)
totalbx.pack()
totalbx.config(height=3, width=14)

transaction = []
from tkinter import simpledialog


def Paying():
    total = 0
    for i in order_list:
        total += i
    totalbx.insert(END, f"\n£{total:.2f}")
    # these line send customer orders to the server to amke changes in teh csv database.
    pickle_transaction = pickle.dumps(transaction)
    client.send(pickle_transaction)

    result = messagebox.askquestion("Payment",
                                    f"The total owed is £{total:.2f}\nItem that are above £200.00 must be paid with Credit/Debit card only Pres yess to continue..",
                                    icon="info")
    if result == 'yes':
        messagebox.showinfo("Card Payment",
                            "Your Bank has Confirmed this purchase.")

    # sending updated stock to server
    pickle_stock = pickle.dumps(gapple)
    client.send(pickle_stock)
    messagebox.showinfo('Thank you!',
                        'Thank you for shopping at the Apple Store Please return next time.',
                        icon="info")
    applestore.destroy()


# deletes all entry in the basket.
def DeleteBasket():
    Entry1.delete(0, END)
    Answer2.delete(1.0, END)
    totalbx.delete(1.0, END)
    applestore.destroy()


# Add item button
def ExtraItems():
    select = Entry1.get()
    amount = int(Entry2.get())

    for item in gapple:
        if select == item.get('PrimaryKey'):
            select = item
            name = select.get('apple')
            price = select.get('price')

            for i in range(amount):
                select['Quantity'] -= 1
                if select['Quantity'] < 0:
                    select['Quantity'] = 0
                    messagebox.showinfo("Sorry this Item Is Out of Stock.")

                else:
                    transaction.append(f"{name},{price},\n")
                    Answer2.insert(END, f"\n{name}, £{price}")
                    order_list.append(float(price))

    Entry1.delete(0, END)
    Entry2.delete(0, END)


# transaction buttons
i_add = Button(applestore, text='Add Product to Kart', background='white', command=ExtraItems)
i_add.config(width=16)
i_add.pack()

paying_bttn = Button(applestore, text='Continue to Pay', background='white', command=Paying)
paying_bttn.config(width=16)
paying_bttn.pack()

dbasket_bttn = Button(applestore, text='Delete Basket', background='white', command=DeleteBasket)
dbasket_bttn.config(width=16)
dbasket_bttn.pack()

Entry2 = Entry(INPUT, borderwidth=3, width=3)
Entry2.pack()

# running tkinter
applestore.mainloop()

# closing connection
client.close()