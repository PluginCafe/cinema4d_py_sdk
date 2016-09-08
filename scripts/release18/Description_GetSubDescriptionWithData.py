# This example highlights how to use Description.GetSubDescriptionWithData() to obtain subdescription parameters information

import c4d


def main():
    # Retrieves active material
    mat = doc.GetActiveMaterial()
    if not mat: return

    # Tries to obtain a gradient shader
    gradient = mat[c4d.MATERIAL_COLOR_SHADER]
    if not gradient: return
    if gradient.GetType() != c4d.Xgradient: return

    # Creates a new Description
    desc = c4d.Description()
    if not desc: return

    # Builds the gradient DescID
    descid = c4d.DescID(c4d.DescLevel(c4d.SLA_GRADIENT_GRADIENT, c4d.CUSTOMDATATYPE_GRADIENT, c4d.Xgradient))

    # Retrieves the gradient knots description
    desc.GetSubDescriptionWithData(descid, [gradient], c4d.BaseContainer(), None)

    # Retrieves the gradient data with its knots
    gradientData = gradient[descid]

    # Prints the gradient knots
    knotCount = gradientData.GetKnotCount()
    for idx in range(knotCount):
        print gradientData.GetKnot(idx)

    # Prints the gradient description
    for bc, paramid, groupid in desc:
        print bc[c4d.DESC_NAME], paramid[-1].dtype


if __name__=='__main__':
    main()
