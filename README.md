# CyberPublisher v0.9.0

CyberPublisher is the next evolution of **phPublisher**, transforming it from a lean PHP-based static publishing engine into a full-fledged **Python GUI application**.

## 🚀 Project Origins

This tool began as **phPublisher**, a minimalist PHP script designed to generate static content from XML templates. While powerful and lightweight, it lacked a graphical interface and modern extensibility.

## 🔥 The Morph

CyberPublisher v0.9.0 represents a major milestone:

- Rebuilt the publishing engine in **Python** for portability, maintainability, and future expansion.
- Developed a **full GUI using `tkinter` and `Customtkinter`**, enabling users to manage publishing cycles without direct CLI editing.
- Structured as a modular, scalable codebase with **py_slices** for clean separation of functionality.

## ⚙️ Current State

- The publishing engine (`prnt_shop.py`) supports:
  - Standard per-page publishing from XML.
  - Loop mode for index generation.
  - Dynamic file extension output (.html, .css, .json, etc.).
  - Real-time CLI-style output within the GUI.
  - Config persistence via `.conf` files.

- **Note:** CyberPublisher v0.9.0 is not yet packaged as a standalone executable.  
  It currently requires:
  - A working Python environment (Python 3.8+ recommended).
  - Installation of dependencies, including `customtkinter`.
  - CLI launch within the proper virtual environment to run the GUI.

## 🛠️ Roadmap

- Package as a standalone desktop app (Windows/Linux/macOS).  
- Enhance GUI with top navigation bar for About, Manpages, and dynamic settings.  
- Extend publishing logic to support multi-directory index linking, relative/absolute path management, and theming.

## 🤝 Contributing

This project is in its active development phase. Contributions, suggestions, or even general interest discussions are welcome.

---

> *CyberPublisher – because publishing should be powerful, fast, and fun.*
