import time
import threading
from py_slices.prnt_shop import run_publish
from py_slices.logging import setup_logger, log_event, log_exception

def _run_publish_task(t, d, o, cli_textbox, btn_publish, progress_bar,
                      overwrite_var, render_mode_var, ext_var, enable_log_var, log_mode_var, write_conf_func):
    enable_logging = enable_log_var.get()
    mode = log_mode_var.get()
    overwrite = overwrite_var.get()
    loop_render_mode = render_mode_var.get()
    logger = None
    if enable_logging:
        logger = setup_logger(mode=mode, enable_logging=enable_logging)
    write_conf_func(t, d, o, overwrite_var, render_mode_var, ext_var, enable_log_var, log_mode_var)
    try:
        logs = run_publish(conf_path='CyberPublisher.conf', logging_enabled=enable_logging, mode=mode, overwrite=overwrite, loop_render_mode=loop_render_mode)
        cli_textbox.configure(state="normal")
        for line in logs:
            cli_textbox.insert("end", line + "\n")
        cli_textbox.see("end")
        cli_textbox.configure(state="disabled")
    except Exception as e:
        import traceback
        cli_textbox.configure(state="normal")
        cli_textbox.insert("end", f"Error running Python publish engine:\n{e}")
        cli_textbox.configure(state="disabled")
        if logger:
            log_exception(logger, e, mode=mode, enable_logging=enable_logging)
    time.sleep(1)  # Artificial delay for user experience
    progress_bar.stop()
    progress_bar.pack_forget()
    btn_publish.configure(state="normal")

def publish(safemode_var, label_template, label_data_xml, label_output, cli_textbox, btn_publish,
            confirm_var, confirm_checkbox, ext_var, overwrite_var, render_mode_var,
            enable_log_var, log_mode_var, progress_bar, write_conf_func, last_check_func):
    if not last_check_func(label_template, label_data_xml, label_output, cli_textbox, btn_publish, confirm_checkbox, confirm_var):
        return
    if safemode_var.get():
        if not confirm_var.get():
            t = label_template.cget("text")
            d = label_data_xml.cget("text")
            o = label_output.cget("text")
            ext = ext_var.get()
            overwrite = 'Enabled' if overwrite_var.get() else 'Disabled'
            render_mode = 'Enabled' if render_mode_var.get() else 'Disabled'
            logging = 'Enabled' if enable_log_var.get() else 'Disabled'
            log_mode = log_mode_var.get() if enable_log_var.get() else ''
            cli_textbox.configure(state="normal")
            cli_textbox.insert("end", "\n=== SafeMode: Please review your selections ===\n")
            cli_textbox.insert("end", f"Template file path: {t}\n")
            cli_textbox.insert("end", f"XML data file path: {d}\n")
            cli_textbox.insert("end", f"\nOptions:\n")
            cli_textbox.insert("end", f"Enable Overwrite: {overwrite}\n")
            cli_textbox.insert("end", f"Enable loop, render mode: {render_mode}\n")
            if enable_log_var.get():
                cli_textbox.insert("end", f"Enable Logging: Enabled ({log_mode})\n")
            else:
                cli_textbox.insert("end", f"Enable Logging: Disabled\n")
            cli_textbox.insert("end", f"\nOutput file path/destination: {o}\n")
            cli_textbox.insert("end", f"Output file extension selected: {ext}\n")
            cli_textbox.insert("end", "\nPlease confirm to continue.\n")
            cli_textbox.see("end")
            cli_textbox.configure(state="disabled")
            confirm_checkbox.pack(anchor="w", padx=10, pady=5)
            btn_publish.configure(state="disabled")
            return
    confirm_checkbox.pack_forget()
    confirm_var.set(False)
    btn_publish.configure(state="disabled")
    t = label_template.cget("text")
    d = label_data_xml.cget("text")
    o = label_output.cget("text")
    progress_bar.pack(fill="x", pady=(5,0))
    progress_bar.start()
    threading.Thread(target=_run_publish_task, args=(
        t, d, o, cli_textbox, btn_publish, progress_bar,
        overwrite_var, render_mode_var, ext_var, enable_log_var, log_mode_var, write_conf_func
    )).start()
