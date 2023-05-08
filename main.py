import argparse
import numpy as np
import math

from PIL import Image

from simple_3dviz import Mesh, Lines
from simple_3dviz.window import show
from simple_3dviz.utils import render
from simple_3dviz.scenes import Scene

GIF_RESOLUTION = 720
STATIC_RESOLUTION = 4096

def render(voxel_space, class_colors, output_path=None, animate=False, pancake=False):
  if pancake:
    voxel_space_expanded = np.zeros((
      voxel_space.shape[0],
      voxel_space.shape[1],
      voxel_space.shape[2] * 5,
      voxel_space.shape[3]
    ))
    voxel_space_expanded[:,:,::5,:] = voxel_space
    voxel_space = voxel_space_expanded
  
  print('space shape', voxel_space.shape)
    
  classes = voxel_space.shape[3]
  arr_x = voxel_space.shape[0]
  arr_y = voxel_space.shape[1]
  arr_z = voxel_space.shape[2]
  max_dim = max(arr_x, arr_y, arr_z)
  voxel_space_class = np.zeros((max_dim, max_dim, max_dim))
  center_point = max_dim // 2 

  voxel_space_class[
    (center_point - math.floor(arr_x / 2.)):(center_point + math.ceil(arr_x / 2.)),
    (center_point - math.floor(arr_y / 2.)):(center_point + math.ceil(arr_y / 2.)),
    (center_point - math.floor(arr_z / 2.)):(center_point + math.ceil(arr_z / 2.))
  ] = np.argmax(voxel_space, axis=3)
  
  ls_x = arr_x / max_dim
  ls_y = arr_y / max_dim
  ls_z = arr_z / max_dim
  
  ls_x_offset = arr_x / max_dim
  ls_y = arr_y / max_dim
  ls_z = arr_z / max_dim
  
  print('Computed voxel space')
  
  x_pt, y_pt, z_pt = ls_x / 2, ls_y / 2, ls_z / 2

  render_objects = [Lines([
    # min point
    [-ls_x / 2, -ls_y / 2, -ls_z / 2],
    [ ls_x / 2, -ls_y / 2, -ls_z / 2],
    
    [-ls_x / 2, -ls_y / 2, -ls_z / 2],
    [-ls_x / 2,  ls_y / 2, -ls_z / 2],
    
    [-ls_x / 2, -ls_y / 2, -ls_z / 2],
    [-ls_x / 2, -ls_y / 2,  ls_z / 2],
    
    # max point
    [ ls_x / 2,  ls_y / 2,  ls_z / 2],
    [-ls_x / 2,  ls_y / 2,  ls_z / 2],
    
    [ ls_x / 2,  ls_y / 2,  ls_z / 2],
    [ ls_x / 2, -ls_y / 2,  ls_z / 2],
    
    [ ls_x / 2,  ls_y / 2,  ls_z / 2],
    [ ls_x / 2,  ls_y / 2, -ls_z / 2],
    
    #ends
    [ ls_x / 2, -ls_y / 2, -ls_z / 2],
    [ ls_x / 2, -ls_y / 2,  ls_z / 2],
    
    [ ls_x / 2, -ls_y / 2, -ls_z / 2],
    [ ls_x / 2,  ls_y / 2, -ls_z / 2],
    
    [-ls_x / 2,  ls_y / 2, -ls_z / 2],
    [-ls_x / 2,  ls_y / 2,  ls_z / 2],
    
    [-ls_x / 2,  ls_y / 2, -ls_z / 2],
    [ ls_x / 2,  ls_y / 2, -ls_z / 2],
    
    [-ls_x / 2, -ls_y / 2,  ls_z / 2],
    [-ls_x / 2,  ls_y / 2,  ls_z / 2],
    
    [-ls_x / 2, -ls_y / 2,  ls_z / 2],
    [ ls_x / 2, -ls_y / 2,  ls_z / 2],
  ], (0.1, 0.1, 0.1, 1.0), width=0.003)]
  
  ground_mesh = Mesh([
    [-ls_x / 2, -ls_y / 2, -ls_z / 2],
    [-ls_x / 2,  ls_y / 2, -ls_z / 2],
    [ ls_x / 2, -ls_y / 2, -ls_z / 2],
    [ ls_x / 2,  ls_y / 2, -ls_z / 2],
    [-ls_x / 2,  ls_y / 2, -ls_z / 2],
    [ ls_x / 2, -ls_y / 2, -ls_z / 2]
  ], [
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
  ], (0.8, 0.8, 0.8, 1.0))
  
  render_objects.append(ground_mesh)
  
  if np.count_nonzero(voxel_space_class > 0) > 0:
    meshes = [Mesh.from_voxel_grid(voxel_space_class == i, colors=class_colors[i - 1]) for i in range(1, classes)]
    render_objects.extend(meshes)
  else:
    print('Empty voxelspace')
    
  print('Computed meshes')
  
  camera_distance = 2
  camera_height = 1
  th = 3 * math.pi / 4. # view from 135 degrees
  x = camera_distance * math.sin(th)
  y = camera_distance * math.cos(th)

  if output_path is None:
    show(render_objects,
        background=(1, 1, 1, 1),
        camera_position=(x, y, camera_height),
        light = (0.5, 0.8, 2))
  elif animate:
    scene = Scene(size=(GIF_RESOLUTION, GIF_RESOLUTION), background=(1, 1, 1, 1))
    for o in render_objects:
      scene.add(o)
    scene.light = (0.7, 1, 4)
        
    frames = []
    frame_count = 120
    
    for f in range(frame_count):
      print('Rendering Frame {}'.format(f))
      
      th = f * (2. * math.pi / frame_count)
      x = camera_distance * math.sin(th)
      y = camera_distance * math.cos(th)
    
      scene.camera_position = (x, y, camera_height)
      scene.render()
      frames.append(scene.frame)
      
    print('Compiling GIF')
    
    ims = [Image.fromarray(a_frame) for a_frame in frames]
    ims[0].save(output_path, save_all=True, append_images=ims[1:], loop=0, duration=40)
  else:
    scene = Scene(size=(STATIC_RESOLUTION, STATIC_RESOLUTION),
                  background=(1, 1, 1, 1))
    for m in meshes:
      scene.add(m)
    
    scene.camera_position = (x, y, camera_height)
    scene.light = (0.5, 0.8, 2)
    scene.render()

    im = Image.fromarray(scene.frame)
    im.save(output_path)
    
