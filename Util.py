
import os, time, re
import subprocess

batcmd="dir"

#---------------------------------------------------------------------------#
class device:

   _Serial = ""
   _XSize = 0
   _YSize = 0

   #---------------------------------------------------------------------------#
   def __init__(self, Serial):
      self._Serial = Serial

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


#574 999 ->

#603 985

   #---------------------------------------------------------------------------#
   def WazeStart( self ):
      Cmd = "adb -s %s shell monkey -p com.waze -v 1"%self._Serial
      subprocess.check_output( Cmd, shell=True)
      time.sleep(5)
                                       # deny previous travel and make search bar clean
      self.Tap( 0.0667, 0.5546 )                                                          # 0.2667, 0.5546
      time.sleep(1)
      self.Tap( 0.0667, 0.5546 )
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

      DevObj.LockitoStart()
      DevObj.LockitoStartTravel()

      DevObj.WazeStart()
      DevObj.WazeGoto( "Lyon" )


      time.sleep(3)
      #DevObj.WazeSignalDeadbeef()
