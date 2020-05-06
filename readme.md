# D2companion
This project aims towards making a "smart Bot" that is able to play Diablo 2 without using scripted actions or manipulating the gamestate in an malicious manner.

## Utilities
### ScreenCapture
We will make a screenshot at certain time intervals

### Mouse/Keyboard
We will record Mouse and Keyboard to provide labels for Model training.
The model itself wil input its action in the same way.

### GANcompressor Model
The idea is to not use the screenshot itself but a compressed version that should still include all the necessary information.
The compression of the images is done by using GANs. The setup is basically an Autoencoder with a latent layer:

Encoder --> Latent Layer --> Decoder

We will use the latent layer as the Input for our following Models. The decoder is to make sure the information in the latent layer is correlating with the original image.
