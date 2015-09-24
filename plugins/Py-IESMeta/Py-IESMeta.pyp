"""
IES Meta
Copyright: MAXON Computer GmbH
Written for Cinema 4D R12.016

Modified Date: 08/30/2010
"""


import c4d
import os
import time
import datetime

from c4d import plugins, documents, utils, gui
from c4d.plugins import GeLoadString

#seperate c4d_strings definitions
IDS_MANUFAC = 1001
IDS_LUMCAT = 1002
IDS_LUMINAIRE = 1003
IDS_LAMPCAT = 1004
IDS_LAMP = 1005
IDS_FOUND_IES = 1006
IDS_FOUND_LIGHTS = 1007
IDS_IES_META_CREATED = 1008
IDS_IES_HEADER = 1009


#be sure to use a unique ID obtained from 'plugincafe.com'
PLUGIN_ID = 1025281

def ObjectToCurrentState(obj):
    """
    Makes each object editable.
    The object stays in the document
    """
    commandid = c4d.MCOMMAND_MAKEEDITABLE
    objdoc = obj.GetDocument()
    flags = c4d.MODELINGCOMMANDFLAGS_CREATEUNDO
    mode = c4d.MODELINGCOMMANDMODE_ALL
    
    converted = utils.SendModelingCommand(command=commandid, list=[obj], doc=objdoc, flags=flags, mode=mode)
    return converted

class IESMeta():
    """
    Represents the meta information
    of an IES light.
    """
    
    #static var
    count = 0
    
    def __init__(self, ieslight):
        self.__manufac = ieslight[c4d.LIGHT_PHOTOMETRIC_INFO_MANUFAC]
        self.__lumcat = ieslight[c4d.LIGHT_PHOTOMETRIC_INFO_LUMCAT]
        self.__luminaire = ieslight[c4d.LIGHT_PHOTOMETRIC_INFO_LUMINAIRE]
        self.__lampcat = ieslight[c4d.LIGHT_PHOTOMETRIC_INFO_LAMPCAT]
        self.__lamp = ieslight[c4d.LIGHT_PHOTOMETRIC_INFO_LAMP]
    
    def __eq__(self, other):
        return repr(self)==repr(other)
    
    def __str__(self):
        lbl_manufac = GeLoadString(IDS_MANUFAC)
        lbl_lumcat = GeLoadString(IDS_LUMCAT)
        lbl_luminaire = GeLoadString(IDS_LUMINAIRE)
        lbl_lampcat = GeLoadString(IDS_LAMPCAT)
        lbl_lamp = GeLoadString(IDS_LAMP)
        
        return "%s: %s\n%s: %s\n%s: %s\n%s: %s\n%s: %s\n" % (lbl_manufac, self.__manufac, lbl_lumcat, self.__lumcat, lbl_luminaire, self.__luminaire , lbl_lampcat, self.__lampcat , lbl_lamp, self.__lamp)
    
    def __repr__(self):
        """Just used if two meta information are equal, see __eq__"""
        return "%s,%s,%s,%s,%s" % (self.__manufac, self.__lumcat, self.__luminaire , self.__lampcat , self.__lamp)

class IESMetaList():
    
    stack = []

class IESMetaSaver(plugins.SceneSaverData):
    
    def Save(self, node, name, old_doc, filterflags):
        doc = old_doc.GetClone()
        
        """ Iteration process to convert the objects"""
        def _start_conversion(doc):
            first = doc.GetFirstObject()
            if not first: return

            def _object_iteration(op):
                if not op: return
    
                ObjectToCurrentState(op)
    
                c4d.StatusSetSpin()
                
                _object_iteration(op.GetDown())
                _object_iteration(op.GetNext())
            
            _object_iteration(first)
        
        #first start the conversion...
        _start_conversion(doc)
        
        #...and now we have a iteratable scene file with the real count of IES lights
        def _start_collect_ies(doc):
            first = doc.GetFirstObject()
            if not first: return
            
            
            def __is_object_ies_light(op):
                if op.GetType()!=c4d.Olight: return False
                
                light = op
                lighttype = light[c4d.LIGHT_TYPE]
                if lighttype!=c4d.LIGHT_TYPE_PHOTOMETRIC: return False
                return True
            
            def __object_iteration(op, ies_meta):
                if not op: return
                
                if __is_object_ies_light(op)==True:
                    minfo = IESMeta(op)
                    IESMeta.count += 1
                    ies_meta.append(minfo)
                
                c4d.StatusSetSpin()
                
                __object_iteration(op.GetDown(), ies_meta)
                __object_iteration(op.GetNext(), ies_meta)
            
            #reset the static var to count the lights in total
            IESMeta.count = 0
            
            ies_meta = []
            __object_iteration(first, ies_meta)
            return ies_meta
        
        
        ies_meta = _start_collect_ies(doc)
        
        def _remove_duplicates(ies_meta):
            """
            Removes duplicates and calculate
            the count of each meta file
            """
            ies_meta_clean = []
            ies_meta_count = []
            for meta in ies_meta:
                if meta not in ies_meta_clean:
                    ies_meta_count.append(1)
                    ies_meta_clean.append(meta)
                else:
                    index = ies_meta_clean.index(meta)
                    counter = ies_meta_count[index]
                    ies_meta_count[index] += 1
            
            return ies_meta_count, ies_meta_clean
        
        def _writeprocess(doc, fn, ies_meta):
            """
            Write the ies_meta list to fn.
            Does attach header information
            of the document.
            """
            
            counts, metas = _remove_duplicates(ies_meta)
            if len(counts)!=len(metas): return c4d.FILEERROR_WRONG_VALUE
            
            try:
                f = open(name, "w")
            except IOError, e:
                return c4d.FILEERROR_OPEN
            
            now = datetime.datetime.now()
            time = now.ctime()
            
            title = GeLoadString(IDS_IES_HEADER)
            created = GeLoadString(IDS_IES_META_CREATED)
            docpath = doc.GetDocumentPath()
            docname = doc.GetDocumentName()
            header = "%s\n%s: %s - %s\n\n" % (title, created, time, os.path.join(docpath, docname))
            f.write(header)
            
            f.write("%s\n" % (GeLoadString(IDS_FOUND_IES, len(counts), IESMeta.count),))
            f.write("="*65 + "\n\n")
            
            for count, meta in zip(counts, metas):
                f.write("%s\n%s\n" % (GeLoadString(IDS_FOUND_LIGHTS, count), str(meta),))
                f.write("-"*65 + "\n")
            
            try:
                f.close()
            except IOError, e:
                return c4d.FILEERROR_CLOSE
            
            return c4d.FILEERROR_NONE
        
        if len(ies_meta)==0:
            if filterflags & c4d.SCENEFILTER_PROGRESSALLOWED:
                gui.MessageDialog("Scene has no IES lights")
                return c4d.FILEERROR_NONE
            else:
                print "Unknown error: No IES Lights"
                return c4d.FILEERROR_UNKNOWN_VALUE
        
        state = _writeprocess(doc, name, ies_meta)
        return state


if __name__=='__main__':
    plugins.RegisterSceneSaverPlugin(id=PLUGIN_ID, str="IES Meta (*.txt)", info=0, g=IESMetaSaver, description="", suffix="txt")
