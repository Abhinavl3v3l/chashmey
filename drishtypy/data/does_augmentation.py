import albumentations as A
from torchvision import transforms
import numpy as np
from drishtypy.data.data_utils import find_stats
from albumentations.pytorch import ToTensor
# from albumentations import CoarseDropout
'''
# A.Resize(input_size,input_size),
# A.CoarseDropout(max_holes=1,max_height=16,max_width=16,min_holes=None,min_height=4,min_width=4,always_apply=True,p=0.7,),
# A.RGBShift(r_shift_limit=50, g_shift_limit=50, b_shift_limit=50, p=0.5),
'''


class AlbumCompose():
    def __init__(self, transform=None):
        self.transform = transform

    def __call__(self, img):
        img = np.array(img)
        img = self.transform(image=img)['image']
        return img


def get_data_transform(path):
    mean, stdev = find_stats(path)
    input_size = 32
    train_albumentation_transform = A.Compose([
        A.Cutout(num_holes=3, max_h_size=8, max_w_size=8,  always_apply=True, p=0.7),
        # CoarseDropout(max_holes=3, max_height=8, max_width=8, min_holes=None, min_height=None, min_width=None,
        #                 fill_value=[i * 255 for i in mean],  always_apply=True, p=0.5),
        # A.RandomCrop(height=8,width=8,p=0.020,always_apply=False),
        A.HorizontalFlip(p=0.7, always_apply=True),
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0, rotate_limit=45, p=0.5),
        A.Normalize(mean=tuple(mean), std=tuple(stdev), max_pixel_value=255, always_apply=True, p=1.0), ToTensor()])

    train_transforms = AlbumCompose(train_albumentation_transform)

    # Test Phase transformation
    test_transforms = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(tuple(mean), tuple(stdev))
    ])

    return train_transforms, test_transforms
