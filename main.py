import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import datetime
import math
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image, ImageTk


class ParkingApp:
    """Main application class for Park-O-Meter parking management system."""

    def __init__(self, root):
        """Initialize the parking application with all UI components and state."""
        self.root = root

        self.slots = {
            "T1": None,
            "T2": None,
            "T3": None,
            "T4": None,
            "T5": None,
            "T6": None,
            "T7": None,
            "T8": None,
            "T9": None,
            "T10": None,
            "F1": None,
            "F2": None,
            "F3": None,
            "F4": None,
            "F5": None,
            "F6": None,
            "F7": None,
            "F8": None,
            "F9": None,
            "F10": None,
            "E1": None,
            "E2": None,
            "E3": None,
            "E4": None,
            "E5": None,
            "E6": None,
            "E7": None,
            "E8": None,
            "E9": None,
            "E10": None,
            "H1": None,
            "H2": None,
            "H3": None,
            "H4": None,
            "H5": None,
            "H6": None,
            "H7": None,
            "H8": None,
            "H9": None,
            "H10": None,
        }
        self.transactions = []
        self.current_slot = None

        self.v_no_entry = None
        self.add_button = None

        self.setup_window()

        # Create all UI components
        self.create_header()
        self.create_logo()
        self.create_entry_frame()
        self.create_revenue_frame()
        self.create_exit_frame()

    def setup_window(self):
        self.root.title("Park-O-Meter")
        self.root.geometry("1366x768")
        self.root.state("zoomed")
        self.root.config(background="#CCCCCC")

    def create_header(self):
        self.header_frame = tk.Frame(self.root, background="#2C3E50")
        self.header_frame.place(x=0, y=0, width=1366, height=80)

        self.title_label = tk.Label(
            self.header_frame,
            text="Park-O-Meter",
            font=("Segoe UI", 24, "bold"),
            background="#2C3E50",
            foreground="#F5F7FA",
        )
        self.title_label.place(width=220, height=30, x=90, y=25)

    def create_logo(self):
        img = Image.open("logo.png")
        img = img.resize((80, 80), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(img)
        self.logo_label = tk.Label(
            self.header_frame, image=self.logo, background="#2C3E50"
        )
        self.logo_label.place(width=80, height=80, x=5, y=5)

    def create_entry_frame(self):
        # Entry Frame
        self.entry_frame = tk.Frame(self.root, background="#FFFFFF")
        self.entry_frame.place(x=60, y=105, width=400, height=300)

        # Frame title
        self.entry_title = tk.Label(
            self.entry_frame,
            text="Vehicle Entry",
            font=("Segoe UI", 12, "bold"),
            background="#2492EB",
            foreground="#FFFFFF",
        )
        self.entry_title.place(x=0, y=0, width=400, height=30)

        # Vehicle type label
        self.type_label = tk.Label(
            self.entry_frame,
            text="Select Vehicle Type",
            background="#FFFFFF",
            foreground="#000000",
            font=("Segoe UI", 12, "bold"),
        )
        self.type_label.place(x=125, y=55, width=150, height=25)

        # Vehicle type dropdown (Combobox)
        self.vehicle_type = tk.StringVar(value="Select")
        self.vehicle_combo = ttk.Combobox(
            self.entry_frame,
            textvariable=self.vehicle_type,
            values=["2 Wheeler", "4 Wheeler", "EV", "Heavy vehicle"],
            state="readonly",
        )
        self.vehicle_combo.place(x=75, y=85, width=250, height=30)

        # Check Slot button
        self.check_slot_btn = tk.Button(
            self.entry_frame,
            text="Check Available Slot",
            font=("Segoe UI", 12, "bold"),
            command=self.check,
            background="#2492EB",
        )
        self.check_slot_btn.place(x=75, y=120, width=250, height=30)

        # Slot label (shows available slot)
        self.slot_label = tk.Label(
            self.entry_frame,
            text="",
            background="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
        )

    def create_revenue_frame(self):
        """Create the revenue/transactions display frame."""
        self.revenue_frame = tk.Frame(self.root, background="#FFFFFF")
        self.revenue_frame.place(width=800, height=615, x=506, y=105)

        # Title
        t2 = tk.Label(
            self.revenue_frame,
            text="Completed Transactions",
            font=("Segoe UI", 12, "bold"),
            background="#2492EB",
            foreground="white",
        )
        t2.place(x=0, y=0, width=800, height=30)

        # Transactions table (Text widget)
        self.transactions_table = tk.Text(
            self.revenue_frame,
            background="#FFFFFF",
            foreground="black",
            font=("Segoe UI", 12, "bold"),
            wrap="none",
        )
        self.transactions_table.place(x=60, y=57.5, width=680, height=500)
        self.transactions_table.config(state="disabled")

        self.y_scroll = ttk.Scrollbar(
            self.transactions_table,
            orient="vertical",
            command=self.transactions_table.yview,
        )
        self.y_scroll.place(x=660, y=0, height=500)

        self.transactions_table.configure(yscrollcommand=self.y_scroll.set)

        # Generate PDF button
        generate = tk.Button(
            self.revenue_frame,
            text="Generate PDF",
            font=("Segoe UI", 12, "bold"),
            command=self.generate_pdf,
            background="#2492EB",
        )
        generate.place(x=275, y=570, width=250, height=30)

    def create_exit_frame(self):
        """Create the vehicle exit frame."""
        self.exit_frame = tk.Frame(self.root, background="#FFFFFF")
        self.exit_frame.place(width=400, height=300, x=60, y=420)

        # Title
        t3 = tk.Label(
            self.exit_frame,
            text="Vehicle Exit",
            font=("Segoe UI", 12, "bold"),
            background="#2492EB",
        )
        t3.place(x=0, y=0, width=400, height=30)

        # Vehicle number label
        vnl2 = tk.Label(
            self.exit_frame,
            text="Enter Vehicle Number",
            background="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
        )
        vnl2.place(x=125, y=35, width=180, height=25)

        # Vehicle number entry
        self.v_no = tk.Entry(self.exit_frame, bd=1, relief="solid")
        self.v_no.place(x=75, y=65, width=250, height=30)

        # Calculate charge button
        calculate = tk.Button(
            self.exit_frame,
            text="Calculate Charge",
            font=("Segoe UI", 14, "bold"),
            command=self.get_info,
            background="#2492EB",
        )
        calculate.place(x=75, y=100, width=250, height=30)

    def check(self):
        """Check for available parking slot based on vehicle type."""
        self.slot_label.place(x=75, y=155, width=250, height=25)
        selected = self.vehicle_type.get()

        if selected == "2 Wheeler":
            prefix = "T"
        elif selected == "4 Wheeler":
            prefix = "F"
        elif selected == "EV":
            prefix = "E"
        elif selected == "Heavy vehicle":
            prefix = "H"
        else:
            self.slot_label.config(text="Please select a vehicle type")
            return

        for slot in sorted(self.slots.keys(), key=lambda x: (x[0], int(x[1:]))):
            if slot.startswith(prefix) and self.slots[slot] is None:
                self.current_slot = slot
                self.slot_label.config(text="Slot Number:" + slot)
                self.enter()
                return

        self.slot_label.config(text="Slot Unavailable")

    def enter(self):
        """Create dynamic entry widgets for vehicle number input."""
        self.vnl1 = tk.Label(
            self.entry_frame,
            text="Enter Vehicle Number",
            background="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
        )
        self.vnl1.place(x=75, y=185, width=250, height=25)

        self.v_no_entry = tk.Entry(self.entry_frame, bd=1, relief="solid")
        self.v_no_entry.place(x=75, y=215, width=250, height=30)

        self.add_button = tk.Button(
            self.entry_frame,
            text="Add Vehicle",
            font=("Segoe UI", 12, "bold"),
            command=lambda: self.add_vehicle(self.current_slot, self.v_no_entry),
            background="#2492EB",
            foreground="#FFFFFF",
            width=25,
            height=1,
        )
        self.add_button.place(x=75, y=250, width=250, height=30)

    def add_vehicle(self, slot, v_no_widget):
        """Add a vehicle to the selected parking slot."""
        no = v_no_widget.get().strip()

        if not no:
            messagebox.showerror("Error", "Enter vehicle number")
        else:
            self.slots.update(
                {
                    slot: {
                        "Slot No": slot,
                        "Vehicle Number": no,
                        "Entry Time": datetime.datetime.now().strftime("%H:%M:%S"),
                    }
                }
            )
            messagebox.showinfo("Successful", "Vehicle Added Successfully")
            self.vehicle_type.set("Select")
            self.v_no_entry.delete(0, tk.END)
            self.slot_label.place_forget()
            self.vnl1.place_forget()
            self.v_no_entry.place_forget()
            self.add_button.place_forget()

    def get_info(self):
        """Get vehicle information and calculate charges."""
        no = self.v_no.get().strip()

        if not no:
            messagebox.showerror("Error", "Enter vehicle number")
            return

        found = False
        for slot, data in self.slots.items():
            if data is not None and data["Vehicle Number"] == no:
                self.calculate_charge(data, no)
                found = True
                break

        if not found:
            messagebox.showerror("Error", "Vehicle Not Found")

    def calculate_charge(self, data, vehicle_number):
        """Calculate parking charges based on duration and vehicle type."""
        entry_time = data["Entry Time"]
        entry_time = datetime.datetime.strptime(entry_time, "%H:%M:%S")
        exit_time = datetime.datetime.now().strftime("%H:%M:%S")
        exit_time = datetime.datetime.strptime(exit_time, "%H:%M:%S")

        duration = exit_time - entry_time
        seconds = duration.total_seconds()
        total_hours = seconds / 3600
        billed_hours = math.ceil(total_hours)

        if billed_hours == 0:
            billed_hours = 1

        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)

        slot = data["Slot No"]
        prefix = slot[0]

        if prefix == "T":
            rate = 10
        elif prefix == "F":
            rate = 20
        elif prefix == "E":
            rate = 15
        else:
            rate = 40

        total_charge = billed_hours * rate

        entry_display = entry_time.strftime("%I:%M %p")
        exit_display = exit_time.strftime("%I:%M %p")

        transaction = {
            "Slot": slot,
            "Vehicle Number": vehicle_number,
            "Entry Time": entry_display,
            "Exit Time": exit_display,
            "Duration": billed_hours,
            "Charge": total_charge,
        }
        self.transactions.append(transaction)

        # Display exit information
        self.entry_time_label = tk.Label(
            self.exit_frame,
            text="Entry Time : " + entry_display,
            background="#FFFFFF",
            foreground="black",
            font=("Segoe UI", 12, "bold"),
        )
        self.entry_time_label.place(x=75, y=135, width=250, height=25)

        self.exit_time_label = tk.Label(
            self.exit_frame,
            text="Exit Time : " + exit_display,
            background="#FFFFFF",
            foreground="black",
            font=("Segoe UI", 12, "bold"),
        )
        self.exit_time_label.place(x=75, y=165, width=250, height=25)

        self.duration_label = tk.Label(
            self.exit_frame,
            text="Total Duration : " + str(hours) + " hr " + str(minutes) + " min",
            background="#FFFFFF",
            foreground="black",
            font=("Segoe UI", 12, "bold"),
        )
        self.duration_label.place(x=75, y=195, width=250, height=25)

        self.charge_label = tk.Label(
            self.exit_frame,
            text="Total Charges : " + str(total_charge),
            background="#FFFFFF",
            foreground="black",
            font=("Segoe UI", 12, "bold"),
        )
        self.charge_label.place(x=75, y=225, width=250, height=25)

        self.exit_button = tk.Button(
            self.exit_frame,
            text="Exit Vehicle",
            font=("Segoe UI", 14, "bold"),
            command=lambda: self.exit_vehicle(slot),
            background="#2492EB",
        )
        self.exit_button.place(x=75, y=255, width=250, height=30)

    def exit_vehicle(self, slot):
        """Process vehicle exit and free up the parking slot."""
        self.slots[slot] = None
        messagebox.showinfo("Success", f"Vehicle Exited From Slot {slot}")
        self.v_no.delete(0, tk.END)
        self.entry_time_label.place_forget()
        self.exit_time_label.place_forget()
        self.duration_label.place_forget()
        self.charge_label.place_forget()
        self.exit_button.place_forget()
        self.show()

    def show(self):
        """Display all transactions in the transactions table."""
        self.transactions_table.config(state="normal")
        self.transactions_table.delete("1.0", tk.END)
        self.transactions_table.configure(font=("Courier New", 11))

        header_frame = (
            f"{'Slot':<6}"
            f"{'Vehicle No':<15}"
            f"{'Entry Time':<18}"
            f"{'Exit Time':<18}"
            f"{'Hours':<8}"
            f"{'Charge':<8}\n"
        )

        self.transactions_table.insert(tk.END, header_frame)
        self.transactions_table.insert(tk.END, "-" * 75 + "\n")

        total_vehicles = 0
        total_revenue = 0

        for data in self.transactions:
            row = (
                f"{data['Slot']:<6}"
                f"{data['Vehicle Number']:<15}"
                f"{data['Entry Time']:<18}"
                f"{data['Exit Time']:<18}"
                f"{str(data['Duration']) + 'hr':<8}"
                f"{'₹' + str(data['Charge']):<8}\n"
            )

            self.transactions_table.insert(tk.END, row)

            total_vehicles += 1
            total_revenue += data["Charge"]

        self.transactions_table.insert(tk.END, "-" * 75 + "\n")
        self.transactions_table.insert(tk.END, f"TOTAL VEHICLES : {total_vehicles}\n")
        self.transactions_table.insert(tk.END, f"TOTAL REVENUE  : ₹{total_revenue}\n")
        self.transactions_table.config(state="disabled")

    def generate_pdf(self):
        """Generate PDF report of all transactions."""
        if not self.transactions:
            messagebox.showerror("Error", "No transactions available!")
            return

        today = datetime.datetime.now().strftime("%d-%m-%Y")
        default_name = f"Revenue_{today}.pdf"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF files", "*.pdf")],
            title="Save Revenue Report",
        )

        if not file_path:
            return

        pdf = SimpleDocTemplate(file_path, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        title = Paragraph(
            "<b><font size=16>Parking Revenue Report</font></b>", styles["Title"]
        )
        date_text = Paragraph(
            f"<b>Date:</b> {datetime.datetime.now().strftime('%d-%m-%Y')}",
            styles["Normal"],
        )

        elements.append(title)
        elements.append(Spacer(1, 12))
        elements.append(date_text)
        elements.append(Spacer(1, 20))

        table_data = [
            [
                "Slot",
                "Vehicle Number",
                "Entry Time",
                "Exit Time",
                "Duration (hrs)",
                "Charge (Rs)",
            ]
        ]

        total_revenue = 0

        for t in self.transactions:
            row = [
                t["Slot"],
                t["Vehicle Number"],
                t["Entry Time"],
                t["Exit Time"],
                str(t["Duration"]),
                str(t["Charge"]),
            ]
            total_revenue += t["Charge"]
            table_data.append(row)

        table_data.append(
            [
                "",
                "TOTAL VEHICLES:",
                str(len(self.transactions)),
                "",
                "TOTAL REVENUE:",
                str(total_revenue),
            ]
        )

        table = Table(table_data, colWidths=[60, 100, 90, 90, 85, 80])

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.lightyellow),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ]
            )
        )

        elements.append(table)
        pdf.build(elements)
        messagebox.showinfo("Success", "PDF saved successfully!")


if __name__ == "__main__":
    main = tk.Tk()
    app = ParkingApp(main)
    main.mainloop()
