import c4d
from c4d import utils


def main():
    # Creates Voronoi Fracture object and inserts it into the active document
    voronoi = c4d.VoronoiFracture()
    doc.InsertObject(voronoi)
    
    # Creates Cube object and inserts it into the active document
    cube = c4d.BaseObject(c4d.Ocube)
    doc.InsertObject(cube)
    
    # Makes it editable and finally insert it as child of Voronoi Fracture object
    editable = utils.SendModelingCommand(c4d.MCOMMAND_MAKEEDITABLE, list=[cube], mode=c4d.MODIFY_ALL, doc=doc)
    doc.InsertObject(editable[0], parent=voronoi)
    
    # Adds a point generator
    ret = voronoi.AddPointGenerator(c4d.ID_POINTCREATOR_CREATORTYPE_DISTRIBUTION)
    generator = ret[0]
    generator[c4d.ID_POINTCREATOR_CREATEDPOINTAMOUNT] = 25
    generator[c4d.ID_POINTCREATOR_CREATEPOINTSSEED] = 73519
    
    # Adds a shader generator
    ret = voronoi.AddPointGenerator(c4d.ID_POINTCREATOR_CREATORTYPE_SHADER)
    generator = ret[0]
    
    # Setups Noise shader
    noise = c4d.BaseShader(c4d.Xnoise)
    noise[c4d.SLA_NOISE_NOISE] = c4d.NOISE_OFFSET+c4d.NOISE_VORONOI_3
    
    # Sets the shader for the generator
    generator[c4d.ID_POINTCREATOR_SHADER_SHADER] = noise
    generator.InsertShader(noise)
    generator.Message(c4d.MSG_UPDATE)
    
    c4d.EventAdd()


if __name__=='__main__':
    main()
