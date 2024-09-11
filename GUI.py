# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 09:24:48 2024

@author: 6204821
"""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.font import Font

# Import extraction classes
from steady_state_extraction import SteadyStateExtractor
from structural_analysis_extraction import StructuralAnalysisExtractor

# Function to get node number
def get_node_number():
    node_number = simpledialog.askinteger("Input", "Enter Node Number:", minvalue=1)
    return node_number

# Function to open file dialog and select a .rst or .rth file
def select_file(index):
    file_path = filedialog.askopenfilename(
        filetypes=[("ANSYS result files", "*.rst"), ("ANSYS result files", "*.rth")],
        title=f"Select File {index + 1}"
    )
    if file_path:
        entry_vars[index].set(file_path)

def process_data():
    try:
        # Node number is asked once for all rows
        node_number = get_node_number()

        # Processing the first row (Steady State Thermal analysis)
        file_path_1 = entry_vars[0].get()
        load_step_1 = int(load_step_vars[0].get())
        sub_step_1 = int(sub_step_vars[0].get())

        steady_state_extractor = SteadyStateExtractor(file_path_1, node_number, load_step_1, sub_step_1)
        temperature = steady_state_extractor.extract_data()
        output_data_vars[0].set(f"{temperature:.2f}")

        # Processing the second row (Structural Analysis)
        file_path_2 = entry_vars[1].get()
        load_step_2 = int(load_step_vars[1].get())
        sub_step_2 = int(sub_step_vars[1].get())

        structural_extractor = StructuralAnalysisExtractor(file_path_2, node_number, load_step_2, sub_step_2)
        stress = structural_extractor.extract_data()
        output_data_vars[1].set(f"{stress:.2f}")

        messagebox.showinfo("Success", "Data extracted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("ANSYS Data Extraction")

# Creating a bold font for headers
header_font = Font(root, weight="bold")

# Parameter descriptions
descriptions = [
    "Steady State Temperature (deg C)",
    "Von Mises Stress during Normal Plant Operation (MPa)"
]

# Variables to hold file paths, load steps, sub steps, and output data
entry_vars = [tk.StringVar() for _ in descriptions]
load_step_vars = [tk.StringVar() for _ in descriptions]
sub_step_vars = [tk.StringVar() for _ in descriptions]
output_data_vars = [tk.StringVar() for _ in descriptions]

# Create the grid layout for inputs
for i, desc in enumerate(descriptions):
    tk.Label(root, text=desc, font=header_font).grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
    tk.Entry(root, textvariable=entry_vars[i], state="readonly", width=50).grid(row=i+1, column=1, padx=5, pady=5)
    tk.Button(root, text="Select File", command=lambda i=i: select_file(i)).grid(row=i+1, column=2, padx=5, pady=5)
    tk.Label(root, text="Load Step:").grid(row=i+1, column=3, padx=5, pady=5, sticky="e")
    tk.Entry(root, textvariable=load_step_vars[i], width=5).grid(row=i+1, column=4, padx=5, pady=5)
    tk.Label(root, text="Sub Step:").grid(row=i+1, column=5, padx=5, pady=5, sticky="e")
    tk.Entry(root, textvariable=sub_step_vars[i], width=5).grid(row=i+1, column=6, padx=5, pady=5)
    tk.Label(root, text="Output:").grid(row=i+1, column=7, padx=5, pady=5, sticky="e")
    tk.Entry(root, textvariable=output_data_vars[i], state="readonly", width=15).grid(row=i+1, column=8, padx=5, pady=5)

# Button to confirm input and extract data
tk.Button(root, text="Confirm", command=process_data).grid(row=len(descriptions) + 1, column=8, padx=5, pady=20)

# Start the main loop
root.mainloop()