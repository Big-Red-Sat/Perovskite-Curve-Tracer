import sys
import threading
import time
import tkinter
from tkinter import messagebox
import os
import datetime
import matplotlib.pyplot as plt
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from serial import SerialException
from serial.tools import list_ports
import pandas as pd

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
fig_color = '#%02x%02x%02x' % (240, 240, 237)

curve_points_i = [[] for _ in range(6)]
curve_points_v = [[] for _ in range(6)]
curve_points_j = [[] for _ in range(6)]
curve_points_p = [[] for _ in range(6)]
curve_point = [[] for _ in range(6)]
current_panel = 1


def clear_plot():
    plot1.clear()


def plot_curve(curve_i):
    plot1.set_title("Perovskite J-V Curve")
    plot1.set_xlabel("Voltage (V)")
    plot1.set_ylabel("Current Density (mA cm^-2)")
    plot1.plot(curve_points_v[curve_i], curve_points_j[curve_i], label=f"Pixel {curve_i}")
    canvas.draw()


def adc_to_voltage(adc_code, ref_voltage=3.3, max_bin=2**12, gain=0.5, bias_voltage=0.0):
    return (((ref_voltage * adc_code) / float(max_bin - 1)) - bias_voltage) / gain


def adc_to_current(adc_code, gain=50.0, ref_voltage=1.2, max_bin=2**12, sense_res=0.01):
    v = adc_to_voltage(adc_code, ref_voltage=ref_voltage, max_bin=max_bin, gain=1)
    return ((v / gain) / sense_res) * 1000


def read_curve():
    clear_plot()
    for i in range(6):
        curve_point[i].clear()
        curve_points_v[i].clear()
        curve_points_i[i].clear()
        curve_points_j[i].clear()
        pixel_area_value = float(1 if pixel_area.get() == "" else pixel_area.get())
        if pixel_area_value < 0:
            pixel_area_value = 1e-7
        irradiance_value = float(100 if irradiance.get() == "" else irradiance.get())
        if irradiance_value < 0:
            irradiance_value = 1e-7
        msp430_port.write(b'C')
        start_time = time.time()
        while len(curve_point[i]) != 256:
            reading = ''.join(map(chr, msp430_port.readline().strip())).split(' ')
            curve_point[i].append(int(reading[0]))
            curve_points_v[i].append(adc_to_voltage(abs(int(reading[1])), ref_voltage=3.29, bias_voltage=0.0, max_bin=2**12))
            curve_points_i[i].append(adc_to_current(abs(int(reading[2])), ref_voltage=3.29, gain=200.0, sense_res=0.51, max_bin=2**12))
            curve_points_j[i].append(curve_points_i[i][-1] / pixel_area_value)
            curve_points_p[i].append(curve_points_v[i][-1] * curve_points_i[i][-1])
        temperature_reading = float(msp430_port.readline().strip()) / 100.0
        end_time = time.time()
        sc_cond.config(text=f"Short Circuit: {curve_points_v[i][-1]:.4f} V | {curve_points_i[i][-1]:.4f} mA")
        oc_cond.config(text=f"Open Circuit: {curve_points_v[i][0]:.4f} V | {curve_points_i[i][0]:.4f} mA")
        curve_time.config(text=f"Trace Time: {(end_time - start_time) * 10**3:.4f} ms")
        temp_label.config(text=f"Panel Temperature: {temperature_reading} \u00b0C")
        plot_curve(i)
        mpp_idx = max(enumerate(curve_points_p[i]), key=lambda x: x[1])[0]
        voc = curve_points_v[i][0]
        isc = curve_points_i[i][-1]
        mpp_v = curve_points_v[i][mpp_idx]
        mpp_i = curve_points_i[i][mpp_idx]
        mpp_p = mpp_v * mpp_i
        ff = (mpp_v * mpp_i) / ((voc * isc) + 1e-7)
        eff = (mpp_p / pixel_area_value) / irradiance_value
        test_time = datetime.datetime.now()
        summary_df = pd.DataFrame(
            [test_time, panel_name.get(), i, pixel_area_value, irradiance_value, temperature_reading, voc, isc, mpp_v, mpp_i, mpp_p, ff, eff],
            index=["Time", "ID", "Pixel", "Pixel Area", "Irradiance", "Panel Temperature", "Voc", "Isc", "Vmp", "Imp", "Pmp", "FF", "Eff"]
        )
        if save_curves.get():
            if panel_name.get() != "":
                root_dir = os.path.join(output_path, panel_name.get())
                if not os.path.exists(root_dir):
                    os.mkdir(root_dir)
                curve_output_path = os.path.join(root_dir,
                                                 f'curve_{temperature_reading}_{get_panel_int()}' + '.xlsx')
            else:
                curve_output_path = os.path.join(output_path,
                                                 f'curve_{temperature_reading}_{get_panel_int()}' + '.xlsx')
            curve_df = pd.DataFrame([curve_points_v[i], curve_points_i[i], curve_points_j[i], curve_points_p[i]],
                                    index=['Voltage', 'Current', 'Current Density', 'Power']).transpose()
            writer = pd.ExcelWriter(curve_output_path, engine='xlsxwriter')
            frames = {'Summary': summary_df, 'Data': curve_df}
            # now loop thru and put each on a specific sheet
            for sheet, frame in frames.items():  # .use .items for python 3.X
                frame.to_excel(writer, sheet_name=sheet)
            # critical last step
            writer.close()
        next_panel()
        plot1.legend()
        canvas.draw()
    if save_curves.get():
        if panel_name.get() != "":
            root_dir = os.path.join(output_path, panel_name.get())
            if not os.path.exists(root_dir):
                os.mkdir(root_dir)
            curve_image_path = os.path.join(root_dir, f'{panel_name.get()}_plotted.png')
        else:
            curve_image_path = os.path.join(output_path, f'all_plotted.png')
        fig.savefig(curve_image_path, dpi=500)


