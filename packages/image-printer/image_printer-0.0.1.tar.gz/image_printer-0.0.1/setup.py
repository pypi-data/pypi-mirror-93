import setuptools


setuptools.setup(
    name="image_printer",  # Replace with your own username
    version="0.0.1",
    description="stdout image as colored text",
    url="https://github.com/Zzznorlax/image-printer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "opencv-python"
    ],
    python_requires='>=3.8',
)
