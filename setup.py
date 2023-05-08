#!/usr/bin/env python

from itertools import dropwhile
import os
from os import path
from setuptools import find_packages, setup

def collect_docstring(lines):
    """Return document docstring if it exists"""
    lines = dropwhile(lambda x: not x.startswith('"""'), lines)
    doc = ""
    for line in lines:
        doc += line
        if doc.endswith('"""\n'):
            break

    return doc[3:-4].replace("\r", "").replace("\n", " ")

def collect_metadata():
    meta = {}
    with open(path.join("voxel_model_vizualizer", "__init__.py")) as f:
        lines = iter(f)
        meta["description"] = collect_docstring(lines)
        for line in lines:
            if line.startswith("__"):
                key, value = map(lambda x: x.strip(), line.split("="))
                meta[key[2:-2]] = value[1:-1]

    return meta
    
if __name__ == '__main__':
  meta = collect_metadata()

  with open("README.md") as f:
    long_description = f.read()

  setup(
      name='voxel-model-vizualizer',
      version=meta["version"],

      description=meta["description"],
      long_description=long_description,
      long_description_content_type='text/markdown',
      url=meta["url"],
      author=meta["author"],
      author_email=meta["email"],
      
      keywords=meta["keywords"],
      license=meta["license"],

      py_modules=['voxel_model_vizualizer'],
      
      install_requires=[
        "moderngl",
        "numpy",
        "pillow",
        "simple_3dviz",
        "wxpython",
      ],
  )