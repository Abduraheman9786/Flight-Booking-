
from abc import ABC, abstractmethod


class Flight:
    def __init__(self, code, airline, source, destination, seats, fare):
        self.code = code
        self.airline = airline
        self.source = source
        self.destination = destination
        self.seats = seats
        self.fare = fare

    def display(self):
        print(self.code, "|", self.airline, "|",
              self.source, "to", self.destination,
              "| Seats:", self.seats, "| Fare: Rs.", self.fare)


class Passenger(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def discount(self):
        pass


class RegularPassenger(Passenger):
    def discount(self):
        return 0


class StudentPassenger(Passenger):
    def discount(self):
        return 0.10


class Booking:
    def __init__(self, booking_id, flight, passengers):
        self.booking_id = booking_id
        self.flight = flight
        self.passengers = passengers

    def display(self):
        subtotal = 0
        discount = 0

        print("\nBooking ID:", self.booking_id)
        print("Flight:", self.flight.code)
        print("Route:", self.flight.source, "to", self.flight.destination)

        for i, passenger in enumerate(self.passengers, 1):
            fare = self.flight.fare
            saving = fare * passenger.discount()
            subtotal += fare
            discount += saving

            if isinstance(passenger, StudentPassenger):
                passenger_type = "Student"
            else:
                passenger_type = "Regular"

            print("\nPassenger", i)
            print("Name:", passenger.name)
            print("Age:", passenger.age)
            print("Type:", passenger_type)
            print("Fare: Rs.", fare)
            print("Discount: Rs.", saving)

        print("\nNumber of Tickets:", len(self.passengers))
        print("Subtotal: Rs.", subtotal)
        print("Total Discount: Rs.", discount)
        print("Final Amount: Rs.", subtotal - discount)


class FlightBookingSystem:
    def __init__(self):
        self.flights = [
            Flight("PN101", "Kiran Air", "Pune", "Delhi", 20, 4000),
            Flight("MB102", "Air India", "Mumbai", "Bengaluru", 15, 4500),
            Flight("PH103", "IndiGo", "Pune", "Hyderabad", 12, 3500),
            Flight("CN104", "Astra", "Hydrabad", "Mumbai", 25, 4300)
        ]
        self.bookings = []
        self.booking_number = 1001

    def find_flight(self, code):
        for flight in self.flights:
            if flight.code == code:
                return flight
        return None

    def view_flights(self):
        for flight in self.flights:
            flight.display()

    def validate_passenger(self, name, age, passenger_type):
        if not name.strip():
            print("Error: Name cannot be blank.")
            return False

        if age < 1 or age > 120:
            print("Error: Age must be between 1 and 120.")
            return False

        if passenger_type not in ("student", "regular"):
            print("Error: Enter Student or Regular.")
            return False

        return True

    def calculate_fare(self, flight, passengers):
        subtotal = flight.fare * len(passengers)
        discount = sum(
            flight.fare * passenger.discount()
            for passenger in passengers
        )
        return subtotal, discount, subtotal - discount

    def book_flight(self):
        code = input("Enter flight code: ").strip().upper()
        flight = self.find_flight(code)

        if flight is None:
            print("Invalid flight code.")
            return

        try:
            tickets = int(input("How many tickets do you want? "))
        except ValueError:
            print("Enter a valid whole number.")
            return

        if tickets <= 0:
            print("Ticket count must be greater than zero.")
            return

        if tickets > flight.seats:
            print("Not enough seats available.")
            return

        passengers = []

        for i in range(1, tickets + 1):
            print("\nPassenger", i)
            name = input("Enter name: ").strip()

            try:
                age = int(input("Enter age: "))
            except ValueError:
                print("Invalid age. Booking cancelled.")
                return

            passenger_type = input(
                "Passenger type (Student/Regular): "
            ).strip().lower()

            if not self.validate_passenger(name, age, passenger_type):
                print("Booking cancelled. Seats remain unchanged.")
                return

            if passenger_type == "student":
                passenger = StudentPassenger(name, age)
            else:
                passenger = RegularPassenger(name, age)

            passengers.append(passenger)

        subtotal, discount, total = self.calculate_fare(
            flight, passengers
        )

        booking = Booking(
            "BK" + str(self.booking_number), flight, passengers
        )

        flight.seats -= tickets
        self.bookings.append(booking)
        self.booking_number += 1

        print("\nBooking confirmed!")
        booking.display()

    def view_booking(self):
        if not self.bookings:
            print("No confirmed booking exists.")
        else:
            self.bookings[-1].display()

    def run(self):
        while True:
            print("\nWelcome to Kiran Air Booking")
            print("1. View Flights")
            print("2. Book Flight")
            print("3. View Booking")
            print("4. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.view_flights()
            elif choice == "2":
                self.book_flight()
            elif choice == "3":
                self.view_booking()
            elif choice == "4":
                print("Thank you for using Kiran Air Booking!")
                break
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    system = FlightBookingSystem()
    system.run()
