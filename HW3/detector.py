import cv2 
import numpy as np
from scipy.ndimage import gaussian_filter, maximum_filter, minimum_filter

class FeatureDetector:
  def __init__(self, sigma = 1, nblur = 10, thresh = 0.05):
    """ Initializes the FeatureDetector object.

        The feature detector detects difference- of-Gaussian (DOG) features.

        Features are detected by finding local minima / maxima in the
        DOG response stack.
        
        Arguments:
          sigma: base sigma value for Gaussian filters
          nblur: number of Gaussian filters
          thresh: minimum absolute response value for a feature detection
    """
    self.sigma = sigma
    self.nblur = nblur
    self.thresh = thresh
  
  def get_dog_response_stack(self,image):
    """ Build the DOG response stack.
        
        The image is first converted to grayscale, floating point on [0 1] range.
        Then a difference-of-Gaussian response stack is built.

        Let I be the original (grayscale) image.
        Let G[i] be the result of applying a Gaussian with sigma s*((1.5)^i) to I,
        where s is the base sigma value.

        Layer i in the stack is computed as G[i+1]-G[i].
        
        Arguments:
            image: 8-bit BGR input image
        Returns:
            DOG response stack [nblur,H,W]
    """
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    I = grayscale/255 # Normalize to values 0 - 1
    '''
        out_array = np.array([])
        for i in range(1, self.nblur+1):
          sigma1 = self.sigma*((1.5)**i)
          G1 = gaussian_filter(I, sigma1)
          sigma2 = self.sigma*((1.5)**(i+1))
          G2 = gaussian_filter(I, sigma2)
          out_array = np.append(out_array, G2 - G1)
          print(out_array)
    #      np.stack()
    '''
    out_lst = []
    sigma3 = self.sigma*((1.5)**1)
    G3 = gaussian_filter(I, sigma3)
    for i in range(1, self.nblur+1):
      sigma4 = self.sigma*((1.5)**(i+1))
      G4 = gaussian_filter(I, sigma4)
      diff = G4-G3
      out_lst.append(diff)
      G3 = G4
    out_array = np.stack(out_lst, axis = 0)
    return out_array

  def find_features(self,responses):
    """ Find features in the DOG response stack.

        Features are detected using non-minima / non-maxima supression
        over a 3x3x3 window.
        
        To do this, compute the local minimum / maximum at each location using
        skimage.ndimage.minimum_filter / maximum_filter.
        
        Then find locations where the response value is equal to the local minimum/
        maximum, and the absolute response value exceeds thresh.
        
        See np.argwhere for a fast way to to do this.
        
        Arguments:
            response: DOG response stack
        Returns:
            List of features (level,y,x)
    """
    pass
  
  def draw_features(self,image,features,color=[0,0,255]):
    """ Draw features on an image.
        
        For each feature, draw it as a dot and a circle.  
        
        The radius of the circle should be equal to the sigma value at that level.
        
        Arguments:
            image: input 8-bit BGR image
            features: list of (level,y,x) features
            color: color in which to draw
        Returns:
            Image with features drawn
    """
    pass

