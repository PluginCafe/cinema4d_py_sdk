#############################################################
## Cinema 4D SDK                                           ##
#############################################################
## (c) 1989-2011 MAXON Computer GmbH, all rights reserved  ##
#############################################################

import os
import math

import c4d
from c4d import plugins, bitmaps, utils

#warning Please obtain your own plugin ID from http://www.plugincafe.com
PLUGIN_ID=1027089

class PyFresnel(plugins.ShaderData):
    
    def __init__(self):
        #if a Python exception occurs during the calculation
        #of a pixel colorize this one in red for debugging purposes
        self.SetExceptionColor(c4d.Vector(1,0,0))
    
    def Sign(self, r):
        """
        Returns -1.0 if r is negative,
        1.0 if r is positive, otherwise 0.0
        """
        if r<0.0:
            return -1.0
        elif r>0.0:
            return 1.0
        return 0.0
    
    def FaceForward(self, N, I):
        return self.Sign((-I)*N) * N
    
    def Fresnel(self, I, N, etasqrt):
        cos_theta=I*N
        
        fuvA = etasqrt - ( 1.0 - ((cos_theta)*(cos_theta)) )
        fuvB = abs( fuvA )
        fu2 = ( fuvA + fuvB )  / 2.0
        fv2 = ( -fuvA + fuvB ) / 2.0
        fv2sqrt = 0.0 if fv2==0.0 else math.sqrt(abs(fv2))
        fu2sqrt = 0.0 if fu2==0.0 else math.sqrt(abs(fu2))
        
        fperp_temp = ((cos_theta + fu2sqrt)*(cos_theta+fu2sqrt)) + fv2
        if fperp_temp==0.0: return 1.0;
        fperp2 = ( ((cos_theta - fu2sqrt)*(cos_theta-fu2sqrt))+fv2 )/fperp_temp
        
        fpara_temp = ((etasqrt * cos_theta + fu2sqrt)*(etasqrt*cos_theta+fu2sqrt))+((fv2sqrt)*(fv2sqrt))
        if fpara_temp==0.0: return 1.0;
        fpara2 = (((etasqrt*cos_theta-fu2sqrt)*(etasqrt*cos_theta-fu2sqrt))+((-fv2sqrt)*(-fv2sqrt)))/fpara_temp
        
        return 0.5 * (fperp2+fpara2)
    
    def Output(self, sh, cd):
        if cd.vd: #if shader is computated in 3d space
            ior=1.6 #default IOR value
            n=self.FaceForward(~cd.vd.bumpn,~cd.vd.ray.v);
            return c4d.Vector(self.Fresnel(-(~cd.vd.ray.v), ~n, ior*ior))
        else: #if shader is computated in 2d space
            return c4d.Vector(0.0)
    
    def FreeRender(self, sh):
        #Free any resources used for the precalculated data from InitRender().
        return

def RegisterPyFresnel():
    IDS_PY_FRESNEL=10000 #string resource, must be manually defined
    return plugins.RegisterShaderPlugin(PLUGIN_ID, plugins.GeLoadString(IDS_PY_FRESNEL), 0, PyFresnel, "", 0)


if __name__=='__main__':
    RegisterPyFresnel()
