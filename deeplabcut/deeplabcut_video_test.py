


class SpiderCroppedVideoReader():
    """ This class mimics OpenCV's VideoCapture class, but instead reads
        the *.ufmf files, which contain 200x200 cropped/rotated and monochrome
        spider images.
    """

    def __init__(self, filename, progressCallback=None):
        self.fname = filename
        self.iframe = 0
        self.progressCallback = progressCallback

        # DEBUG
        self.MAX_NUM_FRAMES = 50 * 3600 * 24 * 100

        # Is this a supported input file?
        if not self.fname.endswith('.ufmf'):
            raise Exception('Unsupported input file. Only *.ufmf files allowed.')

        # Open file to determine size
        from motmot.SpiderMovie import SpiderMovie
        mov = SpiderMovie(filename)
        #self.arr = np.memmap(self.fname, dtype=np.uint8, mode='r')
        #N = self.arr.shape[0]
        N = mov.shape[0]*mov.shape[1]*mov.shape[2]
        #del self.arr
        # Ensure this file has the right size
        if N % (1024 * 1024) != 0:
            raise Exception('Image does not have expected size of 1024x1024.')
        # Open again with right shape
        #self.arr = np.memmap(self.fname, dtype=np.uint8, mode='r', shape=(int(N / (1024 * 1024)), 1024, 1024))
        self.matrix_shape = mov.shape
        self.mov = mov

    # Get various metadata
    def get(self, i):
        # Call progress callback
        if self.progressCallback is not None:
            try:
                self.progressCallback(float(i) / self.matrix_shape[0])
            except:
                pass
        # NUM. FRAMES
        if i == 7:
            if self.matrix_shape is not None:
                return min(self.MAX_NUM_FRAMES, self.matrix_shape[0])
            else:
                raise Exception('File closed.')
        # FPS
        elif i == 5:
            return 50
        # HEIGHT
        elif i == 4:
            return 1024
        # WIDTH
        elif i == 3:
            return 1024
        # ERROR
        else:
            raise Exception('Unsupported metadata requested: {}'.format(i))

    def isOpened(self):
        return True

    def read(self):
        if self.iframe >= self.get(7):
            return False, np.zeros((1024, 1024), dtype=np.uint8)
        else:
            self.iframe += 1
            return True, self.mov[self.iframe - 1]


basepath = 'Z:/HsinYi/Test Video From Darya/test_clip_dlc'
project_name = 'TEST'
scorer = 'PC'

import os, glob

video_list = glob.glob(os.path.join(basepath, 'raw/')+'*.s.ufmf')
print('video list: ' )
print(video_list)


import deeplabcut
deeplabcut.create_new_project(project_name , scorer, video_list, working_directory=basepath, copy_videos=False)