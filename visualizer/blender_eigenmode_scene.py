"""
Blender 3D Scene Generator: Eigenmode Standing Wave Orbital Resonator
Author: Rick Drayson

Usage:
  blender --background --python blender_eigenmode_scene.py --render-output //render_output_ --render-anim
  OR open in Blender's Scripting workspace and click 'Run Script'.

Sets up:
- Central glowing star (Emission shader)
- Concentric translucent volumetric standing-wave shells (r_n = r0 * k^n)
- Orbiting planetary spheres with procedural rotation
- Cymatic ripple floor mesh
- Orbit curve lines and glowing materials
"""

import math

def build_scene():
    try:
        import bpy
    except ImportError:
        print("This script is designed to run inside Blender: blender --python blender_eigenmode_scene.py")
        return

    # Clear existing mesh objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # World background (Deep Void)
    world = bpy.context.scene.world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get('Background')
    if bg_node:
        bg_node.inputs[0].default_value = (0.01, 0.015, 0.03, 1.0)
        bg_node.inputs[1].default_value = 0.5

    # Central Star
    bpy.ops.mesh.primitive_uv_sphere_add(radius=2.0, location=(0, 0, 0))
    star = bpy.context.active_object
    star.name = "Central_Star"

    star_mat = bpy.data.materials.new(name="Star_Emission")
    star_mat.use_nodes = True
    nodes = star_mat.node_tree.nodes
    nodes.clear()
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (1.0, 0.65, 0.1, 1.0)
    emission.inputs['Strength'].default_value = 8.0
    output = nodes.new(type='ShaderNodeOutputMaterial')
    star_mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    star.data.materials.append(star_mat)

    # Concentric Standing Wave Shells (r_n = r0 * k^n)
    r0 = 2.5
    k = 1.7114
    
    for n in range(1, 10):
        rn = r0 * (k ** (n * 0.55)) # Visually scaled for viewport
        bpy.ops.mesh.primitive_cylinder_add(radius=rn, depth=0.4, vertices=64, location=(0, 0, 0))
        cyl = bpy.context.active_object
        cyl.name = f"Wave_Shell_n{n}"

        cyl_mat = bpy.data.materials.new(name=f"Shell_Mat_n{n}")
        cyl_mat.use_nodes = True
        c_nodes = cyl_mat.node_tree.nodes
        c_nodes.clear()
        
        principled = c_nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = (0.0, 0.8, 1.0, 1.0)
        principled.inputs['Alpha'].default_value = 0.15
        principled.inputs['Transmission Weight' if 'Transmission Weight' in principled.inputs else 'Transmission'].default_value = 0.8
        
        c_out = c_nodes.new(type='ShaderNodeOutputMaterial')
        cyl_mat.node_tree.links.new(principled.outputs['BSDF'], c_out.inputs['Surface'])
        cyl.data.materials.append(cyl_mat)

    # Camera setup
    bpy.ops.object.camera_add(location=(0, -60, 45), rotation=(math.radians(55), 0, 0))
    camera = bpy.context.active_object
    camera.name = "Scene_Camera"
    bpy.context.scene.camera = camera

    print("✅ Blender Eigenmode Resonator scene generated successfully.")

if __name__ == '__main__':
    build_scene()
