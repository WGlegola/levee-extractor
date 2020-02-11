import bpy
import numpy as np
import random
import sys
from mathutils import Euler

def get_mesh():
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            return obj

def clear():
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete(use_global=False)

    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)


def set_camera():
    camera = bpy.context.scene.camera

    camera.location.x = 0
    camera.location.y = 0
    camera.location.z = 30
    # camera.data.type = 'ORTHO'

    camera.rotation_euler = Euler((0, 0, 0), "XYZ")

def render(name):
    bpy.context.scene.render.filepath = '/home/mati/Pulpit/drone-pg/renders/' + name
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.ops.render.render(write_still = True)


def load_mesh():
    bpy.ops.import_scene.obj(filepath="/home/mati/Pulpit/drone-pg/models/cleared.obj")


def get_points():
    obj = get_mesh()

    coords = [v.co for v in obj.data.vertices]

    return np.array([(point.x, point.y, point.x) for point in coords if random.randint(0, 100) == 5])


def normalize_plane():
    obj = get_mesh()

    N = len(obj.data.vertices)

    centroid = [0, 0, 0]

    for vertex in obj.data.vertices:
        vertex.co.z *= -1
        centroid[0] += vertex.co.x
        centroid[1] += vertex.co.y
        centroid[2] += vertex.co.z

    for vertex in obj.data.vertices:
        vertex.co.x -= centroid[0] / N
        vertex.co.y -= centroid[1] / N
        vertex.co.z -= centroid[2] / N

    for iteration in range(10):
        print("Iteration {}".format(iteration))
        x_dis = 0
        y_dis = 0

        for vertex in obj.data.vertices:
            x_dis += vertex.co.z / vertex.co.x

        for vertex in obj.data.vertices:
            vertex.co.z -= (x_dis / N) * vertex.co.x * 0.8

        for vertex in obj.data.vertices:
            y_dis += vertex.co.z / vertex.co.y

        for vertex in obj.data.vertices:
            vertex.co.z -= (y_dis / N) * vertex.co.y * 0.8

        print("x={} y={}".format(x_dis, y_dis))

def filter_dam(coeff=1):
    obj = get_mesh()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    z_sum = 0
    z_count = 0

    for vertex in obj.data.vertices:
        z_sum += vertex.co.z
        z_count += 1

    avg_z = z_sum / z_count

    print(avg_z)

    for vertex in obj.data.vertices:
        vertex.select = (vertex.co.z - avg_z) * coeff < 0

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')

#clear()
#load_mesh()

set_camera()
render("1.raw.png")

normalize_plane()

render("2.plane-normalized.png")

filter_dam()

render("3.dam-filtered.png")

normalize_plane()

render("4.plane-normalized2.png")

filter_dam(coeff=-1)

render("5.dam-filtered2.png")

# sys.exit(0)
