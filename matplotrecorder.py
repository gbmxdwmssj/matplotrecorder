"""
 A simple Python module for recording matplotlib animation

 This tool use convert command of ImageMagick

 author: Atsushi Sakai

 How to use:

 - import

    from matplotrecorder import matplotrecorder

 - save file

    matplotrecorder.save_frame()

 - generate movie

    matplotrecorder.save_movie("animation.gif", 0.1)

"""

import os
import subprocess
import matplotlib.pyplot as plt

FRAME_CNT = 0
DO_NOTHING = True  # switch to stop all recordering


def save_frame():
    """
    Save a frame for movie
    """

    if not DO_NOTHING:
        global FRAME_CNT
        plt.savefig("recorder" + '{0:04d}'.format(FRAME_CNT) + '.png')
        FRAME_CNT += 1


def save_movie(fname, d_pause):
    """
    Save movie as gif or video (.mp4 recommended)
    """

    if not DO_NOTHING:
        _, extension = os.path.splitext(fname)

        print("Saving movie......")

        if extension == ".gif":
            cmd = "convert -delay " + str(int(d_pause * 100)) + " recorder*.png " + fname
        else:
            ## imagemagick (convert) cannot find ffmpeg
            cmd = "ffmpeg -framerate " + str(int(d_pause * 100)) + \
                  " -pattern_type glob -i 'recorder*.png' -c:v libx264 " + fname

        subprocess.call(cmd, shell=True)
        cmd = "rm recorder*.png"
        subprocess.call(cmd, shell=True)

        print("Movie has been saved! (Maybe a bad movie, please check it!)")


if __name__ == '__main__':
    print("A sample recording start")
    import math

    TIME = range(50)

    X1 = [math.cos(t / 10.0) for t in TIME]
    Y1 = [math.sin(t / 10.0) for t in TIME]
    X2 = [math.cos(t / 10.0) + 2 for t in TIME]
    Y2 = [math.sin(t / 10.0) + 2 for t in TIME]

    for ix1, iy1, ix2, iy2 in zip(X1, Y1, X2, Y2):
        plt.plot(ix1, iy1, "xr")
        plt.plot(ix2, iy2, "xb")
        plt.axis("equal")
        plt.pause(0.1)

        save_frame()  # save each frame

    save_movie("test_animation.gif", 0.1)
    # save_movie("test_animation.mp4", 0.1)
