import cv2 
import numpy as np

class RANSAC:
    def __init__(self,prob_success=0.99,init_outlier_ratio=0.7,inlier_threshold=5.0):
        """ Initializes a RANSAC estimator.
            Arguments:
                prob_success: probability of success
                init_outlier_ratio: initial outlier ratio
                inlier_threshold: maximum re-projection error for inliers
        """
        self.prob_success = prob_success
        self.init_outlier_ratio = init_outlier_ratio
        self.inlier_threshold = inlier_threshold
    
    def compute_num_iter(self,outlier_ratio):
        """ Compute number of iterations given the current outlier ratio estimate.
            
            The number of iterations is computed as:
    
                N = ceil( log(1-p)/log(1-(1-e)^s) )
            
            where p is the probability of success,
                  e is the outlier ratio, and
                  s is the sample size.
    
            Arguments:
                outlier_ratio: current outlier ratio estimate
            Returns:
                number of iterations
        """
        s = 4 # Num of measurements in a sample is 4 for homography
        N = np.ceil ( np.log(1-self.prob_success)/np.log(1-(1-outlier_ratio)**s) )
        return N
    
    def compute_inlier_mask(self,H,ref_pts,query_pts):
        """ Determine inliers given a homography estimate.
            
            A point correspondence is an inlier if its re-projection error is 
            below the given threshold.
            
            Arguments:
                H: homography to be applied to the reference points [3,3]
                ref_pts: reference points [N,1,2]
                query_pts: query points [N,1,2]
            Returns:
                Boolean array where mask[i] = True means the point i is an inlier. [N]
        """
        ref_pts = ref_pts.reshape(-1, 1, 2)
        query_pts = query_pts.reshape(-1, 1, 2)
        ref_pts_H = cv2.perspectiveTransform(ref_pts, H)
        errors = np.linalg.norm(query_pts - ref_pts_H, axis=2)
        inlier_mask = errors < self.inlier_threshold
        return inlier_mask

    def find_homography(self,ref_pts,query_pts):
        """ Compute a homography and determine inliers using the RANSAC algorithm.
            
            The homography transforms the reference points to match the query points, i.e.
            
            query_pt ~ H * ref_pt
            
            Arguments:
                ref_pts: reference points [N,1,2]
                query_pts: query points [N,1,2]
            Returns:
                H: the computed homography estimate [3,3]
                mask: the Boolean inlier mask [N]
        """
        outlier_ratio = self.init_outlier_ratio
        iter = 0
        max_inliers = 0

        while(iter < self.compute_num_iter(outlier_ratio)):
            # Randomly choose 4 correspondences
            random_idx = np.random.choice(len(ref_pts), 4, replace=False)
            random_ref_pts = ref_pts[random_idx]
            random_query_pts = query_pts[random_idx]

            # Compute homography using cv.find Homography, method = 0
            H, _ = cv2.findHomography(random_ref_pts, random_query_pts, 0, self.inlier_threshold)

            # Count the number of inliers for this homography
            mask = self.compute_inlier_mask(H, ref_pts, query_pts)
            num_inliers = np.sum(mask)
            # If the number of inliers is greater than current best, store homography and list of inliers (mask)
            if num_inliers > max_inliers:
                best_H = H
                best_mask = mask
                max_inliers = num_inliers
                outlier_ratio = 1-(max_inliers/len(ref_pts))
            iter += 1
        indices = np.argwhere(best_mask == 1)
        best_H, _ = cv2.findHomography(ref_pts[indices[:,0]], query_pts[indices[:,0]], 0, self.inlier_threshold)
        return best_H, best_mask

class Tracker:
    def __init__(self,reference,overlay,min_match_count=10,inlier_threshold=5):
        """ Initializes a Tracker object.
            
            During initialization, this function will compute and store SIFT keypoints
            for the reference image.

            Arguments:
                reference: reference image
                overlay: overlay image for augmented reality effect
                min_match_count: minimum number of matches for a video frame to be processed.
                inlier_threshold: maximum re-projection error for inliers in homography computation
        """
        self.overlay = overlay
        self.min_match_count = min_match_count
        self.inlier_threshold = inlier_threshold
        gray_ref= cv2.cvtColor(reference,cv2.COLOR_BGR2GRAY)
        sift = cv2.SIFT_create()
        self.kp_ref, self.des_ref = sift.detectAndCompute(gray_ref,None)

    def compute_homography(self,frame,ratio_thresh=0.7):
        """ Calculate homography relating the reference image to a query frame.
            
            This function first finds matches between the query and reference
            by matching SIFT keypoints between the two image.  The matches are
            filtered using the ratio test.  A match is accepted if the first 
            nearest neighbor's distance is less than ratio_thresh * the second
            nearest neighbor's distance.
            
            RANSAC is then applied to matches that pass the ratio test, to determine
            inliers and compute a homography estimate.
            
            If less than min_match_count matches pass the ratio test,
            the function returns None.

            Arguments:
                frame: query frame from video
            Returns:
                the estimated homography [3,3] or None if not enough matches are found
        """
        gray_query = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sift = cv2.SIFT_create()
        kp_q, des_q = sift.detectAndCompute(gray_query,None)
        matcher = cv2.BFMatcher()
        # Apply ratio test
        good = []
        matches = matcher.knnMatch(self.des_ref, des_q, k=2)
        for m,n in matches:
            if m.distance < ratio_thresh*n.distance:
                good.append(m)
        if len(good) < self.min_match_count:
            return None
        else:
            src_pts = np.float32([ self.kp_ref[m.queryIdx].pt for m in good ])
            vid_pts = np.float32([ kp_q[m.trainIdx].pt for m in good ])
            ransac = RANSAC()
            H, _ = ransac.find_homography(src_pts, vid_pts)
            return H

    def augment_frame(self,frame,H):
        """ Draw overlay image on video frame.
            
            Arguments:
                frame: frame to be drawn on [H,W,3]
                H: homography [3,3]
            Returns:
                augmented frame [H,W,3]
        """
        h, w, _ = frame.shape
        warped = cv2.warpPerspective(self.overlay, H, (w, h))
        ones_array = np.ones((self.overlay.shape[0], self.overlay.shape[1]))
        alpha = cv2.warpPerspective(ones_array, H, (w, h))
        out1 = np.multiply(alpha, warped[:, :, 0]) + np.multiply((1-alpha), frame[:, :, 0],)
        out2 = np.multiply(alpha, warped[:, :, 1]) + np.multiply((1-alpha), frame[:, :, 1])
        out3 = np.multiply(alpha, warped[:, :, 2]) + np.multiply((1-alpha), frame[:, :, 2])
        out = np.stack((out1, out2, out3), axis = -1)
        out = out.astype(np.uint8)
        return out
