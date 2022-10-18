
import cv2
import imutils



#---------------------------------------------------------------------------#
if __name__ == "__main__" :

   method = cv2.TM_SQDIFF_NORMED


   Screen1 = cv2.imread("lock_logo_play.png")
   Screen2 = cv2.imread("lock_logo_stop.png")
   Screen3 = cv2.imread("lock_logo_stop2.png")
   LogoStop = cv2.imread("LockitoStop.png")

   result = cv2.matchTemplate(LogoStop, Screen1, method)
   mn,_,mnLoc,_ = cv2.minMaxLoc(result)
   print(mn)

   result = cv2.matchTemplate(LogoStop, Screen2, method)
   mn,_,mnLoc,_ = cv2.minMaxLoc(result)
   print(mn)

   result = cv2.matchTemplate(LogoStop, Screen3, method)
   mn,_,mnLoc,_ = cv2.minMaxLoc(result)
   print(mn)
