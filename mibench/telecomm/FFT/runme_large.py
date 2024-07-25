import subprocess

subprocess.call(["python3", "mibench/telecomm/FFT/fft.py", "8", "32768"])
subprocess.call(["python3", "mibench/telecomm/FFT/fft.py", "8", "32768", "-i"])
