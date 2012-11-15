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
import os
import aud

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
loadbysound = True
basenamelist = []

print(glob.glob(path))
print(filelist)

def load_object(filename):
    print("loading obj")
    
    try:
        faces,verts = stl_utils.read_stl(filename)
        ob1 = createMesh( filename[len(filename)-14 : len(filename)], verts, [], faces)
        bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])].select = True
        bpy.context.scene.objects.active = bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])]
    except:
        return(False)

def play_object(filename):
    device = aud.device()
    beep = aud.Factory(filename)
    handle = device.play(beep)


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
        global basenamelist
        global cleanpath

        #deletes all the objects
        select_all_objects()
        bpy.ops.object.delete()


        nextloop = True
        while(nextloop == True):
            filename = basenamelist[fileidx]

            if(loadbysound):
                if(os.path.isfile(cleanpath.replace("sound","model")+filename+".stl")==True):
                    load_object(cleanpath.replace("sound","model")+filename+".stl")
                    play_object(cleanpath+filename+".wav")
                    nextloop == False
            else:
                load_object(cleanpath)
                play_object(cleanpath.replace("model","sound")+filename+".wav")
                

            print("Object not found")
            fileidx = (fileidx%len(basenamelist))+1
                
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
        global filelist
        global basenamelist
        global cleanpath

        #deletes all the objects
        select_all_objects()
        bpy.ops.object.delete()

        
        nextloop = True
        while(nextloop == True):
            filename = basenamelist[fileidx]

            if(loadbysound):
                if(os.path.isfile(cleanpath.replace("sound","model")+filename+".stl")==True):
                    load_object(cleanpath.replace("sound","model")+filename+".stl")
                    play_object(cleanpath+filename+".wav")
                    nextloop = False
            else:
                load_object(cleanpath)
                play_object(cleanpath.replace("model","sound")+filename+".wav")
                fileidx = fileidx%(len(basenamelist) - 1)
                
        
        return {'FINISHED'}


class OpenButtom(bpy.types.Operator,ImportHelper):
    '''Load STL triangle mesh data'''
    bl_idname = "open.buttom"
    bl_label = "STL viewer"
    bl_options = {'UNDO'}

    #filename_ext = ".stl"
    directory = StringProperty(
            subtype='DIR_PATH',
            )
    
    def execute(self, context):
        global path
        global filelist
        global fileidx
        global basenamelist
        global cleanpath

        print(self.directory)
        cleanpath = self.directory
        
        if("sound" in self.directory):
            path = self.directory+"*.wav" 
            loadbysound  =True

        else:
            path = self.directory+"*.stl" 
            loadbysound  = False

        filelist = glob.glob(path)

        #generate basename list
        basenamelist = []
        for act in enumerate(filelist):
            
            filenam = os.path.basename(act[1])
            filenam = os.path.splitext(filenam)[0]
            basenamelist.append(filenam)

        #loading the first object
        #deletes all the objects
        select_all_objects()
        bpy.ops.object.delete()

        nextloop = True
        while(nextloop == True):
            filename = basenamelist[fileidx]
            if(loadbysound):
                if(os.path.isfile(self.directory.replace("sound","model")+filename+".stl")==True):
                    load_object(self.directory.replace("sound","model")+filename+".stl")
                    nextloop = False
                    play_object(self.directory+filename+".wav")
            else:
                load_object(self.directory)
                play_object(self.directory.replace("model","sound")+filename+".wav")
                

            print("Object not found")
            nextloop == True
            
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

