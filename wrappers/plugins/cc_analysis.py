import gamera.core
import gamera.gamera_xml
import gamera.classify
import gamera.knn
from rodan.jobs.base import RodanTask


class CCAnalysis(RodanTask):
    name = 'CC Analysis'
    author = "Andrew Fogarty"
    description = "Performs CC analysis on an image, producing a GameraXML file of glyphs."
    enabled = True
    category = "Gamera - Classification"
    interactive = False
    settings = {}
    input_port_types = [{
        'name': 'Staffless Image',
        'resource_types': ['image/onebit+png'],
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'Glyphs',
        'resource_types': ['application/gamera+xml'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):
        image_path = inputs['Staffless Image'][0]['resource_path']
        input_image = gamera.core.load_image(image_path)
        ccs = input_image.cc_analysis()
        output_xml = gamera.gamera_xml.WriteXMLFile(glyphs=ccs,
                                                    with_features=True)
        output_xml.write_filename(outputs['Glyphs'][0]['resource_path'])
