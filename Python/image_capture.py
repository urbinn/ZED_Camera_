########################################################################
#
# Copyright (c) 2017, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS be LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core
from time import time

FRAMES = 0
SAVE = True

def ask_frames():
    number = input('How many frames do you want? ')  
    try:
        global FRAMES
        FRAMES = int(number)
    except:
        print('{} not a valid number!'.format(number))
        ask_frames()

''' Exepects an image as matrix, and a name for the image '''
def saving_image(mat, name, cam):
  img = tp.PyERROR_CODE.PyERROR_CODE_FAILURE
  while img != tp.PyERROR_CODE.PySUCCESS:
      filepath = 'output/{}/{}.png'.format(cam, name)
      img = mat.write(filepath)
      print("Saving image : {0}".format(filepath))
      if img == tp.PyERROR_CODE.PySUCCESS:
          break
      else:
          print("Error!!!")



def main():
    ask_frames()
    # Create a PyZEDCamera object
    zed = zcam.PyZEDCamera()

    # Create a PyInitParameters object and set configuration parameters
    init_params = zcam.PyInitParameters()
    init_params.camera_resolution = sl.PyRESOLUTION.PyRESOLUTION_HD720  # Use HD1080 video mode
    init_params.camera_fps = 60  # Set fps at 30

    # Open the camera
    err = zed.open(init_params)
    if err != tp.PyERROR_CODE.PySUCCESS:
        exit(1)

    i = 0
    image_l = core.PyMat()
    image_r = core.PyMat()
    start = time()  

    while i < FRAMES:
        # Grab an image, a PyRuntimeParameters object must be given to grab()
        if zed.grab(zcam.PyRuntimeParameters()) == tp.PyERROR_CODE.PySUCCESS:
            # A new image is available if grab() returns PySUCCESS
            zed.retrieve_image(image_l, sl.PyVIEW.PyVIEW_LEFT)
            zed.retrieve_image(image_r, sl.PyVIEW.PyVIEW_RIGHT)
            timestamp = zed.get_camera_timestamp()  # Get the timestamp at the time the image was captured
            if SAVE:
               saving_image(image_l, timestamp, 'left')
               saving_image(image_r, timestamp, 'right')
            i += 1
    end = time()
    # Close the camera_fps
    zed.close()
    fps = FRAMES / (end-start)
    print('recorded at {0:.2f} FPS'.format(fps))

if __name__ == "__main__":
    main()









