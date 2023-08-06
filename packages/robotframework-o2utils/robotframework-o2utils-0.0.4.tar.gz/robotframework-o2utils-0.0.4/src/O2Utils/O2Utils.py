from robot.api.deco import keyword
from datetime import datetime
import pytz 


class O2Utils:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.0'

    @keyword('Change XML Parameters')
    def change_xml_parameters(self, xmlString, param_dictionary):
        """ Replace parameters in string XML with dictionary as argument. \n
            Do not add messageId, extOrderId, referenceTransactionId and timestamp,
            those are added automatically """

        # add parameters
        uid = self.generate_unique_id()
        param_dictionary['messageId'] = uid
        param_dictionary['extOrderId'] = uid
        param_dictionary['referenceTransactionId'] = uid
        param_dictionary['timestamp'] = self.generate_timestamp()

        for key in param_dictionary:
            xmlString = xmlString.replace("${" + key + "}", param_dictionary[key])
        return xmlString

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

