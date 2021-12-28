# -*- coding: utf-8 -*-
import bpy
import os
import re
from pathlib import Path

from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

import mmd_tools.core.model as mmd_model

from bpy.props import StringProperty

class PmxAssetize(Operator):
    bl_idname = 'pmx_assetize.assetize'
    bl_label = 'PMX Assetize'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        props = context.scene.PmxAssetizeProp
        pmx_file = os.path.basename(props.source_pmx)   # D:\\pmx\\miku\\tumi\\3.0\\miku.pmx -> miku.pmx
        pmx_dir = os.path.dirname(props.source_pmx)     # -> D:\\pmx\\miku\\tumi\\3.0
        asset_name = os.path.splitext(pmx_file)[0]      # -> miku
        asset_file = props.asset_folder + asset_name + ".blend" # -> D:\\asset\\miku.blend

        if props.preserve_folder_structure:
            p_dir = repr(pmx_dir)[1:-1]                 # r D:\\pmx\\miku\\tumi\\3.0
            p_top_dir = repr(props.source_pmx_folder)[1:-1] # r D:\\pmx\\
            a_top_dir = repr(props.asset_folder)[1:-1]  # r D:\\asset\\

            d = p_dir.replace(p_top_dir, a_top_dir)     # -> D:\\asset\\tumi\\3.0
            os.makedirs(d, exist_ok=True)               # mkdirs ...\\tumi\\3.0

            asset_file = d + os.sep +asset_name + ".blend"    # -> D:\\asset\tumi\\3.0\\miku.blend

        bpy.data.texts.new('PMX asset info.txt')
        bpy.data.texts['PMX asset info.txt'].write("source pmx :" + props.source_pmx +"\n")

        print("start loading pmx:" + asset_name)
        # create collection and set active
        pmx_collection = bpy.data.collections.new(asset_name)
        context.scene.collection.children.link(pmx_collection)
        layer_collection = context.view_layer.layer_collection.children[pmx_collection.name] # auto renameされる可能性がある
        context.view_layer.active_layer_collection = layer_collection

        context.scene.cursor.location = (0.0, 0.0, 0.0)
        bpy.ops.mmd_tools.import_model(filepath=props.source_pmx,
            files=[{"name": pmx_file, "name": pmx_file}],
            directory=pmx_dir,
            types={'MESH', 'ARMATURE', 'PHYSICS', 'DISPLAY', 'MORPHS'},
            scale=0.08, clean_model=True, remove_doubles=False,
            fix_IK_links=False, apply_bone_fixed_axis=False, rename_bones=True, use_underscore=False, dictionary='DISABLED', use_mipmap=True, sph_blend_factor=1, spa_blend_factor=1, log_level='DEBUG', save_log=False)

        print("end loading pmx:" + asset_name)

        root = context.active_object
        if props.auto_smooth is False:
            rig = mmd_model.Model(root)
            for mesh in rig.meshes():
                mesh.data.use_auto_smooth = False

        bpy.ops.mmd_tools.reset_object_visibility()     #アセットblendファイルを次回openした時にリセット不要にするため

        if props.auto_asemble:
            bpy.ops.mmd_tools.assemble_all()

        print("adding colleciton instance:" + pmx_collection.name)
        bpy.ops.object.collection_instance_add(collection=pmx_collection.name)
        print(" colleciton instance:" + pmx_collection.name + " added")

        # 名前
        #   (1) pmxファイル名(.pmx)　→　コレクション名＝blendファイル名(.blend)
        #   (2) mmd_root名(Empty)
        #   (3) (1)をインスタンス化した名前(Empty)＝アセット名
        #   → (1)と(2)が同じ場合Empty名が重複し、.001にリネームされアセットの表示上見栄えが悪いため、001を削除し、末尾"."にしている
        if context.active_object.name.endswith('.001'):
            context.active_object.name = re.sub('001$','',context.active_object.name)

        asset_instance_name = context.active_object.name

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[asset_instance_name].select_set(True)

        bpy.ops.asset.mark({'id': bpy.data.objects[asset_instance_name]})
        print("mark asset donw:" + asset_instance_name)

        print("start making thumbnail")
        PmxUpdateAssetThumbnail.execute(self,context, delete_temp_auto_camera=False)
        print("thumbnail done")

