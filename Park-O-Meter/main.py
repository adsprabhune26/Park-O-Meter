import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,filedialog
import datetime
import math
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image,ImageTk

slots = {"T1":None,"T2":None,"T3":None,"T4":None,"T5":None,
"T6":None,"T7":None,"T8":None,"T9":None,"T10":None,
"F1":None,"F2":None,"F3":None,"F4":None,"F5":None,
"F6":None,"F7":None,"F8":None,"F9":None,"F10":None,
"E1":None,"E2":None,"E3":None,"E4":None,"E5":None,
"E6":None,"E7":None,"E8":None,"E9":None,"E10":None,
"H1":None,"H2":None,"H3":None,"H4":None,"H5":None,
"H6":None,"H7":None,"H8":None,"H9":None,"H10":None}

transactions=[]

def check():
    global s
    selected = vehicle_type.get()
    if selected == "2 Wheeler":
        prefix = "T"
    elif selected == "4 Wheeler":
        prefix = "F"
    elif selected == "EV":
        prefix = "E"
    elif selected =="Heavy vehicle":
        prefix = "H"
    else:
        slot_label.config(text="Please select a vehicle type")
        return

    for slot in sorted(slots.keys(),key=lambda x:(x[0],int(x[1:]))):
        if slot.startswith(prefix) and slots[slot] is None:
            s = slot
            slot_label.config(text="Slot Number:" + s)
            enter()
            return 
    slot_label.config(text="Slot Unavailable")
    
def enter():
    vnl1=tk.Label(entry_frame,text="Enter Vehicle Number",background="#579DDA",foreground="black",font=("Arial",12,"bold"))
    vnl1.place(width=210,x=61.5,y=183)
    
    v_no=ctk.CTkEntry(entry_frame,width=150,height=20,corner_radius=20)
    v_no.place(x=91.5,y=213)
    
    add=ctk.CTkButton(entry_frame,text="Add Vehicle",font=("Arial",12,"bold"),command=lambda:add_vehicle(s,v_no),corner_radius=20,fg_color="#FFFFFF",text_color="#000000",hover_color="#9B9494",)
    add.place(x=96.5,y=240)
    
def add_vehicle(s,v_no):  
    no=v_no.get().strip()
    if not no:
        messagebox.showerror("Error","Enter vehicle number")
    else:
        slots.update({s:{"Slot No":s,"Vehicle Number":no,"Entry Time":datetime.datetime.now().strftime("%H:%M:%S")}})
        messagebox.showinfo("Successful","Vehicle Added Successfully")
        
def get_info(v_no):
    no = v_no.get().strip()
    if not no:
        messagebox.showerror("Error", "Enter vehicle number")
        return
    found = False
    for slot, data in slots.items():
        if data is not None and data["Vehicle Number"] == no:
            calculate_charge(data,no)
            found = True
            break
    if not found:
        messagebox.showerror("Error", "Vehicle Not Found")

def calculate_charge(data,no):
    entry_time=data["Entry Time"]
    entry_time=datetime.datetime.strptime(entry_time,"%H:%M:%S")
    exit_time=datetime.datetime.now().strftime("%H:%M:%S")
    exit_time=datetime.datetime.strptime(exit_time,"%H:%M:%S")
    duration=exit_time-entry_time
    seconds=duration.total_seconds()
    total_hours=seconds/3600
    billed_hours=math.ceil(total_hours)

    if billed_hours == 0:
        billed_hours=1

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

    t={"Slot":slot,"Vehicle Number":no,"Entry Time":entry_display,"Exit Time":exit_display,"Duration":billed_hours,"Charge":total_charge}
    transactions.append(t)

    entry_time_label=tk.Label(exit_frame,text="Entry Time : "+entry_display,background="#579DDA",foreground="black",font=("Arial",12,"bold"))
    entry_time_label.place(width=210,x=61.5,y=134)
    
    exit_time_label=tk.Label(exit_frame,text="Exit Time : "+exit_display,background="#579DDA",foreground="black",font=("Arial",12,"bold"))
    exit_time_label.place(width=210,x=61.5,y=164)

    duration_label=tk.Label(exit_frame,text="Total Duration : "+str(hours)+" hr "+str(minutes)+" min",background="#579DDA",foreground="black",font=("Arial",12,"bold"))
    duration_label.place(width=210,x=61.5,y=194)
    
    charge_label=tk.Label(exit_frame,text="Total Charges : "+str(total_charge),background="#579DDA",foreground="black",font=("Arial",12,"bold"))
    charge_label.place(width=210,x=61.5,y=224)
    
    exit=ctk.CTkButton(exit_frame,text="Exit Vehicle",font=("Arial",14,"bold"),command=lambda:exit_vehicle(slot),corner_radius=20,fg_color="#FFFFFF",text_color="#000000",hover_color="#9B9494")
    exit.place(x=96.5,y=254)