# def reverse_bias():
#     msp430_port.write(b'G')
#     current_bias = str(msp430_port.readline().strip().decode('utf-8'))
#     print(f"Current bias is {current_bias}")
#     if current_bias == '1':
#         reverse_bias_checkbox.select()
#     else:
#         reverse_bias_checkbox.deselect()
#     reverse_bias_checkbox.config(text=f"Reverse Bias = {current_bias}")


def next_panel():
    msp430_port.write(b'E')
    current_panel = msp430_port.readline().strip()
    print(f"Next pixel is {str(int(current_panel))}")
    panel_text.config(text=f"Current Pixel: {str(int(current_panel)+1)} / 6")


def get_panel_int():
    msp430_port.write(b'D')
    return int(msp430_port.readline().strip())


def get_panel():
    msp430_port.write(b'D')
    current_panel = msp430_port.readline().strip()
    print(f"Current pixel is {str(int(current_panel))}")
    panel_text.config(text=f"Current Pixel: {str(int(current_panel)+1)} / 6")


def get_curve():
    thread = threading.Thread(target=read_curve)
    thread.daemon = True
    thread.start()


output_path = os.path.join(os.getcwd(), 'curves')
if not os.path.exists(output_path):
    os.mkdir(output_path)

msp430_port = None
ports = list_ports.comports()
try:
    for port in ports:
        if 'A43F6A5122001A00' in port.serial_number:
            msp430_port = serial.Serial(port.device, baudrate=115200)
    if not msp430_port:
        messagebox.showerror("No MSP430 Found", "Make sure development board is plugged in!")
        sys.exit(1)
except SerialException as se:
    messagebox.showerror("Serial Exception", "Could not connect to serial port!")

msp430_port.flush()

root = tkinter.Tk()
root.title("UNL Aerospace Club | Aerospace eXperimental Payloads 2023")
root.configure(bg='white')

panel_name_text = tkinter.Label(root, text="Perovskite ID", bg='white')
panel_name_text.pack()
panel_name = tkinter.Entry(root)
panel_name.pack()

pixel_area_text = tkinter.Label(root, text="Pixel Area (cm^2)", bg='white')
pixel_area_text.pack()
pixel_area = tkinter.Entry(root)
pixel_area.pack()

irradiance_text = tkinter.Label(root, text="Irradiance (mW/cm^2)", bg='white')
irradiance_text.pack()
irradiance = tkinter.Entry(root)
irradiance.pack()

button = tkinter.Button(root, text="Trace Curve", command=get_curve)
button.pack()
sc_cond = tkinter.Label(root, text="Short Circuit: --.-- V | --.-- mA", bg='white')
sc_cond.pack()
oc_cond = tkinter.Label(root, text="Open Circuit: --.-- V | --.-- mA", bg='white')
oc_cond.pack()
temp_label = tkinter.Label(root, text=f"Panel Temperature: --.-- \u00b0C", bg='white')
temp_label.pack()
curve_time = tkinter.Label(root, text="Trace Time: --.-- ms", bg='white')
curve_time.pack()
# panel_button = tkinter.Button(root, text="Next Pixel", command=next_panel)
# panel_button.pack()
panel_text = tkinter.Label(root, text="Current Pixel: 1 / 6", bg='white')
panel_text.pack()

save_curves = tkinter.IntVar()
save_checkbox = tkinter.Checkbutton(root, text='Save Curves?', bg='white', variable=save_curves)
save_checkbox.pack()
get_panel()

# reverse_bias_checkbox = tkinter.Checkbutton(root, text='Reverse Bias?', bg='white', command=reverse_bias)
# reverse_bias_checkbox.pack()

fig = Figure(figsize=(5, 5), dpi=100)
plot1 = fig.add_subplot(111)
plot1.set_title("Perovskite J-V Curve")
plot1.set_xlabel("Voltage (V)")
plot1.set_ylabel("Current Density (mA cm^-2)")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

canvas.get_tk_widget().pack()
root.mainloop()