#        bpy.ops.asset.tag_add("MMD")   # -> error TODO: タグを付けたい

        current_render_engine = context.scene.render.engine
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'   #ファイルプレビュー用に保存前後はEeveeにする
        bpy.context.space_data.shading.type = 'RENDERED'

        # アセットblendファイルをオープンした場合のために可視状態を設定する
        context.object.hide_render = True   
        context.object.hide_viewport = True

        try:
            bpy.ops.file.pack_all()

        except Exception as e:
            bpy.data.texts['PMX asset info.txt'].write('ERROR:' + str(e))

            if props.ignore_file_pack_error:
                print("file pack error:" + asset_instance_name)
            else:
                raise e

        try:
            bpy.ops.wm.save_as_mainfile(filepath=asset_file, copy=True)

        except Exception as e:          #TODO: file pack以外のエラーをスルーしている
            bpy.data.texts['PMX asset info.txt'].write('ERROR:' + str(e))

            if props.ignore_file_pack_error:
                print("Error:" + asset_instance_name)
            else:
                raise e

        if props.auto_camera:       # ファイル保存が終わってからカメラ削除
            PmxUpdateAssetThumbnail.temp_camera_delete(self,context)

        context.object.hide_viewport = False
        bpy.data.objects[asset_instance_name].select_set(True)
        bpy.ops.asset.clear(set_fake_user=False)         # オブジェクトを削除してもアセットは残るので明示的にクリア要
        bpy.ops.object.delete()

        # TODO:コレクションの階層削除だが非常に遅いので改善したい
        print("start deleting collection")

        for obj in pmx_collection.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
    
        bpy.data.collections.remove(pmx_collection)

        for t in bpy.data.texts:
            bpy.data.texts.remove(t, do_unlink=True)

        print("collection deleted")

        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        context.scene.render.engine = current_render_engine     # 撮影時にcyclesにしたい場合がある可能性があるため戻す


        return {'FINISHED'}

    @classmethod
    def poll(cls,context):
        return True

class PmxUpdateAssetThumbnail(Operator):
    bl_idname = 'pmx_assetize.update_thumbnail'
    bl_label = 'PMX update Asset thumbnail'
    bl_options = {'REGISTER', 'UNDO'}

    def temp_camera_add(self,context):
        props = context.scene.PmxAssetizeProp

        self.current_x = context.scene.render.resolution_x
        self.current_y = context.scene.render.resolution_y
        self.current_asp_x = context.scene.render.pixel_aspect_x
        self.current_asp_y = context.scene.render.pixel_aspect_y
        self.current_camera = context.scene.camera
        self.current_orientation = context.scene.transform_orientation_slots[0].type

        context.scene.render.resolution_y = 512
        context.scene.render.resolution_x = 512
        context.scene.render.pixel_aspect_x = 1
        context.scene.render.pixel_aspect_y = 1

        bpy.ops.object.camera_add(enter_editmode=False,
            align='VIEW',
            location=props.camera_location,
            rotation=props.camera_rotation,
            scale=(1, 1, 1))
        context.active_object.name = "temp_cam_for_thumbnail"
        context.scene.camera = bpy.data.objects[context.active_object.name]


    def temp_camera_delete(self,context):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects["temp_cam_for_thumbnail"].select_set(True)
        bpy.ops.object.delete()
        
        context.scene.render.resolution_x = self.current_x
        context.scene.render.resolution_y = self.current_y
        context.scene.camera = self.current_camera
        context.scene.render.pixel_aspect_x = self.current_asp_x
        context.scene.render.pixel_aspect_y = self.current_asp_y            
        context.scene.transform_orientation_slots[0].type = self.current_orientation

    def set_auto_angle(self, context, target_asset):

        for o in target_asset.instance_collection.all_objects:
            if '_mesh' in o.name:
                mmd_mesh_object = o
                break

        for o in target_asset.instance_collection.all_objects:
            if '_arm' in o.name:
                mmd_arm_object = o

        # 首ボーンがあればキャラクターとしてアングル設定
        for b in mmd_arm_object.data.bones:
            if "首" in b.name:
                PmxUpdateAssetThumbnail.set_auto_angle_charactor(self, context, mmd_mesh_object, mmd_arm_object)
                return

        # 首ボーンがなければ、メッシュ全体を収めるカメラアングルに
        bpy.ops.object.select_all(action='DESELECT')
        mmd_mesh_object.select_set(True)

        bpy.ops.view3d.camera_to_view_selected()



    def set_auto_angle_charactor(self, context, mmd_mesh_object, mmd_arm_object):
    # カメラのy軸を首に合わせ、首にTrack Toする
    # メッシュの大きさに合わせてY軸を後ろに動かす　- dimension_z * 0.5 + zoom_offset

        props = context.scene.PmxAssetizeProp
        zoom_offset = props.auto_angle_zoom_offset

                
        bpy.context.view_layer.objects.active = bpy.data.objects["temp_cam_for_thumbnail"]
        
        bpy.ops.object.constraint_add(type='COPY_LOCATION')
        bpy.context.object.constraints["Copy Location"].target = mmd_arm_object
        bpy.context.object.constraints["Copy Location"].subtarget = '首'

        bpy.context.object.constraints["Copy Location"].use_y = False
        bpy.context.object.constraints["Copy Location"].use_x = False
        
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = mmd_arm_object
        bpy.context.object.constraints["Track To"].subtarget = '首'
        
        d = bpy.context.object.driver_add("location", 1)
        d.driver.type = 'SCRIPTED'
        
        var_z = d.driver.variables.new()
        var_z.name = 'dimension_z'
        var_z.type = 'SINGLE_PROP'
        z_target = var_z.targets[0]
        z_target.id = mmd_mesh_object
        z_target.data_path = 'dimensions.z'
        
        e = re.sub("_offset_", str(zoom_offset), "- dimension_z * 0.5 + _offset_")
        d.driver.expression = e

    def execute(self, context,/,*,delete_temp_auto_camera = True):

        props = context.scene.PmxAssetizeProp

        target_asset = context.active_object
        
        current_file_format = context.scene.render.image_settings.file_format
        current_render_filepath = context.scene.render.filepath
        context.scene.render.image_settings.file_format = 'PNG'

        if props.auto_camera:
            PmxUpdateAssetThumbnail.temp_camera_add(self, context)

            if props.auto_angle:
                PmxUpdateAssetThumbnail.set_auto_angle(self, context, target_asset)

        thumbnail_file_path = bpy.app.tempdir + 'temp_thumb_' + target_asset.name + '.png'
        context.scene.render.filepath = thumbnail_file_path
        bpy.ops.render.render(write_still = True)

        if props.auto_camera:
            if delete_temp_auto_camera:
                PmxUpdateAssetThumbnail.temp_camera_delete(self,context)

        # restore setting
        context.scene.render.image_settings.file_format = current_file_format
        context.scene.render.filepath = current_render_filepath

        # select target asset and set thumbnail image
        bpy.ops.object.select_all(action='DESELECT')
        context.view_layer.objects.active = target_asset
        target_asset.select_set(True)
        override = context.copy()
        override['id'] = target_asset
        bpy.ops.ed.lib_id_load_custom_preview(override,filepath=thumbnail_file_path)

        os.unlink(thumbnail_file_path)

        return {'FINISHED'}

    @classmethod
    def poll(cls,context):
        if context.active_object:
            if context.active_object.instance_collection:
                return True
    
        return False

