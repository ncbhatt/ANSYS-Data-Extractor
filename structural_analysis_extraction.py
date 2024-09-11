from ansys.mapdl import reader as pymapdl_reader

class StructuralAnalysisExtractor:
    def __init__(self, file_path, node_number, load_step, sub_step):
        self.file_path = file_path
        self.node_number = node_number
        self.load_step = load_step
        self.sub_step = sub_step

    def extract_data(self):
        result = pymapdl_reader.read_binary(self.file_path)
        
        # Get the nodal stress data (which is a tuple)
        stress_data_tuple = result.nodal_stress(self.load_step - 1, self.sub_step - 1)
        
        # The first element contains the node numbers associated with the stress data
        stress_node_numbers = stress_data_tuple[0]
        # The second element contains the actual stress values
        stress_data = stress_data_tuple[1]
        
        print(f"Available node numbers: {stress_node_numbers}")  # Debug print
        
        # Check if the specified node number is in the stress data
        if self.node_number not in stress_node_numbers:
            raise RuntimeError(f"Node number {self.node_number} not found in the stress data.")
        
        # Find the index of the node number in the stress data
        stress_node_index = list(stress_node_numbers).index(self.node_number)
        
        # Return the stress value for the specified node
        return stress_data[stress_node_index, 0]  # Assuming you want the first stress component
