from PyQt5.QtWidgets import *
import sys

from .project.workflow import PTProject
from filehandling import BatchProcess
from .toplevel import MainWindow

def track_gui(movie=None, settings=None):
    '''

    Parameters
    ----------
    movie: optional path to movie to process
    settings: optional path to .param settings config file

    Returns None
    -------

    '''
    app = QApplication(sys.argv)
    window = MainWindow(
        movie_filename=movie,
        settings_filename=settings)
    window.show()
    #Start event loop
    app.exec_()





def track_batchprocess(moviefilter, settings,
                       crop=True,
                       preprocess=True,
                       track=True,
                       link=True,
                       postprocess=True,
                       annotate=True):
    '''

    Parameters
    ----------
    filefilter: This is a full filename including filepath which may include wildcard characters
    paramfile: This is a full filename including filepath for a .param config file

    Keyword arguments can be False or True. Determines whether this step is applied or not.

    Returns None
    -------

    '''

    for filename in BatchProcess(moviefilter):
        tracker = PTProject(video_filename=filename, param_filename=settings)
        tracker.crop_select = crop
        tracker.preprocess_select = preprocess
        tracker.track_select = track
        tracker.link_select = link
        tracker.postprocess_select = postprocess
        tracker.annotate_select = annotate
        tracker.process()
