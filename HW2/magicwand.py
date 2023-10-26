import cv2
import numpy as np


class MagicWand:
    def __init__(self,calibration_path,R):
        """ Loads calibration from file and stores ball radius.
            Arguments:
                calibration_path: path to calibration file
                R: ball radius in cm
        """
        self.focal, self.centerx, self.centery = np.loadtxt(calibration_path,delimiter=' ')
        self.R = R

    def detect_ball(self,image):
        """ Detect one or more balls in image.
            Arguments:
                image: RGB image in which to detect balls
            Returns:
                list of tuples (x, y, radius)
        """
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gaussian = cv2.GaussianBlur(grayscale, (9, 9), 2)
        circles = cv2.HoughCircles(gaussian, cv2.HOUGH_GRADIENT, dp=2, minDist=10)
        circles_list = []
        if circles is not None:
            for circle in circles[0]:
                x, y, radius = circle[0], circle[1], circle[2]
                circles_list.append((x, y, radius))
            return circles_list
        else:
            return []

    def calculate_ball_position(self,x,y,r):
        """ Calculate ball's (X,Y,Z) position in world coordinates
            Arguments:
                x,y: 2D position of ball in image
                r: radius of ball in image
            Returns:
                X,Y,Z position of ball in world coordinates
        """
        Z = self.focal*self.R/r
        X = (Z/self.focal)*(x-self.centerx)
        Y = (Z/self.focal)*(y-self.centery)
        return (X, Y, Z)


    def draw_ball(self,image,x,y,r,Z):
        """ Draw circle on ball and write depth estimate in center
            Arguments:
                image: image on which to draw
                x,y,r: 2D position and radius of ball
                Z: estimated depth of ball
        """
        cv2.circle( image, (int(x), int(y)), int(r), (0,0,255),2)
        cv2.putText( image, str(int(Z)) + ' cm', (int(x),int(y)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255))
    
    def project(self,X,Y,Z):
        """ Pinhole projection.
            Arguments:
                X,Y,Z: 3D point
            Returns:    
                (x,y) 2D location of projection in image
        """
        x = self.focal*(X/Z) + self.centerx
        y = self.focal*(Y/Z) + self.centery
        return (x, y)

    def draw_line(self,image,X1,Y1,Z1,X2,Y2,Z2):
        """ Draw a 3D line
            Arguments:
                image: image on which to draw
                X1,Y1,Z1: 3D position of first line endpoint
                X2,Y2,Z2: 3D position of second line endpoint
        """
        x1, y1 = self.project(X1, Y1, Z1)
        x2, y2 = self.project(X2, Y2, Z2)
        cv2.line( image, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 1)


    def draw_bounding_cube(self,image,X,Y,Z):
        """ Draw bounding cube around 3D point, with radius R
            Arguments:
                image: image on which to draw
                X,Y,Z: 3D center point of cube
        """
        # Draw top two horizontal lines
        self.draw_line(image, X-self.R, Y-self.R, Z-self.R, X+self.R, Y-self.R, Z-self.R)
        self.draw_line(image, X-self.R, Y-self.R, Z+self.R, X+self.R, Y-self.R, Z+self.R)
        # Draw top two connecting lines for front to back
        self.draw_line(image, X-self.R, Y-self.R, Z+self.R, X-self.R, Y-self.R, Z-self.R)
        self.draw_line(image, X+self.R, Y-self.R, Z+self.R, X+self.R, Y-self.R, Z-self.R)
        # Draw two connecting lines from top to bottom, front side
        self.draw_line(image, X+self.R, Y-self.R, Z+self.R, X+self.R, Y+self.R, Z+self.R)
        self.draw_line(image, X-self.R, Y-self.R, Z+self.R, X-self.R, Y+self.R, Z+self.R)
        # Draw two connecting lines from top to bottom, back side
        self.draw_line(image, X-self.R, Y-self.R, Z-self.R, X-self.R, Y+self.R, Z-self.R)
        self.draw_line(image, X+self.R, Y-self.R, Z-self.R, X+self.R, Y+self.R, Z-self.R)
        # Draw bottom two horizontal lines
        self.draw_line(image, X+self.R, Y+self.R, Z+self.R, X-self.R, Y+self.R, Z+self.R)
        self.draw_line(image, X+self.R, Y+self.R, Z-self.R, X-self.R, Y+self.R, Z-self.R)
        # Draw bottom two connecting lines for front to back
        self.draw_line(image, X+self.R, Y+self.R, Z-self.R, X+self.R, Y+self.R, Z+self.R)
        self.draw_line(image, X-self.R, Y+self.R, Z-self.R, X-self.R, Y+self.R, Z+self.R)


    def process_frame(self,image):
        """ Detect balls in frame, estimate 3D positions, and draw on image
            Arguments:
                image: image to be processed
            Returns:
                list of (X,Y,Z) 3D points of detected balls
        """
        out_list = []
        circles_detected_list = self.detect_ball(image)
        for circle in circles_detected_list:
            x, y, r = circle[0], circle[1], circle[2]
            world_coords = self.calculate_ball_position(x, y, r)
            out_list.append(world_coords)
            X, Y, Z = world_coords[0], world_coords[1], world_coords[2]
            self.draw_ball(image, x, y, r, Z)
            self.draw_bounding_cube(image, X, Y, Z)
        return out_list