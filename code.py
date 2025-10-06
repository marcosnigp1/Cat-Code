# Cat Logic by Marcos Hernández
# This file was originally the project example given by AdaFruit, for the Propmaker 2040.

# Credits for audio files:

# --------- For day ----------
# Meowing Cat - https://pixabay.com/sound-effects/meowing-cat-401728/
# Cat Meow - https://pixabay.com/sound-effects/cat-meow-401729/

# ----------- For night ---------
# CUTE CAT - https://pixabay.com/sound-effects/cute-cat-352656/
# Cat - https://pixabay.com/sound-effects/cat-89108/

# ------- BOTH --------
# Purring Cat - https://pixabay.com/sound-effects/purring-cat-401727/  - This is kinda low, I have to increase the volume.


import time
import board
import audiocore
import audiobusio
import audiomixer
import analogio  # For the photoresistor.
from digitalio import DigitalInOut, Direction
import adafruit_hcsr04  # We need this to get the ultrasonic sensor working.


# Enable external power pin for the Speaker.
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = False

# Outputs for the ultrasonic sensor.
ultrasonic = adafruit_hcsr04.HCSR04(trigger_pin=board.SDA, echo_pin=board.SCL)

# Photoresistor
photoresistor = analogio.AnalogIn(board.A3)

# Speaker Playback

# Mixer Options
mixer = audiomixer.Mixer(
    voice_count=1,
    sample_rate=22050,
    channel_count=1,
    bits_per_sample=16,
    samples_signed=True,
)
audio = audiobusio.I2SOut(board.I2S_BIT_CLOCK, board.I2S_WORD_SELECT, board.I2S_DATA)
audio.play(mixer)

# ----- AUDIO FILES ---------#
cat_sound1_file = open("audio/meowing-cat-401728.wav", "rb")
cat_sound1 = audiocore.WaveFile(cat_sound1_file)

cat_sound2_file = open("audio/cat-meow-401729.wav", "rb")
cat_sound2 = audiocore.WaveFile(cat_sound2_file)


# ------ GLOBAL VOLUME ---- #
global_volume = 0.5

# ---- AUDIO LOGIC VARIABLES ---- #
check_light = 0


# Function to get the values from the photoresistor.
def get_voltage(pin):
    return (
        pin.value * 3.3
    ) / 65535  # Convert 16-bit reading to volts (suggested by ChatGPT)


while True:
    # Print ultrasonic sensor values.
    # Get distance.
    try:
        # --- Get values ----- #
        voltage = get_voltage(photoresistor)
        distance = ultrasonic.distance  # In cm
        print("Photoresistor voltage:", round(voltage, 3))
        print(f"Distance: {distance:.2f} cm")

        #  ---- Check conditions regarding these values ---- #

        # Check during day (or room is illuminated) case.
        if voltage > 1.40:
            if check_light == 1:
                mixer.voice[0].stop()
                check_light = 0

            if mixer.voice[0].playing:
                pass
            else:
                if distance > 100.00:
                    mixer.voice[0].play(cat_sound1, loop=False)
                    mixer.voice[0].level = global_volume

        # Check during night or no light.
        else:
            if check_light == 0:
                mixer.voice[0].stop()
                check_light = 1

            if mixer.voice[0].playing:
                pass
            else:
                if distance > 100.00 and mixer.voice[0].playing == False:
                    mixer.voice[0].play(cat_sound2, loop=False)
                    mixer.voice[0].level = global_volume

    except RuntimeError:
        # Sometimes a reading may fail due to timeout.
        print("Retrying...")
    time.sleep(0.05)
