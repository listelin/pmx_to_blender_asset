# -*- coding: utf-8 -*-

import bpy
from bpy.props import StringProperty

class PmxAssetizePreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, _context):
        layout: bpy.types.UILayout = self.layout  # pylint: disable=no-member