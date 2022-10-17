
import os, time, re
import subprocess

from PIL import Image
from pytesseract import pytesseract

# Pour l'installation :
# sudo apt install tesseract-ocr
# sudo apt install libtesseract-dev


#---------------------------------------------------------------------------#
class device:

   _Serial = ""
   _XSize = 0
   _YSize = 0

   #---------------------------------------------------------------------------#
   def __init__(self, Serial):
      self._Serial = Serial
      pytesseract.tesseract_cmd = r'tesseract'

   #---------------------------------------------------------------------------#
   def Dbg( self, Msg ):
      print(Msg)

   #---------------------------------------------------------------------------#
   def GetSize( self ):
      Cmd = "adb -s %s shell wm size"%self._Serial
      res = subprocess.check_output( Cmd, shell=True).decode("utf-8")
      m = re.search( r"Physical size: (\d+)x(\d+)\n", res)
      if ( m ):
         self._XSize = int( m.groups()[0], 10)
         self._YSize = int( m.groups()[1], 10)
      print(res)

   #---------------------------------------------------------------------------#
   def Tap( self, RatioX, RatioY ):
      AbsX = RatioX * self._XSize
      AbsY = RatioY * self._YSize
      Cmd = "adb -s %s shell input tap %d %d"%( self._Serial, AbsX, AbsY )
      subprocess.check_output( Cmd, shell=True)

   #---------------------------------------------------------------------------#
   def GetTextFromScreen( self ) :
      Cmd = "adb exec-out screencap -p > _TmpSrc.png"
      subprocess.check_output( Cmd, shell=True)
                                    # Open image with PIL
      img = Image.open("_TmpSrc.png")
                                    # Extract text from image
      text = pytesseract.image_to_string(img)

      Cmd = "rm _TmpSrc.png"
      subprocess.check_output( Cmd, shell=True)

      return text

   #---------------------------------------------------------------------------#
   def Wakeup( self ):
      Cmd = "adb -s %s shell input keyevent KEYCODE_WAKEUP"%self._Serial
      subprocess.check_output( Cmd, shell=True)


   #---------------------------------------------------------------------------#
   def LockitoStart( self ):
      Cmd = "adb -s %s shell monkey -p fr.dvilleneuve.lockito -v 1"%self._Serial
      subprocess.check_output( Cmd, shell=True)
      time.sleep(5)

   #---------------------------------------------------------------------------#
   def LockitoStartTravel( self ):

      self.Tap( 0.4181, 0.1888 )
      time.sleep(3)
      self.Tap( 0.88, 0.72 )                                                              # 642 1086 635 929
      time.sleep(3)

      #Cmd = "adb -s %s shell input tap 301 287"%self._Serial  # 0,4181, 0,1888
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(3)
      #Cmd = "adb -s %s shell input tap 665 1164"%self._Serial # 0,9236, 0,7658
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(1)
      #Cmd = "adb -s %s shell input tap 611 983"%self._Serial  # 0,8486  0,6467
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(1)


   #---------------------------------------------------------------------------#
   def WazeStart( self ):
      Cmd = "adb -s %s shell monkey -p com.waze -v 1"%self._Serial
      subprocess.check_output( Cmd, shell=True)
      time.sleep(5)

      self.WazeBullshitRemover()
      time.sleep(5)
      self.WazeBullshitRemover()

      StdScreenTxt = self.GetTextFromScreen()

      self.Dbg(StdScreenTxt)

      if re.search( r'\d{1,2}:\d{1,2}\s*h\s*.*\s*\d+\s*km', StdScreenTxt) :
         self.Dbg("Parcours en cours trouvé")

         self.Tap( 0.8889, 0.9066 )    # tap on the little arrow to open travel
         time.sleep(1)

         self.Tap( 0.1583, 0.9066 )    # top on stop to cancel travel
         time.sleep(1)

      else:
         self.Tap( 0.4972, 0.3704 )    # top on stop to cancel travel
         time.sleep(1)

      self.WazeBullshitRemover()


   #---------------------------------------------------------------------------#
   def WazeBullshitRemover( self ):
                                       # Tap on back key until
      while ( not re.search( r'Voulez-vous quitter Waze', self.GetTextFromScreen() ) ) :
         Cmd = "adb -s %s shell input keyevent KEYCODE_BACK"%self._Serial
         subprocess.check_output( Cmd, shell=True)
         self.Dbg( "Back")
         time.sleep(1)

      Cmd = "adb -s %s shell input keyevent KEYCODE_BACK"%self._Serial
      subprocess.check_output( Cmd, shell=True)
      self.Dbg( "Quitter Waze détecté : back again pour revenir sur l'écran initial")
      time.sleep(1)


   #---------------------------------------------------------------------------#
   def WazeGoto( self, Name ):
                                       # Tap directly to search bar
      self.Tap( 0.5, 0.82 )                                                            # 374 1238 ->0,516666667, 0,814473684  352 1062 -> 0.488, 0,8296875
      time.sleep(2)
                                       # enter search name
      Cmd = "adb -s %s shell input text %s"%(self._Serial, Name)
      subprocess.check_output( Cmd, shell=True)

                                       # Tap to 2nd proposition
      self.Tap( 0.5, 0.3 )                                                                # 433 -> 0,284868421 427 ->0,33359375
      time.sleep(3)
                                       # Tap to "y aller"
      self.Tap( 0.6972, 0.9237 )
      time.sleep(3)
                                       # Tap to "y aller"
      self.Tap( 0.6972, 0.9237 )

      self.Dbg("Go to %s"%Name)

      time.sleep(15)

      # Cmd = "adb -s %s shell input keyevent 66"%(self._Serial)
      # subprocess.check_output( Cmd, shell=True)
      # time.sleep(5)

      # self.Tap( 0.4458, 0.3138 )
      # time.sleep(3)
      # self.Tap( 0.6972, 0.9237 )
      # time.sleep(3)
      # self.Tap( 0.6972, 0.9237 )
      # time.sleep(5)
      # self.Tap( 0.4875, 0.5993 )
      # time.sleep(1)

      #Cmd = "adb -s %s shell input tap 321 477"%self._Serial                              # 0,4458, 0,3138
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(3)
      #Cmd = "adb -s %s shell input tap 502 1404"%self._Serial                             # 0,6972, 0,9237
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(3)
      #Cmd = "adb -s %s shell input tap 502 1404"%self._Serial                             # 0,6972, 0,9237
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(5)
      #Cmd = "adb -s %s shell input tap 351 911"%self._Serial                              # 0,4875, 0,5993
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(1)

   #---------------------------------------------------------------------------#
   def WazeSignalDeadbeef( self ):

      self.Tap( 0.9042, 0.8184 )
      time.sleep(1)
      self.Tap( 0.184, 0.38 )                                                             # 133 513 -> 0,184722222, 0,40078125  134 568 -> xxx, 0,373684211
      time.sleep(1)
      self.Tap( 0.1542, 0.54 )                                                            # 123 700 817 -> 0,170833333
      time.sleep(1)
      self.Tap( 0.83, 0.88 )                                                               # 600 1140 1310 -> 8.333 0,890625 0,861842105
      time.sleep(1)
                                       # Tap to "envoyer"
      self.Tap( 0.6972, 0.9237 )
      time.sleep(1)

      #self.Dbg( "Tappe bulle orange")
      #Cmd = "adb -s %s shell input tap 651 1244"%self._Serial                             # 0,9042, 0,8184
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(2)
      #self.Dbg( "Tappe Bulle danger orange")
      #Cmd = "adb -s %s shell input tap 634 288"%self._Serial                              # 0,8806, 0,1895
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(2)
      #self.Dbg( "Tappe Sur la route")
      #Cmd = "adb -s %s shell input tap 111 825"%self._Serial                              # 0,1542, 0,5428
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(2)
      #self.Dbg( "Tappe animal mort")
      #Cmd = "adb -s %s shell input tap 595 1314"%self._Serial                             # 0,8264, 0,8645
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(2)
      #self.Dbg( "Tappe Envoyé")
      #Cmd = "adb -s %s shell input tap 479 1375"%self._Serial
      #subprocess.check_output( Cmd, shell=True)
      #time.sleep(2)


#---------------------------------------------------------------------------#
if __name__ == "__main__" :

   LspDevObj = []

   LstDevices = subprocess.check_output("adb devices", shell=True).decode("utf-8").splitlines()

   for StrDevice in LstDevices :
      m = re.search( r"^([A-Z0-9]{2,})", str(StrDevice) )
      if ( m ):
         LspDevObj.append( device( m.group() ) )
         print (m.group())

   print("LstDev done")

   for DevObj in LspDevObj :

      DevObj.Wakeup()
      time.sleep(3)
      DevObj.GetSize()

      #DevObj.LockitoStart()
      #DevObj.LockitoStartTravel()

      DevObj.WazeStart()
      DevObj.WazeGoto( "Cuculet" )        # Note : doit être une ville sans crit'air


      time.sleep(3)
      #DevObj.WazeSignalDeadbeef()
