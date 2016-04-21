#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           gamera-rodan
# Program Description:    Job wrappers that allows some Gamrea functionality to work in Rodan.
#
# Filename:               gamera-rodan/wrappers/threshold.py
# Purpose:                Wrapper for threshold plugins.
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

import gamera
from gamera.core import load_image
from gamera.plugins import threshold
from rodan.jobs.base import RodanTask

import logging
logger = logging.getLogger('rodan')

class gamera_otsu_threshold(RodanTask):

    name = 'Otsu Threshold'
    author = 'Ryan Bannon'
    description = gamera.plugins.threshold.otsu_threshold.escape_docstring().replace("\\n", "\n").replace('\\"', '"')
    settings = {
        'title': 'Otsu threshold settings',
        'type': 'object',
        'properties': {
            'Storage format': {
                'enum': ['Dense (no compression)', 'RLE (run-length encoding compression)'],
                'type': 'string',
                'default': 'Dense (no compression)',
                'description': 'Specifies the compression type for the result.'
            }
        }
    }

    enabled = True
    category = "Gamera - Threshold"
    interactive = False

    input_port_types = [{
        'name': 'Greyscale PNG image',
        'resource_types': ['image/greyscale+png'],
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'Onebit PNG image',
        'resource_types': ['image/onebit+png'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        # Set execution settings.
        compression = 0
        if settings['Storage format'] == 'RLE (run-length encoding compression)':
            compression = 1

        image_source = load_image(inputs['Greyscale PNG image'][0]['resource_path'])
    	image_result = image_source.otsu_threshold(compression) 
    	image_result.save_PNG(outputs['Onebit PNG image'][0]['resource_path'])
        return True