def exit_vehicle(slot):
    slots[slot] = None
    messagebox.showinfo("Success",f"Vehicle Exited From Slot {slot}")
    show()
    
def show():
    transactions_table.delete("1.0", tk.END)
    transactions_table.configure(font=("Courier New", 11))
    header = (
        f"{'Slot':<6}"
        f"{'Vehicle No':<15}"
        f"{'Entry Time':<18}"
        f"{'Exit Time':<18}"
        f"{'Hours':<8}"
        f"{'Charge':<8}\n"
    )

    transactions_table.insert(tk.END, header)
    transactions_table.insert(tk.END, "-" * 75 + "\n")

    total_vehicles = 0
    total_revenue = 0

    for data in transactions:
        row = (
            f"{data['Slot']:<6}"
            f"{data['Vehicle Number']:<15}"
            f"{data['Entry Time']:<18}"
            f"{data['Exit Time']:<18}"
            f"{str(data['Duration'])+'hr':<8}"
            f"{'₹'+str(data['Charge']):<8}\n"
        )

        transactions_table.insert(tk.END, row)

        total_vehicles += 1
        total_revenue += data["Charge"]

    transactions_table.insert(tk.END, "-" * 75 + "\n")
    transactions_table.insert(tk.END, f"TOTAL VEHICLES : {total_vehicles}\n")
    transactions_table.insert(tk.END, f"TOTAL REVENUE  : ₹{total_revenue}\n")

def generate_pdf():
    if not transactions:
        messagebox.showerror("Error", "No transactions available!")
        return

    today = datetime.datetime.now().strftime("%d-%m-%Y") 
    default_name = f"Revenue_{today}.pdf"

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        initialfile=default_name,
        filetypes=[("PDF files", "*.pdf")],
        title="Save Revenue Report"
    )

    if not file_path:
        return

    pdf = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("<b><font size=16>Parking Revenue Report</font></b>", styles["Title"])
    date_text = Paragraph(f"<b>Date:</b> {datetime.datetime.now().strftime('%d-%m-%Y')}", styles["Normal"])

    elements.append(title)
    elements.append(Spacer(1, 12))
    elements.append(date_text)
    elements.append(Spacer(1, 20))

    table_data = [
        ["Slot", "Vehicle Number", "Entry Time", "Exit Time", "Duration (hrs)", "Charge (₹)"]
    ]

    total_revenue = 0

    for t in transactions:
        row = [
            t["Slot"],
            t["Vehicle Number"],
            t["Entry Time"],
            t["Exit Time"],
            str(t["Duration"]),
            str(t["Charge"])
        ]
        total_revenue += t["Charge"]
        table_data.append(row)

    table_data.append([
        "", "TOTAL VEHICLES:", str(len(transactions)), "", "TOTAL REVENUE:", str(total_revenue)
    ])

    table = Table(table_data, colWidths=[60, 100, 90, 90, 85, 80])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightyellow),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ]))

    elements.append(table)
    pdf.build(elements)
    messagebox.showinfo("Success", "PDF saved successfully!")

main=tk.Tk()
main.title("Park-O-Meter")
main.geometry("1366x768")
main.state("zoomed")
main.config(background="#CADFE6")

img=Image.open("Asset_1.png")
img=img.resize((200,165),Image.LANCZOS)
logo=ImageTk.PhotoImage(img)
logo_label=tk.Label(main,image=logo,width=200,height=200,background="#CADFE6")
logo_label.place(x=30,y=20)

