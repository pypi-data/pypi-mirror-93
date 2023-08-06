#!/usr/bin/env python

from setuptools import Extension
from distutils.errors import CCompilerError
import os
from setuptools import setup, find_packages
import shutil
from pathlib import Path

# On Windows, we need the original PATH without Anaconda's compiler in it:
PATH = os.environ.get("PATH")

forceBuild = [Extension("rapidForceBuild.forceBuild", ["rapid/src/forceBuild.c"])]

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

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text(encoding='utf-8')

setup(name="librapid",
      version="0.0.2",
      description="General purpose library optimized to run on the GPU",
      long_description=long_description,
      long_description_content_type="text/markdown",
      ext_modules = forceBuild,
      packages=["rapid"] + ["rapid." + mod for mod in find_packages("rapid", exclude=["examples", "test"])],
      include_package_data=True,
      author="Toby Davis",
      author_email="pencilcaseman@gmail.com",
      url="https://github.com/Pencilcaseman/Rapid",
      license="MIT Licences",
      keywords="cuda math array ndarray matrix gpu",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Utilities",
          "Intended Audience :: Developers",
          "Intended Audience :: Education",
          "License :: OSI Approved :: MIT License"
      ]
      )
