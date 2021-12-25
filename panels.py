# -*- coding: utf-8 -*-

from .operators import (
    AssetizePmx, PmxUpdateAssetThumbnail,
    PMXFolderlector, AssetFolderlector, AssetizePmxBatch
)
from bpy.types import Panel

class PmxAssetizePanel(Panel):
    bl_idname = 'PMX_ASSETIZE_PT_Panel'
    bl_label = 'PMX Assetize'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MMD'
    bl_context = ''

    def draw(self, context):

        preferences = context.preferences.addons[__package__].preferences

        layout = self.layout
        row = layout.row(align=True)

        props = context.scene.PmxAssetizeProp

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
        column_auto_angle = layout.row(align=True)
        column_auto_angle.prop(props,'auto_angle', text='Auto angle')
        column_auto_angle.prop(props,'auto_angle_zoom_offset', text='zoom offset')

        column_auto_angle.enabled = props.auto_camera
        column_auto_angle.active = props.auto_angle

        row_camloc = layout.row(align=True)
        row_camloc.prop(props,'camera_location', text='autocam loc')
        row_camrot = layout.row(align=True)
        row_camrot.prop(props,'camera_rotation', text='autocam rot')

        row_camloc.enabled = props.auto_camera and not props.auto_angle
        row_camrot.enabled = props.auto_camera and not props.auto_angle



