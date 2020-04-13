from pulse.uix.user_input.materialInput import MaterialInput
from pulse.uix.user_input.materialList import MaterialList
from pulse.uix.user_input.crossInput import CrossInput
from pulse.uix.user_input.dofInput import DOFInput
from pulse.uix.user_input.dofInputNode import DOFInputNode
from pulse.uix.user_input.dofImport import DOFImport
from pulse.uix.user_input.forceInput import ForceInput
from pulse.uix.user_input.forceInputNode import ForceInputNode
from pulse.uix.user_input.newProjectInput import NewProjectInput
from pulse.uix.user_input.frequencyInput import FrequencyInput
from pulse.uix.user_input.frequencyList import FrequencyList
from pulse.uix.user_input.preProcessingInfo import PreProcessingInfo

from pulse.processing.solution import direct_method, modal_superposition
from pulse.postprocessing.plot_data import get_displacement_matrix

from pulse.project import Project

class InputUi:
    def __init__(self, project, parent=None):
        self.project = project
        self.parent = parent
        self.opv = self.parent.getOPVWidget()

    def material_input(self):
        pass
        #MaterialInput(self.project.materialPath)

    def material_list(self):
        entities_id = self.opv.getListPickedEntities()
        if len(entities_id) == 0:
            return
        selected_material = MaterialList(self.project.materialListPath)
        if selected_material.material is None:
            return
        for entity in entities_id:
            self.project.setMaterial_by_Entity(entity, selected_material.material)
        print("### Material {} defined in the entities {}".format(selected_material.material.name, entities_id))
        self.opv.changeColorEntities(entities_id, selected_material.material.getNormalizedColorRGB())
        

    def cross_input(self):
        entities_id = self.opv.getListPickedEntities()
        if len(entities_id) == 0:
            return
        cross_section = CrossInput()
        if cross_section.cross is None:
            return
        for entity in entities_id:
            self.project.setCrossSection_by_Entity(entity, cross_section.cross)
        print("### Cross defined in the entities {}".format(entities_id))
        self.opv.changeColorCross()

    def import_dof(self):
        pass
        # last = self.parent.getLastPickedPoint()
        # if last is None:
        #     return
        
        # imd = DOFImport()

    def dof_input(self):
        point_id = self.opv.getListPickedPoints()
        if len(point_id) == 0:
            return

        dof = DOFInput()
        if dof.bondary is None:
            return
        self.project.setBondaryCondition_by_Node(point_id, dof.bondary)
        print("### BC defined in the Points {}".format(point_id))
        self.opv.changeColorPoints(point_id, (0,1,0))

    def dof_input_node(self):
        point_id = self.opv.getListPickedPoints()
        dof = DOFInputNode(point_id)
        if dof.bondary is None:
            return
        if len(dof.nodes) != 0:
            self.project.setBondaryCondition_by_Node(dof.nodes, dof.bondary)
            print("### BC defined in the Points {}".format(dof.nodes))
            self.opv.changeColorPoints(dof.nodes, (0,1,0))

    def force_input_node(self):
        force = ForceInputNode()
        if force.force is None:
            return
        if len(force.nodes) != 0:
            self.project.setFroce_by_Node(force.nodes, force.force)
            print("### Force defined in the Points {}".format(force.nodes))
            self.opv.changeColorPoints(force.nodes, (0,1,0))

    def force_input(self):
        point_id = self.opv.getListPickedPoints()
        if len(point_id) == 0:
            return

        force = ForceInput()
        if force.force is None:
            return
        self.project.setFroce_by_Node(point_id, force.force)
        print("### Force defined in the Points {}".format(point_id))
        self.opv.changeColorPoints(point_id, (0,1,1))

    def newProject(self):
        result = NewProjectInput(self.project)
        return result.create

    def define_material_all(self):
        if not self.project.isReady():
            return   #No project were loaded

        selected_material = MaterialList(self.project.materialListPath)
        
        if selected_material.material is None:
            return
        self.project.setMaterial(selected_material.material)
        entities = []
        for entity in self.project.getEntities():
            entities.append(entity.getTag())
        self.opv.changeColorEntities(entities, selected_material.material.getNormalizedColorRGB())

    def define_cross_all(self):
        if not self.project.isReady():
            return   #No project were loaded

        cross_section = CrossInput()
        if cross_section.cross is None:
            return
        self.project.setCrossSection(cross_section.cross)
        self.opv.changeColorCross()

    def direct_method(self):
        freq = FrequencyInput()
        try:
            if len(freq.frequencies) == 0:
                print("Nenhuma frequencia")
                return
            if not self.project.checkEntityMaterial():
                print("Erro check material")
                return
            if not self.project.checkEntityCross():
                print("Erro check cross")
                return
            direct = direct_method(self.project.getMesh(), freq.frequencies)
            self.project.setDirectMatriz(direct)
            self.project.setFrequencies(freq.frequencies)
            self.opv.change_to_direct_method(0)
        except Exception as e:
            print("{}".format(e))

    def modal_superposition(self):
        freq = FrequencyInput()
        try:
            if len(freq.frequencies) == 0:
                print("Nenhuma frequencia")
                return
            if not self.project.checkEntityMaterial():
                print("Erro check material")
                return
            if not self.project.checkEntityCross():
                print("Erro check cross")
                return
            modes = 140
            modal = modal_superposition(self.project.getMesh(), freq.frequencies, modes)
            self.project.setModalMatriz(modal)
            self.project.setFrequencies(freq.frequencies)
            self.project.setModes(modes)
            self.opv.change_to_modal_superposition(0)
        except Exception as e:
            print("{}".format(e))

    def changeFrequencyInput(self):
        freq = FrequencyList(self.project.getFrequencies())
        if freq.current_item is None:
            return
        self.opv.changeFrequency(freq.current_item)

    def preProcessingInfo(self):
        pre = PreProcessingInfo(self.project.entityPath, self.project.nodePath)
        if not pre.hasError:
            self.project.setTempValues()
            self.project.getGlobalMatrices()
            self.opv.change_to_preProcessing()