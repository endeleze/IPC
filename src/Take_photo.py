import numpy as np
import os
import re
import glob
import bpy
import math

root='/home/endeleze/IPC/IPC/output/alien_'
Out_path='/home/endeleze/IPC/Output/Alien1'
camera_loc=1324
camera_y=1323
camera_x=8822
if not os.path.exists(Out_path):
    os.makedirs(Out_path)
num=len(glob.glob(root+'/status*'))

q=np.empty((num,3))
r=np.empty((num,3))
s=np.empty((num,3))
for i in range(num):
    file=open(root+'/status%d'%i)
    for l,line in enumerate(file):
        if l+1==camera_loc:
            match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
            final_list = [float(x) for x in re.findall(match_number, line)]
            while len(final_list)>3:
                final_list.remove(0.0)
            q[i,0]=final_list[0]
            q[i, 1] = -final_list[2]
            q[i, 2] = final_list[1]
        elif l+1==camera_x:
            match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
            final_list = [float(x) for x in re.findall(match_number, line)]
            while len(final_list)>3:
                final_list.remove(0.0)
            r[i, 0] = final_list[0]
            r[i, 1] = -final_list[2]
            r[i, 2] = final_list[1]
        elif l+1==camera_y:
            match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
            final_list = [float(x) for x in re.findall(match_number, line)]
            while len(final_list)>3:
                final_list.remove(0.0)
            s[i, 0] = final_list[0]
            s[i, 1] = -final_list[2]
            s[i, 2] = final_list[1]
    file.close()
for i in range(num):
    for o in bpy.context.scene.objects:
        o.select_set(True)
    bpy.ops.object.delete()
    qq=q[i,:]
    rr=r[i,:]
    ss=s[i,:]
    t=ss-qq
    n=np.cross(rr-qq,ss-qq)
    n=n/np.linalg.norm(n)
    t=t/np.linalg.norm(t)
    ss=np.cross(t,n)
    A=np.empty((3,3))
    A[:,0]=ss
    A[:,1]=t
    A[:,2]=n
    B=np.array([[-1,0,0],[0,1,0],[0,0,-1]])
    R=A@np.linalg.inv(B)
    x=math.atan2(R[2,1],R[2,2])
    y=math.atan2(-R[2,0],(R[2,1]**2+R[2,2]**2)**0.5)
    z=math.atan2(R[1,0],R[0,0])
    
    file_loc = os.path.join(root,'%d.obj'%i)
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc)
    
    a = 'Camera'
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=qq, rotation=(x,y,z))
    bpy.data.objects["Camera"].name = a
    bpy.data.objects[a].data.lens_unit='MILLIMETERS'
    bpy.data.objects[a].data.lens = 8
    bpy.context.scene.camera = bpy.context.object
    
    b='Point'
    bpy.ops.object.light_add(type='POINT', radius=3.0, align='WORLD', location=qq, rotation=(x,y,z),scale=(10,10,10))
    bpy.data.objects["Point"].name = b
    bpy.data.objects[b].data.energy = 150
        
    bpy.context.scene.render.filepath = os.path.join(Out_path,'%d.png'%i)
    bpy.ops.render.render(write_still = True)
    
