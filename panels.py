# -*- coding: utf-8 -*-

from .operators import (
    AssetizePmx, PmxUpdateAssetThumbnail,
    PMXFolderlector, AssetFolderlector, AssetizePmxBatch
)
import bpy
from bpy.types import Panel

class PmxAssetizePanel(Panel):
    bl_idname = 'PMX Assetize'
    bl_label = 'PMX Assetize'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MMD'
    bl_context = ''

    def draw(self, _context):

        preferences = bpy.context.preferences.addons[__package__].preferences

        layout = self.layout
        row = layout.row(align=True)

        props = bpy.context.scene.PmxAssetizeProp

        row.prop(props,'asset_folder', text='Asset folder')
        row.operator(AssetFolderlector.bl_idname,text='',icon='FILE_FOLDER')
        row = layout.row()

        row.prop(props,'auto_asemble', text='Assemble')
        row.prop(props,'auto_smooth', text='Auto Smooth Mesh')
        row = layout.row()
        row.operator(AssetizePmx.bl_idname,text='single PMX Assetize',icon='FILE_FOLDER')
        row = layout.row()

        row.prop(props,'source_pmx_folder', text='PMX folder')
        row.operator(PMXFolderlector.bl_idname,text='',icon='FILE_FOLDER')

        row = layout.row(align=True)
        row.operator(AssetizePmxBatch.bl_idname,text='Batch Assetize')
        
        row = layout.row(align=True)
        row.operator(PmxUpdateAssetThumbnail.bl_idname,text='Set Asset IMG')
        row.prop(props,'auto_camera', text='Auto cam')

        row_camloc = layout.row(align=True)
        row_camloc.prop(props,'camera_location', text='cam loc')
        row_camrot = layout.row(align=True)
        row_camrot.prop(props,'camera_rotation', text='cam rot')

        row_camloc.enabled = props.auto_camera
        row_camrot.enabled = props.auto_camera



