import numpy as np

def demosaic(raw):
  """ Demosaics a raw 16-bit image captured using a Bayer pattern.
      Arguments:
        raw: the input raw data in 16-bit integer [HxW]
      Returns:
        The demosaiced image in 32-bit floating point [HxWx3]
  """
  normalized_img = raw.astype(np.float32) / (2**16 - 1)
  

  pass

def white_balance(image):
  """ White balanaces a 32-bit floating point demosaiced image.
      This is done by simply scaling each channel so that its mean = 0.5.
      Arguments:
        image: the input image in 32-bit floating point [HxWx3]
      Returns:
        The white balanced image in 32-bit floating point [HxWx3]
  """
  pass

def curve_and_quantize(image,inv_gamma=0.85):
  """ Applies inverse gamma function and quantizes to 8-bit.
      Arguments:
        image: the input image in 32-bit floating point [HxWx3]
        inv_gamma: the value of 1/gamma
      Returns:
        The curved and quantized image in 8-bit unsigned integer [HxWx3]
  """
  pass

