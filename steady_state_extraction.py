from ansys.mapdl.reader import read_binary

class SteadyStateExtractor:
    def __init__(self, file_path, node_number, load_step, sub_step):
        self.file_path = file_path
        self.node_number = node_number
        self.load_step = load_step - 1  # Adjust for zero-based index
        self.sub_step = sub_step - 1  # Adjust for zero-based index

    def extract_data(self):
        try:
            rth = read_binary(self.file_path)
            num_results = rth.nsets
            
            if self.load_step >= num_results:
                raise RuntimeError(f"There are only {num_results} result(s) in the result file.")

            node_numbers, temperatures = rth.nodal_temperature(self.load_step)
            
            if self.node_number in node_numbers:
                node_index = list(node_numbers).index(self.node_number)
                return temperatures[node_index]
            else:
                raise RuntimeError(f"Node number {self.node_number} not found in the results.")
        
        except FileNotFoundError:
            raise RuntimeError(f"The file '{self.file_path}' was not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}")
