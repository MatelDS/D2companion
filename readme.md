# D2companion
This project aims towards making a "smart Bot" that is able to play Diablo 2 without using scripted actions or manipulating the gamestate in an malicious manner.

## Utilities

### d2screenutils - ScreenCapture
Capture the screen at certain time intevals to get "frames" of the visible gamestate.

### d2io - Mouse/Keyboard I/O
A Mouse and Keyboard input is recorded to provide a corresponding label for each recorded frame.
The final model itself wil input via simulated mouse and keyboard actions.

### d2record - Game Recording
Basic functions to capture frames and corresponding mouse/keyboard-input labels to generate Training-Data.

## Models

### GANcompressor Model
The idea is to not use the screenshot itself but a compressed version that should still include all the necessary information.
The compression of the images is done by using GANs. The setup is basically an Autoencoder with a latent layer:

Encoder --> Latent Layer --> Decoder

We will use the latent layer as the Input for our following Models. The decoder is to make sure the information in the latent layer is correlating with the original image.
