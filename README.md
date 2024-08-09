# 2D_Indoor_CQB_Robot_Simulation

![](doc/img/logFull.png)

**Program Design Purpose**: The integration of robots in Close Quarters Battle (CQB) represents a significant advancement in modern military and law enforcement tactics. These robots, designed to navigate tight spaces, gather real-time intelligence, and engage threats, are invaluable assets in high-stakes scenarios. Our goal is to develop a 2D tactical board simulation system, similar to a computer game, that can load building floor blueprints, display CQB squad (robot) positions, enemy locations, and simulate CQB robot enemy search progress in the real world. This program will allow users (attack squad) to plan CQB robot enemy searching strategies and improve robot's enemy prediction within a controlled environment.

The main user interface of the simulation system is shown below:

![](doc/img/screenshot03.png)

```
# Created:     2024/07/30
# Version:     v_0.1.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
```

**Table of Contents**

[TOC]

------

### Introduction

Robots are employed in Close Quarters Battle (CQB) to minimize the risks faced by human soldiers and officers by handling the most hazardous tasks. Equipped with advanced sensors, cameras, and communication systems, CQB robots provide operators with a comprehensive understanding of their environment. Their ability to navigate narrow corridors, stairwells, and cluttered rooms makes them ideal for urban combat and building searches. By relaying live video and audio feeds back to the control center, these robots enable real-time decision-making and seamless coordination with attack squads.

Modern CQB robots are further enhanced by artificial intelligence (AI) and machine learning algorithms, which boost their autonomous capabilities. These technologies allow robots to recognize and respond to threats, navigate complex environments, and communicate effectively with both robotic and human team members.

The **2D Indoor CQB Robot Simulation** program is a simulation tool designed to configure various CQB scenarios, aiding in the improvement of the robot's autopilot, enemy search, and prediction algorithms. The program consists of two main components: the **CQB Scenario Tactical Board Editor** and the **Situation Simulation Viewer**. The Tactical Board Editor allows users to create and configure CQB scenarios, while the Situation Simulation Viewer simulates how the CQB robot utilizes its sensors for environmental visualization, enemy search, and prediction in real-world situations.

#### CQB Scenario Tactical Board Editor Introduction 

The CQB Scenario Tactical Board Editor allows users to create and configure CQB scenarios with the following steps:

- **Step 1**: Load the building's indoor blueprint into the editor to generate the floor map matrix.
- **Step 2**: Set the robot's starting position, then define its autopilot route and enemy search path.
- **Step 3**: Adjust the robot's motion and detection parameters, such as movement speed, sensor sensitivity, and detection range.
- **Step 4**: Place enemies within the scenario and define their movement strategy (e.g., stationary, patrolling, or random wandering).

After finished configuring a CQB scenario, users can save the scenario to a file for future use, allowing them to load and modify it as needed.

#### CQB Situation Simulation Viewer Introduction

The Situation Simulation Viewer replicates real-world conditions as the robot follows the defined enemy search path. The viewer supports both autonomous robot operation and manual control, enabling users to simulate different operational scenarios. It generates real-time sensor data based on the floor blueprint and enemy configuration, such as:

- Sonar detecting wall reflections to calculate the distance between the robot and the building walls.
- Front LIDAR identifying obstacles like glass doors and furniture that the robot cannot pass.
- A 360-degree microphones array pinpointing potential enemy positions based on sound.
- Electro-optical cameras detecting enemies behind glass doors through visual analysis.

The viewer also visualizes the robot's enemy prediction results. During the simulation, users can step forward or backward through the scenario to refine the enemy search path and improve the robot's performance.

#### Use Case and Future Work

In the future, we plan to integrate AI into the enemy strategy configuration, making enemy actions and interactions with the environment more realistic and "human-like." Additionally, we aim to use this program to train AI models to enhance enemy prediction and optimize search paths. This could have applications in computer games or even real-world CQB combat decision-making.



------

### System Design 

The program consists of several subsystems, each with key features that contribute to the overall simulation. This section introduces and details the design of these subsystems, including the CQB environment simulation, CQB robot sensor simulation, enemy detection, and prediction algorithm design.

#### CQB Environment Simulation Design 

