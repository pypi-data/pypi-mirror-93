#!/usr/bin/env python

from distutils.errors import CCompilerError
import os
from setuptools import setup, find_packages
import shutil

# On Windows, we need the original PATH without Anaconda's compiler in it:
PATH = os.environ.get("PATH")

extensionFiles = ["rapid/src/ndarray/rapid_ndarray.cu"]

def buildExtensions(files):
    cwd = os.path.dirname(__file__) or os.path.curdir

    os.system("nvcc --version")
    for ext in files:
        filename = ext[-ext[::-1].find("/"):]

        print(filename)
        print(filename[:filename.find(".")])

        os.system("cd rapid && mkdir bin")
        os.system("nvcc -o rapid/lib{}.dll --shared {} -lcublas".format(filename[:filename.find(".")], ext))

        # Move the files that were created to the lib folder"
        toMove = []

        for file in os.listdir(cwd + "/rapid"):
            if file.startswith("lib{}".format(filename[:filename.find(".")])):
                toMove.append(file)

        if len(toMove) < 1:
            raise CCompilerError("Unable to compile CUDA code")

        for file in toMove:
            shutil.move("rapid/{}".format(file), "rapid/bin/{}".format(file))

        os.listdir(cwd)

buildExtensions(extensionFiles)

setup(name="librapid",
      version="0.0.0",
      description="General purpose library optimized to run on the GPU",
      packages=find_packages(exclude=["examples", "test"]),
      include_package_data=True,
      author="Toby Davis",
      author_email="pencilcaseman@gmail.com",
      license="MIT",
      keywords="cuda math array ndarray matrix gpu",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Utilities",
          "License :: OSI Approved :: MIT License"
      ]
      )
