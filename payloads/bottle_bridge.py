import bpy, math, os
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(name,color,metallic=0.0,rough=0.35,transmission=0.0,ior=1.45):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
 bs=m.node_tree.nodes.get("Principled BSDF"); bs.inputs["Base Color"].default_value=(*color,1); bs.inputs["Metallic"].default_value=metallic; bs.inputs["Roughness"].default_value=rough
 if "Transmission Weight" in bs.inputs: bs.inputs["Transmission Weight"].default_value=transmission
 elif "Transmission" in bs.inputs: bs.inputs["Transmission"].default_value=transmission
 if "IOR" in bs.inputs: bs.inputs["IOR"].default_value=ior
 return m
body_mat=mat("Tritan yellow-green",(0.42,0.72,0.015),rough=0.18,transmission=0.72,ior=1.47)
lid_mat=mat("Lime lid",(0.55,0.88,0.015),rough=0.28); handle_mat=mat("Charcoal handle",(0.035,0.04,0.045),rough=0.3)
water_mat=mat("Water",(0.16,0.45,0.32),rough=0.08,transmission=0.82,ior=1.333); label_mat=mat("Label dark",(0.12,0.13,0.12),rough=0.4); floor_mat=mat("Warm floor",(0.18,0.16,0.14),rough=0.5)
def cube(name,loc,scale,material,bevel=0.12):
 bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel: mod=o.modifiers.new("Soft molded edges","BEVEL"); mod.width=bevel; mod.segments=5
 o.data.materials.append(material); return o
body=cube("Bottle body",(0,0,2.95),(1.32,0.92,2.85),body_mat,0.28)
shoulder=cube("Shoulder",(0,0,5.63),(1.15,0.82,0.28),body_mat,0.22); neck=cube("Neck",(0,0,5.98),(0.95,0.70,0.22),body_mat,0.14); lid=cube("Lime cap",(0,0,6.28),(1.08,0.79,0.36),lid_mat,0.16)
water=cube("Water",(0,0,1.05),(1.12,0.72,0.72),water_mat,0.22)
for x in (-0.78,0.78):
 for y in (-0.925,0.925): cube("Molded rib",(x,y,3.4),(0.09,0.035,1.85),body_mat,0.04)
left=cube("Handle left",(-1.18,0,6.72),(0.16,0.20,0.62),handle_mat,0.12); left.rotation_euler[1]=math.radians(-18)
right=cube("Handle right",(1.18,0,6.72),(0.16,0.20,0.62),handle_mat,0.12); right.rotation_euler[1]=math.radians(18)
grip=cube("Handle grip",(0,0,7.18),(1.25,0.20,0.17),handle_mat,0.13)
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, location=(-0.55,0,6.67), scale=(0.48,0.52,0.34)); spout=bpy.context.object; spout.name="Spout cover"; spout.data.materials.append(handle_mat)
def text_obj(txt,loc,size,extrude=0.012):
 bpy.ops.object.text_add(location=loc, rotation=(math.radians(90),0,0)); t=bpy.context.object; t.data.body=txt; t.data.align_x='CENTER'; t.data.size=size; t.data.extrude=extrude; t.data.materials.append(label_mat); return t
text_obj("LAVA",(0,-0.935,2.05),0.46); text_obj("TRITAN     BPA FREE     2800ml",(0,-0.94,1.55),0.17)
sticker=mat("Sticker blue",(0.02,0.35,0.72),rough=0.32); panel=cube("Sticker",(0.58,-0.945,3.05),(0.24,0.025,0.72),sticker,0.05); panel.rotation_euler[1]=math.radians(-18)
floor=cube("Floor",(0,0,-0.08),(6,6,0.10),floor_mat,0.02)
world=bpy.context.scene.world; world.use_nodes=True; bg=world.node_tree.nodes.get("Background"); bg.inputs["Color"].default_value=(0.025,0.03,0.035,1); bg.inputs["Strength"].default_value=0.35
def area(name,loc,energy,size,color):
 bpy.ops.object.light_add(type='AREA',location=loc); l=bpy.context.object; l.name=name; l.data.energy=energy; l.data.shape='DISK'; l.data.size=size; l.data.color=color; return l
key=area("Key",(-4,-5,8),1100,4.0,(1.0,0.86,0.72)); fill=area("Fill",(4,-2,5),750,3.0,(0.68,0.82,1.0)); rim=area("Rim",(2,4,7),1000,3.0,(0.75,1.0,0.78))
for l in (key,fill,rim): l.rotation_euler=(Vector((0,0,3.3))-l.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(8.5,-10.5,6.4)); cam=bpy.context.object; cam.rotation_euler=(Vector((0,0,3.45))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.lens=58
scene=bpy.context.scene; scene.camera=cam; scene.render.engine='BLENDER_EEVEE'; scene.render.resolution_x=600; scene.render.resolution_y=760; scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'; scene.view_settings.look='AgX - Medium High Contrast'
scene.render.filepath=r"C:\Users\digih\Documents\BridgeBottle\bridge_bottle.png"; blend=r"C:\Users\digih\Documents\BridgeBottle\bridge_bottle.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend); bpy.ops.render.render(write_still=True); print("BOTTLE_DONE",scene.render.filepath,blend)
