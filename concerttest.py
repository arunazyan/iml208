import tkinter as tk
from tkinter import messagebox
import random  # Added import for generating order number

class ConcertTicketBookingSystem:
    def __init__(self, total_tickets, concert_name, concert_date, concert_venue):
        self.total_tickets = total_tickets
        self.available_tickets = total_tickets
        self.booked_tickets = 0
        self.ticket_price_rm = 250
        self.concert_name = concert_name
        self.concert_date = concert_date
        self.concert_venue = concert_venue
        self.bookings = {}

    def view_concert_info(self):
        return f"BLACKPINK OFFICIAL PRESENTS\n {self.concert_name}\nDate: {self.concert_date}\nVenue: {self.concert_venue}"

    def view_available_tickets(self):
        return f"Available Tickets: {self.available_tickets}"

    def view_booking_details(self, username):
        if username in self.bookings:
            details = self.bookings[username]
            return f"Booking Details for {username}:\nTickets: {details['tickets']}\nTotal Cost: RM{details['cost']}\nOrder Number: {details['order_number']}"
        else:
            return f"No bookings have been made yet for {username}."

    def book_tickets(self, username, num_tickets, age):
        try:
            num_tickets = int(num_tickets)
            age = int(age)
            if 0 < num_tickets <= self.available_tickets and age >= 16:
                cost = num_tickets * self.ticket_price_rm
                order_number = random.randint(100000, 999999)  # Generate a random order number

                confirmation = messagebox.askyesno(
                    "Confirm Booking",
                    f"Total Cost: RM{cost}\nConfirm booking for {num_tickets} tickets?"
                )

                if confirmation:
                    self.available_tickets -= num_tickets
                    self.booked_tickets += num_tickets
                    if username in self.bookings:
                        self.bookings[username]['tickets'] += num_tickets
                        self.bookings[username]['cost'] += cost
                    else:
                        self.bookings[username] = {'tickets': num_tickets, 'cost': cost, 'order_number': order_number}
                    messagebox.showinfo("Booking Successful", f"{num_tickets} tickets booked for {username}.")
                else:
                    messagebox.showinfo("Booking Canceled", "Booking canceled.")
            else:
                messagebox.showerror("Error", "Invalid number of tickets, age requirement not met, or booking for users under 16 is not allowed.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    def update_booking(self, username, new_num_tickets):
        try:
            new_num_tickets = int(new_num_tickets)
            if username in self.bookings and 0 < new_num_tickets <= self.available_tickets:
                old_num_tickets = self.bookings[username]['tickets']
                diff_tickets = new_num_tickets - old_num_tickets
                new_cost = new_num_tickets * self.ticket_price_rm

                confirmation = messagebox.askyesno(
                    "Confirm Update",
                    f"Total Cost: RM{new_cost}\nUpdate booking from {old_num_tickets} to {new_num_tickets} tickets?"
                )

                if confirmation:
                    self.available_tickets -= diff_tickets
                    self.booked_tickets += diff_tickets
                    self.bookings[username]['tickets'] = new_num_tickets
                    self.bookings[username]['cost'] = new_cost
                    messagebox.showinfo("Update Successful", f"Booking updated for {username}.")
                else:
                    messagebox.showinfo("Update Canceled", "Update canceled.")
            else:
                messagebox.showerror("Error", "Invalid number of tickets or no existing booking for the user.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    def delete_booking(self, username):
        if username in self.bookings:
            deleted_tickets = self.bookings[username]['tickets']
            self.available_tickets += deleted_tickets
            self.booked_tickets -= deleted_tickets
            deleted_cost = self.bookings[username]['cost']
            del self.bookings[username]
            messagebox.showinfo("Delete Successful", f"Booking for {username} deleted. Refunded RM{deleted_cost}.")
        else:
            messagebox.showerror("Error", f"No existing booking found for {username}.")

class ConcertBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Concert Ticket Booking System")
        self.root.configure(bg='#000000')
        self.system = ConcertTicketBookingSystem(
            total_tickets=100,
            concert_name="BLACKPINK [BORN PINK] Live in Seoul",
            concert_date="16th September 2023",
            concert_venue="Gocheok Sky Dome"
        )
        self.label = tk.Label(root, text=self.system.view_concert_info(), font=("Helvetica", 16), fg='#fc0fc0', bg='#000000')
        self.label.pack(pady=10)
        self.status_label = tk.Label(root, text=self.system.view_available_tickets(), fg='#fc0fc0', bg='#000000')
        self.status_label.pack(pady=10)
        self.username_label = tk.Label(root, text="Enter your name:", fg='#fc0fc0', bg='#000000')
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)
        self.age_label = tk.Label(root, text="Enter your age:", fg='#fc0fc0', bg='#000000')
        self.age_label.pack(pady=5)
        self.age_entry = tk.Entry(root)
        self.age_entry.pack(pady=5)
        self.num_tickets_label = tk.Label(root, text="Enter the number of tickets to book/update:", fg='#fc0fc0', bg='#000000')
        self.num_tickets_label.pack(pady=5)
        self.num_tickets_entry = tk.Entry(root)
        self.num_tickets_entry.pack(pady=5)
        self.book_button = tk.Button(root, text="Book Tickets", command=self.book_tickets, fg='#ffffff', bg='#fc0fc0')
        self.book_button.pack(pady=10)
        self.update_button = tk.Button(root, text="Update Booking", command=self.update_booking, fg='#ffffff', bg='#fc0fc0')
        self.update_button.pack(pady=10)
        self.delete_button = tk.Button(root, text="Delete Booking", command=self.delete_booking, fg='#ffffff', bg='#fc0fc0')
        self.delete_button.pack(pady=10)
        self.details_button = tk.Button(root, text="View Booking Details", command=self.view_booking_details, fg='#ffffff', bg='#fc0fc0')
        self.details_button.pack(pady=10)

    def book_tickets(self):
        username = self.username_entry.get()
        age = self.age_entry.get()
        num_tickets = self.num_tickets_entry.get()
        self.system.book_tickets(username, num_tickets, age)
        self.status_label.config(text=self.system.view_available_tickets())

    def update_booking(self):
        username = self.username_entry.get()
        new_num_tickets = self.num_tickets_entry.get()
        self.system.update_booking(username, new_num_tickets)
        self.status_label.config(text=self.system.view_available_tickets())

    def delete_booking(self):
        username = self.username_entry.get()
        self.system.delete_booking(username)
        self.status_label.config(text=self.system.view_available_tickets())

    def view_booking_details(self):
        username = self.username_entry.get()
        details = self.system.view_booking_details(username)
        messagebox.showinfo("Booking Details", details)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConcertBookingApp(root)
    root.mainloop()
