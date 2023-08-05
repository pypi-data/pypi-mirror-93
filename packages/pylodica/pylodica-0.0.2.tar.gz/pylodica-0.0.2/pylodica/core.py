import numpy as np

def tone_frequency(n):
    '''
    Formula for calculating the frequency of the nth key
    '''
    return 440 * (((2)**(1/12))**(n-49))

note_dict = {
    'A♯': tone_frequency(48)
    'A4': tone_frequency(49),
}

def note_renderer(frequency):
    fs = 44100  # 44100 samples per second
    seconds = 3  # Note duration of 3 seconds
    # Generate a 440 Hz sine wave
    note = np.sin(frequency * t * 2 * np.pi)
    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

class FunkyBeat(object):
    def __init__(self, bpm):
        self._bpm = bpm
