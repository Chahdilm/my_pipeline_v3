from bin.get_packages import * 
import xmltodict

 
class DataGenerate():

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def read_json(self,type_encoding):
        """Read a JSON file and return as a dictionary."""
        with open(self.input_path, 'r', encoding=type_encoding ) as f:
            return json.load(f)


    def save_json(self,file_name, data_dict):
        """Save a dictionary as a JSON file."""
        with open(os.path.join(self.output_path, file_name), 'w') as output_file:
            json.dump(data_dict, output_file)

    def from_xml_to_json(self):

        with open(self.input_path ,encoding="ISO-8859-1") as pd_xml:  
            root  = xmltodict.parse(pd_xml.read())
        return root


