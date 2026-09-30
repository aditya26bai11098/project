# irctc online ticket booking system.py
## IRCTC Ticket Booking & Reservation Management System
A console-based Railway Reservation Portal implemented in Python. This software engineering application simulates core operations of the Indian Railway Catering and Tourism Corporation (IRCTC) ecosystem, handling inventory control, transactional integrity, multi-tier pricing strategies, passenger waitlist allocation queuing, and operational chart deployment.
------------------------------
## 🚀 Key Features

* Session Management Architecture: Dynamic application state configuration based on active authentication parameters (Secure User Registration & Login routing validation).
* Multi-Coach Capacity Tracking: Isolated seat allocations for AC (Air Conditioned), SL (Sleeper), and GEN (General) accommodations with strict concurrency mapping.
* Dynamic Fare Computation: Programmatic adjustment of tariff schedules scaling base metrics against defined coach-tier pricing multipliers.
* Automated Berth Selection Engine: Interactive operational tracking across distinct berth options including Lower, Middle, Upper, and Side Upper.
* Dynamic PNR Generation & Validation: Evaluates user inputs for 10-digit numerical formatting constraints while provisioning randomized, collision-resistant string IDs.
* Real-time Ticket Cancellation: Reallocates seat indices seamlessly, pushing inventory updates back to targeted coach structures instantly upon validation.
* Chart Preparation & Upgrade Engine: Compiles precise passenger manifests. During chart compilation, it automatically updates Waitlisted (WL) and RAC bookings to CONFIRMED if cancellations create open seats.
* Cross-Platform File System Exporter: Bypasses macOS root-directory constraints by programmatically targeting user-level path hierarchies (~/Downloads) to export structured text records securely.

------------------------------
## 🛠️ System Design & Architecture
The application avoids complex framework overhead by managing its persistence model using fast, in-memory data structures:

[Main Menu Interface] <---> [User Session Manager]
         |
         +---> [Trains Inventory Matrix]  (Dictionaries inside Lists)
         +---> [Passenger Booking Ledger] (Dynamic Record Map)
         +---> [Chart Compiler Engine]    (Automated Local File Exporter)

## Data Layer Structure

* trains: Schema structuring numbers, identifiers, stations, base fare indexes, and discrete coach capacity trackers.
* bookings: Ledger recording the distinct properties of active tickets (PNR, identification parameters, berths, status codes, and financial ledger data).

------------------------------
## 💻 How to Execute the Application## Prerequisites

* Python 3.x installed locally.
* Standard command-line terminal environment access.

## Execution Routine

   1. Open your terminal application and change directory to the path holding the code file:
   
   cd /path/to/your/project/folder
   
   2. Run the program using the terminal interpreter:
   
   python3 irctc_system.py
   
   3. Default Admin Login Credentials (Pre-configured for testing):
   * Username: admin
      * Password: password123
   
------------------------------
## 📊 Sample Execution Output## Available Trains Display Matrix

--- Available Trains ---
Train No   Train Name           From   To     AC    SL    GEN   Base Fare 
---------------------------------------------------------------------------
12626      Kerala Express       NDLS   TVC    2     5     10    Rs.500
12952      Mumbai Rajdhani      NDLS   MMCT   4     2     0     Rs.1200
12002      Bhopal Shatabdi      NDLS   BPL    6     0     8     Rs.400

## Official Reservation Chart (Exported File Output)

=======================================================
       OFFICIAL RESERVATION CHART: KERALA EXPRESS (12626)   
=======================================================
PNR Number     Passenger Name     Coach   Berth        Final Status
--------------------------------------------------------------------
8473920193     Aditya Alok        AC      LOWER        CONFIRMED   
5839201948     John Doe           SL      UPPER        CONFIRMED   
2948103957     Jane Smith         AC      LOWER        WL          
=======================================================

------------------------------
## 📁 Technical Specifications & Rules Checked

* Line Limit Compliance: Synthesized within standard parameters (~250 total lines of code) without using high-level dependencies or frameworks.
* Robust Input Handling: Features explicit defensive structures handling alphanumeric runtime evaluation errors (ValueError), string anomalies, and database mismatch situations safely.
* File Write Permissions: File-handling processes utilize automated platform evaluation methods (os.path.expanduser) to ensure proper write execution rules across Unix, macOS, and Windows operating systems.

------------------------------




