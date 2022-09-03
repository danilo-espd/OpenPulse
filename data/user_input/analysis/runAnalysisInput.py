from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox, QWidget
from os.path import basename
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5.Qt import QApplication
from PyQt5 import uic
from time import time, sleep
import configparser
from threading import Thread
from time import time

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from pulse.processing.solution_acoustic import SolutionAcoustic
from pulse.postprocessing.save_data import SaveData
from pulse.postprocessing.read_data import ReadData
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.loadingScreen import LoadingScreen

window_title_1 = "ERROR MESSAGE"
window_title_2 = "WARNING MESSAGE"

class RunAnalysisInput(QDialog):
    def __init__(self, project, analysis_ID, analysis_type_label, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Analysis/runAnalysisInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setWindowModality(Qt.WindowModal)

        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_message = self.findChild(QLabel, 'label_message')
        self.label_message.setWordWrap(True)
        self.config_title_font()
        self.config_message_font()

        self.project = project
        self.solve = None
        self.analysis_ID = project.analysis_ID
        self.analysis_type_label = analysis_type_label
        self.frequencies = self.project.frequencies
        self.damping = self.project.global_damping
        self.modes = self.project.modes
        self.solution_acoustic = None
        self.solution_structural = None
        self.convergence_dataLog = None
        self.natural_frequencies_acoustic = []
        self.natural_frequencies_structural = []
        self.complete = False

        LoadingScreen('SOLUTION IN PROGRESS', 'Processing the cross-sections',  target=self.process_cross_sections, project=project)
        if self.project.preprocessor.stop_processing:
            self.project.preprocessor.stop_processing = False
            return

        LoadingScreen('SOLUTION IN PROGRESS', 'Preparing the model to solve', target=self.preparing_mathematical_model_to_solve)  
        self.pre_non_linear_convergence_plot()

        LoadingScreen('SOLUTION IN PROGRESS', 'Solving the analysis',  target=self.process_analysis, project=project)
        self.post_non_linear_convergence_plot()  

        if self.project.preprocessor.stop_processing:
            self.reset_all_results()
            self.project.preprocessor.stop_processing = False
        else:
            LoadingScreen('SOLUTION IN PROGRESS', 'Post-processing the obtained results', target=self.post_process_results)
            self.exec()
            self.check_warnings()

    def pre_non_linear_convergence_plot(self):
        if isinstance(self.solve, SolutionAcoustic):
            if self.analysis_ID in [3,5,6]:
                if self.solve.non_linear:
                    fig = plt.figure(figsize=[8,6])
                    ax  = fig.add_subplot(1,1,1)
                    self.anime = FuncAnimation(fig, self.solve.graph_callback, fargs=(fig,ax), interval=2000)
                    self.anime._start()
                    plt.ion()
                    plt.show()

    def post_non_linear_convergence_plot(self):
        if isinstance(self.solve, SolutionAcoustic):
            if self.analysis_ID in [3,5,6]:
                if self.solve.non_linear:
                    self.anime._stop()

    def process_cross_sections(self):

        t0i = time()
        self.complete = False
        self.project.process_cross_sections_mapping()
        self.project.time_to_process_cross_sections = time() - t0i

    def preparing_mathematical_model_to_solve(self):

        t0 = time()
        if self.analysis_ID in [0,1,3,5,6]:
            if self.frequencies is None:
                return
            if len(self.frequencies) == 0:
                return

        if self.project.preprocessor._process_beam_nodes_and_indexes():
            if self.analysis_ID not in [0,1,2]:
                title = "INCORRECT ANALYSIS TYPE"
                message = "There are only BEAM_1 elements in the model, therefore, \nonly structural analysis are allowable."
                info_text = [title, message, window_title_2]
                PrintMessageInput(info_text)
                return

        if self.analysis_ID == 2:
            self.project.preprocessor.enable_fluid_mass_adding_effect(reset=True)
            self.solve = self.project.get_structural_solve()

        elif self.analysis_ID == 4:
            self.solve = self.project.get_acoustic_solve()

        elif self.analysis_ID == 3:
            self.solve = self.project.get_acoustic_solve()

        elif self.analysis_ID in [5,6]:
            self.project.preprocessor.enable_fluid_mass_adding_effect()
            self.solve = self.project.get_acoustic_solve()
            
        else:
            self.project.preprocessor.enable_fluid_mass_adding_effect(reset=True)
            self.solve = self.project.get_structural_solve()

        self.project.time_to_preprocess_model = time() - t0
       
    def process_analysis(self):
        
        t0 = time()

        if self.analysis_ID == 0:
            self.solution_structural = self.solve.direct_method(self.damping) # Structural Harmonic Analysis - Direct Method

        elif self.analysis_ID == 1: # Structural Harmonic Analysis - Mode Superposition Method
            self.solution_structural = self.solve.mode_superposition(self.modes, self.damping)

        elif self.analysis_ID == 3: # Acoustic Harmonic Analysis - Direct Method
            self.solution_acoustic, self.convergence_dataLog = self.solve.direct_method()

        elif self.analysis_ID == 5: # Coupled Harmonic Analysis - Direct Method
            
            t0_acoustic = time()
            self.solution_acoustic, self.convergence_dataLog = self.solve.direct_method() #Acoustic Harmonic Analysis - Direct Method
            self.project.time_to_solve_acoustic_model = time() - t0_acoustic
            
            self.project.set_acoustic_solution(self.solution_acoustic)
            self.solve = self.project.get_structural_solve()
            
            t0_structural = time()
            self.solution_structural = self.solve.direct_method(self.damping) #Coupled Harmonic Analysis - Direct Method
            self.project.time_to_solve_structural_model = time() - t0_structural
            
        elif self.analysis_ID == 6: # Coupled Harmonic Analysis - Mode Superposition Method
            
            t0_acoustic = time()
            self.solution_acoustic, self.convergence_dataLog = self.solve.direct_method() #Acoustic Harmonic Analysis - Direct Method
            self.project.time_to_solve_acoustic_model = time() - t0_acoustic
            
            self.project.set_acoustic_solution(self.solution_acoustic)
            self.solve = self.project.get_structural_solve()
            
            t0_structural = time()
            self.solution_structural = self.solve.mode_superposition(self.modes, self.damping)
            self.project.time_to_solve_structural_model = time() - t0_structural
            
        elif self.analysis_ID == 2: # Structural Modal Analysis
            self.natural_frequencies_structural, self.solution_structural = self.solve.modal_analysis(modes = self.modes, sigma=self.project.sigma)

        elif self.analysis_ID == 4: # Acoustic Modal Analysis
            self.natural_frequencies_acoustic, self.solution_acoustic = self.solve.modal_analysis(modes = self.modes, sigma=self.project.sigma)
        
        self.project.time_to_solve_model = time() - t0

        if isinstance(self.solve, SolutionAcoustic):
            if self.analysis_ID in [3,5,6]:
                if self.solve.non_linear:
                    sleep(2)

    def post_process_results(self): 

        t0 = time()
        self.project.set_perforated_plate_convergence_dataLog(self.convergence_dataLog)
        if self.analysis_ID == 2:
            
            if self.solution_structural is None:
                return

            self.project.set_structural_solution(self.solution_structural)
            self.project.set_structural_natural_frequencies(self.natural_frequencies_structural.tolist())

        elif self.analysis_ID == 4:
                    
            if self.solution_acoustic is None:
                return

            self.project.set_acoustic_solution(self.solution_acoustic)
            self.project.set_acoustic_natural_frequencies(self.natural_frequencies_acoustic.tolist())
        
        elif self.analysis_ID == 3:

            if self.solution_acoustic is None:
                return

            self.project.set_acoustic_solution(self.solution_acoustic)
        
        elif self.analysis_ID in [0,1,5,6]:
            
            if self.solution_structural is None:
                return

            self.project.set_structural_solve(self.solve)
            self.project.set_structural_solution(self.solution_structural)
            self.dict_reactions_at_constrained_dofs = self.solve.get_reactions_at_fixed_nodes(self.damping)
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = self.solve.get_reactions_at_springs_and_dampers()
            self.project.set_structural_reactions([ self.dict_reactions_at_constrained_dofs,
                                                    self.dict_reactions_at_springs,
                                                    self.dict_reactions_at_dampers  ])
        
        save = SaveData(self.project)
        # read = ReadData(self.project)

        self.project.time_to_postprocess = time() - t0
        _times =  [self.project.time_to_process_cross_sections, self.project.time_to_preprocess_model, self.project.time_to_solve_model, self.project.time_to_postprocess]
        self.project.total_time = sum(_times)
        self.print_final_log()
        self.complete = True

    def check_warnings(self):
        # WARNINGS REACHED DURING SOLUTION
        title = self.analysis_type_label
        message = ""
        if self.analysis_type_label == "Harmonic Analysis - Structural":
            if self.solve.flag_ModeSup_prescribed_NonNull_DOFs:
                message = self.solve.warning_ModeSup_prescribedDOFs
            if self.solve.flag_Clump and self.analysis_ID==1:
                message = self.solve.warning_Clump[0]
        if self.analysis_type_label == "Modal Analysis - Structural":
            if self.solve.flag_Modal_prescribed_NonNull_DOFs:
                message = self.solve.warning_Modal_prescribedDOFs[0] 
        if message != "":
            PrintMessageInput([title, message, window_title_2])

    def reset_all_results(self):

        self.solution_structural = None
        self.solution_acoustic = None

        if self.analysis_ID == 2:
            self.project.set_structural_solution(None)
            self.project.set_structural_natural_frequencies(None)
        elif self.analysis_ID == 4: 
            self.project.set_acoustic_solution(None)
            self.project.set_acoustic_natural_frequencies(None)
        elif self.analysis_ID == 3:
            self.project.set_acoustic_solution(None)
        elif self.analysis_ID in [0,1,5,6]:
            self.project.set_acoustic_solution(None)
            self.project.set_structural_solution(None)
            self.project.set_structural_reactions([ {}, {}, {} ])

    def config_title_font(self):
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setItalic(True)
        font.setFamily("Arial")
        # font.setWeight(60)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color:black")

    def config_message_font(self):
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        # font.setItalic(True)
        font.setFamily("Arial")
        # font.setWeight(60)
        self.label_message.setFont(font)
        self.label_message.setStyleSheet("color:blue")

    def print_final_log(self):

        text = "Solution finished!\n\n"
        # text += "Time to check all entries: {} [s]\n".format(round(self.project.time_to_checking_entries, 6))
        text += "Time to load/create the project: {} [s]\n".format(round(self.project.time_to_load_or_create_project, 4))
        text += "Time to process cross-sections: {} [s]\n".format(round(self.project.time_to_process_cross_sections, 4))
        text += "Time elapsed in pre-processing: {} [s]\n".format(round(self.project.time_to_preprocess_model, 4))
        if self.analysis_ID in [5,6]:
            text += "Time to solve the acoustic model: {} [s]\n".format(round(self.project.time_to_solve_acoustic_model, 4))
            text += "Time to solve the structural model: {} [s]\n".format(round(self.project.time_to_solve_structural_model, 4))
        else:
            text += "Time to solve the model: {} [s]\n".format(round(self.project.time_to_solve_model, 4))
        text += "Time elapsed in post-processing: {} [s]\n\n".format(round(self.project.time_to_postprocess, 4))
        text += "Total time elapsed: {} [s]\n\n\n".format(round(self.project.total_time, 4))

        text += "Press ESC to continue..."
        self.label_message.setText(text)


    # def check_log_times(self):
    #     #
    #     if self.project.time_to_load_or_create_project is None:
    #         self.project.time_to_load_or_create_project = 0
    #     #
    #     if self.project.time_to_process_cross_sections is None:
    #         self.project.time_to_process_cross_sections = 0
    #     #
    #     if self.project.time_to_preprocess_model is None:
    #         self.project.time_to_preprocess_model = 0
    #     #
    #     if self.project.time_to_solve_acoustic_model is None:
    #         self.project.time_to_solve_acoustic_model = 0
    #     #
    #     if self.project.time_to_solve_structural_model is None:
    #         self.project.time_to_solve_structural_model = 0
    #     #
    #     if self.project.time_to_solve_model is None:
    #         self.project.time_to_solve_model = 0
    #     #
    #     if self.project.time_to_postprocess is None:
    #         self.project.time_to_postprocess = 0
    #     #
    #     if self.project.total_time is None:
    #         self.project.total_time = 0
