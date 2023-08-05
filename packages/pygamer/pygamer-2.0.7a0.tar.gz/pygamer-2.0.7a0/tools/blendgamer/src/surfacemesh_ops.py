# ***************************************************************************
# This file is part of the GAMer software.
# Copyright (C) 2016-2018
# by Christopher Lee, Tom Bartol, John Moody, Rommie Amaro, J. Andrew McCammon,
#    and Michael Holst

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
# ***************************************************************************

import bpy
from bpy.props import (
        BoolProperty, CollectionProperty, EnumProperty,
        FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty,
        PointerProperty, StringProperty, BoolVectorProperty)

import blendgamer.pygamer as g
from blendgamer.util import *
from blendgamer.markers import *


# python imports
import os, sys
import numpy as np
import collections


class GAMER_OT_coarse_dense(bpy.types.Operator):
    bl_idname       = "gamer.coarse_dense"
    bl_label        = "Coarse Dense"
    bl_description  = "Decimate selected dense areas of the mesh"
    bl_options      = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            p = context.scene.gamer.surfmesh_improvement_properties
            gmesh = blenderToGamer(autocorrect_normals=p.autocorrect_normals)
            gmesh.coarse_dense(rate=p.dense_rate, numiter=p.dense_iter, rings=p.rings, verbose=p.verbose)
            gamerToBlender(gmesh)

            self.report({'INFO'}, "GAMer: coarse dense complete")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}


class GAMER_OT_coarse_flat(bpy.types.Operator):
    bl_idname       = "gamer.coarse_flat"
    bl_label        = "Coarse Flat"
    bl_description  = "Decimate selected flat areas of the mesh"
    bl_options      = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:

            p = context.scene.gamer.surfmesh_improvement_properties
            gmesh = blenderToGamer(autocorrect_normals=p.autocorrect_normals)
            gmesh.coarse_flat(rate=p.flat_rate, numiter=p.flat_iter, rings=p.rings, verbose=p.verbose)
            gamerToBlender(gmesh)

            self.report({'INFO'}, "GAMer: coarse flat complete")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

class GAMER_OT_smooth(bpy.types.Operator):
    bl_idname       = "gamer.smooth"
    bl_label        = "Smooth"
    bl_description  = "Smooth selected vertices of the mesh"
    bl_options      = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            p = context.scene.gamer.surfmesh_improvement_properties
            gmesh = blenderToGamer(autocorrect_normals=p.autocorrect_normals)
            gmesh.smooth(max_iter=p.smooth_iter, preserve_ridges=p.preserve_ridges, rings=p.rings, verbose=p.verbose)
            gamerToBlender(gmesh)

            self.report({'INFO'}, "GAMer: Smooth Mesh complete")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}


class GAMER_OT_normal_smooth(bpy.types.Operator):
    bl_idname       = "gamer.normal_smooth"
    bl_label        = "Normal Smooth"
    bl_description  = "Smooth facet normals of selected faces of the mesh"
    bl_options      = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            p = context.scene.gamer.surfmesh_improvement_properties
            gmesh = blenderToGamer(autocorrect_normals=p.autocorrect_normals)
            gmesh.normalSmooth(p.normSmoothAniso)
            gamerToBlender(gmesh)

            self.report({'INFO'}, "GAMer: Normal Smooth complete")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

class GAMER_OT_fill_holes(bpy.types.Operator):
    bl_idname       = "gamer.fill_holes"
    bl_label        = "Fill Holes"
    bl_description  = "Triangulate holes"
    bl_options      = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            p = context.scene.gamer.surfmesh_improvement_properties
            gmesh = blenderToGamer(autocorrect_normals=p.autocorrect_normals)
            gmesh.fillHoles()
            gamerToBlender(gmesh)

            self.report({'INFO'}, "GAMer: Fill Holes complete")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}


class SurfaceMeshImprovementProperties(bpy.types.PropertyGroup):
    dense_rate      = FloatProperty(
        name="Thresh", default=1, min=0.001, max=50.0, precision=4,
        description="Threshold for coarsening dense areas")

    dense_iter      = IntProperty(
        name="Iter", default=1, min=1, max=15,
        description="The number of coarse dense iterations to apply")

    flat_rate       = FloatProperty(
        name="Threshold", default=0.016, min=0.00001, max=0.5, precision=4,
        description="The rate for coarsening flat areas")

    flat_iter       = IntProperty(
        name="Iter", default=1, min=1, max=15,
        description="The number of coarse flat iterations to apply")

    smooth_iter     = IntProperty(
        name="Iter", default=10, min=1, max=50,
        description="The number smoothing iterations to apply")

    preserve_ridges = BoolProperty(
        name="Preserve ridges", default=False,
        description="Skip flipping of edges which lie on ridges")

    normSmoothAniso = FloatProperty(
        name="Anisotropic control", default=1.0, min=0,
        description="The degree of anisotropy in LST correction for normal smooth")

    advanced_options = BoolProperty(
        name="Advanced options", default=False,
        description="Show additional surface mesh improvement options")

    autocorrect_normals = BoolProperty(
        name="Autocorrect normals", default=True,
        description="Automatically flip normals when mesh volume is 'negative'")

    verbose         = BoolProperty(name="Verbose", default=False,
        description="Print additional information to console")

    rings           = IntProperty(
        name="LST rings", default=2, min=1, max=5,
        description="The number of neighborhood rings to consider for LST calculation")


classes = [GAMER_OT_coarse_dense,
           GAMER_OT_coarse_flat,
           GAMER_OT_smooth,
           GAMER_OT_normal_smooth,
           GAMER_OT_fill_holes,
           SurfaceMeshImprovementProperties]

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(make_annotations(cls))

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(make_annotations(cls))
