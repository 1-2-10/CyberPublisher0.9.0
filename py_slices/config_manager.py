import configparser

def write_conf(template, data_xml, output_dir, overwrite_var, render_mode_var, ext_var, enable_log_var, log_mode_var):
    config = configparser.ConfigParser()
    config['paths'] = {
        'template': template,
        'data_xml': data_xml,
        'output_dir': output_dir
    }
    config['settings'] = {
        'overwrite': 'true' if overwrite_var.get() else 'false',
        'render_mode': 'loop' if render_mode_var.get() else 'default',
        'file_ext': ext_var.get()
    }
    log_mode_map = {
        "Brief": "1",
        "Verbose": "2",
        "Developer": "3"
    }
    log_mode_value = log_mode_map.get(log_mode_var.get(), "0") if enable_log_var.get() else "0"
    config['main'] = {
        'log_mode': log_mode_value
    }
    with open('CyberPublisher.conf', 'w') as configfile:
        config.write(configfile)

def last_check(label_template, label_data_xml, label_output, cli_textbox, btn_publish, confirm_checkbox, confirm_var):
    missing = []
    if 'No template' in label_template.cget("text"):
        missing.append("Template File")
    if 'No data XML' in label_data_xml.cget("text"):
        missing.append("Data XML File")
    if 'No output' in label_output.cget("text"):
        missing.append("Output Directory")
    cli_textbox.configure(state="normal")
    cli_textbox.insert("end", f"--- Re-checking selections ---\n")
    if missing:
        cli_textbox.insert("end", f"⚠️ Missing selections: {', '.join(missing)}\n")
        btn_publish.configure(state="disabled")
        confirm_checkbox.pack_forget()
        confirm_var.set(False)
        success = False
    else:
        cli_textbox.insert("end", "✅ All selections confirmed.\n")
        btn_publish.configure(state="normal")
        success = True
    cli_textbox.see("end")
    cli_textbox.configure(state="disabled")
    return success

def log_config_change(cli_textbox, setting_name, new_value):
    cli_textbox.configure(state="normal")
    cli_textbox.insert("end", f"🔧 Config updated: {setting_name} = {new_value}\n")
    cli_textbox.see("end")
    cli_textbox.configure(state="disabled")
