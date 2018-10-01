"""
FieldObject Sampling

Example:
c4d.modules.mograph.FieldObject
c4d.modules.mograph.FieldInput
c4d.modules.mograph.FieldInfo
c4d.modules.mograph.FieldOutput

Samples arbitrary points within a random field.
"""

import c4d
from c4d.modules import mograph

def main():

    # Checks if the selected object is a random field object
    if not op and not op.CheckType(c4d.Frandom):
        return

    # Creates a list of 10 points to sample
    sampleCount = 10
    positions = []
    offset = 0.0
    for i in xrange(sampleCount):
        positions.append(c4d.Vector(offset, 0, 0))
        offset += 10.0

    # Creates FieldInput
    input = mograph.FieldInput(positions, sampleCount)

    # Creates FieldInfo
    flags = c4d.FIELDSAMPLE_FLAG_VALUE
    thread = c4d.threading.GeGetCurrentThread()
    currentThreadIndex = 0
    threadCount = 1
    info = mograph.FieldInfo.Create(flags, thread, doc, currentThreadIndex, threadCount, input)

    # Creates FieldOutput
    output = mograph.FieldOutput()
    output.Resize(sampleCount, c4d.FIELDSAMPLE_FLAG_VALUE)

    # Samples the data
    op.InitSampling(info)
    op.Sample(input, output.GetBlock(), info, c4d.FIELDOBJECTSAMPLE_FLAG_DISABLEDIRECTIONFALLOFF)
    op.FreeSampling(info)

    # Prints the values for the sampled points
    print(output)

if __name__=='__main__':
    main()