# Team JANUS Avionics Problem Statement: Solution

This repository contains the complete solutions for Task 1 and Task 2 of the Team JANUS Avionics Problem Statement.

-----

## Task 1: Planning to Surprise Galactus (Data Analysis)

### How I Approached Task 1

#### 1\. Data Extraction and Cleaning

  * **File Handling**: The script uses the `pandas` library to read pressure data directly from an `.xlsx` file.
  * **Handling Corrupted Data**: The provided data contains corrupted entries. The script is built to identify these non-numeric values, convert them to `NaN` (Not a Number), and then use a robust backward-fill followed by a forward-fill method (`bfill().ffill()`) to replace them with valid data. This ensures the dataset is complete, even if the corruption occurs at the very first data point.

#### 2\. Flight Calculations

  * **Altitude**: Altitude is calculated from pressure using the Barometric Formula. The launch is assumed to be at ground level, so the first valid pressure reading is used as the baseline pressure.
  $$
h = 44330 \cdot \left( 1 - \left( \frac{P}{P_0} \right)^{1/5.255} \right)
$$

  * **Velocity**: Velocity is calculated as the rate of change of altitude. Since data is recorded every second, this is found by taking the difference between consecutive altitude values.

#### 3\. Noise Reduction ("Brownie Points")

  * To handle minor fluctuations and make the graphs less messy, a 5-point moving average is applied to the altitude data. This smooths the flight path. A second moving average is applied to the velocity data for an even cleaner final graph.

#### 4\. Data Visualization ("Making it FANTASTIC\!")

The script uses `matplotlib` to generate four distinct plots:

1.  **Static Altitude vs. Time Plot**: A clear, labeled graph showing the smoothed altitude.
2.  **Static Velocity vs. Time Plot**: A graph of the smoothed velocity.
3.  **Animated Altitude GIF**: An animated graph that adds a new data point every second, as requested.
4.  **Animated Velocity GIF**: A similar animation for the velocity profile.

-----

## Task 2: Surprising Galactus\! (Tinkercad Simulation)

### How I Approached Task 2

#### 1\. Hardware Assembly

The circuit was assembled in Tinkercad using an Arduino Uno, a force sensor, a piezo buzzer, and three LEDs (Green, Yellow, Red). *The screenshot of the final wiring for this task is included in the repository (`tinkercad_wiring.png`).*

#### 2\. Software and Logic

The Arduino was programmed to implement a state machine that intelligently tracks the flight.

  * **Noise Filtering**: Sensor data isn't perfect and has small variations. To filter these out, I implemented a **10-point moving average**, as hinted in the problem statement. The code averages the last 10 sensor readings to get a stable value for calculations.
  * **State Machine**: The code uses three states: `ON_PAD`, `ASCENDING`, and `DESCENDING`.
      * **Ascending**: The green LED lights up when the device detects a launch (a significant drop in force).
      * **Apogee**: The system detects apogee at the moment the flight transitions from ascending to descending. When this happens, a special function is triggered that sounds the **buzzer** and flashes the yellow LED.
      ***Descending**: After the apogee event, the red LED lights up, indicating the device is descending.

-----

## Files in This Repository

  * `flight_analysis.py`: The Python script for Task 1.
  * `tinkercad_code.ino`: The Arduino C++ sketch for Task 2.
  * `altitude_vs_time0254.png`: Static altitude plot from Task 1.
  * `velocity_vs_time0254.png`: Static velocity plot from Task 1.
  * `altitude_animation.gif`: Animated altitude plot from Task 1.
  * `velocity_animation.gif`: Animated velocity plot from Task 1.
  * `tinkercad_wiring.png`: Screenshot of the final circuit wiring for Task 2.
  * `Raw_Test_Flight_Data_25.xlsx`: The sample flight data used for Task 1.

-----

## How to Run

### Task 1

1.  **Prerequisites**: Ensure you have Python and the required libraries:
    ```sh
    pip install pandas numpy matplotlib openpyxl Pillow
    ```
2.  **Execution**: Place `flight_analysis.py` and `Raw_Test_Flight_Data_25.xlsx` in the same folder and run the script:
    ```sh
    python flight_analysis.py
    ```
3.  **Output**: The script will save the four plot files in the same directory.

### Task 2

1.  **Open Tinkercad**: Go to the Tinkercad website.
2.  **Assemble Circuit**: Recreate the circuit using `tinkercad_wiring.png` as a reference.
3.  **Upload Code**: Open the "Code" panel, select "Text" mode, and paste the contents of `tinkercad_code.ino`.
4.  **Simulate**: Click "Start Simulation" and interact with the force sensor to simulate a flight.