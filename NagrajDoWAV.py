import math

import pyaudio
import wave
import soundfile
import tkinter as tk

from termcolor import colored as coloured

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = int(44100 / 1)
RECORD_SECONDS = 4


def calc_log(value):
    return 20 * math.log10(2**value)


def change_rate(nazwa, subtype):
    data, samplerate = soundfile.read(nazwa)
    soundfile.write("nowy_" + nazwa, data, samplerate, subtype=subtype)


def change_rate_16(nazwa="Nagranie.wav", subtype="PCM_16"):
    data, samplerate = soundfile.read(nazwa)
    soundfile.write("nowy1_" + nazwa, data, samplerate, subtype=subtype)
    play("nowy1_Nagranie.wav")


def change_rate_8(nazwa="Nagranie.wav", subtype="PCM_U8"):
    data, samplerate = soundfile.read(nazwa)
    soundfile.write("nowy2_" + nazwa, data, samplerate, subtype=subtype)
    play("nowy2_Nagranie.wav")


def record(nazwa="Nagranie.wav"):
    p = pyaudio.PyAudio()

    # defaultCapability = p.get_default_host_api_info()
    # print(defaultCapability)

    # WAVE_OUTPUT_FILENAME = "output.wav"

    if not p.is_format_supported(input_format=FORMAT, input_channels=CHANNELS, rate=RATE, input_device=1):
        raise pyaudio.paBadIODeviceCombination

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(coloured("Nagrywam", 'green'))

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        frames.append(stream.read(CHUNK))

    print(coloured("Koniec nagrania", 'blue'))

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(nazwa, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def play(nazwa="Nagranie.wav"):
    # define stream chunk

    # open a wav format music
    f = wave.open(nazwa, "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)

    print(coloured("SNR = " + "{:.2f}".format(calc_log(f.getsampwidth() * 8)) + " dB", 'yellow'))

    # read data
    data = f.readframes(CHUNK)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(CHUNK)

        # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()


def __gui_main():
    win = tk.Tk()
    win.title('Zad 4 Tele')
    win.geometry("300x104+1200+100")

    openBtn = tk.Button(win, text='Nagraj', bg='pink', command=record)
    openBtn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

    if FORMAT == pyaudio.paInt24 or FORMAT == pyaudio.paFloat32 or FORMAT == pyaudio.paFloat32:
        saveBtn = tk.Button(win, text='Odtwórz 24 bity', bg='orange', command=play)
        saveBtn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

    if FORMAT == pyaudio.paInt16 or FORMAT == pyaudio.paInt24 or FORMAT == pyaudio.paFloat32 or FORMAT == pyaudio.paFloat32:
        play16 = tk.Button(win, text='Odtwórz 16 bitów', bg='green', command=change_rate_16)
        play16.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)
    if FORMAT == pyaudio.paUInt8 or pyaudio.paInt8 or FORMAT == pyaudio.paInt16 or FORMAT == pyaudio.paInt24 or FORMAT == pyaudio.paFloat32 or FORMAT == pyaudio.paFloat32:
        play8 = tk.Button(win, text='Odtwórz 8 bitów', bg='yellow', command=change_rate_8)
        play8.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

    end = tk.Button(win, text='Zamknij okno', bg='red', command=win.destroy)
    end.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

    win.mainloop()


def main():
    # print(soundfile.available_subtypes('wav'))
    record("Nagranie.wav")
    print("Original")
    play("Nagranie.wav")
    print("PCM_16")
    change_rate("Nagranie.wav", "PCM_16")
    play("nowy_Nagranie.wav")
    print("PCM_U8")
    change_rate("Nagranie.wav", "PCM_U8")
    play("nowy_Nagranie.wav")


if __name__ == "__main__":
    __gui_main()
