#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           gamera-rodan
# Program Description:    Job wrappers that allows some Gamrea functionality to work in Rodan.
#
# Filename:               gamera-rodan/wrappers/classification.py
# Purpose:                Wrapper for classification.
#
# Copyright (C) 2016 DDMAL
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------

import gamera.core
import gamera.gamera_xml
import gamera.classify
import gamera.knn
from gamera.core import load_image
import os
from shutil import copyfile

from rodan.jobs.base import RodanTask


class ClassificationTask(RodanTask):
    name = 'Classifier'
    author = "Ling-Xiao Yang"
    description = "Performs classification on a binarized staff-less image and outputs an xml file."
    enabled = True
    category = "Gamera - Classification"
    settings = {}
    interactive = False

    input_port_types = [{
        'name': 'Staffless Image',
        'resource_types': ['image/onebit+png'],
        'minimum': 1,
        'maximum': 1
    }, {
        'name': 'Classifier',
        'resource_types': ['application/gamera+xml'],
        'minimum': 1,
        'maximum': 1
    }, {
        'name': 'Feature Selection',
        'resource_types': ['application/gamera+xml'],
        'minimum': 0,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'Classification Result',
        'resource_types': ['application/gamera+xml'],
        'minimum': 1,
        'maximum': 2
    }]

    def run_my_task(self, inputs, settings, outputs):
        staffless_image_path = inputs['Staffless Image'][0]['resource_path']
        classifier_path = inputs['Classifier'][0]['resource_path']
        tempPath = ''
        with self.tempdir() as tdir:
            tempPath = os.path.join(tdir, classifier_path + '.xml')
        copyfile(classifier_path, tempPath)
        result_path = outputs['Classification Result'][0]['resource_path']
        cknn = gamera.knn.kNNNonInteractive(tempPath)
        if 'Feature Selection' in inputs:
            cknn.load_settings(inputs['Feature Selection'][0]['resource_path'])
        func = gamera.classify.BoundingBoxGroupingFunction(4)
        input_image = gamera.core.load_image(staffless_image_path)
        ccs = input_image.cc_analysis()

        cs_image = cknn.group_and_update_list_automatic(ccs,
                                                        grouping_function=func,
                                                        max_parts_per_group=4,
                                                        max_graph_size=16)

        cknn.generate_features_on_glyphs(cs_image)
        output_xml = gamera.gamera_xml.WriteXMLFile(glyphs=cs_image, with_features=True)
        for i in range(len(outputs['Classification Result'])):
            output_xml.write_filename(outputs['Classification Result'][i]['resource_path'])
