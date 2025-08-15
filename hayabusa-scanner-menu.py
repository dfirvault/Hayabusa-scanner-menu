import os
import subprocess
import time
import platform
from datetime import datetime
import sys
import ctypes
import win32con
import re
from tkinter import Tk, filedialog

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if platform.system() != 'Windows':
        print("This script requires Windows.")
        return False
        
    if not is_admin():
        print("Requesting administrator privileges...")
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:])
        
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
        except Exception as e:
            print(f"Failed to elevate privileges: {str(e)}")
            return False
        return True
    return False

def select_file(title, initialdir=None, filetypes=None):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(
        title=title,
        initialdir=initialdir,
        filetypes=filetypes
    )
    root.destroy()
    return file_path

def select_folder(title, initialdir=None):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder_path = filedialog.askdirectory(
        title=title,
        initialdir=initialdir
    )
    root.destroy()
    return folder_path

def find_evtx_folder(start_path):
    evtx_folders = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.lower().endswith('.evtx'):
                if root not in evtx_folders:
                    evtx_folders.append(root)
    return evtx_folders

def main():
    #if platform.system() == 'Windows' and not is_admin():
    #    if run_as_admin():
    #        sys.exit(0)
    #    else:
    #        print("This script must be run as administrator.")
    #        input("Press Enter to exit...")
    #        sys.exit(1)

    print("\nHayabusa Event Log Processing Tool")
    print("Version 1.2 - Includes HTML Reports\n")

    # Hayabusa path configuration
    config_file = "hayabusa-config.txt"
    hayabusa_path = ""
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            hayabusa_path = f.readline().strip()

    if not hayabusa_path:
        hayabusa_path = r"C:\Tools\Hayabusa\hayabusa.exe"
        if not os.path.exists(hayabusa_path):
            if os.path.exists("hayabusa.exe"):
                hayabusa_path = os.path.join(os.getcwd(), "hayabusa.exe")

    while not os.path.exists(hayabusa_path):
        print("\nHayabusa executable not found.")
        try:
            hayabusa_path = select_file(
                "Select Hayabusa executable (hayabusa.exe)",
                initialdir=os.getcwd(),
                filetypes=[("Hayabusa Executable", "hayabusa*.exe"), ("All files", "*.*")]
            )
            
            if not hayabusa_path:
                print("File selection cancelled. Exiting...")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error showing file dialog: {e}")
            hayabusa_path = input("Enter full path to Hayabusa executable: ").strip()
        
        if hayabusa_path and os.path.isdir(hayabusa_path):
            hayabusa_path = os.path.join(hayabusa_path, "hayabusa.exe")
    
    with open(config_file, 'w') as f:
        f.write(hayabusa_path)

    # Main menu
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===============================")
        print("    Hayabusa Event Log Scanner")
        print("===============================\n")
        print("[1] Scan a folder or mounted image containing EVTX files")
        #print("[2] Scan a mounted forensic image")
        print("[0] Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            scan_folder_with_evtx(hayabusa_path)
        #elif choice == "2":
        #    scan_mounted_image(hayabusa_path)
        elif choice == "0":
            print("\nExiting...")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(1)

def scan_folder_with_evtx(hayabusa_path):
    print("\nPlease select the folder containing EVTX files:")
    evtx_folder = select_folder("Select folder containing EVTX files")
    
    if not evtx_folder:
        print("Folder selection cancelled.")
        return
    
    evtx_files = [f for f in os.listdir(evtx_folder) if f.lower().endswith('.evtx')]
    if not evtx_files:
        print("\nNo EVTX files found in the selected folder.")
        search_subfolders = input("Search subfolders for EVTX files? (y/n): ").strip().lower()
        
        if search_subfolders == 'y':
            evtx_folders = find_evtx_folder(evtx_folder)
            if not evtx_folders:
                print("No EVTX files found in any subfolders.")
                input("Press Enter to continue...")
                return
            elif len(evtx_folders) == 1:
                evtx_folder = evtx_folders[0]
                print(f"\nUsing EVTX files from: {evtx_folder}")
            else:
                print("\nMultiple folders with EVTX files found:")
                for i, folder in enumerate(evtx_folders, 1):
                    print(f"[{i}] {folder}")
                
                while True:
                    selection = input("\nSelect folder to scan (1-{} or 'a' for all): ".format(len(evtx_folders))).strip().lower()
                    if selection == 'a':
                        for folder in evtx_folders:
                            run_hayabusa_scan(hayabusa_path, folder)
                        return
                    elif selection.isdigit() and 1 <= int(selection) <= len(evtx_folders):
                        evtx_folder = evtx_folders[int(selection)-1]
                        break
                    else:
                        print("Invalid selection.")
        else:
            input("Press Enter to continue...")
            return
    
    run_hayabusa_scan(hayabusa_path, evtx_folder)

def scan_mounted_image(hayabusa_path):
    print("\nPlease select the mounted image drive or folder:")
    image_path = select_folder("Select mounted image location")
    
    if not image_path:
        print("Folder selection cancelled.")
        return
    
    possible_paths = [
        os.path.join(image_path, "Windows", "System32", "winevt", "Logs"),
        os.path.join(image_path, "Windows", "System32", "winevt", "Logs"),
        os.path.join(image_path, "Windows", "EventLogs"),
        os.path.join(image_path, "Windows", "Logs"),
        os.path.join(image_path, "EventLogs"),
        os.path.join(image_path, "Logs")
    ]
    
    evtx_folder = None
    for path in possible_paths:
        if os.path.exists(path):
            evtx_files = [f for f in os.listdir(path) if f.lower().endswith('.evtx')]
            if evtx_files:
                evtx_folder = path
                break
    
    if not evtx_folder:
        print("\nCould not automatically find EVTX files in standard locations.")
        search_image = input("Search all folders for EVTX files? (y/n): ").strip().lower()
        
        if search_image == 'y':
            evtx_folders = find_evtx_folder(image_path)
            if not evtx_folders:
                print("No EVTX files found in the image.")
                input("Press Enter to continue...")
                return
            elif len(evtx_folders) == 1:
                evtx_folder = evtx_folders[0]
                print(f"\nUsing EVTX files from: {evtx_folder}")
            else:
                print("\nMultiple folders with EVTX files found:")
                for i, folder in enumerate(evtx_folders, 1):
                    print(f"[{i}] {folder}")
                
                while True:
                    selection = input("\nSelect folder to scan (1-{} or 'a' for all): ".format(len(evtx_folders))).strip().lower()
                    if selection == 'a':
                        for folder in evtx_folders:
                            run_hayabusa_scan(hayabusa_path, folder)
                        return
                    elif selection.isdigit() and 1 <= int(selection) <= len(evtx_folders):
                        evtx_folder = evtx_folders[int(selection)-1]
                        break
                    else:
                        print("Invalid selection.")
        else:
            input("Press Enter to continue...")
            return
    
    run_hayabusa_scan(hayabusa_path, evtx_folder)

def run_hayabusa_scan(hayabusa_path, evtx_folder):
    print("\nPlease select the folder to save reports:")
    report_path = select_folder(
        "Select folder to save reports",
        initialdir=os.path.dirname(hayabusa_path) if hayabusa_path else os.path.expanduser("~\\Documents")
    )
    
    if not report_path:
        print("Folder selection cancelled.")
        return
    
    os.makedirs(report_path, exist_ok=True)
    if not os.path.isdir(report_path):
        print("ERROR: Could not create directory")
        return

    # Get folder name for output
    folder_name = os.path.basename(os.path.normpath(evtx_folder))
    folder_name = re.sub(r'[^a-zA-Z0-9_-]', '_', folder_name)
    if not folder_name:
        folder_name = "hayabusa_scan"

    # Get case name from user
    while True:
        case_name = input("\nEnter a case name (e.g., MAL2024-001): ").strip()
        if case_name:
            case_name = re.sub(r'[^a-zA-Z0-9_-]', '_', case_name)
            break
        print("Case name cannot be empty. Please try again.")

    # Generate filenames in YYYYMMDD-FolderName-CaseName format
    now = datetime.now()
    date_prefix = now.strftime("%Y%m%d")
    
    base_filename = f"{date_prefix}-{folder_name}-{case_name}"
    csv_file = f"{base_filename}-results.csv"
    html_file = f"{base_filename}-report.html"
    log_file = f"{base_filename}-log.txt"

    # Run Hayabusa with both CSV and HTML output
    cmd = [
        hayabusa_path,
        "csv-timeline",
        "-d", evtx_folder,
        "-o", os.path.join(report_path, csv_file),
        "--ISO-8601",
        "--no-wizard",
        "--quiet",
        "--HTML-report", os.path.join(report_path, html_file)
    ]
    
    try:
        print(f"\nStarting Hayabusa scan on: {evtx_folder}")
        print(f"Output files will be saved with prefix: {base_filename}")
        print(f"CSV Output: {os.path.join(report_path, csv_file)}")
        print(f"HTML Report: {os.path.join(report_path, html_file)}")
        
        with open(os.path.join(report_path, log_file), 'w') as log:
            process = subprocess.Popen(
                cmd,
                stdout=log,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            _, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"\nError during scan (exit code {process.returncode}):")
                if stderr:
                    print(stderr.strip())
                else:
                    print("No error details available. Check the log file for more information.")
            else:
                print("\nScan completed successfully!")
        
    except Exception as e:
        print(f"\nFailed to start Hayabusa: {str(e)}")
    
    if platform.system() == 'Windows':
        os.startfile(report_path)
    
    input("\nPress Enter to return to main menu...")

def is_process_running(process_name):
    try:
        if platform.system() == 'Windows':
            output = subprocess.check_output(
                ['tasklist', '/FI', f'IMAGENAME eq {process_name}'], 
                stderr=subprocess.DEVNULL, 
                universal_newlines=True
            )
            return process_name.lower() in output.lower()
        return False
    except:
        return False

if __name__ == "__main__":
    main()
