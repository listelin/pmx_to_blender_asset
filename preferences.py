# -*- coding: utf-8 -*-

import bpy
from bpy.props import StringProperty

class PmxAssetizePreferences(bpy.types.AddonPreferences):
    bl_idname = __package__


    pmx_folder: StringProperty(
        name='PMX Folder',
        description='アセット化対象のPMXフォルダ',
        default='',
    )

    pmx_blasset_folder: StringProperty(
        name='Asset Folder',
        description='アセットフォルダ',
        default='',
    )

    def draw(self, _context):
        layout: bpy.types.UILayout = self.layout  # pylint: disable=no-member

        col = layout.box().column()
        col.prop(self, 'pmx_blasset_folder')

        col = layout.box().column()
        col.prop(self, 'pmx_folder')