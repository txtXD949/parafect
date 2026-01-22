import pyaudio
import numpy as np

class MicManager:
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.is_active = False
        self.audio_buffer = []

        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100

        self.voice_volume = 0.0

    def start(self):
        if self.is_active:
            return

        self.is_active = True
        self.audio_buffer = []

        self.stream = self.pa.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self.audio_callback
        )
        self.stream.start_stream()

    def stop(self):
        self.is_active = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def audio_callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        self.audio_buffer.append(audio_data)

        if len(self.audio_buffer) * self.chunk / self.rate > 1.0:
            self.audio_buffer.pop(0)

        return in_data, pyaudio.paContinue

    def update(self, delta_time):
        if not self.audio_buffer:
            self.voice_volume = 0.0
            return

        recent_data = np.concatenate(self.audio_buffer[-20:])

        if len(recent_data) > 0:
            rms = np.sqrt(np.mean(recent_data.astype(np.float32) ** 2))
            self.voice_volume = min(1.0, rms / 32768.0 * 300.0)
        else:
            self.voice_volume = 0.0

    def is_voice_active(self, threshold=0.000001):
        return self.voice_volume > threshold
