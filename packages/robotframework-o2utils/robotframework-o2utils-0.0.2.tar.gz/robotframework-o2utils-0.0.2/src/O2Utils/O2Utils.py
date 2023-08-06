from robot.api.deco import keyword
from datetime import datetime
import pytz 

class O2Utils:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.0'

    @keyword('Change XML Parameters')
    def change_xml_parameters(self, xmlstring, param_dictionary):
        """ Replace parameters in string XML with dictionary as argument """
        for key in param_dictionary:
            xmlstring = xmlstring.replace("${" + key + "}", param_dictionary[key])
        return xmlstring

    @keyword('Generate Timestamp')
    def generate_timestamp(self):
        UTC = pytz.timezone('Europe/Prague')
        timestamp = datetime.now(UTC) 
        return timestamp.strftime('%Y-%m-%dT%H:%M:%S.000%z')[:-2]+':00'

    @keyword('Generate Unique ID')
    def generate_unique_id(self):
        timestamp = datetime.now() 
        return 'aut.' + timestamp.strftime('%Y%m%d.%H%M%S.%f')[:-3]



# zmenit verzi v setup.py
# python setup.py bdist_wheel sdist
# twine upload dist/*

