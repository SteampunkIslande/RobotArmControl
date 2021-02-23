import bpy
from math import degrees

def exportAnimationToCSV():
    sce = bpy.context.scene
    ob = bpy.context.active_object
    if ob.animation_data is not None:
        if ob.animation_data.action is not None:
            actionName = ob.animation_data.action.name
            fileName = f"{actionName}.csv" # Will name the file as the action name
            currentFrame = sce.frame_current
            file=open(fileName,'w')
            for frame in range(sce.frame_start,sce.frame_end+1):
                sce.frame_set(frame)
                base=ob.pose.bones["Base"].rotation_euler.y
                shoulder=ob.pose.bones["Shoulder"].rotation_euler.z
                elbow=ob.pose.bones["Elbow"].rotation_euler.z
                wrist=ob.pose.bones["Wrist vertical"].rotation_euler.z
                toArmRot = lambda angle:int((degrees(angle)+90)%360)
                file.write(f"{toArmRot(base)};{toArmRot(shoulder)};{toArmRot(elbow)};{toArmRot(wrist)}\n")
            file.close()
            sce.frame_set(currentFrame)

if __name__ == "__main__":
    exportAnimationToCSV()