def generate_simple_model(scaling_mult=None):
  voxel_space = np.ones((7,7,7,4)) * np.array([1, 0, 0, 0])
  voxel_space[2:5, 2:5, 1:4] = np.ones((3,3,3,4)) * np.array([0, 1, 0, 0])
  voxel_space[1:6, 1:6,   0] = np.ones((5,5,4)) * np.array([0, 0, 1, 0])
  voxel_space[2:5, 2:5, 4:6] = np.ones((3,3,2,4)) * np.array([0, 0, 0, 1])

  if scaling_mult is None:
    return voxel_space
  else:
    return np.repeat(voxel_space, scaling_mult, axis=2).repeat(scaling_mult, axis=1).repeat(scaling_mult, axis=0)

def test():
  render(generate_simple_model(scaling_mult=3),
         class_colors=[(0.8, 0, 0), (0, 0.8, 0), (0, 0, 0.8)],
         output_path='./out.gif',
         animate=True)

  np_arr = np.load('./2800_2023-04-10_00-54-07_0generated.npy')
  np_arr = np.load('./models/4000_2023-04-04_13-03-30_0generated.npy')

  render(np_arr, [(0.8, 0, 0)], './out_full.gif', animate=True)
  render(np_arr, [(0.8, 0, 0)], './out_full.png', animate=False, pancake=True)
  
def parse_options():
  parser = argparse.ArgumentParser(description="Voxel Model Renderer",
                                  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("filepath", help="Model input filepath")
  parser.add_argument("-a", "--animate", action="store_true", help="Generated an Animated GIF")
  parser.add_argument("-p", "--pancake", action="store_true", help="Render model as pancake slices")
  parser.add_argument("-o", dest="output", help="Output filepath", default="./out.png")

  args = parser.parse_args()
  config = vars(args)
  
  return config

if __name__ == '__main__':
  args = parse_options()
  
  input_path = args["filepath"]
  is_animate = args["animate"]
  is_pancake = args["pancake"]
  output_path = args["output"]
  print(args)
  
  np_arr = np.load(input_path)
  render(np_arr,
         [(0.8, 0, 0), (0, 0.8, 0), (0, 0, 0.8)],
         output_path,
         animate=is_animate,
         pancake=is_pancake)
