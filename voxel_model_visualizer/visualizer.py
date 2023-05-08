import math
import numpy as np
from PIL import Image

from simple_3dviz import Mesh, Lines
from simple_3dviz.window import show
from simple_3dviz.utils import render
from simple_3dviz.scenes import Scene

class VoxelModelVisualizer():
  def __init__(self, gif_resolution=720, static_resolution=4096, frame_count=120, fps=24, camera_distance=2, camera_height=1, pancake_spread=5, verbose=False):
    self.gif_resolution = gif_resolution
    self.static_resolution = static_resolution
    self.frame_count = frame_count
    self.fps = fps
    self.camera_distance = camera_distance
    self.camera_height = camera_height
    self.pancake_spread = pancake_spread
    self.verbose = verbose

    self.initial_angle = 3 * math.pi / 4. # view from 135 degrees

  def render(self, voxel_space, class_colors, output_path=None, animate=False, pancake=False):
    if pancake:
      voxel_space_expanded = np.zeros((
        voxel_space.shape[0],
        voxel_space.shape[1],
        voxel_space.shape[2] * self.pancake_spread,
        voxel_space.shape[3]
      ))
      voxel_space_expanded[:,:,::self.pancake_spread,:] = voxel_space
      voxel_space = voxel_space_expanded
    
    if self.verbose:
      print('space shape', voxel_space.shape)
      
    arr_x = voxel_space.shape[0]
    arr_y = voxel_space.shape[1]
    arr_z = voxel_space.shape[2]
    classes = voxel_space.shape[3]

    max_dim = max(arr_x, arr_y, arr_z)
    voxel_space_class = np.zeros((max_dim, max_dim, max_dim))
    center_point = max_dim // 2 

    voxel_space_class[
      (center_point - math.floor(arr_x / 2.)):(center_point + math.ceil(arr_x / 2.)),
      (center_point - math.floor(arr_y / 2.)):(center_point + math.ceil(arr_y / 2.)),
      (center_point - math.floor(arr_z / 2.)):(center_point + math.ceil(arr_z / 2.))
    ] = np.argmax(voxel_space, axis=3)
    
    if self.verbose:
      print('Computed voxel space')
    
    render_objects = [
      self.__get_wireframe_boundary(voxel_space.shape),
      self.__get_floor_mesh(voxel_space.shape)
    ]
    
    if np.count_nonzero(voxel_space_class > 0) > 0:
      meshes = [Mesh.from_voxel_grid(voxel_space_class == i, colors=class_colors[i - 1]) for i in range(1, classes)]
      render_objects.extend(meshes)
    elif self.verbose:
      meshes = []
      print('Empty voxelspace')

    if self.verbose: 
      print('Computed meshes')
   
    if output_path is None:
      self.__render_simple(render_objects)
    elif animate:
      self.__render_gif(render_objects, output_path)
    else:
      self.__render_static(meshes, output_path)

  def __get_wireframe_boundary(self, space_shape):
    arr_x = space_shape[0]
    arr_y = space_shape[1]
    arr_z = space_shape[2]
    max_dim = max(arr_x, arr_y, arr_z)

    ls_x = arr_x / max_dim
    ls_y = arr_y / max_dim
    ls_z = arr_z / max_dim

    return Lines([
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
    ], (0.1, 0.1, 0.1, 1.0), width=0.003)

  def __get_floor_mesh(self, space_shape):
    arr_x = space_shape[0]
    arr_y = space_shape[1]
    arr_z = space_shape[2]
    max_dim = max(arr_x, arr_y, arr_z)

    ls_x = arr_x / max_dim
    ls_y = arr_y / max_dim
    ls_z = arr_z / max_dim

    return Mesh([
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

  def __render_simple(self, render_objects):
      # Initialize parameters
      th = self.initial_angle
      x = self.camera_distance * math.sin(th)
      y = self.camera_distance * math.cos(th)

      # Attempt to render on screen
      show(render_objects,
          background=(1, 1, 1, 1),
          camera_position=(x, y, self.camera_height),
          light = (0.5, 0.8, 2))

  def __render_static(self, render_objects, output_path):
      # Initialize parameters
      th = self.initial_angle
      x = self.camera_distance * math.sin(th)
      y = self.camera_distance * math.cos(th)

      # Compose Scene
      scene = Scene(size=(self.static_resolution, self.static_resolution), background=(1, 1, 1, 1))
      for o in render_objects:
        scene.add(o)
      scene.camera_position = (x, y, self.camera_height)
      scene.light = (0.5, 0.8, 2)
      scene.render()

      # Save to file
      im = Image.fromarray(scene.frame)
      im.save(output_path)

  def __render_gif(self, render_objects, output_path):
      # Initialize parameters
      th = self.initial_angle
      x = self.camera_distance * math.sin(th)
      y = self.camera_distance * math.cos(th)
      frame_duration = math.floor(1000 / max(self.fps, 1))
      frames = []

      # Compose Scene
      scene = Scene(size=(self.gif_resolution, self.gif_resolution), background=(1, 1, 1, 1))
      for o in render_objects:
        scene.add(o)
      scene.light = (0.7, 1, 4)
      
      # Render frames
      for f in range(self.frame_count):
        if self.verbose:
          print('Rendering Frame {}'.format(f))
        
        th = f * (2. * math.pi / self.frame_count)
        x = self.camera_distance * math.sin(th)
        y = self.camera_distance * math.cos(th)
      
        scene.camera_position = (x, y, self.camera_height)
        scene.render()
        frames.append(scene.frame)
      
      if self.verbose:
        print('Compiling GIF')
      
      # Compile into GIF
      ims = [Image.fromarray(a_frame) for a_frame in frames]
      ims[0].save(output_path, save_all=True, append_images=ims[1:], loop=0, duration=frame_duration)