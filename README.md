# Hayabusa Event Log Scanner Menu

<img width="977" height="510" alt="image" src="https://github.com/user-attachments/assets/352a5f97-8325-4017-ae72-d8e1a8dda191" />

![WindowsSandboxRemoteSession_3dOWevfA7m](https://github.com/user-attachments/assets/4d204f41-d243-4c0d-95f3-a46cf2351634)


**Version:** 1.2 (Includes HTML Report Support)  
**Author:** DFIRVault

This Python script is a Windows-friendly wrapper for the [Hayabusa](https://github.com/Yamato-Security/hayabusa) event log timeline tool.  
It provides a simple, menu-driven interface to scan folders or mounted forensic images containing `.evtx` files, then generates **CSV timelines** and **HTML reports** for digital forensic and incident response (DFIR) work.

---

## ✨ Features

- **GUI Folder/File Selection**  
  Uses a simple Tkinter interface to pick Hayabusa's executable, EVTX folders, and output locations.
- **CSV + HTML Output**  
  Automatically generates both a machine-readable CSV timeline and a human-readable HTML report.
- **Case-Based Naming**  
  Outputs files with the format:
  ```
  YYYYMMDD-FolderName-CaseName-results.csv
  YYYYMMDD-FolderName-CaseName-report.html
  YYYYMMDD-FolderName-CaseName-log.txt
  ```
- **Subfolder Search**  
  Optionally scans subdirectories to find EVTX files if not in the main folder.
- **Forensic Image Support**  
  Can scan mounted images or point directly to standard Windows log locations.
- **Portable**  
  No installation needed — run directly from Python.

---

## 📦 Requirements

- **Operating System:** Windows 10/11  
- **Python:** 3.7+  
- **Dependencies:**
  ```bash
  pip install pywin32
  ```
- **Hayabusa:** Download the latest release from  
  [https://github.com/Yamato-Security/hayabusa/releases](https://github.com/Yamato-Security/hayabusa/releases)

---

## 🚀 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/dfirvault/hayabusa-log-tool.git
   cd hayabusa-log-tool
   ```

2. **Install Python dependencies:**
   ```bash
   pip install pywin32
   ```

3. **Download Hayabusa** and place `hayabusa.exe` in:
   - `C:\Tools\Hayabusa\hayabusa.exe`, or  
   - The same directory as this script.

---

## 🖥️ Usage

Run the script with Python:
```bash
python hayabusa_tool.py
```

### Menu Options:
```
[1] Scan a folder or mounted image containing EVTX files
[0] Exit
```

---

## 📂 Example Workflow

1. Start the script.
2. Select the location of `hayabusa.exe` (first run only).
3. Choose **[1]** to scan EVTX files.
4. Select a folder containing `.evtx` files (or let the tool search subfolders).
5. Choose an output location for reports.
6. Enter a **case name** (e.g., MAL2024-001).
7. Wait for Hayabusa to complete — results will open automatically in Windows Explorer.

---

## 📄 Example Output

**CSV Timeline:**  
```
20240815-WorkstationLogs-MAL2024-001-results.csv
```

**HTML Report:**  
```
20240815-WorkstationLogs-MAL2024-001-report.html
```

**Log File:**  
```
20240815-WorkstationLogs-MAL2024-001-log.txt
```

---

## ⚠️ Notes & Tips

- **Run as Admin:** Some log locations may require elevated privileges. Uncomment the `is_admin()` section in `main()` if you want automatic UAC prompts.
- **Forensic Image Support:** Mount the image and point the tool to the mounted drive’s `Windows\System32\winevt\Logs` folder.
- **Performance:** Hayabusa scan time depends on the number and size of EVTX files.

---

## 📜 License

This script is released under the MIT License.  
Hayabusa is maintained by Yamato Security and follows its own licensing terms.

---

## 🔗 References

- [Hayabusa GitHub Repository](https://github.com/Yamato-Security/hayabusa)
- [DFIRVault Blog](https://github.com/dfirvault)
