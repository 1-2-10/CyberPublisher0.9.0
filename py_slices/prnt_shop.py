#!/usr/bin/env python3
# prnt-shop.py – Python publishing engine for CyberPublisher

import configparser
import os
import sys
import xml.etree.ElementTree as ET
import re
from datetime import datetime
from py_slices.logging import setup_logger, log_event, log_exception

def run_publish(conf_path='CyberPublisher.conf', logging_enabled=False, mode="Brief", overwrite=False, loop_render_mode=False):
    logger = None
    if logging_enabled:
        logger = setup_logger(mode=mode, enable_logging=logging_enabled)
    logs = []

    # Add simple timestamp for Brief mode
    if mode == "Brief":
        logs.append(datetime.now().strftime("%Y-%m-%d"))
    logs.append("############################")

    # === Config Parsing ===
    if not os.path.exists(conf_path):
        msg = f"❌ 🤣 Config file '{conf_path}' not found."
        logs.append(msg)
        if logger:
            log_event(logger, msg, level="error", mode=mode, enable_logging=logging_enabled)
        return logs

    config = configparser.ConfigParser()
    config.read(conf_path)
    msg = f"✅ 👉 Config file '{conf_path}' parsed."
    logs.append(msg)
    if logger:
        log_event(logger, msg, mode=mode, enable_logging=logging_enabled)

    # === Paths from config ===
    try:
        template_file = config['paths']['template']
        xml_file = config['paths']['data_xml']
        output_dir = config['paths']['output_dir']
        file_ext = config.get('settings', 'file_ext', fallback='.html')
        if not file_ext.startswith('.'):
            file_ext = '.' + file_ext
    except KeyError as e:
        msg = f"❌ 🤣 Missing config key: {e}"
        logs.append(msg)
        if logger:
            log_event(logger, msg, level="error", mode=mode, enable_logging=logging_enabled)
        return logs

    os.makedirs(output_dir, exist_ok=True)
    msg = f"✅ 👉 Output directory ensured: {output_dir}"
    logs.append(msg)
    if logger:
        log_event(logger, msg, mode=mode, enable_logging=logging_enabled)

    # === XML Parsing ===
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        msg = f"✅ 👉 XML file '{xml_file}' parsed."
        logs.append(msg)
        if logger:
            log_event(logger, msg, mode=mode, enable_logging=logging_enabled)
    except ET.ParseError as e:
        msg = f"❌ 🤣 Failed to parse XML file '{xml_file}': {e}"
        logs.append(msg)
        if logger:
            log_event(logger, msg, level="error", mode=mode, enable_logging=logging_enabled)
        return logs

    # === Load Template ===
    with open(template_file, 'r') as f:
        template_content = f.read()
    msg = f"✅ 👉 Template file '{template_file}' loaded."
    logs.append(msg)
    if logger:
        log_event(logger, msg, mode=mode, enable_logging=logging_enabled)

    # === Loop Render Mode ===
    if loop_render_mode:
        loop_pattern = re.compile(r'\[\[loop\]\](.*?)\[\[endloop\]\]', re.DOTALL)
        match = loop_pattern.search(template_content)
        if match:
            before = template_content[:match.start()]
            after = template_content[match.end():]
            loop_block = match.group(1)
            loop_content = ''
            for page in root.findall('page'):
                pg_data = {child.tag: (child.text or "") for child in page}

                # Use pg-id as base filename with selected ext for index links
                pg_id = pg_data.get('id', 'output')
                selected_ext = config['settings'].get('file_ext', '.html')
                link_href = pg_id + selected_ext
                pg_data['pg-id'] = link_href

                entry = loop_block
                for key, value in pg_data.items():
                    entry = entry.replace(f"[[{key}]]", value)
                entry = re.sub(r'\[\[[^\]]+\]\]', '', entry)
                loop_content += entry

            output_content = before + loop_content + after
        else:
            # No loop block, fallback to first page
            page = root.find('page')
            output_content = template_content
            if page is not None:
                pg_data = {child.tag: child.text for child in page}
                for key, value in pg_data.items():
                    output_content = output_content.replace(f"[[{key}]]", value)

        output_path = os.path.join(output_dir, 'index' + file_ext)
        with open(output_path, 'w') as f:
            f.write(output_content)
        msg = f"gen'd: {output_path}"
        logs.append(msg)
        if logger:
            log_event(logger, msg, mode=mode, enable_logging=logging_enabled)


    # === Standard Per-Page Publishing ===
    else:
        for page in root.findall('page'):
            pg_data = {child.tag: (child.text or "") for child in page}
            output_content = template_content
            for key, value in pg_data.items():
                output_content = output_content.replace(f"[[{key}]]", value)

            base_name = os.path.splitext(pg_data.get('file_nm', 'output'))[0]
            file_nm = base_name + file_ext
            pg_data['file_nm'] = file_nm

            output_path = os.path.join(output_dir, file_nm)

            if not overwrite and os.path.exists(output_path):
                msg = f"Skipped (already exists): {output_path}"
                logs.append(msg)
                if logger:
                    log_event(logger, msg, mode=mode, enable_logging=logging_enabled)
                continue

            with open(output_path, 'w') as f:
                f.write(output_content)
            msg = f"gen'd: {output_path}"
            logs.append(msg)
            if logger:
                log_event(logger, msg, mode=mode, enable_logging=logging_enabled)

    # === Completion Banner ===
    msg = "############################"
    logs.append(msg)
    if logger:
        log_event(logger, msg, mode=mode, enable_logging=logging_enabled)
    msg = "✅ 👉 CyberPublisher op completed."
    logs.append(msg)
    if logger:
        log_event(logger, msg, mode=mode, enable_logging=logging_enabled)
    msg = f" 🕒 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    logs.append(msg)
    if logger:
        log_event(logger, msg, mode=mode, enable_logging=logging_enabled)
    msg = "############################"
    logs.append(msg)
    if logger:
        log_event(logger, msg, mode=mode, enable_logging=logging_enabled)

    return logs
