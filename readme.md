GANcompressor

Compression of images using GANs. The setup is basically an Autoencoder with a latent layer:

Encoder --> Latent Layer --> Decoder

We will use the latent layer as the Input for our following Model. The decoder is to make sure the information in the latent layer is correlating with the original image.
