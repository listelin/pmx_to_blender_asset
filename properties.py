import bpy
from math import pi
from bpy.props import (FloatProperty, StringProperty, FloatVectorProperty,BoolProperty)

class PmxAssetizeProp(bpy.types.PropertyGroup):

    source_pmx_folder : StringProperty(default="")
    source_pmx : StringProperty(default="")
    auto_asemble: BoolProperty(default = True)
    auto_smooth: BoolProperty(default = False)
    asset_folder : StringProperty(default="")

    camera_location: FloatVectorProperty(name="Thumbnail auto camera location", default = (0, -0.75, 1.3))
    camera_rotation: FloatVectorProperty(name="Thumbnail auto camera rotation", default = (pi/2, 0.0, 0.0))
    auto_camera: BoolProperty(default = True)
    auto_angle: BoolProperty(default = True)
    auto_angle_zoom_offset: FloatProperty(default=0.0)

    @staticmethod
    def register():
        bpy.types.Scene.PmxAssetizeProp = bpy.props.PointerProperty(type=PmxAssetizeProp)  # pylint: disable=assignment-from-no-return

    @staticmethod
    def unregister():
        del bpy.types.Scene.PmxAssetizeProp