class AssetizePmx(Operator, ImportHelper):
    bl_idname = "pmx_assetize.pmx_assetize"
    bl_label = "pmx assetize"

    filter_glob: StringProperty(
        default='*.pmx',
        options={'HIDDEN'} )

    def execute(self, context):
        fdir = self.properties.filepath
        context.scene.PmxAssetizeProp.source_pmx = fdir

        PmxAssetize.execute(self, context)
        return{'FINISHED'}

    @classmethod
    def poll(cls,context):
        if context.scene.PmxAssetizeProp.asset_folder == '':
            return False
        
        return True

class AssetFolderlector(Operator, ImportHelper):
    bl_idname = "pmx_assetize.asset_folder_selector"
    bl_label = "pmx folder"

    def execute(self, context):
        fdir = self.properties.filepath
        context.scene.PmxAssetizeProp.asset_folder = fdir
        return{'FINISHED'}

class PMXFolderlector(Operator, ImportHelper):
    bl_idname = "pmx_assetize.pmx_folder_selector"
    bl_label = "pmx folder"

    def execute(self, context):
        fdir = self.properties.filepath
        context.scene.PmxAssetizeProp.source_pmx_folder = fdir

        return{'FINISHED'}

class AssetizePmxBatch(Operator):
    bl_idname = "pmx_assetize.pmx_assetize_batch"
    bl_label = "pmx assetize batch"

    def execute(self, context):
        pmx_folder = context.scene.PmxAssetizeProp.source_pmx_folder

        for pmx_file_path in Path(pmx_folder).rglob('*.pmx'):
            context.scene.PmxAssetizeProp.source_pmx = str(pmx_file_path)
            PmxAssetize.execute(self,context)

        return{'FINISHED'}

    @classmethod
    def poll(cls,context):
        if context.scene.PmxAssetizeProp.source_pmx_folder == '':
            return False
        
        return True