Before simulating the CQB robot's operations, it is essential to accurately build the environment from the building's floor blueprint. This enables the robot's sensors to "interact" with the environment as they would in the real world. This section explains how we construct the environment using the building blueprint and convert it into a map matrix through image visualization analysis. There are three main steps involved in this process:

##### Step 1: Establish the Floor Blueprint Coordinate System Using UWB Position Amplifiers

Typically, the attack squad deploys three UWB (Ultra-Wideband) position amplifiers in a right-angled triangle configuration to cover the building area. We set the positions of these three UWB amplifiers as the origin (0,0), (max(x), 0), and (0, max(y)) of our blueprint matrix map. By scaling the loaded blueprint image to fit within this coordinate system, we ensure that the robot's location identification and the building environment are aligned within the same 2D coordinate system. The steps workflow is shown below:![](doc/img/rm03_coordinate.png)

This alignment allows for precise interaction between the robot's sensors and the simulated environment. 

##### Step 2: Construct the Indoor Environment Map Matrix

Once the blueprint is correctly positioned and scaled within the coordinate system, we use computer vision (CV) techniques to convert the floor blueprint into a 2D matrix for simulation purposes, as illustrated below:

 ![](doc/img/rm04_mapmatrix.png)

In this 2D matrix, different numerical values represent various materials or spaces within the environment (with material values ranging from 1 to 255). For example:

- An empty space, where the robot can move freely, is represented by the value `0`.
- A glass door, which sonar sensors cannot penetrate but LIDAR and cameras can, is represented by the value `10`.
- A furniture which LIDAR can scan its shape and the sound can pass thought is represented by the value `100`.
- A wall, which blocks all sensors and sound, is assigned the value `255`.

This matrix format enables the simulation to distinguish between different types of obstacles and open areas, allowing for accurate robot-environment interaction.

##### Step 3: Simulate Robot and Environment Interaction

After constructing the environment matrix, we develop an interaction module that simulates how the robot's sensors interact with the environment, mimicking real-world scenarios. An example of this interaction is shown below:

![](doc/img/rm05_sensorAct.png)

When the robot encounters different elements like glass doors, wooden furniture, or walls, the interaction manager module traces the sensor’s detection line from the robot's position, checking the material values in the matrix along the sensor's path. The detection continues until it encounters a material value that the sensor cannot penetrate, based on its settings. For instance:

- **Movement sound sensors** stop detecting when they reach a glass door (material value = `10`).
- **Camera and LIDAR sensors** can see through the glass door (material value = `10`) but are blocked by wooden furniture (material value = `100`).
- **Sound detection sensors** can penetrate wooden doors (material value = `100`) but are halted by building walls (material value = `255`).

This system allows for detailed and realistic simulation of sensor interactions, critical for testing and refining CQB robot strategies.

#### CQB Robot Sensor Simulation Design

The sensor system in Close Quarters Battle (CQB) robots is critical for navigating, detecting threats, and providing real-time intelligence in confined and potentially hostile environments. Typically, a CQB robot is equipped with eight types of sensors:  `Optical Sensors`, `Thermal Imaging Sensors`, `Proximity and Obstacle Detection Sensors`, `Environmental Sensors`,  `Audio Sensors`, `Motion and Vibration Sensors`, `Communication and Signal Sensors` and `Multispectral and Hyperspectral Sensors`.  These sensors enable the robot to map the environment, identify potential dangers, and make informed decisions.

In our system, we simulate five key types of sensors used on the robot, as shown below:

![](doc/img/sensors.png)

| Sensors Name                                  | Sensor Type                              | Description                                                  |
| --------------------------------------------- | ---------------------------------------- | ------------------------------------------------------------ |
| **Electro Optical Camera**                    | Optical Sensors                          | Capture detailed visual data for navigation, threat identification, and situational awareness. |
| **UWB Indoor Position Sensor**                | Motion and Vibration Sensors             | Ultra-Wideband (UWB) positioning sensor that allows the robot to determine its location within the building. |
| **Environment Sonars**                        | Environmental Sensors                    | Four sonars positioned around the robot (front, left, right, back) detect environmental features, such as the distance between the robot and surrounding walls. |
| **360' LF Sound Direction Detector**          | Audio Sensors                            | An array of low-frequency sound microphones that capture ambient sounds and determine the general direction of sound sources, such as footsteps, voices, or machinery noises. This audio data helps identify potential threats or locate individuals in nearby rooms or behind obstacles. |
| **Front LIDAR (Light Detection and Ranging)** | Proximity and Obstacle Detection Sensors | Measures distances by illuminating the target with laser light and measuring the reflection. LIDAR creates a 3D map of the environment, helping the robot navigate through tight spaces and avoid obstacles. |

