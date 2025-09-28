from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdflayoutai",
    version="1.0.0",
    author="yxshee",
    author_email="yxshee@example.com",
    description="AI-powered PDF layout detection and annotation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yxshee/pdflayoutai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyMuPDF>=1.23.0",
        "tqdm",
        "opencv-python",
        "ultralytics",
        "torch",
        "torchvision",
        "numpy",
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "pdflayoutai=pdflayoutai.cli:main",
        ],
    },
)
