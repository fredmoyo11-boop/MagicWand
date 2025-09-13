# Magic Wand: Gesture Recognition and Dueling Game

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/fredmoyo11-boop/MagicWand)

This project combines hardware, machine learning, and web development to create a "magic wand" that recognizes hand gestures. These gestures are classified as spells, which can be used in a networked dueling game.

The system uses an Arduino with an MPU-6050 IMU to capture accelerometer and gyroscope data. This data is streamed to a Python client, which uses a pre-trained Random Forest model to classify the performed gesture. The resulting spell is sent to a Flask server that orchestrates the duel between two players and displays the results in a web-based arena.

## Core Components

*   **`arduino-firmware-magicwand`**: Contains the Arduino sketch (`.ino`) that reads sensor data from the MPU-6050 module and transmits it over the serial port.
*   **`python-recorder`**: A Python script with a Tkinter GUI for recording gesture data from the wand. The data is saved in CSV format and can be used for training the machine learning model.
*   **`Data Folders` (`Orbrix`, `Quadrix`, `Threnix`)**: These directories contain the CSV files of recorded gesture data used to train the spell-recognition model.
*   **`python-client-wandduel`**: A Python client with a Tkinter GUI that:
    *   Connects to the Arduino wand.
    *   Records a user's gesture.
    *   Uses the trained machine learning model (`random_forest_model.joblib`) to classify the gesture into a spell.
    *   Sends the classified spell to the dueling server.
*   **`python-server-wandduel`**: A Flask-based web server that manages the duel logic, tracks scores, and serves the `arena.htm` web page to visualize the game in real-time.

## Spell Vocabulary and Duel Logic

The wand recognizes three distinct spell gestures:

| Gesture Shape | Spell Name | Duel Class |
| :-----------: | :--------: | :--------: |
|   Circular    |   `Orbrix`   |  Class 1   |
|  Rectangular  |  `Quadrix`  |  Class 2   |
|  Triangular   |  `Threnix`  |  Class 3   |

The dueling game follows a rock-paper-scissors-style system:
*   **Orbrix** (Class 1) beats **Quadrix** (Class 2).
*   **Quadrix** (Class 2) beats **Threnix** (Class 3).
*   **Threnix** (Class 3) beats **Orbrix** (Class 1).

## Getting Started

### 1. Hardware Setup

*   An Arduino board compatible with the MPU-6050 (e.g., Bluno Beetle).
*   An MPU-6050 Accelerometer + Gyroscope module.
*   Connect the MPU-6050 to the Arduino via the I2C interface (SDA, SCL, VCC, GND).

### 2. Firmware Installation

1.  Open `arduino-firmware-magicwand/arduino-firmware-magicwand.ino` in the Arduino IDE.
2.  Select your board and the corresponding serial port.
3.  Upload the sketch to your Arduino.

### 3. Software Dependencies

Each of the Python directories (`python-recorder`, `python-client-wandduel`, `python-server-wandduel`) has its own `requirements.txt` file. Install the dependencies for each component you plan to use.

For example, to set up the dueling client:
```bash
cd python-client-wandduel
pip install -r requirements.txt
```

### 4. Running the Dueling Game

#### Start the Server

1.  Navigate to the `python-server-wandduel` directory.
2.  Edit `wand-duel-server.py` and set the `self_ip` variable to the local IP address of the machine that will run the server.
3.  Run the server using the command:
    ```bash
    python wand-duel-server.py
    ```
4.  Open a web browser and navigate to `http://<your-server-ip>:5000/arena` to view the dueling arena.

#### Start the Client

1.  Connect your assembled wand to your computer via USB.
2.  Navigate to the `python-client-wandduel` directory.
3.  Edit `wand-duel-client.py` and configure the following variables:
    *   Set `arduino_port` to the serial port your wand is connected to (e.g., `COM3` or `/dev/cu.usbmodem12345`).
    *   Set `duel_server_ip` to the IP address of the machine running the server.
4.  Run the client application:
    ```bash
    python wand-duel-client.py
    ```
5.  In the client window:
    *   Enter your team name and select your slot (1 for left, 2 for right).
    *   Click **Connect** to establish a connection with the wand.
    *   Click **Cast Spell** to begin recording a gesture. Perform the gesture, then click **Stop Casting** to classify the spell and send it to the server.

## Data Recording and Model Training (Optional)

### Recording New Gesture Data

If you wish to record your own gestures to train a new model:

1.  Connect your wand and navigate to the `python-recorder` directory.
2.  Run the recorder script: `python recorder.py`.
3.  In the GUI, enter a wizard name and a spell name.
4.  Click **Connect** to link to the wand.
5.  Click **Record Spell** to start and stop the data capture for a single gesture. CSV files will be saved in a new `recordings` directory.

### Training a New Model

1.  Organize your recorded CSV files into spell-specific subdirectories (e.g., `Orbrix`, `Quadrix`) inside the `python-recorder/recordings/` folder.
2.  Open `python-client-wandduel/__init__.py`.
3.  Update the `basis_ordner` path to point to your `recordings` directory.
4.  Run the `__init__.py` script. This will train a new Random Forest classifier and scaler, saving them as `random_forest_model.joblib` and `scaler_neu.joblib` in the `python-client-wandduel` directory.
