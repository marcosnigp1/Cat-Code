# Cat Logic by Marcos Hernández
# This file was originally the project example given by AdaFruit, for the Propmaker 2040.

"""RP2040 Prop-Maker Feather Example"""

import time
import board
import audiocore
import audiobusio
import audiomixer
from digitalio import DigitalInOut, Direction

# enable external power pin
# provides power to the external components
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = False

# i2s playback
wave_file = open("StreetChicken.wav", "rb")
wave = audiocore.WaveFile(wave_file)
audio = audiobusio.I2SOut(board.I2S_BIT_CLOCK, board.I2S_WORD_SELECT, board.I2S_DATA)
mixer = audiomixer.Mixer(
    voice_count=1,
    sample_rate=22050,
    channel_count=1,
    bits_per_sample=16,
    samples_signed=True,
)
audio.play(mixer)
mixer.voice[0].play(wave, loop=True)
mixer.voice[0].level = 0.5


while True:
    # rainbow animation on external neopixels

    time.sleep(0.02)
