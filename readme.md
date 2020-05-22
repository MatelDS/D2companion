# D2companion
This project aims towards making a "smart Bot" that is able to play Diablo 2 without using scripted actions or manipulating the gamestate in an malicious manner.

## d2recorderui

A basic UI that allows you to start recording your gameplay in a format that may be used for training of the models.

![](docs/images/recordUI.jpg)

## d2utilities

### d2utilities/d2io - Mouse/Keyboard/Screen I/O Utilities
A Mouse and Keyboard input is recorded to provide a corresponding label for each recorded frame.
The final model itself wil input via simulated mouse and keyboard actions.

#### D2Screen
Connect to your running D2 application and includes the utilities to capture the screen at certain time intevals to get "frames" of the visible gamestate.
These images are used as features for the model training.

#### D2Mouse/D2Keyboard
These utilities listen to mouse and keyboard inputs and save them in a format that allows to connect them to the captured frames of the d2screen class.
These mouse/keyboard-input are used as labels in the Training-Data.

### d2utilities/d2pipehandler - DiabloInterface communication

Collection of the hidden gamestate is done by [DiabloInterface](https://github.com/Zutatensuppe/DiabloInterface) from Zutatensuppe.

#### D2PipeHandler
DiabloInterface has a namedPipeServer that can be used to querry information invisible like items and stats. The D2PipeHandler class provides the functionality for communication with the PipeServer. 

###

### d2utilities/d2recordsession

#### d2recordsession
The d2recordsession class contains the methods to manage your screen, mouse and keyboard and set the needed parameters and values for the gameplay recordings.

## Models

### Autoencoder Model
Basic Autoencoder-Model for testing purposes:

original image --> Encoder --> Latent Layer --> Decoder --> reconstructed image
