# Name - Mradul Purohit
# ID - 2025AAPS0254H
# Email ID - f20250254@hyderabad.bits-pilani.ac.in
# Code for Avionics Problem Statement Task 1
# This script processes flight data, generates animated GIFs,
# and displays them in a simple GUI window.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from PIL import Image, ImageTk
import itertools

# --- 1. Data Loading and Cleaning ---
try:
    df = pd.read_excel(
        'Raw_Test_Flight_Data_25.xlsx',
        header=None,
        names=['Pressure'],
        na_values=['*****']
    )
    df['Pressure'] = pd.to_numeric(df['Pressure'], errors='coerce')
    df['Pressure'] = df['Pressure'].bfill().ffill()
    print("Successfully loaded and cleaned the data file.")
except FileNotFoundError:
    print("Error: 'Raw_Test_Flight_Data_25.xlsx' not found.")
    exit()
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

# --- 2. Calculations ---
df['Time'] = range(len(df))
P0 = df['Pressure'].iloc[0]
df['Altitude'] = 44330 * (1 - (df['Pressure'] / P0)**(1/5.255))
window_size = 5
df['Altitude_Smoothed'] = df['Altitude'].rolling(window=window_size, center=True, min_periods=1).mean()
df['Velocity'] = df['Altitude_Smoothed'].diff().fillna(0)
df['Velocity_Smoothed'] = df['Velocity'].rolling(window=window_size, center=True, min_periods=1).mean()
print("Calculations for altitude and velocity are complete.")

# --- 3. Animated Plots ---
# Animation 1: Altitude
fig_alt, ax_alt = plt.subplots(figsize=(6, 4))
ax_alt.set_xlim(0, len(df['Time']))
ax_alt.set_ylim(df['Altitude_Smoothed'].min() - 5, df['Altitude_Smoothed'].max() + 5)
ax_alt.set_title('Altitude vs. Time')
ax_alt.set_xlabel('Time (s)')
ax_alt.set_ylabel('Altitude (m)')
ax_alt.grid(True)
line_alt, = ax_alt.plot([], [], lw=2, color='red')
def animate_alt(i):
    line_alt.set_data(df['Time'][:i+1], df['Altitude_Smoothed'][:i+1])
    return line_alt,
ani_alt = animation.FuncAnimation(fig_alt, animate_alt, frames=len(df), blit=True, interval=50)

# Animation 2: Velocity
fig_vel, ax_vel = plt.subplots(figsize=(6, 4))
ax_vel.set_xlim(0, len(df['Time']))
ax_vel.set_ylim(df['Velocity_Smoothed'].min() - 2, df['Velocity_Smoothed'].max() + 2)
ax_vel.set_title('Velocity vs. Time')
ax_vel.set_xlabel('Time (s)')
ax_vel.set_ylabel('Velocity (m/s)')
ax_vel.grid(True)
ax_vel.axhline(0, color='black', linestyle='--', linewidth=1)
line_vel, = ax_vel.plot([], [], lw=2, color='green')
def animate_vel(i):
    line_vel.set_data(df['Time'][:i+1], df['Velocity_Smoothed'][:i+1])
    return line_vel,
ani_vel = animation.FuncAnimation(fig_vel, animate_vel, frames=len(df), blit=True, interval=50)

# --- 5. Saving the animations ---
try:
    print("Saving animations... this may take a moment.")
    ani_alt.save('altitude_animation.gif', writer='pillow', fps=50)
    print("Saved animation: 'altitude_animation.gif'")
    ani_vel.save('velocity_animation.gif', writer='pillow', fps=50)
    print("Saved animation: 'velocity_animation.gif'")
except Exception as e:
    print(f"\nCould not save the animations: {e}")
    exit()

plt.close('all')

# --- 6. GUI to Display GIFs ---

class GifPlayer(tk.Label):
    def __init__(self, master, filename):
        im = Image.open(filename)
        self.frames = []
        try:
            for frame in itertools.count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(frame)
        except EOFError:
            pass
        
        self.idx = 0
        super().__init__(master, image=self.frames[0])
        self.after(50, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx = (self.idx + 1) % len(self.frames)
        self.after(50, self.play)

# Create the main window
root = tk.Tk()
root.title("Flight Profile Animation")

# Create and place the GIF players
altitude_gif = GifPlayer(root, 'altitude_animation.gif')
altitude_gif.pack(side=tk.LEFT, padx=10, pady=10)

velocity_gif = GifPlayer(root, 'velocity_animation.gif')
velocity_gif.pack(side=tk.RIGHT, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()