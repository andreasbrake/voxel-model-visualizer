import numpy as np
from voxel_model_vizualizer import VoxelModelVizualizer

def generate_simple_model(scaling_mult=None):
  voxel_space = np.ones((7,7,7,4)) * np.array([1, 0, 0, 0])
  voxel_space[2:5, 2:5, 1:4] = np.ones((3,3,3,4)) * np.array([0, 1, 0, 0])
  voxel_space[1:6, 1:6,   0] = np.ones((5,5,4)) * np.array([0, 0, 1, 0])
  voxel_space[2:5, 2:5, 4:6] = np.ones((3,3,2,4)) * np.array([0, 0, 0, 1])

  if scaling_mult is None:
    return voxel_space
  else:
    return np.repeat(voxel_space, scaling_mult, axis=2).repeat(scaling_mult, axis=1).repeat(scaling_mult, axis=0)

if __name__ == '__main__':
  sample_model = generate_simple_model(generate_simple_model(scaling_mult=3))
  colours = [(0.8, 0, 0), (0, 0.8, 0), (0, 0, 0.8)]

  np.save('./sample/input.npy', sample_model)

  vizualizer = VoxelModelVizualizer()

  vizualizer.render(sample_model, colours, output_path='./sample/out.png')
  vizualizer.render(sample_model, colours, output_path='./sample/out_pancake.png', pancake=True)
  vizualizer.render(sample_model, colours, output_path='./sample/out_animate.gif', animate=True)
  vizualizer.render(sample_model, colours, output_path='./sample/out_animate_pancake.gif', animate=True, pancake=True)