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
    "name" : "Line Up",
    "author" : "neuralworm",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


# Props
class OBJECT_SPREAD_PROPERTIES(bpy.types.PropertyGroup):
    spread: bpy.props.FloatProperty(name="Object Spread", default= 1.0) 
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
    bl_options = {"REGISTER", "UNDO"}
    axis : bpy.props.EnumProperty(name = "axis", default= "x", items = {("x", "x", "Change axis to X"), ("y", "y", "Change axis to Y"), ("z", "z", "Change axis to Z")})
    spacing: bpy.props.FloatProperty(name = "Spacing", default = 1.0)
    @classmethod
    def poll(self, context):
        objects = self.get_selected(self, context)
        return objects is not None
    def execute(self, context):
        print(self.axis)
        selected_objects = self.get_selected(context)
        if not len(selected_objects):
            return {"FINISHED"}
        #  Measure length
        length = self.getTotalLength(selected_objects) + self.spacing * (len(selected_objects) - 1)
        offset = - length / 2 + selected_objects[0].dimensions.x / 2
        #  Get spread
        spread = self.getTotalSpread(selected_objects)
        #  Place Objects
        for indx, i in enumerate(selected_objects):
            self.placeObject(spread, offset, i, self.axis)
            offset += self.getObjectDimension(i) + self.spacing
        
        return {"FINISHED"}
    
    def get_selected(self, blenderContext):
        return blenderContext.selected_objects
    
    def getObjectDimension(self, object):
        return object.dimensions.x
    # get total length of all objects stacked together
    def getTotalLength(self, objects):
        length = 0
        for i in objects:
            length += i.dimensions.x
        return length
    # get average location of all selected objects
    def getTotalSpread(self, objects):
        spread = 0
        minX = 0
        maxX = 0
        minY = 0
        maxY = 0
        minZ = 0
        maxZ = 0
        for i in objects:
            if i.location.x > maxX:
                maxX = i.location.x
            if i.location.x < minX:
                minX = i.location.x
            if i.location.y > maxY:
                maxY = i.location.y
            if i.location.y < minY:
                minY = i.location.y
            if i.location.z > maxZ:
                maxZ = i.location.z
            if i.location.z < minZ:
                minZ = i.location.z
        # print("spread X - " + str(minX) + " " + str(maxX))
        # print("spread Y - " + str(minY) + " " + str(maxY))
        # print("spread Z - " + str(minZ) + " " + str(maxZ))
        avgX = (minX - maxX) / 2
        avgY = (minY - maxY) / 2
        avgZ = (minZ - maxZ) / 2
        return {
            "x": avgX,
            "y": avgY,
            "z": avgZ
        }
    # Move object to provided location
    def placeObject(self, spread, offset, object, axis):
        match axis:
            case "x":
                object.location = (offset, 0, 0)
            case "y":
                object.location = (0, offset, 0)
            case "z":
                object.location = (0, 0, offset)
                

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



# PANEL AND UI
class LINE_UP_PT_PANEL(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Line Up"
    bl_category = "LineUp"
    
    def draw(self, context):
        layout = self.layout
        # SET SPACING
        row = layout.row()
        row.label(text="Spacing")
        layout.prop(context.scene.spread_props, "spread")
        # LINE UP
        row = layout.row()
        row.label(text="Line Up Objects")
        row = layout.row()
        col = row.column()
        col.operator(LINE_UP_OPERATOR.bl_idname, icon="EVENT_X").axis = "x"
        col = row.column()
        col.operator(LINE_UP_OPERATOR.bl_idname, icon="EVENT_Y").axis = "y"
        col = row.column()
        col.operator(LINE_UP_OPERATOR.bl_idname, icon="EVENT_Z").axis = "z"
        # REORIENT
        row = layout.row()
        row.label(text="Orient To Face")
        row = layout.row()
        col = row.column()
        col.operator(ORIENT_TO_FRONT_OPERATOR.bl_idname, icon="EVENT_X")
        col = row.column()
        col.operator(ORIENT_TO_FRONT_OPERATOR.bl_idname, icon="EVENT_Y")
        col = row.column()
        col.operator(ORIENT_TO_FRONT_OPERATOR.bl_idname, icon="EVENT_Z")

class LineUpPopup(bpy.types.Panel):
    pass


toRegister = [
    LINE_UP_PT_PANEL,
    LINE_UP_OPERATOR,
    ORIENT_TO_FRONT_OPERATOR,
    OBJECT_SPREAD_PROPERTIES
]
def register():
    for i in toRegister:
        bpy.utils.register_class(i)
    bpy.types.Scene.spread_props = bpy.props.PointerProperty(type = OBJECT_SPREAD_PROPERTIES)
def unregister():
    for i in toRegister:
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.spread_props
    
    
if __name__ == "__main__":
    register()