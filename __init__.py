# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
from bpy.types import Operator
from bpy.types import Panel
from mathutils import Euler

bl_info = {
    "name" : "one",
    "author" : "j",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


# VARIABLES
spacing = 1
 
# DATA MODEL
class UserObject:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        

class LINE_UP_OPERATOR(Operator):
    bl_idname = "object.line_up"
    bl_label = "LineUp"
    bl_description = "Line Up all selected objects."
   
    
    @classmethod
    def poll(self, context):
        objects = self.get_selected(self, context)
        return {"FINISHED"}
    def set_spacing(self, newSpacing):
        spacing = newSpacing
        
    def execute(self, context):
        selected_objects = self.get_selected(context)
        print(selected_objects)
#        Measure length
        length = self.getTotalLength(selected_objects) + spacing * (len(selected_objects) - 1)
        offset = - length / 2 + selected_objects[0].dimensions.x / 2
#        Place Objects
        for indx, i in enumerate(selected_objects):
            self.placeObject(offset, i)
            offset += self.getObjectDimension(i) + spacing
        
        return {"FINISHED"}
    
    def get_selected(self, blenderContext):
        return blenderContext.selected_objects
    
    def getObjectDimension(self, object):
        return object.dimensions.x
        
    def getTotalLength(self, objects):
        length = 0
        for i in objects:
            length += i.dimensions.x
        return length
        
    def placeObject(self, offset, object):
        object.location = (0, offset, 0)

class ORIENT_TO_FRONT_OPERATOR(Operator):
    bl_idname = "object.orient_all"
    bl_label = "OrientAll"
    bl_description = "Orient all objects to face forward."

    @classmethod
    def poll(self, context):
      
        return {"FINISHED"}
    def execute(self, context):
        for i in context.selected_objects:
            i.rotation_euler = Euler((0.0, 0.0, 0.0), 'XYZ')
        
        return {"FINISHED"}

class LineupPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Line Up"
    bl_category = "LineUp"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Line Up Objects")
        row = layout.row()
        row.operator(LINE_UP_OPERATOR.bl_idname, text="Line Up Selected")
        row = layout.row()
        row.label(text="Reorient Objects")
        row = layout.row()
        row.operator(ORIENT_TO_FRONT_OPERATOR.bl_idname, text="Reorient Selected")


toRegister = [
    LineupPanel,
    LINE_UP_OPERATOR,
    ORIENT_TO_FRONT_OPERATOR
]
def register():
    for i in toRegister:
        bpy.utils.register_class(i)
def unregister():
    for i in toRegister:
        bpy.utils.unregister_class(i)
    
if __name__ == "__main__":
    register()