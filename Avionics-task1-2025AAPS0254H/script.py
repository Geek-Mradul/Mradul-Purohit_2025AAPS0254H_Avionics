# Name - Mradul Purohit
# ID - 2025AAPS0254H
# Email ID - f20250254@hyderabad.bits-pilani.ac.in
# Code for Avionics Problem Statement Task 1
# This script processes flight data from 'Raw_Test_Flight_Data_25.xlsx'
# and uses the Pillow writer to create animations.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. Data Loading and Cleaning (from .xlsx file)

try:
    # Using pd.read_excel to read the data from the specified Excel file.
    df = pd.read_excel(
        'Raw_Test_Flight_Data_25.xlsx',
        header=None,
        names=['Pressure'],
        na_values=['*****']
    )
    
    # Forcing the 'Pressure' column to be a numeric type.
    df['Pressure'] = pd.to_numeric(df['Pressure'], errors='coerce')

    # Using a robust fill method to handle corrupted data.
    df['Pressure'] = df['Pressure'].bfill().ffill()
    
    print("Successfully loaded and cleaned the data file.")
except FileNotFoundError:
    print("Error: 'Raw_Test_Flight_Data_25.xlsx' not found. Please ensure the file is in the same directory.")
    exit()
except Exception as e:
    print(f"An error occurred: {e}")
    exit()


# Creating a time column, assuming data is recorded every second.
df['Time'] = range(len(df))

# 2. Calculations

# Calculating Altitude using the Barometric Formula.
P0 = df['Pressure'].iloc[0]
df['Altitude'] = 44330 * (1 - (df['Pressure'] / P0)**(1/5.255))

# Smoothing the altitude data to reduce sensor noise using a moving average.
window_size = 5
df['Altitude_Smoothed'] = df['Altitude'].rolling(window=window_size, center=True, min_periods=1).mean()

# Calculating velocity (rate of change of altitude).
df['Velocity'] = df['Altitude_Smoothed'].diff().fillna(0)

# Smoothing the velocity data itself to get a cleaner graph.
df['Velocity_Smoothed'] = df['Velocity'].rolling(window=window_size, center=True, min_periods=1).mean()

print("Calculations for altitude and velocity are complete.")

# 3. Static Plots

# Plot 1: Static Altitude vs. Time
plt.figure(figsize=(12, 6))
plt.plot(df['Time'], df['Altitude'], label='Raw Altitude Data', alpha=0.4, color='skyblue')
plt.plot(df['Time'], df['Altitude_Smoothed'], label=f'Smoothed Altitude (Window={window_size})', color='red', linewidth=2)
plt.title('Altitude vs. Time', fontsize=16)
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Altitude (meters)', fontsize=12)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('altitude_vs_time0254.png')
print("Saved static plot: 'altitude_vs_time0254.png'")

# Plot 2: Static Velocity vs. Time
plt.figure(figsize=(12, 6))
plt.plot(df['Time'], df['Velocity'], label='Original Velocity', alpha=0.4, color='orange')
plt.plot(df['Time'], df['Velocity_Smoothed'], label=f'Smoothed Velocity (Window={window_size})', color='green', linewidth=2)
plt.title('Smoothed Velocity vs. Time', fontsize=16)
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Velocity (m/s)', fontsize=12)
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('velocity_vs_time0254.png')
print("Saved static plot: 'velocity_vs_time0254.png'")


# 4. Animated Plots

# Animation 1: Altitude
fig_alt, ax_alt = plt.subplots(figsize=(12, 6))
ax_alt.set_xlim(0, len(df['Time']))
ax_alt.set_ylim(df['Altitude_Smoothed'].min() - 5, df['Altitude_Smoothed'].max() + 5)
ax_alt.set_title('Altitude vs. Time (Animated)', fontsize=16)
ax_alt.set_xlabel('Time (seconds)', fontsize=12)
ax_alt.set_ylabel('Altitude (meters)', fontsize=12)
ax_alt.grid(True)
line_alt, = ax_alt.plot([], [], lw=2, color='red', marker='o', markersize=4)
time_text_alt = ax_alt.text(0.05, 0.9, '', transform=ax_alt.transAxes)

def init_alt():
    line_alt.set_data([], [])
    time_text_alt.set_text('')
    return line_alt, time_text_alt

def animate_alt(i):
    line_alt.set_data(df['Time'][:i+1], df['Altitude_Smoothed'][:i+1])
    time_text_alt.set_text(f'Time = {i}s')
    return line_alt, time_text_alt

ani_alt = animation.FuncAnimation(fig_alt, animate_alt, frames=len(df),
                                  init_func=init_alt, blit=True, interval=50)

# Animation 2: Velocity
fig_vel, ax_vel = plt.subplots(figsize=(12, 6))
ax_vel.set_xlim(0, len(df['Time']))
ax_vel.set_ylim(df['Velocity_Smoothed'].min() - 2, df['Velocity_Smoothed'].max() + 2)
ax_vel.set_title('Velocity vs. Time (Animated)', fontsize=16)
ax_vel.set_xlabel('Time (seconds)', fontsize=12)
ax_vel.set_ylabel('Velocity (m/s)', fontsize=12)
ax_vel.grid(True)
ax_vel.axhline(0, color='black', linestyle='--', linewidth=1)
line_vel, = ax_vel.plot([], [], lw=2, color='green', marker='o', markersize=4)
time_text_vel = ax_vel.text(0.05, 0.9, '', transform=ax_vel.transAxes)

def init_vel():
    line_vel.set_data([], [])
    time_text_vel.set_text('')
    return line_vel, time_text_vel

def animate_vel(i):
    line_vel.set_data(df['Time'][:i+1], df['Velocity_Smoothed'][:i+1])
    time_text_vel.set_text(f'Time = {i}s')
    return line_vel, time_text_vel

ani_vel = animation.FuncAnimation(fig_vel, animate_vel, frames=len(df),
                                  init_func=init_vel, blit=True, interval=50)

# Saving the animations
try:
    ani_alt.save('altitude_animation.gif', writer='pillow', fps=80)
    print("Saved animation: 'altitude_animation.gif'")
    ani_vel.save('velocity_animation.gif', writer='pillow', fps=80)
    print("Saved animation: 'velocity_animation.gif'")
except Exception as e:
    print("\nCould not save the animations.")
    print("Please ensure the 'Pillow' library is installed (`pip install Pillow`).")

plt.close('all')