import maude
import fullmaude # <--- change here

import os.path
from pyfmi import load_fmu

maude.init(advise=False)
fullMaudePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'Maude_Python', 'full-maude.maude'))
portModulePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'Maude_Python', 'port.maude'))
massSpringDamper1Path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'Maude_Python', 'fmus', 'MassSpringDamper1.fmu'))
massSpringDamper2Path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'Maude_Python', 'fmus', 'MassSpringDamper2.fmu'))

massSpringDamper1 = load_fmu(massSpringDamper1Path)
massSpringDamper2 = load_fmu(massSpringDamper2Path)
 

inputs = massSpringDamper1.get_model_variables(0,True, 2)
outputs = massSpringDamper1.get_model_variables(0,True, 3)


fmus = [massSpringDamper1, massSpringDamper2]

maude.load(fullMaudePath)
maude.load(portModulePath)

portModule = fullmaude.getFMModule('Ports') # <--- change here
print('--->', portModule) # <--- outputs Ports


modules = maude.getModules()

for module in modules:
  print(module)

class Port:
    # class Port | value : FMIValue, type : PortType, time : Nat, status : PortStatus . 
    def __init__(self, value, type):
            self.value = value
            self.type = type
            self.time = '0'
            self.status = 'Undef'

    def encodePort(self):
        """
            Returns a string with the port encoded in Maude format
        """
        return 'value : < ' + self.value + ' >, ' + 'type : ' + self.type + ', ' + 'time : ' + self.time + ', ' + 'status : ' + self.status

class Input(Port):
    # class Input | contract : Contract .

    def __init__(self, value, valueType, name, contract):
        Port.__init__(self, value, valueType)
        self.name = name
        self.contract = contract

    def get_type(self):
        return self.type

    def encode(self):
        """
        Returns the maude class
        """
        return '< "' + self.name + '" : Input | contract : ' + self.contract + ', ' + self.encodePort() +' >'

class OutputPort(Port):
    # class Output | dependsOn : OidSet .
    def __init__(self, value, valueType, name, dependsOn):
        Port.__init__(self, value, valueType)
        self.name = name
        self.dependsOn = dependsOn

    def get_type(self):
        return self.type

    def encode(self):
        """
        Returns the maude class
        """
        return '< "' + self.name + '" : Output | dependsOn : ' + self.dependsOn + ',' + self.encodePort() +' >'
        
class FMU:
    # Maude representation of the FMU
    #class SU |
    #  path : String, 
    #  time : Nat, 
    #  inputs : Configuration, ***Input ports
    #  outputs : Configuration, ***Output ports
    #  canReject : Bool, 
    #  fmistate : fmiState,
    #  parameters : LocalState,
    #  localState : LocalState .'
    def __init__(self, name, path, canReject):
        self.name = name
        self.path = path
        self.time = 0
        self.fmu = load_fmu(path)
        self.inputs = self.fmu.get_model_variables()

        self.canReject = canReject

#Type
#Real==0, Int==1, Bool==2, String==3,

#Causality:
# Parameter==0, 
#     Calculated Parameter==1, Input==2, Output==3, Local==4, 
#     Independent==5, Unknown==6

    def setUpInputs(self):
        #self.inputs =
        pass

    def setUpOutputs(self):
        #self.inputs =
        pass

    def encode(self):
        """
        Returns the maude class
        """
        '< "'
        + self.name + '" : SU | time : 0, inputs : ' + self.inputs.encode() + ', outputs : ' + self.outputs.encode() + ', canReject : ' + self.canReject + ', fmistate : ' + self.fmistate + ', parameters : ' + self.parameters.encode() + ', localState : ' + self.localState.encode() + '>'
        self.name + ' >'


class SourceRef:
    # fmu ! port .

    def __init__(self, fmu, port):
        self.fmu = fmu
        self.port = port

    def encode(self):
        """
        Returns the maude class
        """
        return self.fmu + ' ! ' + self.port
    
        

class Connection:
    def __init__(self, src, trg):
        self.src = src
        self.trg = trg

    def __str__(self):
        """
        Encode the connection as a Maude formula.
        """
        return 'Connection: {} -> {}'.format(self.src.encode(), self.trg.encode())

class Scenario:
    def __init__(self, fmus, connections):
        self.fmus = fmus
        self.connections = connections

    def encode_Scenario(self):
        """
        Encode the scenario as a Maude formula.
        """
        connectionString = self.connections.format(', '.join(map(str, self.connections)))
        fmuString = self.fmus.format(', '.join(map(str, self.fmus)))
        return 'Scenario: {} -> {}'.format(fmuString, connectionString)

    def isValidScenario(self):
        """
        Check if the scenario is valid in Maude.
        """
        pass

    def get_connections(self):
        """
        Return the list of connections.
        """
        return self.connections

    def get_fmus(self):
        """
        Return the list of FMUs.
        """
        return self.fmus

    def get_Initialization(self):
        """
        Return the initialization algorithm through Maude.
        """
        pass

    def get_CoSimStep(self):
        """
        Return the cosim-step algorithm through Maude.
        """
        pass


def initialize(fmu):
    fmu.enter_initialization_mode()

def exit_initialization(fmu):
    fmu.exit_initialization_mode()

def free_instance(fmu):
    """
        Free the FMU
    """
    fmu.free_instance()



def set(fmu, port,val):
    """
    Set the value of a port in a FMU
    """
    # match port.getType():
    #     case "Real":
    #         fmu.get_real([port.getPortRef()])
    #     case "Bool":
    #         fmu.get_boolean([port.getPortRef()])
    #     case "Int":
    #         fmu.get_integer([port.getPortRef()])
    #     case "String":
    #         fmu.get_string([port.getPortRef()])


def get(fmu, port):
    """
    Get the value of a port in a FMU
    """
    # match port.getType():
    #     case "Real":
    #         fmu.get_real([port.getPortRef()])
    #     case "Bool":
    #         fmu.get_boolean([port.getPortRef()])
    #     case "Int":
    #         fmu.get_integer([port.getPortRef()])
    #     case "String":
    #         fmu.get_string([port.getPortRef()])

def step(fmu, stepSize):
    """
    Update the state of the FMU before performing a step
    """
    currentTime = 0
    return fmu.do_step(currentTime, stepSize)


def runSimulation(scenario):
    """
    Run the simulation through Maude.
    """
    pass
