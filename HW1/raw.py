import numpy as np

def demosaic(raw):
  """ Demosaics a raw 16-bit image captured using a Bayer pattern.
      Arguments:
        raw: the input raw data in 16-bit integer [HxW]
      Returns:
        The demosaiced image in 32-bit floating point [HxWx3]
  """
  normalized_img = raw.astype(np.float32) / (2**16 - 1)
  padded = np.pad(normalized_img, pad_width=1, mode='constant', constant_values=0)
  row = padded.shape[0] # num of rows of padded array
  col = padded.shape[1] # num of col of padded array
  Red_array= np.empty((normalized_img.shape[0], normalized_img.shape[1]))
  Blue_array= np.empty((normalized_img.shape[0], normalized_img.shape[1]))
  Green_array= np.empty((normalized_img.shape[0], normalized_img.shape[1]))
  for i in range(1, row-1, 1): 
      for j in range(1, col-1, 1):
        # At red pixel
        if i%2 != 0 and j%2 != 0:
            Red_array[i-1 ,j-1] = padded[i, j]
            Green_array[i-1 ,j-1] = np.mean([padded[i+1, j], padded[i-1, j], padded[i, j-1], padded[i, j+1]], dtype = np.float32)
            Blue_array[i-1 ,j-1] = np.mean([padded[i+1, j+1], padded[i-1, j-1], padded[i-1, j+1], padded[i+1, j-1]], dtype = np.float32)
        # At green pixel with red adjacent
        elif i%2 != 0 and j%2 == 0:
            Red_array[i-1,j-1] = np.mean([padded[i, j-1], padded[i, j+1]], dtype = np.float32)
            Green_array[i-1 ,j-1] = padded[i,j]
            Blue_array[i-1 ,j-1] = np.mean([padded[i-1, j], padded[i+1, j]], dtype = np.float32)
        # At green pixel with blue adjacent
        elif i%2 == 0 and j%2 != 0:
            Red_array[i-1,j-1] = np.mean([padded[i-1, j], padded[i+1, j]], dtype = np.float32)
            Green_array[i-1 ,j-1] = padded[i,j]
            Blue_array[i-1 ,j-1] = np.mean([padded[i, j-1], padded[i, j+1]], dtype = np.float32)
        # At blue pixel
        elif i%2 == 0 and j%2 == 0:
            Red_array[i-1,j-1] = np.mean([padded[i+1, j+1], padded[i-1, j-1], padded[i-1, j+1], padded[i+1, j-1]], dtype = np.float32)
            Green_array[i-1 ,j-1] = np.mean([padded[i+1, j], padded[i-1, j], padded[i, j-1], padded[i, j+1]], dtype = np.float32)
            Blue_array[i-1 ,j-1] = padded[i, j]
  demosaic_img = np.stack((Red_array, Green_array, Blue_array), axis = 2)
  demosaic_img = demosaic_img.astype(np.float32)
  return demosaic_img

def white_balance(image):
  """ White balanaces a 32-bit floating point demosaiced image.
      This is done by simply scaling each channel so that its mean = 0.5.
      Arguments:
        image: the input image in 32-bit floating point [HxWx3]
      Returns:
        The white balanced image in 32-bit floating point [HxWx3]
  """
  red_array = image[:, :, 0]
  green_array = image[:, :, 1]
  blue_array = image[:, :, 2]
  red_scalar = 0.5/np.mean(red_array)
  green_scalar = 0.5/np.mean(green_array)
  blue_scalar = 0.5/np.mean(blue_array)
  new_red = red_array*red_scalar
  new_green = green_array*green_scalar
  new_blue = blue_array*blue_scalar
  white_balance_img = np.stack((new_red, new_green, new_blue), axis = 2)
  white_balance_img = white_balance_img.astype(np.float32)
  return white_balance_img


def curve_and_quantize(image,inv_gamma=0.85):
  """ Applies inverse gamma function and quantizes to 8-bit.
      Arguments:
        image: the input image in 32-bit floating point [HxWx3]
        inv_gamma: the value of 1/gamma
      Returns:
        The curved and quantized image in 8-bit unsigned integer [HxWx3]
  """
  gamma_img = image**(inv_gamma)
  clipped_img = np.clip(gamma_img, 0, 1)
  out_img = clipped_img*255
  out_img = out_img.astype(np.uint8)
  return out_img

