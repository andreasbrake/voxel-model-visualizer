# Voxel Model Visualizer

[![PyPI version](https://badge.fury.io/py/voxel-model-visualizer.svg)](https://badge.fury.io/py/voxel-model-visualizer)
[![PyPI downloads](https://img.shields.io/pypi/dm/voxel-model-visualizer.svg)](https://pypistats.org/packages/voxel-model-visualizer)

This code acts as a standalone tool to vizualize voxelized models stored as 4 dimensional numpy arrays (3 geometric dimensions + 1 class dimension).

<img src="https://raw.githubusercontent.com/andreasbrake/voxel-model-visualizer/master/sample/output_animate.gif" width="400" height="400"/>


## Package Installation

Can be done directly from `pypi`

```bash
pip install voxel-model-visualizer
```

## Dependencies

* [moderngl](https://github.com/moderngl/moderngl)
* [numpy](http://www.numpy.org/)
* [pillow](https://pillow.readthedocs.io/en/stable/)
* [simple-3dviz](https://github.com/angeloskath/simple-3dviz)
* [wxpython](https://wxpython.org/)

## Package Usage

```python
from voxel_model_visualizer import VoxelModelVisualizer

model = np.load('./sample/input.npy')
colours = [(0.8, 0, 0), (0, 0.8, 0), (0, 0, 0.8)]
visualizer = VoxelModelVisualizer(gif_resolution=720,
                                  static_resolution=4096,
                                  frame_count=120,
                                  fps=24,
                                  pancake_spread=5,
                                  verbose=False)

visualizer.render(model, colours, output_path='./example_pancake.png', pancake=True)
visualizer.render(model, colours, output_path='./example_animate.gif', animate=True)
```

## Standalone Usage

```text
usage: main.py [-h] [-a] [-p] [-o OUTPUT] filepath

Voxel Model Renderer

positional arguments:
  filepath       Model input filepath

optional arguments:
  -h, --help     show this help message and exit
  -a, --animate  Generated an Animated GIF (default: False)
  -p, --pancake  Render model as pancake slices (default: False)
  -v, --verbose  Verbose console printing (default: False)
  -o OUTPUT      Output filepath (default: ./out.png)
```
