import os
import sys
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
PYZBAR = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "pyzbar")
ICON = os.path.join(BASE, "qr.ico")
ENTRY = os.path.join(BASE, "appQRGenerator.py")

args = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm", "--clean", "--onefile", "--windowed",
    "--name", "appQRGenerator",
    "--icon", ICON,
    "--add-data", f"{ICON};.",
    "--add-binary", os.path.join(PYZBAR, "libiconv.dll") + ";.",
    "--add-binary", os.path.join(PYZBAR, "libzbar-64.dll") + ";.",
    "--distpath", os.path.join(BASE, "dist"),
    "--workpath", os.path.join(BASE, "build"),
    ENTRY,
]

subprocess.run(args, check=True)
print("Build completado en", os.path.join(BASE, "dist", "appQRGenerator.exe"))
