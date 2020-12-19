# Nordic_bluetooth_learningProject
Learning about the BLE with Nordic.

This code sets up a BLE advertiser on the nRF51 Developer Kit. The code is used to simulate several proximate devices advertising to probe effects like interference. The code supports two "roles". Master and Slave. Master and Slave has to be wired together both on the PIN1. The Master will advertise on channel 37 upon a button press to Button1. The Master will also toggle PIN1 to synchronize with the Slave. The Slave can then advertise a message after a chosen delay. This is used to probe the effects of interference. The Slave will also advertise when Button4 is pressed.

Define roles and delay in settings.h

Current bugs: The advertisers seems to be blocking the frequency band. It atleast appears this way because the nRF Sniffer will not detect any other traffic when our boards are just turned on and ramped to TXIDLE.
