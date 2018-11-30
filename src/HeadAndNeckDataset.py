import os.path
import unicodecsv as csv
from torch.utils.data import Dataset
from medpy.io import load
import torch
import numpy as np

class HeadAndNeckDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, csv_file, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.transform = transform
        csvtrainingFiles =  open(csv_file, 'rb')
        try:        
          trianingCSVFileReader = csv.reader(csvtrainingFiles, delimiter=';', encoding='iso8859_15')
          self.dataFileList = []
          self.labelFileList = []
          self.maskFileList = []
          for trainingFilePath in trianingCSVFileReader:
            imgFiles = []
            maskFiles = []
            labelFiles = []
            i = 0
            while (True):
              trainingFileName = trainingFilePath[0] + '/img' + str(i) + '.nii.gz'
              if (os.path.isfile(trainingFileName)):
                imgFiles.append(trainingFileName)
              else:
                break
                
              maskFileName = trainingFilePath[0] + '/mask' + str(i) + '.nii.gz'
              if (os.path.isfile(maskFileName)):
                maskFiles.append(maskFileName)
              labelsFileName = trainingFilePath[0] + '/struct' + str(i) + '.nii.gz'  
              if (os.path.isfile(labelsFileName)):
                labelFiles.append(labelsFileName)
              i=i+1
              
            self.dataFileList.append(imgFiles)
            self.labelFileList.append(labelFiles)
            self.maskFileList.append(maskFiles)
            
        finally:
          csvtrainingFiles.close()
          

    def __len__(self):
        return len(self.dataFileList)

    def __getitem__(self, idx):
        
        trainingFileNames = self.dataFileList[idx]
        maskFileNames = self.maskFileList[idx]
        labelsFileNames = self.labelFileList[idx]
        
        imgData = []
        for trainingFileName in trainingFileNames:
          imgNii, imgHeader = load(trainingFileName)
          imgData.append(imgNii)
        imgData = np.stack(imgData)
          
        maskData = []
        if (len(trainingFileNames) == len(maskFileNames)):
          for maskFileName in maskFileNames:
            maskNii, maskHeader = load(maskFileName)
            maskData.append(maskNii)
          maskData = np.stack(maskData)
        
        labelData = []
        if (len(trainingFileNames) == len(labelsFileNames)):
          for labelsFileName in labelsFileNames:
            labelsNii, labelsHeader = load(labelsFileName)
            labelData.append(labelsNii)
          labelData = np.stack(labelData)

        sample = {'image': imgData, 'label': labelData, 'mask': maskData}
        
        if self.transform:
            sample = self.transform(sample)

        return sample
      
class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        image, label, mask = sample['image'], sample['label'], sample['mask']

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W
#         image = image.transpose((2, 0, 1))
#         label = label.transpose((2, 0, 1))
#         mask = mask.transpose((2, 0, 1))
        labelTorch = torch.tensor([1])
        if(len(label) > 0):
          labelTorch = torch.from_numpy(label)
          
        maskTorch = torch.tensor([1])
        if(len(mask) > 0):
          maskTorch = torch.from_numpy(mask)
          
          
        return {'image': torch.from_numpy(image),
                'label': labelTorch,
                'mask': maskTorch}      
        