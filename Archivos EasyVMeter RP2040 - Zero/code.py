import usb_midi
import adafruit_midi
import board
import time
import pwmio
import neopixel

from adafruit_midi.channel_pressure import ChannelPressure
from adafruit_midi.note_on import NoteOn

PWM_PIN = board.GP29
PWM_FREQUENCY = 150
PWM_DUTY_CYCLE_MAX = 65535
PWM_DUTY_CYCLE_MIN = 0

CLIP_ANIMATION_COOLDOWN_SECONDS = 1.0
clip_animation_ready_time = 0.0

NEOPIXEL_PIN = getattr(board, 'NEOPIXEL', board.GP16)

COLOR_OK = (0, 255, 0)
COLOR_ERROR = (255, 0, 0)
COLOR_RECIVE = (255, 255, 0)
COLOR_SOLO = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_OFF = (0, 0, 0)

SOLO_TRIGGER_NOTE = 08

pixels = neopixel.NeoPixel(NEOPIXEL_PIN, 1, brightness=1, auto_write=False)

pwm = None

def led_error():
    pixels.fill(COLOR_ERROR)
    pixels.show()

def led_ok():
    pixels.fill(COLOR_OK)
    pixels.show()

def led_recive():
    pixels.fill(COLOR_RECIVE)
    pixels.show()

def led_off():
    pixels.fill(COLOR_OFF)
    pixels.show()

def led_solo():
    pixels.fill(COLOR_SOLO)
    pixels.show()
    
def startup_animation():
    if pwm:
        pwm.duty_cycle = PWM_DUTY_CYCLE_MAX
        pixels.fill(COLOR_OK)
        pixels.show()
        time.sleep(1)

        fade_steps = 100
        fade_delay = 2.0 / fade_steps
        duty_cycle_decrease_per_step = (PWM_DUTY_CYCLE_MAX - PWM_DUTY_CYCLE_MIN) / (fade_steps - 1) if fade_steps > 1 else 0

        for i in range(fade_steps):
            duty_cycle = PWM_DUTY_CYCLE_MAX - int(duty_cycle_decrease_per_step * i)
            duty_cycle = max(PWM_DUTY_CYCLE_MIN, duty_cycle)
            pwm.duty_cycle = duty_cycle
            time.sleep(fade_delay)

        pwm.duty_cycle = PWM_DUTY_CYCLE_MIN
        pixels.fill(COLOR_OK)
        pixels.show()

clipping_is_playing = False

def trigger_clip_animation():
    global clipping_is_playing
    global last_message_time
    global clip_animation_ready_time
    
    current_time = time.monotonic()

    if clipping_is_playing or (current_time < clip_animation_ready_time):
        return

    last_message_time = current_time
    clipping_is_playing = True
    
    if pwm:
        for _ in range(2):
            pwm.duty_cycle = PWM_DUTY_CYCLE_MAX
            led_error()
            time.sleep(0.2)

            pwm.duty_cycle = PWM_DUTY_CYCLE_MIN
            led_recive()
            time.sleep(0.2)

            pwm.duty_cycle = PWM_DUTY_CYCLE_MAX
            led_error()
            time.sleep(0.2)

            pwm.duty_cycle = PWM_DUTY_CYCLE_MIN
            led_recive()
            time.sleep(0.2)

            pwm.duty_cycle = PWM_DUTY_CYCLE_MAX
            led_error()
            time.sleep(0.2)

            pwm.duty_cycle = PWM_DUTY_CYCLE_MIN
            led_recive()
            time.sleep(0.4)

        pwm.duty_cycle = PWM_DUTY_CYCLE_MIN
    
    clipping_is_playing = False
    last_message_time = time.monotonic()

    clip_animation_ready_time = time.monotonic() + CLIP_ANIMATION_COOLDOWN_SECONDS

try:
    pwm = pwmio.PWMOut(PWM_PIN, frequency=PWM_FREQUENCY, duty_cycle=PWM_DUTY_CYCLE_MIN)
except Exception as e:
    pixels.fill(COLOR_ERROR)
    pixels.show()
    while True:
        pass

midi = None
midi_setup_successful = False

midi_in_port = None
for port in usb_midi.ports:
    if isinstance(port, usb_midi.PortIn):
        midi_in_port = port
        break

if midi_in_port:
    try:
        midi = adafruit_midi.MIDI(midi_in=midi_in_port)
        midi_setup_successful = True
        led_ok()
        startup_animation()

    except Exception as e:
        midi_setup_successful = False
        led_error()

