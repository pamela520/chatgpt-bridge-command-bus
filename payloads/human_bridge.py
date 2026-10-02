import bpy, math
from mathutils import Vector
BASE=r"C:\Users\digih\Documents\ChatGPTBridgeV2\comparison\makehuman_bridge_body.obj"
OB=r"C:\Users\digih\Documents\ChatGPTBridgeV2\comparison\human_bridge.blend"
OP=r"C:\Users\digih\Documents\ChatGPTBridgeV2\comparison\human_bridge.png"
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.ops.wm.obj_import(filepath=BASE); human=bpy.context.selected_objects[0]; human.name="Bridge Human"
scale=1.80/16.945; human.scale=(scale,scale,scale); human.rotation_euler=(math.radians(90),0,0)
bpy.context.view_layer.objects.active=human; bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
minz=min((human.matrix_world@Vector(c)).z for c in human.bound_box); human.location.z-=minz
bpy.context.view_layer.update(); bpy.ops.object.transform_apply(location=True,rotation=False,scale=False)
for p in human.data.polygons: p.use_smooth=True
sub=human.modifiers.new("Surface refinement","SUBSURF"); sub.levels=1; sub.render_levels=1
mat=bpy.data.materials.new("Neutral cool sculpt"); mat.use_nodes=True
bs=mat.node_tree.nodes["Principled BSDF"]; bs.inputs["Base Color"].default_value=(0.15,0.14,0.14,1); bs.inputs["Roughness"].default_value=.55
human.data.materials.append(mat)
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.72,depth=.08,location=(0,0,-.04))
ped=bpy.context.object; ped.name="Pedestal"; pm=bpy.data.materials.new("Pedestal"); pm.use_nodes=True
pbs=pm.node_tree.nodes["Principled BSDF"]; pbs.inputs["Base Color"].default_value=(.05,.055,.065,1); pbs.inputs["Roughness"].default_value=.70; ped.data.materials.append(pm)
bpy.ops.object.camera_add(location=(2.00,-3.75,1.95)); cam=bpy.context.object; cam.name="Camera"; cam.data.lens=68; bpy.context.scene.camera=cam
cam.rotation_euler=(Vector((0,0,1.00))-cam.location).to_track_quat('-Z','Y').to_euler()
for loc,energy,size,color in [((-2.4,-3.0,3.5),230,2.7,(1.0,.90,.82)),((2.4,-1.5,2.7),150,2.2,(.75,.84,1.0)),((0,2.6,3.6),260,2.7,(1.0,.96,.90))]:
 bpy.ops.object.light_add(type='AREA',location=loc); L=bpy.context.object; L.data.energy=energy; L.data.shape='DISK'; L.data.size=size; L.data.color=color; L.rotation_euler=(Vector((0,0,1.05))-L.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.light_add(type='AREA',location=(0,-.9,.3)); fill=bpy.context.object; fill.data.energy=55; fill.data.size=1.0; fill.rotation_euler=(Vector((0,0,1.0))-fill.location).to_track_quat('-Z','Y').to_euler()
S=bpy.context.scene; S.render.engine='CYCLES'; S.cycles.device='CPU'; S.cycles.samples=28; S.cycles.use_denoising=True
S.render.resolution_x=720; S.render.resolution_y=900; S.render.resolution_percentage=100; S.render.image_settings.file_format='PNG'
S.world.color=(.025,.028,.034); S.view_settings.look='AgX - Medium High Contrast'; S.view_settings.exposure=-0.5; S.render.filepath=OP
bpy.ops.wm.save_as_mainfile(filepath=OB); bpy.ops.render.render(write_still=True); print("BRIDGE_REALISTIC_DONE")
