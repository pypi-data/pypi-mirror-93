from setuptools import setup
setup(
    name="MNSD",
    version="2021.0.3",
    author="Pranav",
    packages=["MNSD"],
    license="MIT",
    install_requires=['matplotlib','pytube','pyyaml','PrtSc','OS_Platform','psutil','batterycharge','opencv-python','pyjokes','requests','flask','pyautogui','pypiwin32','rotate-screen'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    py_requires='>3.7',
)