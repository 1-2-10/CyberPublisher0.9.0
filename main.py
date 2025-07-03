import customtkinter as ctk
from tkinter import filedialog
import threading
from customtkinter import CTkTextbox
import os
import sys
import traceback

from py_slices.logging import setup_logger, log_event
from py_slices.file_picker import pick_template, pick_data_xml, pick_output_location
from py_slices.config_manager import write_conf, last_check, log_config_change  # <-- Added log_config_change
from py_slices.publisher import publish
from py_slices.reset import reset_all

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("CyberPublisher0.9.0")
root.geometry("860x780")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# === Input Frame ===
input_frame = ctk.CTkFrame(root, fg_color="#D0D0D0", corner_radius=14)
input_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

input_label = ctk.CTkLabel(input_frame, text="Input Files", font=("Arial", 18, "bold"))
input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

label_template = ctk.CTkLabel(input_frame, text="No template selected", wraplength=600, font=("Arial", 16))
label_template.grid(row=2, column=0, padx=5, sticky="w")
btn_template = ctk.CTkButton(input_frame, text="Pick Template File",
    command=lambda: pick_template(label_template, label_data_xml, label_output, cli_textbox, btn_publish, confirm_checkbox, confirm_var),
    width=180, font=("Arial", 16))
btn_template.grid(row=1, column=0, padx=5, pady=5, sticky="w")

label_data_xml = ctk.CTkLabel(input_frame, text="No data XML selected", wraplength=600, font=("Arial", 16))
label_data_xml.grid(row=4, column=0, padx=5, sticky="w")

btn_data_xml = ctk.CTkButton(input_frame, text="Pick Data XML File",
    command=lambda: pick_data_xml(label_data_xml, label_template, label_output, cli_textbox, btn_publish, confirm_checkbox, confirm_var),
    width=180, font=("Arial", 16))
btn_data_xml.grid(row=3, column=0, padx=5, pady=5, sticky="w")

# === Output Frame ===
output_frame = ctk.CTkFrame(root, fg_color="#D0D0D0", corner_radius=14)
output_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

output_label = ctk.CTkLabel(output_frame, text="Output Settings", font=("Arial", 18, "bold"))
output_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

label_output = ctk.CTkLabel(output_frame, text="No output dir selected", wraplength=600, font=("Arial", 16))
label_output.grid(row=2, column=0, padx=5, sticky="w")

btn_output = ctk.CTkButton(output_frame, text="Pick Output Directory",
    command=lambda: pick_output_location(label_output, label_template, label_data_xml, cli_textbox, btn_publish, confirm_checkbox, confirm_var),
    width=180, font=("Arial", 16))
btn_output.grid(row=1, column=0, padx=5, pady=5, sticky="w")

ext_var = ctk.StringVar(value=".html")
ext_options = [".html", ".php", ".txt", ".css", ".md", ".json", ".xml"]

def ext_change_callback(choice):
    log_config_change(cli_textbox, "File Extension", choice)
    write_conf(label_template.cget("text"), label_data_xml.cget("text"), label_output.cget("text"),
               overwrite_var, render_mode_var, ext_var, enable_log_var, log_mode_var)

ext_menu = ctk.CTkOptionMenu(output_frame, variable=ext_var, values=ext_options, width=120, font=("Arial", 16),
                             command=ext_change_callback)
ext_menu.grid(row=3, column=0, padx=5, pady=(5,10), sticky="w")

# === Options Frame ===
options_frame = ctk.CTkFrame(root, fg_color="#D0D0D0", corner_radius=14)
options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

options_label = ctk.CTkLabel(options_frame, text="Options", font=("Arial", 18, "bold"))
options_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

overwrite_var = ctk.BooleanVar()

def overwrite_toggle_callback():
    new_value = 'Enabled' if overwrite_var.get() else 'Disabled'
    log_config_change(cli_textbox, "Overwrite", new_value)
    write_conf(label_template.cget("text"), label_data_xml.cget("text"), label_output.cget("text"),
               overwrite_var, render_mode_var, ext_var, enable_log_var, log_mode_var)

overwrite_checkbox = ctk.CTkCheckBox(options_frame, text="Enable Overwrite", variable=overwrite_var,
                                     command=overwrite_toggle_callback, font=("Arial", 14))
overwrite_checkbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")

render_mode_var = ctk.BooleanVar()

def render_mode_toggle_callback():
    new_value = 'Loop' if render_mode_var.get() else 'Default'
    log_config_change(cli_textbox, "Render Mode", new_value)
    write_conf(label_template.cget("text"), label_data_xml.cget("text"), label_output.cget("text"),
               overwrite_var, render_mode_var, ext_var, enable_log_var, log_mode_var)

render_mode_checkbox = ctk.CTkCheckBox(options_frame, text="Enable Loop Render Mode", variable=render_mode_var,
                                       command=render_mode_toggle_callback, font=("Arial", 14))
render_mode_checkbox.grid(row=2, column=0, padx=5, pady=5, sticky="w")

enable_log_var = ctk.BooleanVar()
log_mode_var = ctk.StringVar(value="Mode")

