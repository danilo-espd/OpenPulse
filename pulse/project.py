from PyQt5.QtWidgets import QProgressBar, QLabel
from pulse.utils import get_new_path
from pulse.preprocessing.preprocessor import Preprocessor
from pulse.processing.solution_structural import SolutionStructural
from pulse.processing.solution_acoustic import SolutionAcoustic
from pulse.preprocessing.entity import Entity
from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.cross_section import CrossSection
from pulse.projectFile import ProjectFile
from data.user_input.model.setup.structural.expansionJointInput import get_list_cross_sections_to_plot_expansion_joint
from data.user_input.project.printMessageInput import PrintMessageInput

import numpy as np
import configparser
from collections import defaultdict
import os

window_title = "ERROR"

class Project:
    def __init__(self):

        self._project_name = ""
        self.project_folder_path = ""

        #Analysis
        self.reset_info()
        # self.analysis_ID = None
        # self.analysis_type_label = ""
        # self.analysis_method_label = ""
        # self.global_damping = [0,0,0,0]
        # self.modes = 0
        # self.frequencies = None
        # self.f_min = 0
        # self.f_max = 0
        # self.f_step = 0
        # self.natural_frequencies_structural = []
        # self.solution_structural = None
        # self.solution_acoustic = None
        # self.flag_set_material = False
        # self.flag_set_crossSection = False
        # self.plot_pressure_field = False
        # self.plot_stress_field = False
        # self.is_file_loaded = False
        # self.setup_analysis_complete = False
        # self.none_project_action = False

        # self.time_to_load_or_create_project = None
        # self.time_to_checking_entries = None 
        # self.time_to_process_cross_sections = None
        # self.time_to_preprocess_model = None
        # self.time_to_solve_model = None
        # self.time_to_solve_acoustic_model = None
        # self.time_to_solve_structural_model = None
        # self.time_to_postprocess = None
        # self.total_time = None

        # self.number_sections_by_line = {}
        # self.lines_with_cross_section_by_elements = []
        # self.stresses_values_for_color_table = None
        # self.min_stress = ""
        # self.max_stress = ""
        # self.stress_label = ""

    def reset_info(self):

        self.preprocessor = Preprocessor()
        self.file = ProjectFile()

        self.analysis_ID = None
        self.analysis_type_label = ""
        self.analysis_method_label = ""
        self.global_damping = [0,0,0,0]
        self.modes = 0
        self.frequencies = None
        self.f_min = 0
        self.f_max = 0
        self.f_step = 0
        self.natural_frequencies_structural = []
        self.solution_structural = None
        self.solution_acoustic = None
        self.flag_set_material = False
        self.flag_set_crossSection = False
        self.plot_pressure_field = False
        self.plot_stress_field = False
        self.is_file_loaded = False
        self.setup_analysis_complete = False
        self.none_project_action = False

        self.time_to_load_or_create_project = None
        self.time_to_checking_entries = None
        self.time_to_process_cross_sections = None
        self.time_to_preprocess_model = None
        self.time_to_solve_model = None
        self.time_to_solve_acoustic_model = None
        self.time_to_solve_structural_model = None
        self.time_to_postprocess = None
        self.total_time = None

        self.number_sections_by_line = {}
        self.lines_with_cross_section_by_elements = []
        self.stresses_values_for_color_table = None
        self.min_stress = ""
        self.max_stress = ""
        self.stress_label = ""

    def new_project(self, project_folder_path, project_name, element_size, geometry_tolerance, import_type, material_list_path, fluid_list_path, geometry_path = "", coord_path = "", conn_path = ""):
        
        self.reset_info()
        self.file.new(project_folder_path, project_name, element_size, geometry_tolerance, import_type, material_list_path, fluid_list_path, geometry_path, coord_path, conn_path)
        self._project_name = project_name
        self.project_folder_path = project_folder_path

        self.process_geometry_and_mesh()
        self.entities = self.preprocessor.dict_tag_to_entity.values()
        self.file.create_entity_file(self.preprocessor.all_lines)

    def copy_project(self, project_folder_path, project_name, material_list_path, fluid_list_path, geometry_path = "", coord_path = "", conn_path = ""):
        self.file.copy(project_folder_path, project_name, material_list_path, fluid_list_path, geometry_path, coord_path, conn_path)
        self._project_name = project_name
         
    def load_project(self, project_file_path):
        self.initial_load_project_actions(project_file_path)
        self.load_project_files()
    
    def initial_load_project_actions(self, project_file_path):
        self.reset_info()
        self.file.load(project_file_path)
        self._project_name = self.file._project_name
        self.project_folder_path = os.path.dirname(project_file_path)
        self.process_geometry_and_mesh()
        self.entities = self.preprocessor.dict_tag_to_entity.values()

    def load_project_files(self):
        self.load_structural_bc_file()
        self.load_acoustic_bc_file()
        self.load_entity_file()
        self.load_analysis_file()
        if self.file.temp_table_name is not None:
            self.load_frequencies_from_table()

    def update_node_ids_in_file_after_remesh(self, dict_old_to_new_extenal_indexes):
        # print(f"Dictionary: \n {dict_old_to_new_extenal_indexes}")
        self.file.modify_node_ids_in_acoustic_bc_file(dict_old_to_new_extenal_indexes)
        self.file.modify_node_ids_in_structural_bc_file(dict_old_to_new_extenal_indexes)

    def reset_project(self):
        self.reset_info()
        self.remove_all_unnecessary_files()
        self.file.reset_project_setup()
        self.process_geometry_and_mesh()
        self.file.create_entity_file(self.preprocessor.all_lines)

    def remove_all_unnecessary_files(self):
        list_filenames = os.listdir(self.file._project_path).copy()
        geometry_filename = os.path.basename(self.file._geometry_path)
        for filename in list_filenames:
            if filename not in ["entity.dat", "fluidList.dat", "materialList.dat", "project.ini", geometry_filename]:
                file_path = get_new_path(self.file._project_path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)

    def process_geometry_and_mesh(self):
        if self.file.get_import_type() == 0:
            self.preprocessor.generate(self.file.geometry_path, self.file.element_size)
        elif self.file.get_import_type() == 1:
            self.preprocessor.load_mesh(self.file.coord_path, self.file.conn_path)
  
    def set_entity(self, tag):
        return Entity(tag)

    def load_entity_file(self):
        self.lines_with_cross_section_by_elements = []
        self.number_sections_by_line = {}
        self.file.get_dict_of_entities_from_file()
        dict_structural_element_type = self.file.dict_structural_element_type
        dict_acoustic_element_types = self.file.dict_acoustic_element_type
        dict_element_length_correction = self.file.dict_length_correction
        dict_element_perforated_plate = self.file.dict_perforated_plate
        dict_materials = self.file.dict_material
        dict_cross_sections = self.file.dict_cross
        dict_variable_sections = self.file.dict_variable_sections
        dict_beam_xaxis_rotation = self.file.dict_beam_xaxis_rotation
        dict_fluids = self.file.dict_fluid
        dict_element_length_correction = self.file.dict_length_correction
        dict_capped_end = self.file.dict_capped_end
        dict_stress_stiffening = self.file.dict_stress_stiffening
        dict_B2PX_rotation_decoupling = self.file.dict_B2XP_rotation_decoupling
        dict_expansion_joint = self.file.dict_expansion_joint_parameters
        
        # Structural element type to the entities
        for key, el_type in dict_structural_element_type.items():
            if self.file.element_type_is_structural:
                self.load_structural_element_type_by_entity(key, el_type)

        # Acoustic element type to the entities
        for key, [el_type, hysteretic_damping] in dict_acoustic_element_types.items():
            if self.file.element_type_is_acoustic:
                self.load_acoustic_element_type_by_entity(key, el_type, hysteretic_damping=hysteretic_damping)

        # Length correction to the elements
        for key, value in dict_element_length_correction.items():
            self.load_length_correction_by_elements(value[0], value[1], key)

        for key, value in dict_element_perforated_plate.items():
            self.load_perforated_plate_by_elements(value[0], value[1], key)

        # Material to the entities
        for key, mat in dict_materials.items():
            self.load_material_by_entity(key, mat)

        # Fluid to the entities
        for key, fld in dict_fluids.items():
            self.load_fluid_by_entity(key, fld)

        # Straight Cross-section to the entities
        for key, cross in dict_cross_sections.items():
            if "-" in key:
                self.load_cross_section_by_element(cross[1], cross[0])
                prefix_key = int(key.split("-")[0])
                if prefix_key in list(self.number_sections_by_line.keys()):
                    self.number_sections_by_line[prefix_key] += 1
                else:
                    self.number_sections_by_line[prefix_key] = 1
            else:
                self.load_cross_section_by_entity(int(key), cross)
        
        # Variable Cross-section to the entities
        for key, value in dict_variable_sections.items():
            self.load_variable_cross_section_by_entity(int(key), value)

        # Beam X-axis rotation to the entities
        for key, angle in dict_beam_xaxis_rotation.items():
            self.load_beam_xaxis_rotation_by_entity(key, angle)
        if len(dict_beam_xaxis_rotation) > 0:
            self.preprocessor.process_all_rotation_matrices() 

        # B2PX Rotation Decoupling
        for key, item in dict_B2PX_rotation_decoupling.items():
            if "B2PX ROTATION DECOUPLING" in str(key):
                self.preprocessor.dict_B2PX_rotation_decoupling[str(item[2])] = [item[0], item[1], key]
                for i in range(len(item[0])):
                    self.load_B2PX_rotation_decoupling(item[0][i], item[1][i], rotations_to_decouple=item[2])

        # Expansion Joint to the entities
        for key, parameters in dict_expansion_joint.items():
            self.load_expansion_joint_by_line(key, parameters)
        
        # Stress Stiffening to the entities and elements
        for key, parameters in dict_stress_stiffening.items():
            if "STRESS STIFFENING" in str(key):
                self.load_stress_stiffening_by_elements(parameters[0], parameters[1], section=key)
            else:
                self.load_stress_stiffening_by_entity(key, parameters)        

        # Capped end to the entities and elements
        for key, group in dict_capped_end.items():
            if "CAPPED END" in key:  
                self.load_capped_end_by_elements(group, True, key)
            elif "True" in key:
                self.load_capped_end_by_entity(group, True, key)

    def load_mapped_cross_section(self):  

        label_etypes = ['pipe_1', 'pipe_2', 'beam_1']
        indexes = [0, 1, 2]
        dict_etype_index = dict(zip(label_etypes,indexes))
        dict_index_etype = dict(zip(indexes,label_etypes))
        map_cross_section_to_elements = defaultdict(list)

        for index, element in self.preprocessor.structural_elements.items():

            e_type  = element.element_type
            if e_type in ['beam_1','expansion_joint']:
                continue
            elif e_type is None:
                e_type = 'pipe_1'
                self.acoustic_analysis = True
            index_etype = dict_etype_index[e_type]

            poisson = element.material.poisson_ratio
            if poisson is None:
                poisson = 0

            outer_diameter = element.cross_section.outer_diameter
            thickness = element.cross_section.thickness
            offset_y = element.cross_section.offset_y
            offset_z = element.cross_section.offset_z
            insulation_thickness = element.cross_section.insulation_thickness
            insulation_density = element.cross_section.insulation_density
        
            map_cross_section_to_elements[str([ outer_diameter, 
                                                thickness, 
                                                offset_y, 
                                                offset_z, 
                                                poisson, 
                                                index_etype, 
                                                insulation_thickness, 
                                                insulation_density ])].append(index)
        # print(len(map_cross_section_to_elements))
            
        for key, elements in map_cross_section_to_elements.items():

            cross_strings = key[1:-1].split(',')
            vals = [float(value) for value in cross_strings]
            el_type = dict_index_etype[vals[5]]

            section_parameters = {  "outer_diameter" : vals[0],
                                    "thickness" : vals[1], 
                                    "offset_y" : vals[2], 
                                    "offset_z" : vals[3], 
                                    "insulation_thickness" : vals[6], 
                                    "insulation_density" : vals[7] }

            pipe_section_info = {   "section_type_label" : "Pipe section",
                                    "section_parameters" : section_parameters }

            if el_type in ['pipe_1', 'pipe_2']:

                cross_section = CrossSection(pipe_section_info=pipe_section_info)                                

                if self.analysis_ID in [3,4]:
                    self.preprocessor.set_cross_section_by_element(elements, cross_section, update_cross_section=False)  
                else:
                    self.preprocessor.set_cross_section_by_element(elements, cross_section, update_cross_section=True)  

    def get_dict_multiple_cross_sections(self):
        '''This methods updates the file information of multiples cross-sections
        
        '''
        if len(self.lines_with_cross_section_by_elements)==0:
            return

        for line in self.lines_with_cross_section_by_elements:
            dict_multiple_cross_sections = defaultdict(list)
            list_elements = self.preprocessor.line_to_elements[line]
            elements = self.preprocessor.structural_elements
            count_sections = 0

            for element_id in list_elements:

                outer_diameter = elements[element_id].cross_section.outer_diameter
                thickness = elements[element_id].cross_section.thickness
                offset_y = elements[element_id].cross_section.offset_y
                offset_z = elements[element_id].cross_section.offset_z
                insultation_thickness = elements[element_id].cross_section.insulation_thickness
                insultation_density = elements[element_id].cross_section.insulation_density
                key_string = str([  outer_diameter, 
                                    thickness, 
                                    offset_y, 
                                    offset_z, 
                                    insultation_thickness, 
                                    insultation_density])

                if key_string not in list(dict_multiple_cross_sections.keys()):
                    count_sections += 1
                dict_multiple_cross_sections[key_string].append(element_id)
    
            if len(dict_multiple_cross_sections) == 1:
                if count_sections == 1:
                    _cross_section = elements[element_id].cross_section
                    self.set_cross_section_by_line(line, _cross_section)
                    self.number_sections_by_line.pop(line)
            else:
                self.number_sections_by_line[line] = count_sections
                self.file.add_multiple_cross_section_in_file(line, dict_multiple_cross_sections)     

    def load_structural_bc_file(self):

        [   prescribed_dofs, 
            external_loads, 
            mass, 
            spring, 
            damper, 
            elastic_link_stiffness, 
            elastic_link_damping    ] = self.file.get_dict_of_structural_bc_from_file()

        title = "ERROR WHILE LOADING STRUCTURAL DATA"
        
        for key, dofs in prescribed_dofs.items():
            if isinstance(dofs, list):
                try:
                    self.load_prescribed_dofs_bc_by_node(key, dofs)
                except Exception:
                    message = "There is some error while loading prescribed dofs data." 
                    PrintMessageInput([title, message, window_title])

        for key, loads in external_loads.items():
            if isinstance(loads, list):
                try:
                    self.load_structural_loads_by_node(key, loads)
                except Exception:
                    message = "There is some error while loading nodal loads data." 
                    PrintMessageInput([title, message, window_title])

        for key, masses in mass.items():
            if isinstance(masses, list):
                try:
                    self.load_mass_by_node(key, masses)
                except Exception:
                    message = "There is some error while loading lumped masses/moments of inertia data."
                    PrintMessageInput([title, message, window_title])
                
        for key, stiffness in spring.items():
            if isinstance(stiffness, list):
                try:
                    self.load_spring_by_node(key, stiffness)
                except Exception:
                    message = "There is some error while loading lumped stiffness data." 
                    PrintMessageInput([title, message, window_title])  

        for key, dampings in damper.items():
            if isinstance(dampings, list):
                try:
                    self.load_damper_by_node(key, dampings)
                except Exception:
                    message = "There is some error while loading lumped damping data." 
                    PrintMessageInput([title, message, window_title]) 

        for key, stiffness_data in elastic_link_stiffness.items():
            if isinstance(stiffness_data, list):
                nodes = [int(node) for node in key.split("-")]
                try:
                    self.load_elastic_nodal_link_stiffness(nodes, stiffness_data)
                except Exception:
                    message = "There is some error while loading elastic nodal link stiffness data." 
                    PrintMessageInput([title, message, window_title]) 

        for key, damping_data in elastic_link_damping.items():
            if isinstance(damping_data, list):
                nodes = [int(node) for node in key.split("-")]
                try:
                    self.load_elastic_nodal_link_damping(nodes, damping_data)
                except Exception:
                    message = "There is some error while loading elastic nodal link damping data." 
                    PrintMessageInput([title, message, window_title]) 

    def load_acoustic_bc_file(self):
        pressure, volume_velocity, specific_impedance, radiation_impedance = self.file.get_dict_of_acoustic_bc_from_file()
        for key, ActPres in pressure.items():
            if ActPres is not None:
                self.load_acoustic_pressure_bc_by_node(key, ActPres)
        for key, data in volume_velocity.items():
            for VelVol, additional_info in data:
                if VelVol is not None:
                    self.load_volume_velocity_bc_by_node(key, VelVol, additional_info=additional_info)
        for key, SpecImp in specific_impedance.items():
            if SpecImp is not None:
                self.load_specific_impedance_bc_by_node(key, SpecImp)
        for key, RadImp in radiation_impedance.items():
            if RadImp is not None:
                self.load_radiation_impedance_bc_by_node(key, RadImp)

    def load_analysis_file(self):
        self.f_min, self.f_max, self.f_step, self.global_damping = self.file.load_analysis_file()

    def load_frequencies_from_table(self):
        self.f_min, self.f_max, self.f_step = self.file.f_min, self.file.f_max, self.file.f_step
        self.frequencies = self.file.frequencies 

    def set_material(self, material):
        self.preprocessor.set_material_by_element('all', material)
        self._set_material_to_all_entities(material)
        for line in self.preprocessor.all_lines:
            self.file.add_material_in_file(line, material.identifier)

    def set_material_by_line(self, entity_id, material):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_material_by_line(entity_id, material)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_material_by_element('all', material)

        self._set_material_to_selected_entity(entity_id, material)
        self.file.add_material_in_file(entity_id, material.identifier)

    def set_cross_section_to_all(self, cross_section):
        self.preprocessor.set_cross_section_by_element('all', cross_section)
        self._set_cross_section_to_all_entities(cross_section)
        for line in self.preprocessor.all_lines:
            self.file.add_cross_section_in_file(line, cross_section)

    def set_cross_section_by_elements(self, elements, cross_section):
        self.preprocessor.set_cross_section_by_element(elements, cross_section)
        dict_elements_to_line = self.preprocessor.elements_to_line
        for element in elements:
            line = dict_elements_to_line[element]
            if line not in self.lines_with_cross_section_by_elements:
                self.lines_with_cross_section_by_elements.append(line)

    def set_cross_section_by_line(self, line_id, cross_section):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_cross_section_by_line(line_id, cross_section)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_cross_section_by_element('all', cross_section)

        self._set_cross_section_to_selected_entity(line_id, cross_section)
        self.file.add_cross_section_in_file(line_id, cross_section)

    def set_variable_cross_section_by_line(self, line_id, parameters):
        self._set_variable_cross_section_to_selected_entity(line_id, parameters)
        self.file.modify_variable_cross_section_in_file(line_id, parameters)
    
    def set_structural_element_type_to_all(self, element_type):
        self.preprocessor.set_structural_element_type_by_element('all', element_type)
        self._set_structural_element_type_to_all_entities(element_type)
        for line in self.preprocessor.all_lines:
            self.file.modify_structural_element_type_in_file(line, element_type)

    def set_structural_element_type_by_entity(self, entity_id, element_type):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_structural_element_type_by_line(entity_id, element_type)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_structural_element_type_by_element('all', element_type)

        self._set_structural_element_type_to_selected_entity(entity_id, element_type)
        self.file.modify_structural_element_type_in_file(entity_id, element_type)
        
    def set_acoustic_element_type_to_all(self, element_type, hysteretic_damping=None):
        self.preprocessor.set_acoustic_element_type_by_element('all', element_type, hysteretic_damping=hysteretic_damping)
        self._set_acoustic_element_type_to_all_entities(element_type, hysteretic_damping=hysteretic_damping)
        for line_id in self.preprocessor.all_lines:
            self.file.modify_acoustic_element_type_in_file(line_id, element_type, hysteretic_damping=hysteretic_damping)

    def set_acoustic_element_type_by_line(self, entity_id, element_type, hysteretic_damping=None):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_acoustic_element_type_by_line(entity_id, element_type, hysteretic_damping=hysteretic_damping)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_acoustic_element_type_by_element('all', element_type, hysteretic_damping=hysteretic_damping)

        self._set_acoustic_element_type_to_selected_entity(entity_id, element_type, hysteretic_damping=hysteretic_damping)
        self.file.modify_acoustic_element_type_in_file(entity_id, element_type, hysteretic_damping=hysteretic_damping)

    def set_beam_xaxis_rotation_by_line(self, line_id, delta_angle):
        self.preprocessor.set_beam_xaxis_rotation_by_line(line_id, delta_angle)
        angle = self.preprocessor.dict_lines_to_rotation_angles[line_id]
        self._set_beam_xaxis_rotation_to_selected_entity(line_id, angle)
        self.file.modify_beam_xaxis_rotation_by_lines_in_file(line_id, angle)

    def set_prescribed_dofs_bc_by_node(self, node_id, values, imported_table, table_name=""):
        self.preprocessor.set_prescribed_dofs_bc_by_node(node_id, values)
        labels = ["displacements", "rotations"]
        if imported_table:
            values = table_name
        self.file.add_structural_bc_in_file(node_id, values, labels)

    def set_B2PX_rotation_decoupling(self, element_id, node_id, rotations_mask, remove=False):
        self.preprocessor.set_B2PX_rotation_decoupling(element_id, node_id, rotations_to_decouple=rotations_mask, remove=remove)
        count_add, count_remove = 0, 0
        temp_dict = self.preprocessor.dict_elements_with_B2PX_rotation_decoupling.copy()

        for key, elements in temp_dict.items():
            count_add += 1
            section_key = "B2PX ROTATION DECOUPLING || Selection-{}".format(count_add-count_remove)              
            nodes = self.preprocessor.dict_nodes_with_B2PX_rotation_decoupling[key] 

            if elements != []:   
                self.file.modify_B2PX_rotation_decoupling_in_file(elements, nodes, key, section_key)
                self.preprocessor.dict_B2PX_rotation_decoupling[key] = [elements, nodes, section_key]

            elif elements == [] or rotations_mask==str([False, False, False]):
                count_remove += 1
                self.file.modify_B2PX_rotation_decoupling_in_file(elements, nodes, key, section_key, remove=True)
                self.preprocessor.dict_nodes_with_B2PX_rotation_decoupling.pop(key)
                self.preprocessor.dict_elements_with_B2PX_rotation_decoupling.pop(key)
                self.preprocessor.dict_B2PX_rotation_decoupling.pop(key)

    def reset_B2PX_totation_decoupling(self):
        N = self.preprocessor.DOFS_ELEMENT
        mat_reset = np.ones((N,N), dtype=int)
        for list_elements in self.preprocessor.dict_elements_with_B2PX_rotation_decoupling.values():
            for element_ID in list_elements:
                element = self.preprocessor.structural_elements[element_ID]
                element.decoupling_matrix = mat_reset
                element.decoupling_info = None
        self.preprocessor.dict_nodes_with_B2PX_rotation_decoupling = {}
        self.preprocessor.dict_elements_with_B2PX_rotation_decoupling = {}
        self.file.modify_B2PX_rotation_decoupling_in_file([], [], [], [], reset=True)

    def set_loads_by_node(self, node_id, values, imported_table, table_name=""):
        self.preprocessor.set_structural_load_bc_by_node(node_id, values)
        labels = ["forces", "moments"]
        if imported_table:
            values = table_name
        self.file.add_structural_bc_in_file(node_id, values, labels)

    def add_lumped_masses_by_node(self, node_id, values, imported_table, table_name=""):
        self.preprocessor.add_mass_to_node(node_id, values)
        labels = ["masses", "moments of inertia"]
        if imported_table:
            values = table_name
        self.file.add_structural_bc_in_file(node_id, values, labels)

    def add_lumped_stiffness_by_node(self, node_id, values, imported_table, table_name=""):
        self.preprocessor.add_spring_to_node(node_id, values)
        labels = ["spring stiffness", "torsional spring stiffness"]
        if imported_table:
            values = table_name
        self.file.add_structural_bc_in_file(node_id, values, labels)

    def add_lumped_dampings_by_node(self, node_id, values, imported_table, table_name=""):
        self.preprocessor.add_damper_to_node(node_id, values)
        labels = ["damping coefficients", "torsional damping coefficients"]
        if imported_table:
            values = table_name        
        self.file.add_structural_bc_in_file(node_id, values, labels)

    def add_elastic_nodal_link_stiffness(self, nodeID_1, nodeID_2, parameters, imported_table, table_name=""):
        min_node_ID = min(nodeID_1, nodeID_2)
        max_node_ID = max(nodeID_1, nodeID_2)
        self.preprocessor.add_elastic_nodal_link(min_node_ID, max_node_ID, parameters, _stiffness=True)
        labels = ["connecting stiffness", "connecting torsional stiffness"]
        section_string = ["{}-{}".format(min_node_ID, max_node_ID)]
        if imported_table:
            values = table_name
        else:
            values = parameters
        self.file.add_structural_bc_in_file(section_string, values, labels)

    def add_elastic_nodal_link_damping(self, nodeID_1, nodeID_2, parameters, imported_table, table_name=""):
        min_node_ID = min(nodeID_1, nodeID_2)
        max_node_ID = max(nodeID_1, nodeID_2)
        self.preprocessor.add_elastic_nodal_link(min_node_ID, max_node_ID, parameters, _damping=True)
        labels = ["connecting damping", "connecting torsional damping"]
        section_string = ["{}-{}".format(min_node_ID, max_node_ID)]
        if imported_table:
            values = table_name
        else:
            values = parameters
        self.file.add_structural_bc_in_file(section_string, values, labels)

    def add_expansion_joint_by_line(self, lineID, parameters, imported_table, list_table_names=[]):
        self.preprocessor.add_expansion_joint_by_line(lineID, parameters)
        self.set_structural_element_type_by_entity(lineID, "expansion_joint")
        # self.set_cross_section_by_line(lineID, None)  
        self._set_expansion_joint_to_selected_entity(lineID, parameters)
        if imported_table:
            self.file.modify_expansion_joint_in_file(lineID, parameters, list_table_names=list_table_names) 
        else:
            self.file.modify_expansion_joint_in_file(lineID, parameters)   
           

    def add_expansion_joint_by_elements(self, list_elements, _parameters):
        parameters = _parameters
        self.preprocessor.add_expansion_joint_by_elements(list_elements, parameters)
        self.preprocessor.set_structural_element_type_by_element(list_elements, "expansion_joint")

    def set_stress_stiffening_by_elements(self, elements, parameters, section, remove=False):
        self.preprocessor.set_stress_stiffening_by_elements(elements, parameters, section=section, remove=remove)
        self.file.modify_stress_stiffnening_element_in_file(elements, parameters, section, remove=remove)

    def set_stress_stiffening_by_line(self, lines, parameters, remove=False):
        
        if isinstance(lines, int):
            lines = [lines]
        
        if self.file.get_import_type() == 0:
            self.preprocessor.set_stress_stiffening_by_line(lines, parameters, remove=remove)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_stress_stiffening_by_elements('all', parameters)
        
        for line in lines:    
            if remove:
                self._set_stress_stiffening_to_selected_entity(line, [None, None, None, None])
                self.file.modify_stress_stiffnening_entity_in_file(line, [], remove=True)
            else:
                self._set_stress_stiffening_to_selected_entity(line, parameters)
                self.file.modify_stress_stiffnening_entity_in_file(line, parameters)

    def set_stress_stiffening_to_all_lines(self, parameters):
        self.preprocessor.set_stress_stiffening_by_elements('all', parameters)
        self._set_stress_stiffening_to_all_entities(parameters)
        for line in self.preprocessor.all_lines:
            self.file.modify_stress_stiffnening_entity_in_file(line, parameters)

    def load_material_by_entity(self, entity_id, material):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_material_by_line(entity_id, material)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_material_by_element('all', material)
        self._set_material_to_selected_entity(entity_id, material)
    
    def load_stress_stiffening_by_elements(self, elements_id, parameters, section=None):
        self.preprocessor.set_stress_stiffening_by_elements(elements_id, parameters, section=section)

    def load_stress_stiffening_by_entity(self, entity_id, parameters):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_stress_stiffening_by_line(entity_id, parameters)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_fluid_by_element('all', parameters)
        self._set_fluid_to_selected_entity(entity_id, parameters)

    def load_fluid_by_entity(self, entity_id, fluid):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_fluid_by_line(entity_id, fluid)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_fluid_by_element('all', fluid)
        self._set_fluid_to_selected_entity(entity_id, fluid)

    def load_cross_section_by_element(self, elements_id, cross_section):
        self.preprocessor.set_cross_section_by_element(elements_id, cross_section)

    def load_cross_section_by_entity(self, entity_id, cross_section):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_cross_section_by_line(entity_id, cross_section)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_cross_section_by_element('all', cross_section)
        self._set_cross_section_to_selected_entity(entity_id, cross_section)

    def load_variable_cross_section_by_entity(self, entity_id, data):
        self._set_variable_cross_section_to_selected_entity(entity_id, data)

    def load_expansion_joint_by_line(self, line_id, data):
        self.preprocessor.add_expansion_joint_by_line(line_id, data)
        self._set_expansion_joint_to_selected_entity(line_id, data)
        list_elements = self.preprocessor.line_to_elements[line_id]
        list_cross_sections = get_list_cross_sections_to_plot_expansion_joint(  list_elements, 
                                                                                data[0][1]  )
        self._set_cross_section_to_selected_entity(line_id, list_cross_sections[0])
        self.preprocessor.set_cross_section_by_element(list_elements, list_cross_sections)
    
    def load_beam_xaxis_rotation_by_entity(self, line_id, angle):
        self.preprocessor.set_beam_xaxis_rotation_by_line(line_id, angle)
        self._set_beam_xaxis_rotation_to_selected_entity(line_id, angle)

    def load_structural_element_type_by_entity(self, entity_id, element_type):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_structural_element_type_by_line(entity_id, element_type)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_structural_element_type_by_element('all', element_type)
        self._set_structural_element_type_to_selected_entity(entity_id, element_type)

    def load_acoustic_element_type_by_entity(self, entity_id, element_type, hysteretic_damping=None):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_acoustic_element_type_by_line(entity_id, element_type, hysteretic_damping=hysteretic_damping)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_acoustic_element_type_by_element('all', element_type, hysteretic_damping=hysteretic_damping)
        self._set_acoustic_element_type_to_selected_entity(entity_id, element_type, hysteretic_damping=hysteretic_damping)

    def load_structural_loads_by_node(self, node_id, values):
        self.preprocessor.set_structural_load_bc_by_node(node_id, values)

    def load_mass_by_node(self, node_id, mass):
        self.preprocessor.add_mass_to_node(node_id, mass)

    def load_spring_by_node(self, node_id, stiffness):
        self.preprocessor.add_spring_to_node(node_id, stiffness)

    def load_damper_by_node(self, node_id, dampings):
        self.preprocessor.add_damper_to_node(node_id, dampings)

    def load_elastic_nodal_link_stiffness(self, nodes, stiffness_info):
        self.preprocessor.add_elastic_nodal_link(nodes[0], nodes[1], stiffness_info, _stiffness=True)
    
    def load_elastic_nodal_link_damping(self, nodes, damping_info):
        self.preprocessor.add_elastic_nodal_link(nodes[0], nodes[1], damping_info, _damping=True)

    def load_B2PX_rotation_decoupling(self, element_ID, node_ID, rotations_to_decouple):
        self.preprocessor.set_B2PX_rotation_decoupling(element_ID, node_ID, rotations_to_decouple=rotations_to_decouple)
    
    def load_capped_end_by_elements(self, elements, value, selection):
        self.preprocessor.set_capped_end_by_elements(elements, value, selection)

    def load_capped_end_by_entity(self, lines, value, selection):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_capped_end_by_line(lines, value)
        # elif self.file.get_import_type() == 1:
        #     self.preprocessor.set_capped_end_by_element('all', value)

    def get_nodes_bc(self):
        return self.preprocessor.nodes_with_prescribed_dofs

    def get_structural_elements(self):
        return self.preprocessor.structural_elements
    
    def get_structural_element(self, element_id):
        return self.preprocessor.structural_elements[element_id]

    def get_acoustic_elements(self):
        return self.preprocessor.acoustic_elements    

    def get_acoustic_element(self, element_id):
        return self.preprocessor.acoustic_elements[element_id]

    def set_frequencies(self, frequencies, min_, max_, step_):
        if max_ != 0 and step_ != 0:
            self.f_min, self.f_max, self.f_step = min_, max_, step_
            self.file.add_frequency_in_file(min_, max_, step_)
        self.frequencies = frequencies

    def load_prescribed_dofs_bc_by_node(self, node_id, bc):
        self.preprocessor.set_prescribed_dofs_bc_by_node(node_id, bc)

    def _set_material_to_selected_entity(self, entity_id, material):
        entity = self.preprocessor.dict_tag_to_entity[entity_id]
        entity.material = material

    def _set_material_to_all_entities(self, material):
        for entity in self.entities:
            entity.material = material

    def _set_fluid_to_selected_entity(self, line_id, fluid):
        entity = self.preprocessor.dict_tag_to_entity[line_id]
        if entity.structural_element_type not in ['beam_1']:
            entity.fluid = fluid
        else:
            entity.fluid = None

    def _set_fluid_to_all_entities(self, fluid):
        for entity in self.entities:
            if entity.structural_element_type not in ['beam_1']:
                entity.fluid = fluid
            else:
                entity.fluid = None

    def _set_cross_section_to_selected_entity(self, entity_id, cross):
        entity = self.preprocessor.dict_tag_to_entity[entity_id]
        entity.cross_section = cross

    def _set_cross_section_to_all_entities(self, cross):
        for entity in self.entities:
            entity.cross_section = cross

    def _set_variable_cross_section_to_selected_entity(self, entity_id, parameters):
        entity = self.preprocessor.dict_tag_to_entity[entity_id]
        entity.variable_cross_section_data = parameters

    def _set_structural_element_type_to_selected_entity(self, entity_id, element_type):
        entity = self.preprocessor.dict_tag_to_entity[entity_id]
        entity.structural_element_type = element_type

    def _set_structural_element_type_to_all_entities(self, element_type):
        for entity in self.entities:
            entity.structural_element_type = element_type

    def _set_acoustic_element_type_to_selected_entity(self, entity_id, element_type, hysteretic_damping=None):
        entity = self.preprocessor.dict_tag_to_entity[entity_id]
        entity.acoustic_element_type = element_type
        entity.hysteretic_damping = hysteretic_damping

    def _set_acoustic_element_type_to_all_entities(self, element_type, hysteretic_damping=None):
        for entity in self.entities: 
            entity.acoustic_element_type = element_type
            entity.hysteretic_damping = hysteretic_damping

    def _set_beam_xaxis_rotation_to_selected_entity(self, line_id, angle):
        entity = self.preprocessor.dict_tag_to_entity[line_id]
        entity.beam_xaxis_rotation = angle

    def _set_stress_stiffening_to_selected_entity(self, entity_id, parameters):
        entity = self.preprocessor.dict_tag_to_entity[entity_id]
        entity.external_temperature = parameters[0]
        entity.internal_temperature = parameters[1]
        entity.external_pressure = parameters[2]
        entity.internal_pressure = parameters[3]

    def _set_stress_stiffening_to_all_entities(self, parameters):
        for entity in self.entities:
            entity.external_temperature = parameters[0]
            entity.internal_temperature = parameters[1]
            entity.external_pressure = parameters[2]
            entity.internal_pressure = parameters[3]

    def _set_expansion_joint_to_selected_entity(self, entity_id, parameters):
        entity = self.preprocessor.dict_tag_to_entity[entity_id]
        entity.expansion_joint_parameters = parameters
    
    def get_nodes_with_prescribed_dofs_bc(self):
        return self.preprocessor.nodes_with_prescribed_dofs

    def set_fluid_by_line(self, line_id, fluid):
        if self.file.get_import_type() == 0:
            self.preprocessor.set_fluid_by_line(line_id, fluid)
        elif self.file.get_import_type() == 1:
            self.preprocessor.set_fluid_by_element('all', fluid)

        self._set_fluid_to_selected_entity(line_id, fluid)
        if fluid is None:
            self.file.add_fluid_in_file(line_id, "")
        else:
            self.file.add_fluid_in_file(line_id, fluid.identifier)

    def set_fluid_to_all_lines(self, fluid):
        self.preprocessor.set_fluid_by_element('all', fluid)
        self._set_fluid_to_all_entities(fluid)
        for line in self.preprocessor.all_lines:
            self.file.add_fluid_in_file(line, fluid.identifier)

    def set_acoustic_pressure_bc_by_node(self, node_ids, values, imported_table, table_name=""):
        self.preprocessor.set_acoustic_pressure_bc_by_node(node_ids, values) 
        label = ["acoustic pressure"] 
        for node_id in node_ids:
            self.file.add_acoustic_bc_in_file([node_id], values, imported_table, table_name, label) 
    
    def set_volume_velocity_bc_by_node(self, node_ids, values, imported_table, table_name="", table_index=None, additional_info=None):
        if self.preprocessor.set_volume_velocity_bc_by_node(node_ids, values, additional_info=additional_info):
            return True
        if table_index is None:
            label = ["volume velocity"]
        else:
            label = ["volume velocity - {}".format(table_index)]
        for node_id in node_ids:
            self.file.add_acoustic_bc_in_file([node_id], values, imported_table, table_name, label)
        return False    
    
    def set_specific_impedance_bc_by_node(self, node_ids, values, imported_table, table_name=""):
        for node_id in node_ids: 
            self.preprocessor.set_specific_impedance_bc_by_node(node_id, values) 
            label = ["specific impedance"] 
            self.file.add_acoustic_bc_in_file([node_id], values, imported_table, table_name, label)   

    def set_radiation_impedance_bc_by_node(self, node_ids, values, imported_table = None, table_name=""):
        for node_id in node_ids:    
            self.preprocessor.set_radiation_impedance_bc_by_node(node_id, values) 
            label = ["radiation impedance"] 
            self.file.add_acoustic_bc_in_file([node_id], values, imported_table, table_name, label) 
    
    def set_element_length_correction_by_elements(self, elements, value, section):
        # label = ["acoustic element length correction"] 
        self.preprocessor.set_length_correction_by_element(elements, value, section)
        self.file.add_length_correction_in_file(elements, value, section)
    
    def set_perforated_plate_by_elements(self, elements, perforated_plate, section):
        self.preprocessor.set_perforated_plate_by_elements(elements, perforated_plate, section)
        self.file.add_perforated_plate_in_file(elements, perforated_plate, section)

    def set_capped_end_by_elements(self, elements, value, selection):
        self.preprocessor.set_capped_end_by_elements(elements, value, selection)
        self.file.modify_capped_end_element_in_file(elements, value, selection)

    def set_capped_end_by_line(self, lines, value):
        if isinstance(lines, int):
            lines = [lines]
        self.preprocessor.set_capped_end_by_line(lines, value)
        if lines == "all":
            for tag in self.preprocessor.all_lines:
                self.file.modify_capped_end_entity_in_file(tag, value)
        else:
            for tag in lines:
                if value:
                    self.file.modify_capped_end_entity_in_file(tag, value)
                else:
                    self.file.modify_capped_end_entity_in_file(tag, value)      

    def get_nodes_with_acoustic_pressure_bc(self):
        return self.preprocessor.nodesAcousticBC

    def load_acoustic_pressure_bc_by_node(self, node_id, bc):
        self.preprocessor.set_acoustic_pressure_bc_by_node(node_id, bc)

    def load_volume_velocity_bc_by_node(self, node_id, value, additional_info=None):
        self.preprocessor.set_volume_velocity_bc_by_node(node_id, value, additional_info=additional_info)

    def load_specific_impedance_bc_by_node(self, node_id, value):
        self.preprocessor.set_specific_impedance_bc_by_node(node_id, value)

    def load_radiation_impedance_bc_by_node(self, node_id, value):
        self.preprocessor.set_radiation_impedance_bc_by_node(node_id, value)

    def load_length_correction_by_elements(self, elements, value, key):
        self.preprocessor.set_length_correction_by_element(elements, value, key)
    
    def load_perforated_plate_by_elements(self, elements, perforated_plate, key):
        self.preprocessor.set_perforated_plate_by_elements(elements, perforated_plate, key)

    def get_map_nodes(self):
        return self.preprocessor.map_nodes

    def get_map_elements(self):
        return self.preprocessor.map_elements

    def get_preprocess(self):
        return self.preprocessor

    def get_nodes_color(self):
        return self.preprocessor.nodes_color

    def get_nodes(self):
        return self.preprocessor.nodes

    # def get_entities(self):
    #     return self.preprocessor.entities

    def get_node(self, node_id):
        return self.preprocessor.nodes[node_id]

    def get_entity(self, entity_id):
        self.preprocessor.dict_tag_to_entity[entity_id]
        return self.preprocessor.dict_tag_to_entity[entity_id]

    def get_element_size(self):
        return self.file.element_size

    def check_entity_material(self):
        for entity in self.entities:#get_entities():
            if entity.getMaterial() is None:
                return False
        return True

    def check_entity_crossSection(self):
        for entity in self.entities:#get_entities():
            if entity.getCrossSection() is None:
                return False
        return True

    def set_modes_sigma(self, modes, sigma=1e-2):
        self.modes = modes
        self.sigma = sigma

    def get_frequencies(self):
        return self.frequencies

    def get_frequency_setup(self):
        return self.f_min, self.f_max, self.f_step

    def get_modes(self):
        return self.modes

    def get_material_list_path(self):
        return self.file.material_list_path
    
    def get_fluid_list_path(self):
        return self.file._fluid_list_path

    def get_project_name(self):
        return self._project_name

    def set_analysis_type(self, ID, analysis_text, method_text = ""):
        self.analysis_ID = ID
        self.analysis_type_label = analysis_text
        self.analysis_method_label = method_text

    def get_analysis_id(self): 
        return self.analysis_ID

    def get_analysis_type_label(self):
        return self.analysis_type_label

    def get_analysis_method_label(self):
        return self.analysis_method_label

    def set_damping(self, value):
        self.global_damping = value
        self.file.add_damping_in_file(value)

    def get_damping(self):
        return self.global_damping

    def set_structural_solve(self, structural_solve):
        self.structural_solve = structural_solve

    def get_structural_solve(self):
        if self.analysis_ID in [5,6]:
            results = SolutionStructural(self.preprocessor, self.frequencies, acoustic_solution=self.solution_acoustic)
        else:
            results = SolutionStructural(self.preprocessor, self.frequencies)
        return results

    def set_structural_solution(self, value):
        self.solution_structural = value

    def get_structural_solution(self):
        return self.solution_structural

    def get_acoustic_solve(self):
        return SolutionAcoustic(self.preprocessor, self.frequencies)

    def set_acoustic_solution(self, value):
        self.solution_acoustic = value
    
    def get_acoustic_solution(self):
        return self.solution_acoustic

    def set_acoustic_natural_frequencies(self, value):
        self.natural_frequencies_acoustic = value

    def get_acoustic_natural_frequencies(self):
        return self.natural_frequencies_acoustic
    
    def set_structural_natural_frequencies(self, value):
        self.natural_frequencies_structural  = value

    def set_structural_reactions(self, value):
        self.structural_reactions = value

    def get_structural_natural_frequencies(self):
        return self.natural_frequencies_structural

    def get_structural_reactions(self):
        return self.structural_reactions

    def get_unit(self):
        analysis = self.analysis_ID
        if analysis >=0 and analysis <= 6:
            if (analysis in [3,5,6] and self.plot_pressure_field) or self.plot_stress_field:
                return "Pa"
            elif analysis in [5,6] and not self.plot_pressure_field:
                return "m"            
            elif analysis in [0,1]:
                return "m"
            else:
                return "-"  

    def set_stresses_values_for_color_table(self, values):
        self.stresses_values_for_color_table = values
    
    def set_min_max_type_stresses(self, min_stress, max_stress, stress_label):
        self.min_stress = min_stress
        self.max_stress = max_stress
        self.stress_label = stress_label