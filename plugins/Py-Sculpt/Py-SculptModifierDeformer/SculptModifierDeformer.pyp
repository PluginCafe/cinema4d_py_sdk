import c4d, os
import random
from c4d import plugins, utils, bitmaps, gui
from c4d.modules import sculpting as sculpt

# be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1031586 
ID_SCULPT_BRUSH_PULL_MODIFIER = 1030505

class SculptModifierDeformer(plugins.ObjectData):

	brushInterface = None
	
	def Message(self, node, type, data):
		if type==c4d.MSG_MENUPREPARE:
			node.SetDeformMode(True)
		return True
	
	def Init(self, op):
		self.InitAttr(op, float, [c4d.PYSCULPTMODIFIERDEFORMER_RADIUS])
		self.InitAttr(op, float, [c4d.PYSCULPTMODIFIERDEFORMER_PRESSURE])
		self.InitAttr(op, bool, [c4d.PYSCULPTMODIFIERDEFORMER_STAMP_ACTIVE])
		self.InitAttr(op, int, [c4d.PYSCULPTMODIFIERDEFORMER_NUMSTAMPS])
		self.InitAttr(op, bool, [c4d.PYSCULPTMODIFIERDEFORMER_STAMP_USEFALLOFF])
		self.InitAttr(op, int, [c4d.PYSCULPTMODIFIERDEFORMER_SEED])
		self.InitAttr(op, float, [c4d.PYSCULPTMODIFIERDEFORMER_STAMP_ROTATION])
		
		op[c4d.PYSCULPTMODIFIERDEFORMER_RADIUS] =  20
		op[c4d.PYSCULPTMODIFIERDEFORMER_PRESSURE] = 0.2
		op[c4d.PYSCULPTMODIFIERDEFORMER_STAMP_ACTIVE] = False
		op[c4d.PYSCULPTMODIFIERDEFORMER_NUMSTAMPS] = 10
		op[c4d.PYSCULPTMODIFIERDEFORMER_STAMP_USEFALLOFF] = True
		op[c4d.PYSCULPTMODIFIERDEFORMER_SEED] = 0
		op[c4d.PYSCULPTMODIFIERDEFORMER_STAMP_ROTATION] = 0

		self.brushInterface = sculpt.SculptModifierInterface()

		return True

	def ModifyObject(self, mod, doc, op, op_mg, mod_mg, lod, flags, thread):
		data = mod.GetDataInstance()
		radius = data[c4d.PYSCULPTMODIFIERDEFORMER_RADIUS]
		pressure = data[c4d.PYSCULPTMODIFIERDEFORMER_PRESSURE] * 100.0
		stampActive = data[c4d.PYSCULPTMODIFIERDEFORMER_STAMP_ACTIVE]
		stampTexture = data[c4d.PYSCULPTMODIFIERDEFORMER_STAMP_TEXTURE]
		numStamps = data[c4d.PYSCULPTMODIFIERDEFORMER_NUMSTAMPS]
		useFalloff = data[c4d.PYSCULPTMODIFIERDEFORMER_STAMP_USEFALLOFF]
		seed = data[c4d.PYSCULPTMODIFIERDEFORMER_SEED]
		rotation = data[c4d.PYSCULPTMODIFIERDEFORMER_STAMP_ROTATION]

		if not op.CheckType(c4d.Opolygon):
			return True

		if not self.brushInterface.Init(op):
			return True

		pointCount = op.GetPointCount()

		brushData = self.brushInterface.GetDefaultData()
		modifierData = c4d.BaseContainer()
		vertex = int(0)

		brushData.SetFloat(c4d.MDATA_SCULPTBRUSH_SETTINGS_STRENGTH, pressure)
		brushData.SetFloat(c4d.MDATA_SCULPTBRUSH_SETTINGS_RADIUS, radius)
		brushData.SetBool(c4d.MDATA_SCULPTBRUSH_STAMP, stampActive)
		brushData.SetFilename(c4d.MDATA_SCULPTBRUSH_STAMP_TEXTUREFILENAME, stampTexture)
		brushData.SetBool(c4d.MDATA_SCULPTBRUSH_STAMP_USEFALLOFF, useFalloff)
		brushData.SetFloat(c4d.MDATA_SCULPTBRUSH_STAMP_ROTATION_VALUE, rotation)

		self.brushInterface.SetData(brushData,modifierData)
		random.seed(seed)
		for i in xrange(0,numStamps):
			vertex = int(random.random()*pointCount)
			self.brushInterface.ApplyModifier(ID_SCULPT_BRUSH_PULL_MODIFIER,vertex,brushData,modifierData)

		op.Message(c4d.MSG_UPDATE)
		
		return True

if __name__ == "__main__":
    plugins.RegisterObjectPlugin(id=PLUGIN_ID, str="Py-SculptModifierDeformer",
                                g=SculptModifierDeformer,
                                description="opysculptmodifierdeformer", icon=None,
                                info=c4d.OBJECT_MODIFIER)