The usage and display of these sensors in the 2D scenario viewer are illustrated below:

![](doc/img/rm08_sensorMap.png)

The robot's enemy detection data processor integrates information from multiple sensors to form a comprehensive understanding of the environment. This processor analyzes sensor fusion data, providing the robot control team with both confirmed and predicted enemy positions, enhancing the accuracy of combine visual recognition and decision-making.



#### Design of enemy detection and the prediction 

Our system simulates the process of enemy detection and prediction during the robot enemy searching progress. 

**Detection Enemy Position**

To detect enemy positions on the map matrix, we utilize the camera and LIDAR sensors. The camera continuously scans the area in front of the robot to identify any enemy pixels. Once the camera detects an enemy, it sends the direction data to the detection data processor module. Since the camera cannot measure distance, the processor then instructs the LIDAR to scan in that direction to determine the distance to the detected object (enemy). Using the robot's own position, enemy direction, and distance data, the processor calculates the enemy's precise location on the map.

The workflow for enemy detection is illustrated below:

![](doc/img/rm06_enemyDect.png)

**Predict Enemy Position**

To predict the enemy’s position, we use the 360° low-frequency sound microphone array. This audio sensor captures the direction of the sound source. As the robot moves, the system records its trajectory and, combined with the sound source direction data, the enemy data processor estimates the enemy's approximate position, even if they are behind obstacles.

The enemy prediction workflow is shown below:

 ![](doc/img/rm07_enemyPred.png)

During the prediction calculation process, we have the robot's trajectory distance (X) from Time-T0 to Time-T1, the enemy sound direction angle (a) at Time-T0 relative to the robot's position (Pos-0), and the enemy sound direction angle (b) at Time-T1 relative to the robot's position (Pos-1).

```
tan(a) = Z/(X+Y)
tan(b) = Z/Y
```

Using these equations, we calculate distances Y and Z. With the data from Pos-1, we can determine the enemy’s predicted position.



------

### System Setup

##### Development Environment

- python 3.7.2rc2+ 64bit [ Windows11 ]

##### Additional Lib/Software Need

- **wxPython** :  https://wxpython.org/index.html , install : `pip install wxPython`
- **Pillow Python Imaging Library** : https://pypi.org/project/pillow/, install : `pip install pillow`
- **OpenCV** : https://opencv.org/get-started/, install: `pip install opencv-python`

##### Hardware Needed : None

##### Program Files List 

| Folder             | Program File        | Execution Env | Description                                                  |
| ------------------ | ------------------- | ------------- | ------------------------------------------------------------ |
| src/floorBluePrint | *.png, *.jpg, *.bmp |               | All the floor blue print image files example.                |
| src/heatmap        | *.png               |               | The enemy predication possibility transparent heat map image file. |
| src/img            | *.png               |               | The image file used by the program.                          |
| src/lib            | ConfigLoader.py     | python 3.7 +  | Configuration file read and write library module.            |
| src/lib            | Log.py              | python 3.7 +  | Customized log recording library module.                     |
| src/scenario       | *.json              | JSON          | Scenario record files.                                       |
| src                | 2DCQBSimuRun.py     | python 3.7 +  | The 2D CQB robot simulation program main execution program.  |
| src                | Config_template.txt |               | The program configure file template                          |
| src                | cqbSimuGlobal.py    | python 3.7 +  | Module to set constants,  global parameters which will be used in the other modules. |
| src                | cqbSimuMapMgr.py    | python 3.7 +  | UI map component management module.                          |
| src                | cqbSimuMapPanel.py  | python 3.7 +  | This module is used to create different map panel to show the  simulation viewer and scenario editor. |
| src                | cqbSimuPanel.py     | python 3.7 +  | This module is used to create different function panels which can  handle user's interaction (such as parameters adjustment) for the CQB robot simulation program. |



------

### Program Execution and Usage