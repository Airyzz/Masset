import bpy

from . import utils

import json

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class MassAssetImport(Operator):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "masset.mass_import_assets"
    bl_label = "Mass Asset Import"

    filename_ext = "."
    
    filter_folder: bpy.props.BoolProperty(default=True, options={'HIDDEN'})
    test: bpy.props.BoolProperty(default=True, options={'HIDDEN'})

    directory: bpy.props.StringProperty(name="Directory", options={"HIDDEN"})
    template: bpy.props.StringProperty(name="Template Material")
    ignore_regex: bpy.props.StringProperty(name="Ignore Regex")
    mark_as_asset: bpy.props.BoolProperty(name="Mark As Asset")

    def execute(self, context):

        if not self.template in bpy.data.materials:
            self.report({"ERROR"}, "Error: No valid template material found")
            return {"CANCELLED"}

        assets = utils.find_assets(self.directory, self.ignore_regex)
        utils.import_assets(assets, self.template, self.mark_as_asset)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "template")
        row = layout.row()
        row.prop(self, "ignore_regex")
        row = layout.row()
        row.prop(self, "mark_as_asset")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


# Only needed if you want to add into a dynamic menu.
def menu_func_import(self, context):
    self.layout.operator(MassAssetImport.bl_idname, text="Mass Asset Import")

# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def register():
    bpy.utils.register_class(MassAssetImport)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(MassAssetImport)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)