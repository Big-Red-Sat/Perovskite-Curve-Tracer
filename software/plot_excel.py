import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science', 'ieee', 'high-vis'])
xticks = np.arange(0, 1.2, 0.2)
xticks = [float(f'{x:1.1f}') for x in xticks]

x018 = r"C:\Users\Walker Arce\Documents\GitHub\Perovskite-Curve-Tracer\software\curves\3. Final Round\X018_LM"
files = os.listdir(x018)
files = [f for f in files if "curve" in f]
forward_files = [f for f in files if "Forward" in f]
reverse_files = [f for f in files if "Reverse" in f]

pixel_number = 0
for f in forward_files:
    test = pd.read_excel(os.path.join(x018, f), sheet_name="Data")
    if pixel_number == 0:
        plt.plot(test['Voltage'][40:], test['Current Density'][40:], label=f"Pixel {pixel_number}")
    else:
        plt.plot(test['Voltage'], test['Current Density'], label=f"Pixel {pixel_number}")
    pixel_number += 1
plt.ylabel("Current Density ($mA/cm^{-2}$)")
plt.xlabel("Voltage ($V$)")
plt.title("X018 Forward JV Curves")
plt.xticks(xticks, labels=xticks)
plt.legend()
plt.savefig("x018_forward.png", dpi=300, bbox_inches="tight")
plt.clf()

pixel_number = 0
for f in reverse_files:
    test = pd.read_excel(os.path.join(x018, f), sheet_name="Data")
    plt.plot(test['Voltage'], test['Current Density'], label=f"Pixel {pixel_number}")
    pixel_number += 1
plt.ylabel("Current Density ($mA/cm^{-2}$)")
plt.xlabel("Voltage ($V$)")
plt.title("X018 Reverse JV Curves")
plt.xticks(xticks, labels=xticks)
plt.legend()
plt.savefig("x018_reverse.png", dpi=300, bbox_inches="tight")
plt.clf()

leakage = r"C:\Users\Walker Arce\Documents\GitHub\Perovskite-Curve-Tracer\software\curves\X031_ShuntTest_500"
files = os.listdir(leakage)
files = [f for f in files if "curve" in f]
forward_files = [f for f in files if "Forward" in f]
reverse_files = [f for f in files if "Reverse" in f]

pixel_number = 0
for f in forward_files:
    test = pd.read_excel(os.path.join(leakage, f), sheet_name="Data")
    if pixel_number == 0:
        plt.plot(test['Voltage'][40:], test['Current Density'][40:], label=f"Pixel {pixel_number}")
    else:
        plt.plot(test['Voltage'], test['Current Density'], label=f"Pixel {pixel_number}")
    pixel_number += 1
plt.ylabel("Current Density ($mA/cm^{-2}$)")
plt.xlabel("Voltage ($V$)")
plt.title("X032 Forward JV Curves")
plt.xticks(xticks, labels=xticks)
plt.legend()
plt.savefig("leakage_forward.png", dpi=300, bbox_inches="tight")
plt.clf()

pixel_number = 0
for f in reverse_files:
    test = pd.read_excel(os.path.join(leakage, f), sheet_name="Data")
    plt.plot(test['Voltage'], test['Current Density'], label=f"Pixel {pixel_number}")
    pixel_number += 1
plt.ylabel("Current Density ($mA/cm^{-2}$)")
plt.xlabel("Voltage ($V$)")
plt.title("X032 Reverse JV Curves")
plt.xticks(xticks, labels=xticks)
plt.legend()
plt.savefig("leakage_reverse.png", dpi=300, bbox_inches="tight")
plt.clf()