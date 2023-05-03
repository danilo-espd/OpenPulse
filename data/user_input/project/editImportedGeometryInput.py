from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QRect

from pulse.utils import *
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

import gmsh
import sys
import os

window_title_1 = "ERROR MESSAGE"
window_title_2 = "WARNING MESSAGE"

class EditImportedGeometryInput(QDialog):
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.project_ini_file_path = get_new_path(self.project.file._project_path, self.project.file._project_base_name)
        
        self.geometry_edited = False

        if os.path.basename(self.project.file._geometry_path) != "":
            self.call_gmsh(self.project.file._geometry_path)
    
    def call_gmsh(self, path):
       
        gmsh.initialize('', False)
        gmsh.option.setNumber("General.Terminal", 0)
        
        try:
            gmsh.option.setNumber("General.NumThreads", 4)
        except:
            pass
        gmsh.open(path)
        # gmsh.option.setString("General.OCCTargetUnit", "m")

        gmsh.model.occ.synchronize()

        if '-nopopup' not in sys.argv:
            gmsh.option.setNumber('General.FltkColorScheme', 1)
            gmsh.fltk.run()

        title = f"Geometry edition confirm"
        message = "Do you really want to confirm the current geometry edition?\n\n"
        message += "\n\nPress the Confirm and save button to proceed with the edtion and save the modified geometry "
        message += "into the project file, otherwise, press Cancel or Close buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message, leftButton_label='Cancel', rightButton_label='Confirm and save', rightButton_size=220)

        if read._doNotRun:
            return
        
        if read._continue:

            new_path, new_basename = get_edited_filename(path)

            if new_path != "" and new_basename != "":
  
                self.project.edit_imported_geometry(new_basename)
                gmsh.write(new_path)
                self.geometry_edited = True
                # self.project.initial_load_project_actions(self.project_ini_file_path)

        gmsh.finalize()
        return True