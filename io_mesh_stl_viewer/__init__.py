# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import glob
from io_mesh_stl import stl_utils
from io_mesh_stl import blender_utils
from bpy.props import StringProperty, BoolProperty, CollectionProperty
from bpy_extras.io_utils import ExportHelper, ImportHelper

bl_info = {
    "name": "Stlviewer",
    "author": "Miguel Jimenez ",
    "version": (1, 0),
    "blender": (2, 6, 3),
    "location": "File > stl viewer",
    "description": "Stl viewer",
    "warning": "",
    "wiki_url": "https://github.com/migvel/stlview/"
                "Scripts/Setl viewer",
    "category": "Import-Export"}

path = ""
fileidx = 0
filelist = glob.glob(path)

print(glob.glob(path))
print(filelist)

class GeneralUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Stl Viewer"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        
        col = layout.column(align=True)
        row = col.row()
        row.operator("open.buttom", text="open")        

        col = layout.column(align=True)
        row = col.row()
        row.operator("next.buttom", text="next")        

        col = layout.column(align=True)
        row = col.row()
        row.operator("prev.buttom", text="prev")        

        
class NextButtom(bpy.types.Operator):
    #''''''
    bl_idname = "next.buttom"
    bl_label = "Start"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        global fileidx
        global filelist

        #deletes all the objects
        select_all_objects()
        bpy.ops.object.delete()

        #next object
        print("-- Filename opened:")
        print("idx"+str(fileidx))
        print(filelist[fileidx])

        faces,verts = stl_utils.read_stl(filelist[fileidx])
        filename = filelist[fileidx]
        ob1 = createMesh( filename[len(filename)-14 : len(filename)], verts, [], faces)
        bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])].select = True
        bpy.context.scene.objects.active = bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])]

        if(fileidx < len(filelist)):
            fileidx = fileidx + 1
        else:
            fileidx = 0
        

        return {'FINISHED'}

class PrevButtom(bpy.types.Operator):
    #''''''
    bl_idname = "prev.buttom"
    bl_label = "Previous"

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        global fileidx

        #deletes all the objects
        select_all_objects()
        bpy.ops.object.delete()

        #next object
        print("-- Filename opened:")
        print("idx:"+str(fileidx))
        print(filelist[fileidx])

        faces,verts = stl_utils.read_stl(filelist[fileidx])
        filename = str(filelist[fileidx])
        ob2 = createMesh(filename[len(filename)-14 : len(filename)], verts, [], faces)
        bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])].select = True
        bpy.context.scene.objects.active = bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])]
        
        if(fileidx > 0):
            fileidx = fileidx - 1
        else:
            fileidx = 0
    
        
        return {'FINISHED'}


class OpenButtom(bpy.types.Operator,ImportHelper):
    '''Load STL triangle mesh data'''
    bl_idname = "open.buttom"
    bl_label = "STL viewer"
    bl_options = {'UNDO'}

    filename_ext = ".stl"
    directory = StringProperty(
            subtype='DIR_PATH',
            )
    
    def execute(self, context):
        global path
        global filelist
        global fileidx

        path = self.directory+"*.stl"
        filelist = glob.glob(path)
        
        #loading the first object
        #deletes all the objects
        select_all_objects()
        bpy.ops.object.delete()

        faces,verts = stl_utils.read_stl(filelist[fileidx])
        filename = filelist[fileidx]
        ob1 = createMesh( filename[len(filename)-14 : len(filename)], verts, [], faces)
        bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])].select = True
        bpy.context.scene.objects.active = bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])]

        fileidx = fileidx + 1
        
        return {'FINISHED'}

def find_object(targetname):
    """ Return index of objects that contains targename in name """
    for index,object in enumerate(bpy.data.objects):
        if(object.name == targetname):
            return(index)

def deselect_all_objects():
    """ Deselects all objects """
    for object in bpy.data.objects:
        object.select = False

def select_all_objects():
    """ Deselects all objects """
    for object in bpy.data.objects:
        object.select = True

def createMesh(name, verts, edges, faces):
    me = bpy.data.meshes.new(name+'Mesh')     # Create mesh and object
    ob = bpy.data.objects.new(name, me)
    ob.show_name = True
    bpy.context.scene.objects.link(ob)     # Link object to scene
    me.from_pydata(verts, edges, faces)
    me.update(calc_edges=True)    # Update mesh with new data
    return ob

def register():
    bpy.utils.register_class(GeneralUI)
    bpy.utils.register_class(NextButtom)
    bpy.utils.register_class(PrevButtom)
    bpy.utils.register_class(OpenButtom)
        
def unregister():
    bpy.utils.register_class(GeneralUI)
    bpy.utils.register_class(StartButtom)
    bpy.utils.register_class(OpenButtom)
    pass

if __name__ == "__main__":
    register()

