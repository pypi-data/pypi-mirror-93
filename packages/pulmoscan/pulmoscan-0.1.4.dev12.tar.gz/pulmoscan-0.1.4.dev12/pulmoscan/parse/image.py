'''
Contains image-related utils for parsing DICOMs.
'''

from PIL import Image
from pydicom import dcmread


def extract_image(dcm_path: str) -> Image:
    '''
    Extracts and returns image from a DICOM file.
    '''

    dataset = dcmread(dcm_path)
    return Image.fromarray(dataset.pixel_array)
    