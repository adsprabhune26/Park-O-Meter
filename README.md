# Park-O-Meter — Smart Parking Lot Management System

Park-O-Meter is a Python-based GUI application developed as part of an internship project.  
It simulates a real-world parking lot system with vehicle entry, exit, parking charge calculation, transaction tracking, and revenue reporting in a single unified interface.

The project focuses on real-time logic, slot management, and user interaction, similar to how a small to medium parking system works in practice.

---

## Features

- Vehicle entry with automatic slot allocation
- Support for multiple vehicle types
  - 2-Wheeler
  - 4-Wheeler
  - EV
  - Heavy Vehicle
- Time-based parking charge calculation
- Vehicle exit with charge display and slot release
- Live transaction tracking from entry to exit
- Revenue report export as PDF
- Single-screen GUI application

---

## Design Overview

The application is designed for real-time execution rather than long-term data storage.

It uses in-memory Python data structures:
- Dictionaries for parking slot management
- Lists for completed transactions

This design follows the original project scope, which focused on:
- Slot availability logic
- Billing calculation
- Transaction flow
- GUI-based interaction

All data exists only during runtime and resets when the application is closed.

---

## User Interface

The application runs on a single screen divided into three sections.

### Vehicle Entry Section
- Vehicle type selection
- Slot allocation
- Vehicle number input

### Vehicle Exit Section
- Charge calculation
- Entry time and exit time display
- Slot release

### Transactions Section
- Completed transaction list
- Parking details and charges
- PDF export option

A logo is displayed in the interface for visual identity.

---

## Screenshot

![Park-O-Meter Main Screen](main_ui.png)

---

## Tech Stack

- Python 3
- Tkinter
- CustomTkinter
- ReportLab
- Datetime
- Math
- Pillow (PIL)

---

## Future Enhancements

- UI layout and theming improvements
- Session-based data export and import
- Enhanced reporting and summaries
- Configurable parking rate settings
- Improved validation and user feedback

---

## Notes

This project was intentionally built without database persistence, as the project description focused on real-time system behavior rather than long-term data storage.

The current implementation reflects the defined requirements and demonstrates core parking management logic effectively.
