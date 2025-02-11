# from pulse.preprocessing.before_run import BeforeRun
from collections import defaultdict
from data.user_input.project.printMessageInput import PrintMessageInput
import numpy as np

window_title_1 = "ERROR"
window_title_2 = "WARNING"

class BeforeRun:
    def __init__(self, project, opv, **kwargs):
        self.project = project
        self.opv = opv
        self.preprocessor = project.preprocessor
        self.nodes = project.preprocessor.nodes
        self.structural_elements = project.preprocessor.structural_elements
        self.acoustic_elements = project.preprocessor.acoustic_elements
        self.dict_tag_to_entity = project.preprocessor.dict_tag_to_entity

    def check_modal_analysis_imported_data(self):
        message = ""
        title = "Modal analysis with imported data from tables"
        if len(self.project.file.non_zero_frequency_info)==3:
            [zero_frequency, f_min, table_name] = self.project.file.non_zero_frequency_info
            if not zero_frequency:
                message = "The current project setup has at least one loaded table of values for boundary conditions or external elements. "
                message += f"The first frequency point\n f={f_min}Hz from '{table_name}' file has been considered in the \ncurrent analysis, "
                message += "however, it differs from the 0Hz value. Please, take \nthis information into account when checking the obtained results."

        elif self.project.file.zero_frequency:    
            message = "The current project setup has at least one loaded table of values for boundary conditions or external elements. "
            message += "The first frequency point\n f=0Hz from imported files have been considered in the current analysis. \nPlease, "
            message += "take this information into account when checking the obtained results."
            
        if message != "":
            PrintMessageInput([title, message, window_title_2])

    def check_input_NodeID(self, lineEdit, single_ID=False):
        try:

            title = "Invalid entry to the Node ID"
            message = ""
            tokens = lineEdit.strip().split(',')

            try:
                tokens.remove('')
            except:
                pass

            _size = len(self.nodes)

            list_nodes_typed = list(map(int, tokens))

            if len(list_nodes_typed) == 0:
                    message = "An empty input field for the Node ID has been detected. \n\nPlease, enter a valid Node ID to proceed!"
            
            elif len(list_nodes_typed) >= 1: 
                if single_ID and len(list_nodes_typed) > 1:
                    message = "Multiple Node IDs"
                else:
                    try:
                        for node_ID in list_nodes_typed:
                            self.nodes[node_ID]
                    except:
                        message = "Dear user, you have typed an invalid entry at the Node ID input field.\n\n" 
                        message += f"The input value(s) must be integer(s) number(s) greater than 1 and\n less than {_size}."

        except Exception as log_error:
            message = f"Wrong input for the Node ID's! \n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title_1])               
            return True, [] 

        if single_ID:
            return False, list_nodes_typed[0]
        else:
            return False, list_nodes_typed


    def check_input_ElementID(self, lineEdit, single_ID=False):
        try:

            title = "Invalid entry to the Element ID"
            message = ""
            tokens = lineEdit.strip().split(',')

            try:
                tokens.remove('')
            except:
                pass

            _size = len(self.structural_elements)

            list_elements_typed = list(map(int, tokens))

            if len(list_elements_typed) == 0:
                    message = "An empty input field for the Element ID has been detected. \n\nPlease, enter a valid Element ID to proceed!"

            elif len(list_elements_typed) >= 1: 
                if single_ID and len(list_elements_typed)>1:
                    message = "Multiple Element IDs"
                else:
                    try:
                        for element_ID in list_elements_typed:
                            self.structural_elements[element_ID]
                    except:
                        message = "Dear user, you have typed an invalid entry at the Element ID input field.\n\n" 
                        message += f"The input value(s) must be integer(s) number(s) greater than 1 and\n less than {_size}."

        except Exception as log_error:
            message = f"Wrong input for the Element ID's! \n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title_1])               
            return True, [] 

        if single_ID:
            return False, list_elements_typed[0]
        else:
            return False, list_elements_typed


    def check_input_LineID(self, lineEdit, single_ID=False):
        try:

            title = "Invalid entry to the Line ID"
            message = ""
            tokens = lineEdit.strip().split(',')

            try:
                tokens.remove('')
            except:
                pass

            _size = len(self.dict_tag_to_entity)

            list_lines_typed = list(map(int, tokens))

            if len(list_lines_typed) == 0:
                    message = "An empty input field for the Line ID has been detected. \n\nPlease, enter a valid Line ID to proceed!"

            elif len(list_lines_typed) >= 1: 
                if single_ID and len(list_lines_typed)>1:
                    message = "Multiple Line IDs"
                else:
                    try:
                        for line_ID in list_lines_typed:
                            self.dict_tag_to_entity[line_ID]
                    except:
                        message = "Dear user, you have typed an invalid entry at the Line ID input field.\n\n" 
                        message += f"The input value(s) must be integer(s) number(s) greater than 1 and\n less than {_size}."

        except Exception as log_error:
            message = f"Wrong input for the Line ID's! \n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title_1])               
            return True, [] 

        if single_ID:
            return False, list_lines_typed[0]
        else:
            return False, list_lines_typed


    def check_material_all_elements(self):
        """
        This method checks if all structural elements have a material object attributed.
        """
        self.check_set_material = False
        self.check_poisson = False
        lines_without_materials = []
        for element in self.structural_elements.values():
            line_id = self.preprocessor.elements_to_line[element.index]
            if element.material is None:
                self.check_set_material = True
                if line_id not in lines_without_materials:
                    lines_without_materials.append(line_id)
                
        return lines_without_materials

    def check_poisson_all_elements(self):
        """
        This method checks if all structural elements have a Poisson ratio attributed.
        """
        self.check_poisson = False
        lines_without_poisson = []
        for element in self.structural_elements.values():
            line_id = self.preprocessor.elements_to_line[element.index]
            if element.material.poisson_ratio == 0:
                self.check_poisson = True
                if line_id not in lines_without_poisson:
                    lines_without_poisson.append(line_id)
                
        return lines_without_poisson

    def check_material_and_cross_section_in_all_elements(self):
        """
        This method checks if all structural elements have a material object and a cross section object attributed.
        """
        self.check_set_material = False
        self.check_set_crossSection = False
        self.check_poisson = False
        lines_without_materials = []
        lines_without_cross_sections = []
        elements_without_cross_sections = defaultdict(list)  
        for element in self.structural_elements.values():
            line_id = self.preprocessor.elements_to_line[element.index]
            if element.material is None:
                self.check_set_material = True
                if line_id not in lines_without_materials:
                    lines_without_materials.append(line_id)
                
            if element.cross_section is None:
                if element.element_type:
                    self.check_set_crossSection = True
                    if element.index not in elements_without_cross_sections[line_id]:
                        elements_without_cross_sections[line_id].append(element.index)
                    if line_id not in lines_without_cross_sections:
                        lines_without_cross_sections.append(line_id)
                    
            else:        

                if element.element_type == 'expansion_joint':
                    if element.cross_section.area_fluid == 0:
                        self.check_set_crossSection = True
                        if element.index not in elements_without_cross_sections[line_id]:
                            elements_without_cross_sections[line_id].append(element.index)
                        if line_id not in lines_without_cross_sections:
                            lines_without_cross_sections.append(line_id)
                        
                else:
                    if element.cross_section.thickness == 0:
                        if element.cross_section.area == 0:
                            self.check_set_crossSection = True
                            if element.index not in elements_without_cross_sections[line_id]:
                                elements_without_cross_sections[line_id].append(element.index)
                            if line_id not in lines_without_cross_sections:
                                lines_without_cross_sections.append(line_id)
                            
        return lines_without_materials, elements_without_cross_sections

    def check_fluid_and_cross_section_in_all_elements(self):
        """
        This method checks if all acoustic elements have a fluid object and a cross section object attributed.
        """
        self.check_set_fluid = False
        self.check_set_crossSection = False
        lines_without_fluids = []
        lines_without_cross_sections = []
        elements_without_cross_sections = defaultdict(list)
        for element in self.acoustic_elements.values():
            line_id = self.preprocessor.elements_to_line[element.index]
            if element.fluid is None:
                if 'pipe_' in self.structural_elements[element.index].element_type:
                    self.check_set_fluid = True
                    if line_id not in lines_without_fluids:
                        lines_without_fluids.append(line_id)
                    
            if element.cross_section is None:
                self.check_set_crossSection = True
                if element.index not in elements_without_cross_sections[line_id]:
                    elements_without_cross_sections[line_id].append(element.index)
                if line_id not in lines_without_cross_sections:
                        lines_without_cross_sections.append(line_id)
            else:
                if self.structural_elements[element.index].element_type == 'expansion_joint':
                    if element.cross_section.area_fluid == 0:
                        self.check_set_crossSection = True
                        if element.index not in elements_without_cross_sections[line_id]:
                            elements_without_cross_sections[line_id].append(element.index)
                        if line_id not in lines_without_cross_sections:
                            lines_without_cross_sections.append(line_id)     
                else:    
                    if element.cross_section.thickness == 0:
                        if element.cross_section.area == 0:
                            self.check_set_crossSection = True
                            if element.index not in elements_without_cross_sections[line_id]:
                                elements_without_cross_sections[line_id].append(element.index)
                            if line_id not in lines_without_cross_sections:
                                lines_without_cross_sections.append(line_id)
                        
        return lines_without_fluids, elements_without_cross_sections

    def check_fluid_inputs_in_all_elements(self):
        """
        This method checks if each acoustic element has the necessary fluid data to evaluate the analysis according to its element type.
        """
        self.check_all_fluid_inputs = False
        lines_without_fluids = []
        for element in self.acoustic_elements.values():
            line_id = self.preprocessor.elements_to_line[element.index]
            if element.element_type in ['wide-duct', 'LRF fluid equivalent', 'LRF full']:
                if 'pipe_' in self.structural_elements[element.index].element_type:
                    _list = [   element.fluid.isentropic_exponent, element.fluid.thermal_conductivity, 
                                element.fluid.specific_heat_Cp, element.fluid.dynamic_viscosity   ]
                    if None in _list:
                        self.check_all_fluid_inputs = True
                        if line_id not in lines_without_fluids:
                            lines_without_fluids.append(line_id)
                        
        return lines_without_fluids


    def check_nodes_attributes(self, acoustic=False, structural=False, coupled=False):
        """
        This method checks if there is the necessary nodal input data to evaluate the analysis according to its type.

        Parameters
        ----------
        acoustic : boll, optional
            True if a acoustic analysis will be performed. False otherwise.
            Default is False.

        structural : boll, optional
            True if a structural analysis will be performed. False otherwise.
            Default is False.

        coupled : boll, optional
            True if a coupled analysis will be performed. False otherwise.
            Default is False.
        """
        self.is_there_loads = False
        self.is_there_prescribed_dofs = False
        self.is_there_acoustic_pressure = False
        self.is_there_volume_velocity = False
        for node in self.nodes.values():

            if structural:
                if node.there_are_nodal_loads:
                    self.is_there_loads = True
                    return

                if node.there_are_prescribed_dofs:
                    if True in [True if isinstance(value, np.ndarray) else False for value in node.prescribed_dofs]:
                        self.is_there_prescribed_dofs = True
                        return

                    elif sum([value if value is not None else complex(0) for value in node.prescribed_dofs]) != complex(0):
                        self.is_there_prescribed_dofs = True
                        return

            if acoustic or coupled:
                if node.acoustic_pressure is not None:
                    self.is_there_acoustic_pressure = True
                    return

                if node.volume_velocity is not None:
                    self.is_there_volume_velocity = True
                    return    


    def check_all_acoustic_criteria(self):
        window_title = "WARNING"
        title = "Acoustic criteria not satisfied"
        
        flag_plane_wave = False
        flag_wide_duct = False
        flag_lrf_fluid_eq = False
        flag_lrf_full = False
        flag_unflanged_radiation_impedance = False
        
        message_plane_wave = "The acoustic model is out of the plane wave validity frequency range. It is recommended to check the high frequency results carefully."
        message_wide_duct = "The wide-duct acoustic damping model is out of its validity frequency range. It is recommended to check the results carefully."
        message_lrf_fluid_eq = "The Low Reduced Frequency (LRF fluid equivalent) acoustic damping model is out of its validity frequency range. It is recommended to check the results carefully."
        message_lrf_full = "The Low Reduced Frequency (LRF) acoustic damping model is out of its validity frequency range. It is recommended to check the results carefully."
        message_unflanged_radiation_impedance  = "The unflanged radiation impedance model is out of its validity frequency range. It is recommended to check the results carefully."

        list_plane_wave = []
        list_wide_duct = []
        list_lrf_fluid_eq = []
        list_lrf_full = []
        list_max_valid_freq = []
        list_min_valid_freq = []

        for element in self.acoustic_elements.values():
            if element.flag_plane_wave:
                list_plane_wave.append(element.index)
            if element.flag_wide_duct:
                list_wide_duct.append(element.index)
            if element.flag_lrf_fluid_eq:
                list_lrf_fluid_eq.append(element.index)
            if element.flag_lrf_full:
                list_lrf_full.append(element.index)
            list_max_valid_freq.append(element.max_valid_freq) 
            list_min_valid_freq.append(element.min_valid_freq)
                
            if element.flag_unflanged_radiation_impedance and not flag_unflanged_radiation_impedance:
                flag_unflanged_radiation_impedance = True

        self.dict_criterias = {}

        if len(list_plane_wave)>=1:
            flag_plane_wave = True
            self.dict_criterias['Plane wave'] = list_plane_wave
        if len(list_wide_duct)>=1:
            flag_wide_duct = True
            self.dict_criterias['Wide duct'] = list_wide_duct
        if len(list_lrf_fluid_eq)>=1:
            flag_lrf_fluid_eq = True
            self.dict_criterias['LRF fluid eq'] = list_lrf_fluid_eq
        if len(list_lrf_full)>=1:
            flag_lrf_full = True
            self.dict_criterias['LRF full'] = list_lrf_full
        
        self.max_valid_freq = np.array(list_max_valid_freq)[np.array(list_max_valid_freq)!=None]
        self.min_valid_freq = np.array(list_min_valid_freq)[np.array(list_min_valid_freq)!=None]

        self.max_valid_freq = np.min(self.max_valid_freq)
        self.min_valid_freq = np.max(self.min_valid_freq)

        list_flags = [flag_plane_wave, flag_wide_duct, flag_lrf_fluid_eq, flag_lrf_full, flag_unflanged_radiation_impedance]
        list_messages = [message_plane_wave, message_wide_duct, message_lrf_fluid_eq, message_lrf_full, message_unflanged_radiation_impedance]
        lists_elements = [list_plane_wave, list_wide_duct, list_lrf_fluid_eq, list_lrf_full, []]

        for index, flag in enumerate(list_flags):
            if flag:
                self.opv.changePlotToMesh()
                self.opv.opvRenderer.highlight_elements(lists_elements[index])
                PrintMessageInput([title, list_messages[index], window_title])


    def check_is_there_a_problem(self, analysis_ID):

        title = " Insufficient model inputs "

        cross_section_message = "You should set a Cross-Section to all elements \nbefore proceeding with the model solution.!\n\n"
        #
        material_message = "You should to set a Material to all elements\n before trying to run any Analysis!\n\n"
        material_message += "Lines without material assignment: \n{}"
        #
        fluid_message = "You should to set a Fluid to all elements\n before trying to run any Analysis!\n\n"
        fluid_message += "Lines without fluid assignment: \n{}"
        #
        all_fluid_inputs_message = "You should insert all fluid properties for wide-duct, LRF \nfluid equivalent and " 
        all_fluid_inputs_message += "LRF full acoustic element types \n before proceeding with the model solution.\n\n"
        all_fluid_inputs_message += "Lines with incomplete fluid properties: \n{}"
        #
        structural_message = "You should to apply an external load to the model or prescribe a \nnon-null DOF value before trying to solve the Harmonic Analysis!"
        acoustic_message = "You should to insert a Volume Velocity or prescribe an Acoustic \nPressure to a node before trying to solve the Harmonic Analysis!"
    
        if analysis_ID == 2:
            lines_without_materials, elements_without_cross_sections = self.check_material_and_cross_section_in_all_elements()
            if self.check_set_material:
                self.opv.opvRenderer.highlight_lines(lines_without_materials)
                PrintMessageInput([title, material_message.format(lines_without_materials), window_title_1])
                return True
            elif self.check_set_crossSection:
                list_lines, list_elements = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if list_elements == []:  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}\n"                 
                    self.opv.opvRenderer.highlight_lines(list_lines)
                elif list_lines == []:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n"
                    self.opv.opvRenderer.highlight_elements(list_elements)
                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"
                    self.opv.opvRenderer.highlight_lines(list_lines)
                    self.opv.opvRenderer.highlight_elements(list_elements, reset_colors=False)
                PrintMessageInput([title, cross_section_message, window_title_1])
                return True
        
        elif analysis_ID == 4:
            lines_without_materials = self.check_material_all_elements()
            lines_without_fluids, elements_without_cross_sections = self.check_fluid_and_cross_section_in_all_elements()
            lines_without_all_fluids_inputs = self.check_fluid_inputs_in_all_elements()
            if self.check_set_material:
                self.opv.opvRenderer.highlight_lines(lines_without_materials)
                PrintMessageInput([title, material_message.format(lines_without_materials), window_title_1])
                return True
            elif self.check_set_fluid:
                self.opv.opvRenderer.highlight_lines(lines_without_fluids)
                PrintMessageInput([title, fluid_message.format(lines_without_fluids), window_title_1])
                return True
            elif self.check_all_fluid_inputs:
                self.opv.opvRenderer.highlight_lines(lines_without_all_fluids_inputs)
                PrintMessageInput([title, all_fluid_inputs_message.format(lines_without_all_fluids_inputs), window_title_1])
                return True
            elif self.check_set_crossSection:
                list_lines, list_elements = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if list_elements == []:  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"                 
                    self.opv.opvRenderer.highlight_lines(list_lines)
                elif list_lines == []:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}"
                    self.opv.opvRenderer.highlight_elements(list_elements)
                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"
                    self.opv.opvRenderer.highlight_lines(list_lines)
                    self.opv.opvRenderer.highlight_elements(list_elements, reset_colors=False)
                PrintMessageInput([title, cross_section_message, window_title_1])
                return True

        elif analysis_ID == 0 or analysis_ID == 1:
            lines_without_materials, elements_without_cross_sections = self.check_material_and_cross_section_in_all_elements()
            self.check_nodes_attributes(structural=True)
            if self.check_set_material:
                self.opv.opvRenderer.highlight_lines(lines_without_materials)
                PrintMessageInput([title, material_message.format(lines_without_materials), window_title_1])
                return True
            elif self.check_set_crossSection:
                list_lines, list_elements = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if list_elements == []:  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"                 
                    self.opv.opvRenderer.highlight_lines(list_lines)
                elif list_lines == []:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}"
                    self.opv.opvRenderer.highlight_elements(list_elements)
                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"
                    self.opv.opvRenderer.highlight_lines(list_lines)
                    self.opv.opvRenderer.highlight_elements(list_elements, reset_colors=False)
                PrintMessageInput([title, cross_section_message, window_title_1])
                return True
            elif not self.is_there_loads:
                if not self.is_there_prescribed_dofs:
                    PrintMessageInput([title, structural_message, window_title_1])
                    return True
    
        elif analysis_ID == 3:
            lines_without_materials = self.check_material_all_elements()
            lines_without_fluids, elements_without_cross_sections = self.check_fluid_and_cross_section_in_all_elements()
            lines_without_all_fluids_inputs = self.check_fluid_inputs_in_all_elements()
            self.check_nodes_attributes(acoustic=True)
            if self.check_set_fluid:
                self.opv.opvRenderer.highlight_lines(lines_without_fluids)
                PrintMessageInput([title, fluid_message.format(lines_without_fluids), window_title_1])
                return True
            elif self.check_all_fluid_inputs:
                self.opv.opvRenderer.highlight_lines(lines_without_all_fluids_inputs)
                PrintMessageInput([title, all_fluid_inputs_message.format(lines_without_all_fluids_inputs), window_title_1])
                return True
            elif self.check_set_material:
                self.opv.opvRenderer.highlight_lines(lines_without_materials)
                PrintMessageInput([title, material_message.format(lines_without_materials), window_title_1])
                return True
            elif self.check_set_crossSection:
                list_lines, list_elements = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if list_elements == []:  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"                 
                    self.opv.opvRenderer.highlight_lines(list_lines)
                elif list_lines == []:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}"
                    self.opv.opvRenderer.highlight_elements(list_elements)
                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"
                    self.opv.opvRenderer.highlight_lines(list_lines)
                    self.opv.opvRenderer.highlight_elements(list_elements, reset_colors=False)
                PrintMessageInput([title, cross_section_message, window_title_1])
                return True
            elif not self.is_there_volume_velocity:
                if not self.is_there_acoustic_pressure:
                    PrintMessageInput([title, acoustic_message, window_title_1])
                    return True

        elif analysis_ID == 5 or analysis_ID == 6:
            lines_without_materials, elements_without_cross_sections = self.check_material_and_cross_section_in_all_elements()
            lines_without_fluids, elements_without_cross_sections = self.check_fluid_and_cross_section_in_all_elements()
            lines_without_all_fluids_inputs = self.check_fluid_inputs_in_all_elements()
            self.check_nodes_attributes(coupled=True)
            if self.check_set_material:
                self.opv.opvRenderer.highlight_lines(lines_without_materials)
                PrintMessageInput([title, material_message.format(lines_without_materials), window_title_1])
                return True
            elif self.check_set_fluid:
                self.opv.opvRenderer.highlight_lines(lines_without_fluids)
                PrintMessageInput([title, fluid_message.format(lines_without_fluids), window_title_1])
                return True
            elif self.check_all_fluid_inputs:
                self.opv.opvRenderer.highlight_lines(lines_without_all_fluids_inputs)
                PrintMessageInput([title, all_fluid_inputs_message.format(lines_without_all_fluids_inputs), window_title_1])
                return True
            elif self.check_set_crossSection:  
                list_lines, list_elements = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if list_elements == []:  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"                 
                    self.opv.opvRenderer.highlight_lines(list_lines)
                elif list_lines == []:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}"
                    self.opv.opvRenderer.highlight_elements(list_elements)
                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"
                    self.opv.opvRenderer.highlight_lines(list_lines)
                    self.opv.opvRenderer.highlight_elements(list_elements, reset_colors=False)
                PrintMessageInput([title, cross_section_message, window_title_1])
                return True
            elif not self.is_there_volume_velocity:
                if not self.is_there_acoustic_pressure:
                    PrintMessageInput([title, acoustic_message, window_title_1])
                    return True
    
    def check_cross_section_in_lines_and_elements(self, data):
        list_lines = []
        list_elements = []
        for line_id, element_ids in data.items():
            if list(np.sort(element_ids)) == list(np.sort(self.preprocessor.line_to_elements[line_id])):
                list_lines.append(line_id)
            else:
                for element_id in element_ids:
                    list_elements.append(element_id)
        return list_lines, list_elements