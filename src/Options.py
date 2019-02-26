import torch


numberOfEpochs = 500
testMode = True
trainMode = True
oneShot = True
usePaddedNet=True
ccW=0.9999
smoothW = 0.0001
vecLengthW = 0.0
cycleW = 0.00
trainingFileNamesCSV=''
device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
outputPath='.'
patchSize=80
maxNumberOfSamples=6 # samples for one batch must be < maxNumberOfSamples
netDepth=3
numberOfFiltersFirstLayer=32
receptiveField = (44, 44, 44) #adapt depth and receptive field according to ReceptiveFieldSizeCalculator in repository
netMinPatchSize = 48
normImgPatches=False
trainTillConvergence = True
lossTollerances=(0.00001,)
cumulativeLossTollerance=100#0.001
downSampleRates = (0.25,0.5,1.0)
boundarySmoothnessW=(100.0,10.0,1.0)
useMedianForSampling = (False,False,True,)



