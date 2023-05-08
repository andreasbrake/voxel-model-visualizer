# Voxel Model Renderer

This code acts as a standalone tool to vizualize voxelized models stored as 4 dimensional numpy arrays (3 geometric dimensions + 1 class dimension).

## Usage
```
usage: main.py [-h] [-a] [-p] [-o OUTPUT] filepath

Voxel Model Renderer

positional arguments:
  filepath       Model input filepath

optional arguments:
  -h, --help     show this help message and exit
  -a, --animate  Generated an Animated GIF (default: False)
  -p, --pancake  Render model as pancake slices (default: False)
  -o OUTPUT      Output filepath (default: ./out.png)
  ```
  
## Installation

can be done with conda using the provided `conda_env.yml`

Dependencies:
- python=3.9
- numpy
- pandas
- argparse
- pip:
  - moderngl
  - simple_3dviz
  - wxpython
