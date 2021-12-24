import bpy
from bpy.props import (StringProperty, FloatVectorProperty,BoolProperty)

class PmxAssetizeProp(bpy.types.PropertyGroup):

    source_pmx_folder : StringProperty(default="")
    source_pmx : StringProperty(default="")
    auto_asemble: BoolProperty(default = True)
    auto_smooth: BoolProperty(default = False)
    asset_folder : StringProperty(default="")

    camera_location: FloatVectorProperty(name="Thumbnail auto camera location", default = (0, -0.75, 1.3))
    camera_rotation: FloatVectorProperty(name="Thumbnail auto camera rotation", default = (1.7, 0.0, 0.0))
    auto_camera: BoolProperty(default = True)

    @staticmethod
    def register():
        bpy.types.Scene.PmxAssetizeProp = bpy.props.PointerProperty(type=PmxAssetizeProp)  # pylint: disable=assignment-from-no-return

    @staticmethod
    def unregister():
        del bpy.types.Scene.PmxAssetizeProp
