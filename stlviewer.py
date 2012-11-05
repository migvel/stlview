import bpy
import glob
from io_mesh_stl import stl_utils
from io_mesh_stl import blender_utils


path = "set the path here"

fileidx = 0
filelist = glob.glob(path)

print(glob.glob(path))

class GeneralUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Cylinder modeler"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
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

        #deletes all the objects
        select_all_objects()
        bpy.ops.object.delete()

        #next object
        print(filelist[fileidx])

        faces,verts = stl_utils.read_stl(filelist[fileidx])
        filename = filelist[fileidx]
        ob1 = createMesh( filename[len(filename)-14 : len(filename)], verts, [], faces)
        bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])].select = True
        bpy.context.scene.objects.active = bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])]

        fileidx = fileidx + 1
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
        print(filelist[fileidx])

        faces,verts = stl_utils.read_stl(filelist[fileidx])
        filename = str(filelist[fileidx])
        ob2 = createMesh( filename[len(filename)-14 : len(filename)], verts, [], faces)
        bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])].select = True
        bpy.context.scene.objects.active = bpy.data.objects[find_object(filename[len(filename)-14 : len(filename)])]
        fileidx = fileidx - 1
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
        
def unregister():
    bpy.utils.register_class(GeneralUI)
    bpy.utils.register_class(StartButtom)
    bpy.utils.register_class(PrevButtom)
    pass

if __name__ == "__main__":
    register()

