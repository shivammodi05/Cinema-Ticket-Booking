import random
import sqlite3
import string
from fpdf import FPDF

class User:

    def __init__(self,name):
        self.name = name

    def buy(self,seat,card):
        """ Buy ticket for user if card and seat are valid """
        if not seat.is_free():
            return "Seat is already taken"

        if not card.validate(seat.get_price()):
            return "Card is invalid or doesn't have enough balance"

        seat.occupy()
        ticket = Ticket(self, seat.get_price(), seat)
        return "Ticket bought successfully"

class Seat:

    database = "cinema.db"

    def __init__(self,seat_id):
        self.seat_id = seat_id

    def get_connection(self):
        connection = sqlite3.connect(self.database)
        return connection

    def get_price(self):
        """ Get price of certain seat """
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT price FROM seat WHERE seat_id = ?", (self.seat_id,))
        price = cursor.fetchall()[0][0]
        return price

    def is_free(self):
        """ Check if seat is taken """
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT taken FROM seat WHERE seat_id = ?", (self.seat_id,))
        result = cursor.fetchall()[0][0]

        if result == 0:
            return True
        else:
            return False


    def occupy(self):
        """ Occupy seat """
        connection = self.get_connection()
        connection.execute("UPDATE seat SET taken = 1 WHERE seat_id = ?", (self.seat_id,))
        connection.commit()
        connection.close()

class Card:

    database = "banking.db"

    def __init__(self, type, number, cvc, holder):
        self.type = type
        self.number = number
        self.cvc = cvc
        self.holder = holder

    def validate(self,price):
        """ Validate card if all parameters are correct and has balance to buy ticket"""
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM card WHERE number = ? AND cvc = ? AND holder = ?", (self.number, self.cvc, self.holder))

        result = cursor.fetchall()

        if result:
            balance = result[0][0]
            if balance >= price:
                connection.execute("UPDATE card SET balance = ? WHERE number = ? AND cvc = ?", (balance-price, self.number, self.cvc))
                connection.commit()
                connection.close()
                return True

        return False

class Ticket:

    def __init__(self, user, price, seat):
        self.id = "".join([random.choice(string.ascii_letters) for i in range(8)])
        self.user = user
        self.price = price
        self.seat_number = seat

    def to_pdf(self):
        """ Creates a PDF Ticket """
        pdf = FPDF(orientation='p', unit='pt', format='A4')
        pdf.add_page()

        pdf.set_font(family="Times", style="B", size=24)
        pdf.cell(w=0, h=80, txt="Your Digital Ticket", border=0, ln=1, align='C')

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Name: ", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=self.user.name, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)


        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Ticket ID : ", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=self.id, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)


        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Price: ", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=str(self.price), border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)


        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Seat Number: ", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=self.seat_number, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.output("result.pdf", 'F')


if __name__ == "__main__":

    name = input("Enter your name: ")
    user = User(name)
    seat_id = input("Enter seat number: ")
    seat = Seat(seat_id)
    card_number = input("Enter card number: ")
    card_cvc = input("Enter card cvc: ")
    card_holder = input("Enter card holder: ")
    card_type = input("Enter card type: ")
    card = Card(card_type, card_number, card_cvc, card_holder)

    print(User.buy(user,seat,card))
