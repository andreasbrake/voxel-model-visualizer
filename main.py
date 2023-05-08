#!/usr/bin/env python

import argparse
import numpy as np
from voxel_model_vizualizer import VoxelModelVizualizer

def parse_options():
  parser = argparse.ArgumentParser(description="Voxel model renderer will take a 4 dimensional numpy array (.npy file) and render it into a static image or a gif. This model should have 3 geometric dimensions and a single class dimensions with a maximum of 3 classes",
                                  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("filepath", help="Model input filepath")
  parser.add_argument("-a", "--animate", action="store_true", help="Generated an Animated GIF")
  parser.add_argument("-p", "--pancake", action="store_true", help="Render model as pancake slices")
  parser.add_argument("-v", "--verbose", action="store_true", help="Verbose console printing")
  parser.add_argument("-o", dest="output", help="Output filepath", default="./out.png")

  args = parser.parse_args()
  config = vars(args)
  
  return config

if __name__ == '__main__':
  args = parse_options()
  
  input_path = args["filepath"]
  is_animate = args["animate"]
  is_pancake = args["pancake"]
  is_verbose = args["verbose"]
  output_path = args["output"]
  
  np_arr = np.load(input_path)
  
  VoxelModelVizualizer(
    verbose=is_verbose
  ).render(
    np_arr,
    [(0.8, 0, 0), (0, 0.8, 0), (0, 0, 0.8)],
    output_path,
    animate=is_animate,
    pancake=is_pancake
  )
