__version__ = "0.0.2"

from gamera.core import init_gamera
init_gamera()
from rodan.jobs import module_loader

module_loader('rodan.jobs.gamera-rodan.wrappers.classification')
module_loader('rodan.jobs.gamera-rodan.wrappers.masking')

module_loader('rodan.jobs.gamera-rodan.wrappers.plugins.binarization')
module_loader('rodan.jobs.gamera-rodan.wrappers.plugins.image_conversion')
module_loader('rodan.jobs.gamera-rodan.wrappers.plugins.morphology')
module_loader('rodan.jobs.gamera-rodan.wrappers.plugins.threshold')
module_loader('rodan.jobs.gamera-rodan.wrappers.plugins.image_utilities')
