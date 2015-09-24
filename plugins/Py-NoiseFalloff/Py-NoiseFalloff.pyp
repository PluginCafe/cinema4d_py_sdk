"""
Noise Falloff
Copyright: MAXON Computer GmbH
Written for Cinema 4D R14.014

Modified Date: 27/08/2012
"""


import c4d

from c4d import gui, plugins, utils

# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1028347

class NoiseFalloff(plugins.FalloffData):
    """Noise Falloff"""
    
    HANDLECOUNT = 6
    FBM_TYPES = (c4d.NOISE_ZADA, c4d.NOISE_DISPL_VORONOI, c4d.NOISE_OBER, c4d.NOISE_FBM, c4d.NOISE_BUYA)
    
    noise = utils.noise.C4DNoise()
    type = c4d.NOISE_BOX_NOISE
    octaves = 4.0
    absolute = False
    sampling = True
    sampleRad = 0.25
    detailAtt = 0.25
    repeat = 0
    maxoctave = 21
    lacunarity = 2.1
    h = 0.5
    
    dirty = 0
    
    @staticmethod
    def PointInBox(p, data):
        res = True
        
        point = [p.x, p.y, p.z]
        
        size = data.size * data.nodemat * data.scale
        size -= data.nodemat.off
        size = [size.x, size.y, size.z]
        
        offset = [data.offset.x, data.offset.y, data.offset.z]
        
        pos = c4d.Vector() * data.nodemat
        pos = [pos.x, pos.y, pos.z]
        
        for i in xrange(3):
            res = point[i] < pos[i]+offset[i]+size[i] and point[i] > pos[i]+offset[i]-size[i]
            if not res: break
        
        return res
    
    @staticmethod
    def FillHandle(info, dir, pos):
    
        if dir==c4d.FALLOFF_SHAPE_AXIS_XP:
            info.position = pos
            info.direction = c4d.Vector(1.0, 0.0, 0.0)
        elif dir==c4d.FALLOFF_SHAPE_AXIS_XN:
            info.position = pos
            info.direction = c4d.Vector(-1.0, 0.0, 0.0)
        elif dir==c4d.FALLOFF_SHAPE_AXIS_YP:
            info.position = pos
            info.direction = c4d.Vector(0.0, 1.0, 0.0)
        elif dir==c4d.FALLOFF_SHAPE_AXIS_YN:
            info.position = pos
            info.direction = c4d.Vector(0.0, -1.0, 0.0)
        elif dir==c4d.FALLOFF_SHAPE_AXIS_ZP:
            info.position = pos
            info.direction = c4d.Vector(0.0, 0.0, 1.0)
        elif dir==c4d.FALLOFF_SHAPE_AXIS_ZN:
            info.position = pos
            info.direction = c4d.Vector(0.0, 0.0, -1.0)
        
        info.type = c4d.HANDLECONSTRAINTTYPE_LINEAR
    
    @staticmethod
    def DrawHandleLines(bd, size, i):
    
        bd.SetPen(c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT))
        
        if i==0:
            p1 = c4d.Vector(0, -size.y, -size.z)
            p2 = c4d.Vector(0, -size.y, size.z)
            p3 = c4d.Vector(0, size.y, size.z)
            p4 = c4d.Vector(0, size.y, -size.z)
        elif i==1:
            p1 = c4d.Vector(-size.x, 0, -size.z)
            p2 = c4d.Vector(-size.x, 0, size.z)
            p3 = c4d.Vector(size.x, 0, size.z)
            p4 = c4d.Vector(size.x, 0, -size.z)
        elif i==2:
            p1 = c4d.Vector(-size.x, -size.y, 0)
            p2 = c4d.Vector(-size.x, size.y, 0)
            p3 = c4d.Vector(size.x, size.y, 0)
            p4 = c4d.Vector(size.x, -size.y, 0)
        
        bd.DrawLine(p1, p2, 0)
        bd.DrawLine(p2, p3, 0)
        bd.DrawLine(p3, p4, 0)
        bd.DrawLine(p4, p1, 0)
    
    def Init(self, falldata, bc):
        if bc is None: return False
        
        if bc.GetData(c4d.PYNOISEFALLOFF_SEED) is None:
            bc.SetLong(c4d.PYNOISEFALLOFF_SEED, 1234567)
        
        if bc.GetData(c4d.PYNOISEFALLOFF_TYPE) is None:
            bc.SetLong(c4d.PYNOISEFALLOFF_TYPE, c4d.NOISE_BOX_NOISE)
        
        if bc.GetData(c4d.PYNOISEFALLOFF_SAMPRAD) is None:
            bc.SetReal(c4d.PYNOISEFALLOFF_SAMPRAD, 0.25)
        
        if bc.GetData(c4d.PYNOISEFALLOFF_DETATT) is None:
            bc.SetReal(c4d.PYNOISEFALLOFF_DETATT, 0.25)
        
        if bc.GetData(c4d.PYNOISEFALLOFF_OCTAVES) is None:
            bc.SetReal(c4d.PYNOISEFALLOFF_OCTAVES, 4.0)
        
        if bc.GetData(c4d.PYNOISEFALLOFF_ABSOLUTE) is None:
            bc.SetBool(c4d.PYNOISEFALLOFF_ABSOLUTE, False)
        
        if bc.GetData(c4d.PYNOISEFALLOFF_MAXOCTAVE) is None:
            bc.SetLong(c4d.PYNOISEFALLOFF_MAXOCTAVE, 21)
        
        if bc.GetData(c4d.PYNOISEFALLOFF_LACUNARITY) is None:
            bc.SetReal(c4d.PYNOISEFALLOFF_LACUNARITY, 2.1)
        
        if bc.GetData(c4d.PYNOISEFALLOFF_H) is None:
            bc.SetReal(c4d.PYNOISEFALLOFF_H, 0.5)
        
        return True
    
    def InitFalloff(self, bc, falldata):
        if bc is None: return False
        
        dirty = bc.GetDirty()
        if self.dirty < dirty:
            
            self.seed = bc.GetLong(c4d.PYNOISEFALLOFF_SEED)
            self.type = bc.GetLong(c4d.PYNOISEFALLOFF_TYPE)
            self.octaves = bc.GetReal(c4d.PYNOISEFALLOFF_OCTAVES)
            self.absolute = bc.GetBool(c4d.PYNOISEFALLOFF_ABSOLUTE)
            self.sampling = bc.GetLong(c4d.PYNOISEFALLOFF_SAMPLING) is 0
            self.sampleRad = bc.GetReal(c4d.PYNOISEFALLOFF_SAMPRAD)
            self.detailAtt = bc.GetReal(c4d.PYNOISEFALLOFF_DETATT)
            self.repeat = bc.GetLong(c4d.PYNOISEFALLOFF_REPEAT)
            
            self.maxoctave = bc.GetLong(c4d.PYNOISEFALLOFF_MAXOCTAVE)
            self.lacunarity = bc.GetReal(c4d.PYNOISEFALLOFF_LACUNARITY)
            self.h = bc.GetLong(c4d.PYNOISEFALLOFF_H)
            
            self.noise = utils.noise.C4DNoise(seed=self.seed)
            if self.type in self.FBM_TYPES:
                self.noise.InitFbm(self.maxoctave, self.lacunarity, self.h)
            
            self.dirty = dirty
        
        return True
    
    def FreeFalloff(self, falldata):
        pass
    
    def Sample(self, p, data):
        
        if NoiseFalloff.PointInBox(data.mat * p, data):
            return self.noise.Noise(self.type, self.sampling, data.mat * p, 0.0, self.octaves, self.absolute, self.sampleRad, self.detailAtt, self.repeat)
        else:
            return 1.0
    
    def GetHandle(self, bc, i, info, data):
        if bc is None: return
        
        size = (bc.GetVector(c4d.FALLOFF_SIZE) * bc.GetReal(c4d.FALLOFF_SCALE))
        offset = bc.GetVector(c4d.FALLOFF_SHAPE_OFFSET)
        if i==0:
            NoiseFalloff.FillHandle(info, c4d.FALLOFF_SHAPE_AXIS_XP, c4d.Vector(size.x+offset.x, offset.y, offset.z))
        elif i==1:
            NoiseFalloff.FillHandle(info, c4d.FALLOFF_SHAPE_AXIS_XN, c4d.Vector(-size.x+offset.x, offset.y, offset.z))
        elif i==2:
            NoiseFalloff.FillHandle(info, c4d.FALLOFF_SHAPE_AXIS_YP, c4d.Vector(offset.x, size.y+offset.y, offset.z))
        elif i==3:
            NoiseFalloff.FillHandle(info, c4d.FALLOFF_SHAPE_AXIS_YN, c4d.Vector(offset.x, -size.y+offset.y, offset.z))
        elif i==4:
            NoiseFalloff.FillHandle(info, c4d.FALLOFF_SHAPE_AXIS_ZP, c4d.Vector(offset.x, offset.y, size.z+offset.z))
        elif i==5:
            NoiseFalloff.FillHandle(info, c4d.FALLOFF_SHAPE_AXIS_ZN, c4d.Vector(offset.x, offset.y, -size.z+offset.z))
    
    def SetHandle(self, bc, i, p, data):
        if bc is None: return False
        
        size = bc.GetVector(c4d.FALLOFF_SIZE)
        
        if i==0 or i ==1:
            size = c4d.Vector(abs(p.x), size.y, size.z)
        elif i==2 or i ==3:
            size = c4d.Vector(size.x, abs(p.y), size.z)
        elif i==4 or i ==5:
            size = c4d.Vector(size.x, size.y, abs(p.z))
        
        bc.SetVector(c4d.FALLOFF_SIZE, size)
    
    def GetHandleCount(self, bc, data):
        return self.HANDLECOUNT

    def Draw(self, data, drawpass, bd, bh):

        if drawpass==c4d.DRAWPASS_HIGHLIGHTS:
            return True
        
        size = data.size * data.scale
        mat = c4d.Matrix(data.nodemat.off+data.offset, data.nodemat.v1, data.nodemat.v2, data.nodemat.v3)
        
        bd.SetMatrix_Matrix(None, mat)
        
        box = c4d.Matrix()
        box.v1 = box.v1 * size.x
        box.v2 = box.v2 * size.y
        box.v3 = box.v3 * size.z
        bd.DrawBox(box, 1.0, c4d.GetViewColor(c4d.VIEWCOLOR_ACTIVEPOINT), True)
        
        NoiseFalloff.DrawHandleLines(bd, size, 0)
        NoiseFalloff.DrawHandleLines(bd, size, 1)
        NoiseFalloff.DrawHandleLines(bd, size, 2)
        
        return True
    
    def GetDVisible(self, id, bc, desc_bc):
        
        if id[0].id==c4d.PYNOISEFALLOFF_OCTAVES:
            return self.noise.HasOctaves(bc.GetLong(c4d.PYNOISEFALLOFF_TYPE))
        elif id[0].id==c4d.PYNOISEFALLOFF_ABSOLUTE:
            return self.noise.HasAbsolute(bc.GetLong(c4d.PYNOISEFALLOFF_TYPE))
        elif id[0].id==c4d.PYNOISEFALLOFF_FBMSETTINGS:
            return bc.GetLong(c4d.PYNOISEFALLOFF_TYPE) in self.FBM_TYPES
        else:
            return True


if __name__ == "__main__":
    plugins.RegisterFalloffPlugin(id=PLUGIN_ID, str="Py-NoiseFalloff",
                                  info=0, g=NoiseFalloff,
                                  description="Ofalloff_pynoise")
