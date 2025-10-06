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
external_power.value = True  # Turn ON or OFF.

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

cat_sound3_file = open("audio/cute-cat-352656.wav", "rb")
cat_sound3 = audiocore.WaveFile(cat_sound3_file)

cat_sound4_file = open("audio/cat-89108.wav", "rb")
cat_sound4 = audiocore.WaveFile(cat_sound4_file)

cat_sound5_file = open("audio/purring-cat-401727.wav", "rb")
cat_sound5 = audiocore.WaveFile(cat_sound5_file)

cat_sound6_file = open(
    "audio/purring-cat-401727.wav", "rb"
)  # I copied and paste the similar one to avoid a bug.
cat_sound6 = audiocore.WaveFile(cat_sound6_file)

# ------ GLOBAL VOLUME ---- #
global_volume = 0.2

# ---- AUDIO LOGIC VARIABLES ---- #
check_light = 0

# ---- Last sound variable (to store and compare files) ---#
last_play_time = 0
last_played = None
cooldown = 5  # This will let some audios play over and over again seemingly.

# -- Distance variables ---#
temp_distance = 0


# Function to get the values from the photoresistor.
def get_voltage(pin):
    return (
        pin.value * 3.3
    ) / 65535  # Convert 16-bit reading to volts (suggested by ChatGPT)


def change_detected():
    if mixer.voice[0].playing:
        mixer.voice[0].stop()


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
        if voltage >= 1.40:
            if distance > 300:
                sound = cat_sound1

            elif distance > 40:
                sound = cat_sound4

            elif distance > 1:
                sound = cat_sound5

            else:
                sound = None  # No sounds! Somehow?

            # If there is sound.
            if sound:
                now = time.monotonic()
                # Play sound if there is a new audio file and the cooldown has finished.
            if sound != last_played or now - last_play_time > cooldown:
                change_detected()
                mixer.voice[0].play(sound, loop=False)
                mixer.voice[0].level = global_volume
                last_played = sound
                last_play_time = now

        # Check during night or no light.
        elif voltage <= 1.39:
            if distance > 300:
                sound = cat_sound2

            elif distance > 40:
                sound = cat_sound3

            elif distance > 1:
                sound = cat_sound6

            else:
                sound = None  # No sounds! Somehow?

            # If there is sound.
            if sound:
                now = time.monotonic()
                # Play sound if there is a new audio file and the cooldown has finished.
            if sound != last_played or now - last_play_time > cooldown:
                change_detected()
                mixer.voice[0].play(sound, loop=False)
                mixer.voice[0].level = global_volume
                last_played = sound
                last_play_time = now

    except RuntimeError:
        # Sometimes a reading may fail due to timeout.
        print("Retrying...")
    time.sleep(1)