def toggle_log_dropdown():
    if enable_log_var.get():
        log_mode_dropdown.configure(state="normal")
        log_config_change(cli_textbox, "Logging", "Enabled")
    else:
        log_mode_dropdown.configure(state="disabled")
        log_config_change(cli_textbox, "Logging", "Disabled")
    write_conf(label_template.cget("text"), label_data_xml.cget("text"), label_output.cget("text"),
               overwrite_var, render_mode_var, ext_var, enable_log_var, log_mode_var)

enable_log_checkbox = ctk.CTkCheckBox(options_frame, text="Enable Logging",
                                      variable=enable_log_var, command=toggle_log_dropdown,
                                      font=("Arial", 14))
enable_log_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w")

def log_mode_change_callback(choice):
    log_config_change(cli_textbox, "Log Mode", choice)
    write_conf(label_template.cget("text"), label_data_xml.cget("text"), label_output.cget("text"),
               overwrite_var, render_mode_var, ext_var, enable_log_var, log_mode_var)

log_mode_dropdown = ctk.CTkOptionMenu(options_frame, variable=log_mode_var,
                                      values=["Brief", "Verbose", "DevMode"],
                                      width=100, font=("Arial", 14),
                                      command=log_mode_change_callback)
log_mode_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")
log_mode_dropdown.configure(state="disabled")

# === Right Bottom Frame ===
right_bottom_frame = ctk.CTkFrame(root, fg_color="#D0D0D0", corner_radius=14)
right_bottom_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

# === Safemode Sub Frame ===
safemode_var = ctk.BooleanVar()
confirm_var = ctk.BooleanVar()

def toggle_safemode_checkbox():
    if safemode_var.get():
        confirm_checkbox.pack_forget()
        confirm_var.set(False)
        log_config_change(cli_textbox, "SafeMode", "Enabled")
    else:
        confirm_checkbox.pack_forget()
        confirm_var.set(False)
        btn_publish.configure(state="normal")
        log_config_change(cli_textbox, "SafeMode", "Disabled")
    write_conf(label_template.cget("text"), label_data_xml.cget("text"), label_output.cget("text"),
               overwrite_var, render_mode_var, ext_var, enable_log_var, log_mode_var)

def enable_publish():
    if confirm_var.get():
        btn_publish.configure(state="normal")
    else:
        btn_publish.configure(state="disabled")

safemode_checkbox = ctk.CTkCheckBox(right_bottom_frame,
                                    text="Enable SafeMode (double-check before publish)",
                                    variable=safemode_var,
                                    command=toggle_safemode_checkbox,
                                    font=("Arial", 14))
safemode_checkbox.pack(anchor="w", padx=10, pady=5)

confirm_checkbox = ctk.CTkCheckBox(right_bottom_frame,
                                   text="Confirm and Continue",
                                   variable=confirm_var,
                                   font=("Arial", 14),
                                   command=enable_publish)
confirm_checkbox.pack_forget()

# === Publish Button and Frame ===
publish_frame = ctk.CTkFrame(right_bottom_frame, fg_color="transparent")
publish_frame.pack(fill="x", padx=10, pady=5)

btn_publish = ctk.CTkButton(publish_frame, text_color="#000000", text="Push Publish Cycle",
                            font=("Arial", 18, "bold"),
                            command=lambda: publish(
    safemode_var, label_template, label_data_xml, label_output,
    cli_textbox, btn_publish, confirm_var, confirm_checkbox,
    ext_var, overwrite_var, render_mode_var, enable_log_var,
    log_mode_var, progress_bar, write_conf, last_check
))
btn_publish.pack(fill="x")
btn_publish.configure(state="normal")  # Start active unless SafeMode disables

# === Progress Bar ===
progress_bar = ctk.CTkProgressBar(publish_frame, mode="indeterminate", height=8)
progress_bar.pack(fill="x", pady=(5, 0))
progress_bar.pack_forget()

# === Reset All Button ===
reset_btn = ctk.CTkButton(publish_frame, text="Reset All", font=("Arial", 14),
    command=lambda: reset_all(label_template, label_data_xml, label_output, cli_textbox, btn_publish, confirm_checkbox, confirm_var,
                             ext_var, overwrite_var, render_mode_var, enable_log_var, log_mode_var, progress_bar))
reset_btn.pack(fill="x", pady=(8, 0))

# --- Disable Reset All during publish ---
def set_buttons_state(state):
    btn_publish.configure(state=state)
    reset_btn.configure(state=state)

# Patch publish to disable Reset All during execution
old_publish = btn_publish.cget('command')
def wrapped_publish():
    reset_btn.configure(state="disabled")
    publish(
        safemode_var, label_template, label_data_xml, label_output,
        cli_textbox, btn_publish, confirm_var, confirm_checkbox,
        ext_var, overwrite_var, render_mode_var, enable_log_var,
        log_mode_var, progress_bar, write_conf, last_check
    )
    reset_btn.configure(state="normal")
btn_publish.configure(command=wrapped_publish)

# === CLI Output Frame ===
cli_frame = ctk.CTkFrame(root, fg_color="#333333", corner_radius=14)
cli_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

cli_label = ctk.CTkLabel(cli_frame, text="system Output", font=("Arial", 14, "bold"), text_color="#FFFFFF")
cli_label.pack(pady=(5, 0))

cli_textbox = ctk.CTkTextbox(cli_frame, height=240, wrap="word")
cli_textbox.pack(fill="both", expand=True, padx=10, pady=10)
cli_textbox.configure(state="disabled", font=("monospace", 15))

root.mainloop()
