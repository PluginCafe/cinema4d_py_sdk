# This example creates a material from the given substance asset

import c4d
from c4d import modules


def main():
    # Retrieve first substance
    substance = modules.substance.GetFirstSubstance(doc)
    if substance is None:
        return

    # Retrieve material creation mode set in Substance preferences
    mode = modules.substance.PrefsGetMaterialModeSetting()

    # Create material based on the passed Substance asset
    mat = modules.substance.CreateMaterial(substance, 0, mode)
    if mat is not None:
        # Changes name and insert material into the document
        mat.SetName(substance.GetName() + " Material From Script")
        doc.InsertMaterial(mat)
        c4d.EventAdd()


if __name__=='__main__':
        main()