l1=tk.Label(main,background="#0074D9").place(x=0,y=234,width=264,height=3)
l2=tk.Label(main,background="#0074D9").place(x=264,y=234,width=3,height=320)
l3=tk.Label(main,background="#0074D9").place(x=264,y=554,width=676,height=3)
l4=tk.Label(main,background="#0074D9").place(x=940,y=554,width=3,height=240)
l5=tk.Label(main,background="#0074D9").place(x=960,y=698,width=3,height=90)
l6=tk.Label(main,background="#0074D9").place(x=960,y=698,width=353,height=3)
l7=tk.Label(main,background="#0074D9").place(x=1313,y=600,width=3,height=101)
l8=tk.Label(main,background="#0074D9").place(x=1313,y=600,width=53,height=3)
l8=tk.Label(main,background="#0074D9").place(x=1313,y=580,width=53,height=3)
l10=tk.Label(main,background="#0074D9").place(x=1313,y=0,width=3,height=580)
l11=tk.Label(main,background="#0074D9").place(x=284,y=0,width=3,height=214)
l12=tk.Label(main,background="#0074D9").place(x=284,y=214,width=659,height=3)
l13=tk.Label(main,background="#0074D9").place(x=940,y=70,width=3,height=144)
l14=tk.Label(main,background="#0074D9").place(x=940,y=70,width=353,height=3)
l15=tk.Label(main,background="#0074D9").place(x=1290,y=0,width=3,height=70)

entry_frame=tk.Frame(background="#579DDA",bd=1,relief="solid")
entry_frame.place(width=333,height=300,x=284,y=234)

t1=tk.Label(entry_frame,text="Vehicle Entry",font=("Arial",12,"bold"),background="#0074D9")
t1.place(width=333,x=0,y=0)

type_label=tk.Label(entry_frame,text="Select Vehicle Type",background="#579DDA",foreground="black",font=("Arial",12,"bold"))
type_label.place(width=210,x=61.5,y=57)

vehicle_type = tk.StringVar(value="Select")
vehicle_combo = ctk.CTkOptionMenu(entry_frame, variable=vehicle_type, values=["2 Wheeler", "4 Wheeler","EV","Heavy vehicle"],corner_radius=18,fg_color="#FFFFFF",text_color="#000000",button_hover_color="#FFFFFF",dropdown_fg_color="#FFFFFF",)
vehicle_combo.place(x=96.5, y=87)

check_slot=ctk.CTkButton(entry_frame,text="Check Slot",font=("Arial",14,"bold"),command=lambda:check(),corner_radius=20,fg_color="#FFFFFF",text_color="#000000",hover_color="#9B9494")
check_slot.place(x=96.5,y=120)

slot_label=tk.Label(entry_frame,text="",background="#579DDA",foreground="black",font=("Arial",12,"bold"))
slot_label.place(width=210,x=61.5,y=153)

revenue_frame=tk.Frame(background="#579DDA",bd=1,relief="solid")
revenue_frame.place(width=333,height=588,x=960,y=90)

t2=tk.Label(revenue_frame,text="Completed Transactions",font=("Arial",12,"bold"),background="#0074D9")
t2.place(width=333,x=0,y=0) 

transactions_table=tk.Text(revenue_frame,background="#579DDA",foreground="black",font=("Arial",12,"bold"),wrap="none")
transactions_table.place(width=333,height=510,x=0,y=25)

x_scroll=ttk.Scrollbar(revenue_frame,orient="horizontal",command=transactions_table.xview)
x_scroll.place(x=0,y=520,width=318)

y_scroll=ttk.Scrollbar(revenue_frame,orient="vertical",command=transactions_table.yview)
y_scroll.place(x=318,y=25,height=512)

transactions_table.configure(xscrollcommand=x_scroll.set,yscrollcommand=y_scroll.set)

generate=tk.Button(revenue_frame,text="Generate PDF",font=("Arial",12,"bold"),command=lambda:generate_pdf())
generate.place(x=106,y=545)

exit_frame=tk.Frame(background="#579DDA",bd=1,relief="solid")
exit_frame.place(width=333,height=300,x=622,y=234)

t3=tk.Label(exit_frame,text="Vehicle Exit",font=("Arial",12,"bold"),background="#0074D9")
t3.place(width=333,x=0,y=0)

vnl2=tk.Label(exit_frame,text="Enter Vehicle Number",background="#579DDA",foreground="black",font=("Arial",12,"bold"))
vnl2.place(width=210,x=61.5,y=44)

v_no=ctk.CTkEntry(exit_frame,width=150,height=20,corner_radius=20)
v_no.place(x=91.5,y=74)

calculate=ctk.CTkButton(exit_frame,text="Calculate Charge",font=("Arial",14,"bold"),command=lambda:get_info(v_no),corner_radius=20,fg_color="#FFFFFF",text_color="#000000",hover_color="#9B9494")
calculate.place(x=91.5,y=101)

main.mainloop()