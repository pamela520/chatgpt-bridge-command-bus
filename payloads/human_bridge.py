import bpy, math
from mathutils import Vector
OUT_BLEND=r"C:\Users\digih\Documents\ChatGPTBridgeV2\comparison\human_bridge.blend"
OUT_PNG=r"C:\Users\digih\Documents\ChatGPTBridgeV2\comparison\human_bridge.png"
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(n,c): m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);return m
SK=mat('skin',(.50,.29,.19)); SKH=mat('skin_hi',(.60,.36,.24)); HR=mat('hair',(.022,.016,.011)); TS=mat('shirt',(.11,.14,.18)); PN=mat('pants',(.05,.06,.075)); SH=mat('shoes',(.022,.024,.027)); WH=mat('eyes',(.88,.84,.78)); IR=mat('iris',(.11,.06,.028)); LP=mat('lips',(.31,.095,.075)); GD=mat('ground',(.17,.18,.19))
def smooth(o,s=1):
 for p in o.data.polygons:p.use_smooth=True
 if s:
  m=o.modifiers.new('subd','SUBSURF');m.levels=s;m.render_levels=s
 return o
def sph(n,l,sc,ma,s=1,seg=40,ring=24):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=ring,location=l);o=bpy.context.object;o.name=n;o.scale=sc;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma);return smooth(o,s)
def seg(n,a,b,r1,r2,ma):
 a,b=Vector(a),Vector(b);v=b-a;L=v.length;bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=r1,radius2=r2,depth=L,location=(a+b)/2);o=bpy.context.object;o.name=n;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(ma);q=o.modifiers.new('bevel','BEVEL');q.width=.009;q.segments=2;return smooth(o,1)
def box(n,l,sc,ma,b=.025):
 bpy.ops.mesh.primitive_cube_add(location=l);o=bpy.context.object;o.name=n;o.scale=sc;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma);q=o.modifiers.new('bev','BEVEL');q.width=b;q.segments=3;return smooth(o,1)
def loft(n,levels,ma,N=40):
 vs=[];fs=[]
 for z,rx,ry,cx,cy in levels:
  for i in range(N):
   a=2*math.pi*i/N;vs.append((cx+rx*math.cos(a),cy+ry*math.sin(a),z))
 for j in range(len(levels)-1):
  for i in range(N):
   a=j*N+i;b=j*N+(i+1)%N;c=(j+1)*N+(i+1)%N;d=(j+1)*N+i;fs.append((a,b,c,d))
 fs.append(tuple(range(N-1,-1,-1)));s=(len(levels)-1)*N;fs.append(tuple(s+i for i in range(N)))
 me=bpy.data.meshes.new(n+'Mesh');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);o.data.materials.append(ma);return smooth(o,2)
box('shoeL',(-.118,-.045,.072),(.105,.20,.066),SH);box('shoeR',(.118,-.045,.072),(.105,.20,.066),SH)
for sx,l in [(-1,'L'),(1,'R')]:
 seg('shin'+l,(sx*.118,0,.15),(sx*.118,0,.59),.071,.089,PN);sph('knee'+l,(sx*.118,0,.62),(.094,.088,.088),PN);seg('thigh'+l,(sx*.118,0,.65),(sx*.128,0,1.01),.10,.136,PN)
loft('pelvis',[(.90,.27,.16,0,0),(.98,.268,.172,0,0),(1.08,.235,.165,0,0),(1.16,.218,.15,0,0)],PN)
loft('torso',[(1.08,.205,.145,0,0),(1.19,.236,.165,0,-.004),(1.31,.272,.18,0,-.008),(1.44,.305,.198,0,-.012),(1.57,.298,.19,0,-.008)],TS)
seg('neck',(0,0,1.56),(0,0,1.685),.102,.094,SK)
sph('head',(0,-.006,1.80),(.147,.119,.18),SK,2,48,30);sph('jaw',(0,-.015,1.71),(.119,.106,.10),SK,1);sph('cheekL',(-.075,-.092,1.76),(.055,.03,.052),SKH,1);sph('cheekR',(.075,-.092,1.76),(.055,.03,.052),SKH,1)
sph('earL',(-.151,0,1.79),(.024,.019,.046),SKH);sph('earR',(.151,0,1.79),(.024,.019,.046),SKH);sph('hairTop',(0,.01,1.898),(.15,.121,.087),HR);box('hairBack',(0,.092,1.83),(.132,.024,.086),HR)
for sx,l in [(-1,'L'),(1,'R')]:
 x=sx*.053;sph('eye'+l,(x,-.114,1.817),(.028,.012,.017),WH);sph('iris'+l,(x,-.126,1.817),(.0105,.005,.0105),IR);box('brow'+l,(x,-.13,1.855),(.035,.006,.0065),HR,.006)
sph('noseBridge',(0,-.123,1.80),(.024,.032,.052),SKH);sph('noseTip',(0,-.153,1.767),(.032,.025,.027),SKH);box('mouth',(0,-.118,1.716),(.050,.006,.006),LP,.006);sph('chin',(0,-.095,1.676),(.059,.035,.033),SKH)
for sx,l in [(-1,'L'),(1,'R')]:
 sph('shoulder'+l,(sx*.323,0,1.50),(.105,.116,.105),TS);seg('upper'+l,(sx*.323,0,1.48),(sx*.375,-.014,1.20),.082,.067,TS);sph('elbow'+l,(sx*.375,-.014,1.20),(.068,.064,.07),SK)
 seg('fore'+l,(sx*.375,-.014,1.20),(sx*.356,-.035,.94),.065,.05,SK);sph('wrist'+l,(sx*.356,-.035,.94),(.05,.043,.043),SK);sph('hand'+l,(sx*.356,-.048,.855),(.060,.035,.086),SK)
 seg('thumb'+l,(sx*.391,-.05,.875),(sx*.408,-.07,.826),.017,.012,SK)
 for j,dx in enumerate([-.026,-.009,.009,.026]): seg('finger'+l+str(j),(sx*(.356+abs(dx)*.20),-.064+abs(dx)*.15,.83),(sx*(.356+abs(dx)*.20),-.068,.785),.0115,.009,SK)
 seg('sleeve'+l,(sx*.272,0,1.51),(sx*.337,0,1.37),.105,.09,TS)
bpy.ops.mesh.primitive_torus_add(major_radius=.104,minor_radius=.012,major_segments=40,minor_segments=12,location=(0,-.01,1.575));bpy.context.object.data.materials.append(TS)
box('ground',(0,0,-.035),(2.25,2.25,.035),GD)
bpy.ops.object.camera_add(location=(2.72,-4.45,2.22));cam=bpy.context.object;bpy.context.scene.camera=cam;cam.data.lens=72;cam.rotation_euler=(Vector((0,0,1.02))-cam.location).to_track_quat('-Z','Y').to_euler()
sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='STUDIO';sc.display.shading.studio_light='paint.sl';sc.display.shading.color_type='MATERIAL';sc.display.shading.show_shadows=True;sc.display.shading.show_cavity=True;sc.display.shading.cavity_type='WORLD';sc.display.shading.curvature_ridge_factor=1.2;sc.display.shading.curvature_valley_factor=.8;sc.render.resolution_x=640;sc.render.resolution_y=900;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.world.color=(.035,.038,.045);sc.render.filepath=OUT_PNG
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND);bpy.ops.render.render(write_still=True);print('HUMAN_BRIDGE_DONE')
