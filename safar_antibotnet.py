import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess, shutil, hashlib, os, platform, threading
from pathlib import Path
from datetime import datetime

APP_NAME = "SAFAR ANTI-BOTNET SECURITY"
SUSPICIOUS_EXTENSIONS = {".scr", ".pif", ".vbs", ".vbe", ".js", ".jse", ".hta", ".bat", ".cmd", ".ps1"}

def run_command(args, timeout=90):
    try:
        p = subprocess.run(args, capture_output=True, text=True, errors="replace", timeout=timeout,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return f"Command could not run: {e}"

def defender_path():
    candidates = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Windows Defender" / "MpCmdRun.exe",
        Path(os.environ.get("ProgramData", r"C:\ProgramData")) / "Microsoft" / "Windows Defender" / "Platform"
    ]
    for p in candidates:
        if p.is_file():
            return str(p)
        if p.is_dir():
            found = sorted(p.glob("*/MpCmdRun.exe"), reverse=True)
            if found:
                return str(found[0])
    return shutil.which("MpCmdRun.exe")

class App:
    def __init__(self, root):
        self.root = root
        root.title(APP_NAME)
        root.geometry("900x620")
        root.minsize(760, 520)
        root.configure(bg="#101820")
        style = ttk.Style()
        try: style.theme_use("clam")
        except: pass
        style.configure("TButton", padding=8)
        style.configure("Treeview", rowheight=25)
        header = tk.Frame(root, bg="#101820")
        header.pack(fill="x", padx=22, pady=(18, 8))
        tk.Label(header, text=APP_NAME, font=("Segoe UI", 19, "bold"),
                 fg="#f4f7fa", bg="#101820").pack(anchor="w")
        tk.Label(header, text="Professional Edition • Local Windows security assistant",
                 font=("Segoe UI", 10), fg="#9fb3c8", bg="#101820").pack(anchor="w", pady=(4,0))

        self.status = tk.Label(root, text="● READY — protection checks available",
                               font=("Segoe UI", 11, "bold"), fg="#54d68b", bg="#172733",
                               padx=12, pady=12, anchor="w")
        self.status.pack(fill="x", padx=22, pady=10)

        actions = tk.Frame(root, bg="#101820")
        actions.pack(fill="x", padx=22, pady=4)
        ttk.Button(actions, text="Run Microsoft Defender Quick Scan", command=self.defender_scan).pack(side="left", padx=(0,8))
        ttk.Button(actions, text="Inspect Network Connections", command=self.network_scan).pack(side="left", padx=8)
        ttk.Button(actions, text="Scan a Folder", command=self.folder_scan).pack(side="left", padx=8)
        ttk.Button(actions, text="System Information", command=self.system_info).pack(side="left", padx=8)

        self.output = tk.Text(root, wrap="word", bg="#0b1117", fg="#d8e2ec",
                              insertbackground="white", font=("Consolas", 10),
                              relief="flat", padx=14, pady=12)
        self.output.pack(fill="both", expand=True, padx=22, pady=(10, 8))
        self.write("Welcome.\n\nThis starter build provides on-demand checks using Windows tools.\n"
                   "It is not a certified antivirus and does not claim to identify every botnet.\n"
                   "Keep Microsoft Defender and Windows Update enabled.\n")
        footer = tk.Label(root, text="No automatic deletion or blocking • Review findings before taking action",
                          bg="#101820", fg="#9fb3c8", font=("Segoe UI", 9))
        footer.pack(anchor="w", padx=24, pady=(0,12))

    def write(self, text):
        self.output.insert("end", f"\n[{datetime.now().strftime('%H:%M:%S')}] {text}\n")
        self.output.see("end")

    def busy(self, label):
        self.status.config(text=f"● RUNNING — {label}", fg="#f5c451")

    def done(self, label="CHECK COMPLETE"):
        self.status.config(text=f"● READY — {label}", fg="#54d68b")

    def background(self, label, fn):
        self.busy(label)
        def worker():
            try: fn()
            finally: self.root.after(0, self.done)
        threading.Thread(target=worker, daemon=True).start()

    def defender_scan(self):
        def work():
            if platform.system() != "Windows":
                self.root.after(0, lambda: self.write("Windows Defender scan is available only on Windows."))
                return
            exe = defender_path()
            if not exe:
                self.root.after(0, lambda: self.write("Microsoft Defender command-line tool was not found. Check that Defender is installed and enabled."))
                return
            self.root.after(0, lambda: self.write("Starting Microsoft Defender quick scan. This may take several minutes..."))
            result = run_command([exe, "-Scan", "-ScanType", "1"], timeout=1800)
            self.root.after(0, lambda: self.write("Microsoft Defender scan output:\n" + (result[-10000:] or "(No text output)")))
        self.background("MICROSOFT DEFENDER QUICK SCAN", work)

    def network_scan(self):
        def work():
            if platform.system() != "Windows":
                out = "Network inspection in this prototype is designed for Windows."
            else:
                out = run_command(["netstat", "-ano"], timeout=30)
            self.root.after(0, lambda: self.write(
                "NETWORK CONNECTION SNAPSHOT\n"
                "Review unfamiliar remote addresses and owning PIDs. An established connection alone is not proof of botnet activity.\n\n" + out[:18000]))
        self.background("NETWORK INSPECTION", work)

    def folder_scan(self):
        folder = filedialog.askdirectory(title="Choose a folder to inspect")
        if not folder: return
        def work():
            findings, count = [], 0
            for path in Path(folder).rglob("*"):
                try:
                    if not path.is_file(): continue
                    count += 1
                    if path.suffix.lower() in SUSPICIOUS_EXTENSIONS:
                        findings.append(f"Review file type: {path}")
                except (PermissionError, OSError):
                    continue
            report = f"Folder inspection complete.\nFiles checked: {count}\nFiles requiring review by extension: {len(findings)}\n\n"
            report += "\n".join(findings[:250]) if findings else "No files matched the basic extension review list."
            report += "\n\nImportant: file extensions are weak indicators, not proof of malware. This scan does not execute files or remove anything."
            self.root.after(0, lambda: self.write(report))
        self.background("FOLDER INSPECTION", work)

    def system_info(self):
        info = (f"OS: {platform.platform()}\n"
                f"Machine: {platform.machine()}\n"
                f"Python runtime: {platform.python_version()}\n"
                f"Microsoft Defender CLI: {defender_path() or 'Not detected'}")
        self.write(info)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