else:
    midi_setup_successful = False
    led_error()

MODE_MIDI_CONTROL = 0
MODE_SOLO = 1
MODE_CONFIG = 2

current_mode = MODE_MIDI_CONTROL

TIMEOUT_SECONDS = 0.5
last_message_time = time.monotonic()

def run_midi_control_mode(msg=None):
    global last_message_time

    if not clipping_is_playing and (time.monotonic() - last_message_time) > TIMEOUT_SECONDS:
        if pwm and pwm.duty_cycle != PWM_DUTY_CYCLE_MIN:
            pwm.duty_cycle = PWM_DUTY_CYCLE_MIN
            led_ok()

    if msg is not None:
        if isinstance(msg, ChannelPressure):
            if msg.channel == 0:
                data_byte = msg.pressure
                track_index = (data_byte >> 4) & 0x0F
                volume_clip_status = data_byte & 0x0F

                if track_index == 0:
                    if volume_clip_status > 0: 
                        last_message_time = time.monotonic()

                    if volume_clip_status <= 0x0B:
                        if not clipping_is_playing:
                            level_0_11 = volume_clip_status
                            if pwm:
                                if level_0_11 == 0:
                                    pwm.duty_cycle = PWM_DUTY_CYCLE_MIN
                                    led_ok()
                                else:
                                    duty_cycle = int((level_0_11 / 11.0) * PWM_DUTY_CYCLE_MAX)
                                    duty_cycle = max(PWM_DUTY_CYCLE_MIN + 1000, duty_cycle)
                                    pwm.duty_cycle = duty_cycle
                                    led_recive()

                    elif volume_clip_status == 0x0C or volume_clip_status == 0x0D:
                        trigger_clip_animation()

def run_solo_mode(msg=None):
    global last_message_time

    if not clipping_is_playing and (time.monotonic() - last_message_time) > TIMEOUT_SECONDS:
        if pwm and pwm.duty_cycle != PWM_DUTY_CYCLE_MIN:
            pwm.duty_cycle = PWM_DUTY_CYCLE_MIN
            led_solo()

    if msg is not None:
        if isinstance(msg, ChannelPressure):
            if msg.channel == 0:
                data_byte = msg.pressure
                track_index = (data_byte >> 4) & 0x0F
                volume_clip_status = data_byte & 0x0F

                if track_index == 0:
                    if volume_clip_status >= 6:
                        last_message_time = time.monotonic()

                    if volume_clip_status <= 0x0B:
                        if not clipping_is_playing:
                            if volume_clip_status < 6:
                                if pwm:
                                    pwm.duty_cycle = PWM_DUTY_CYCLE_MIN
                                    led_solo()
                            else:
                                level_mapped_0_5 = volume_clip_status - 6
                                if pwm:
                                    duty_cycle = int((level_mapped_0_5 / 5.0) * PWM_DUTY_CYCLE_MAX)
                                    if duty_cycle > PWM_DUTY_CYCLE_MIN and duty_cycle < PWM_DUTY_CYCLE_MIN + 1000:
                                        duty_cycle = PWM_DUTY_CYCLE_MIN + 1000

                                    pwm.duty_cycle = duty_cycle
                                    led_recive()

                    elif volume_clip_status == 0x0C or volume_clip_status == 0x0D:
                        trigger_clip_animation()

while True:
    received_msg = None

    if midi_setup_successful:
        received_msg = midi.receive()

        if received_msg is not None:
            if isinstance(received_msg, NoteOn):
                if received_msg.note == SOLO_TRIGGER_NOTE:
                    last_message_time = time.monotonic()

                    if received_msg.velocity == 1:
                        if current_mode != MODE_SOLO:
                            current_mode = MODE_SOLO
                            if pwm: pwm.duty_cycle = PWM_DUTY_CYCLE_MIN
                            led_solo()
                            received_msg = None
                    elif received_msg.velocity == 0:
                        if current_mode != MODE_MIDI_CONTROL:
                            current_mode = MODE_MIDI_CONTROL
                            if pwm: pwm.duty_cycle = PWM_DUTY_CYCLE_MIN
                            led_ok()
                            received_msg = None

    if midi_setup_successful:
        if current_mode == MODE_MIDI_CONTROL:
            run_midi_control_mode(received_msg)
        elif current_mode == MODE_SOLO:
            run_solo_mode(received_msg)

    if not clipping_is_playing:
        time.sleep(0.001)