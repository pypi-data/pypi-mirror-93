#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from flask_restplus import Resource, abort
from flask import request

from nomad.datamodel import OptimadeEntry

from .api import api
from .common import base_request_args, base_search_request, nentries, ns
from .models import json_api_single_response_model, entry_listing_endpoint_parser, Meta, \
    Links as LinksModel, single_entry_endpoint_parser, base_endpoint_parser, \
    json_api_info_response_model, json_api_list_response_model, EntryDataObject, \
    get_entry_properties, to_calc_with_metadata
from .filterparser import parse_filter, FilterException


@ns.route('/structures')
class StructureList(Resource):
    @api.doc('structures')
    @api.response(400, 'Invalid requests, e.g. bad parameter.')
    @api.expect(entry_listing_endpoint_parser, validate=True)
    @api.marshal_with(json_api_list_response_model, skip_none=True, code=200)
    def get(self):
        ''' Returns a list of structures that match the given optimade filter expression. '''
        response_fields = base_request_args()

        try:
            filter = request.args.get('filter', None)
            page_limit = int(request.args.get('page_limit', 10))
            page_number = int(request.args.get('page_number', 1))
            sort = request.args.get('sort', request.args.get('sort', 'chemical_formula_reduced'))

            order = 1
            if sort[0:1] == '-':
                order = -1
                sort = sort[1:]

        except Exception:
            abort(400, message='bad parameter types')  # TODO Specific json API error handling

        sort_quantity = OptimadeEntry.m_def.all_quantities.get(sort, None)
        if sort_quantity is None:
            abort(400, message='cannot sort by %s' % sort)  # TODO Specific json API error handling
        sort_quantity_a_optimade = sort_quantity.m_get_annotations('optimade')
        if not sort_quantity_a_optimade.sortable:
            abort(400, message='cannot sort by %s' % sort)  # TODO Specific json API error handling

        search_request = base_search_request().include('calc_id', 'upload_id')

        if filter is not None:
            try:
                search_request.query(parse_filter(filter))
            except FilterException as e:
                abort(400, message='Could not parse filter expression: %s' % str(e))

        result = search_request.execute_paginated(
            page=page_number,
            per_page=page_limit,
            order=order,
            order_by='dft.optimade.%s' % sort)

        returned = result['pagination']['total']
        results = to_calc_with_metadata(result['results'])
        assert len(results) == len(result['results']), 'archive and elasticsearch are not consistent'

        return dict(
            meta=Meta(
                query=request.url,
                returned=returned,
                available=nentries(),
                last_id=results[-1].calc_id if len(results) > 0 else None),
            links=LinksModel(
                'structures',
                returned=returned,
                page_number=page_number,
                page_limit=page_limit,
                sort=sort, filter=filter),
            data=[EntryDataObject(d, optimade_type='structures', response_fields=response_fields) for d in results]
        ), 200


@ns.route('/structures/<string:id>')
class Structure(Resource):
    @api.doc('structure')
    @api.response(400, 'Invalid requests, e.g. bad parameter.')
    @api.response(404, 'Id does not exist.')
    @api.expect(single_entry_endpoint_parser, validate=True)
    @api.marshal_with(json_api_single_response_model, skip_none=True, code=200)
    def get(self, id: str):
        ''' Retrieve a single structure for the given id '''
        response_fields = base_request_args()
        search_request = base_search_request().search_parameters(calc_id=id)

        result = search_request.execute_paginated(
            page=1,
            per_page=1)

        available = result['pagination']['total']
        results = to_calc_with_metadata(result['results'])
        assert len(results) == len(result['results']), 'Mongodb and elasticsearch are not consistent'

        if available == 0:
            abort(404, 'The calculation with id %s does not exist' % id)

        return dict(
            meta=Meta(query=request.url, returned=1),
            data=EntryDataObject(results[0], optimade_type='structures', response_fields=response_fields)
        ), 200


@ns.route('/info/structures')
class StructuresInfo(Resource):
    @api.doc('structures_info')
    @api.response(400, 'Invalid requests, e.g. bad parameter.')
    @api.expect(base_endpoint_parser, validate=True)
    @api.marshal_with(json_api_info_response_model, skip_none=True, code=200)
    def get(self):
        ''' Returns information about the structures endpoint implementation '''
        base_request_args()

        result = {
            'description': 'a structure entry',
            'properties': get_entry_properties(),
            'formats': ['json'],
            'output_fields_by_format': {
                'json': list(OptimadeEntry.m_def.all_properties.keys())}
        }

        return dict(
            meta=Meta(query=request.url, returned=1),
            data=result
        ), 200
