import os
from tkinter import filedialog
from py_slices.config_manager import last_check
from py_slices.logging import setup_logger, log_event

# Setup logger once at module load
logger = setup_logger()

def pick_template(label_template, label_data_xml, label_output, cli_textbox, btn_publish, confirm_checkbox, confirm_var, log_mode_var=None):
    file_path = filedialog.askopenfilename(
        title="Select Template File",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        label_template.configure(text=f"{file_path}")
        log_event(logger, f"Template file selected: {file_path}", level="debug" if log_mode_var and log_mode_var.get() == "DevMode" else "info")
    last_check(label_template, label_data_xml, label_output, cli_textbox, btn_publish, confirm_checkbox, confirm_var)

def pick_data_xml(label_data_xml, label_template, label_output, cli_textbox, btn_publish, confirm_checkbox, confirm_var, log_mode_var=None):
    file_path = filedialog.askopenfilename(
        title="Select Data XML File",
        filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
    )
    if file_path:
        label_data_xml.configure(text=f"{file_path}")
        log_event(logger, f"Data XML file selected: {file_path}", level="debug" if log_mode_var and log_mode_var.get() == "DevMode" else "info")
    last_check(label_template, label_data_xml, label_output, cli_textbox, btn_publish, confirm_checkbox, confirm_var)

def pick_output_location(label_output, label_template, label_data_xml, cli_textbox, btn_publish, confirm_checkbox, confirm_var, log_mode_var=None):
    dir_path = filedialog.askdirectory(title="Select Output Directory")
    if dir_path:
        label_output.configure(text=f"{dir_path}")
        log_event(logger, f"Output directory selected: {dir_path}", level="debug" if log_mode_var and log_mode_var.get() == "DevMode" else "info")
    last_check(label_template, label_data_xml, label_output, cli_textbox, btn_publish, confirm_checkbox, confirm_var)
