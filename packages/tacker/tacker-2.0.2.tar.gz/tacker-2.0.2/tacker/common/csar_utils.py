# Copyright (C) 2019 NTT DATA
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import shutil

from oslo_log import log as logging
from oslo_utils import encodeutils
from oslo_utils import excutils
from toscaparser.tosca_template import ToscaTemplate
import zipfile

from tacker.common import exceptions
import tacker.conf


CONF = tacker.conf.CONF
LOG = logging.getLogger(__name__)


def _check_type(custom_def, node_type, type_list):
    for node_data_type, node_data_type_value in custom_def.items():
        if node_data_type == node_type and node_type in type_list:
            return True, node_data_type_value
        for k, v in node_data_type_value.items():
            if k == 'derived_from':
                if v in type_list and node_type == node_data_type:
                    return True, node_data_type_value
    return False, None


def _get_sw_image_artifact(artifacts):
    if not artifacts:
        return

    for artifact_value in artifacts.values():
        if 'type' in artifact_value:
            if artifact_value['type'] == 'tosca.artifacts.nfv.SwImage':
                return artifact_value


def _update_default_vnfd_data(node_value, node_type_value):
    vnf_properties = node_value['properties']
    type_properties = node_type_value['properties']
    for property_key, property_value in type_properties.items():
        if property_key == 'descriptor_id':
            # if descriptor_id is parameterized, then get the value from the
            # default property and set it in the vnf_properties.
            if vnf_properties and isinstance(
                    vnf_properties.get('descriptor_id'), dict):
                vnf_properties['descriptor_id'] = property_value.get("default")
    return vnf_properties


def _get_vnf_data(nodetemplates):
    type_list = ['tosca.nodes.nfv.VNF']
    for nt in nodetemplates:
        for node_name, node_value in nt.templates.items():
            type_status, node_type_value = _check_type(nt.custom_def,
                                            node_value['type'], type_list)
            if type_status and node_type_value:
                return _update_default_vnfd_data(node_value, node_type_value)


def _get_instantiation_levels(policies):
    if policies:
        for policy in policies:
            if policy.type_definition.type == \
                    'tosca.policies.nfv.InstantiationLevels':
                return policy.properties


def _update_flavour_data_from_vnf(custom_defs, node_tpl, flavour):
    type_list = ['tosca.nodes.nfv.VNF']

    type_status, _ = _check_type(custom_defs, node_tpl['type'], type_list)
    if type_status and node_tpl['properties']:
        vnf_properties = node_tpl['properties']
        if 'flavour_description' in vnf_properties:
            flavour.update(
                {'flavour_description': vnf_properties[
                    'flavour_description']})
        if 'flavour_id' in vnf_properties:
            flavour.update({'flavour_id': vnf_properties['flavour_id']})


def _get_software_image(custom_defs, nodetemplate_name, node_tpl):
    type_list = ['tosca.nodes.nfv.Vdu.Compute',
                 'tosca.nodes.nfv.Vdu.VirtualBlockStorage']
    type_status, _ = _check_type(custom_defs, node_tpl['type'], type_list)
    if type_status:
        properties = node_tpl['properties']
        sw_image_artifact = _get_sw_image_artifact(node_tpl.get('artifacts'))
        if sw_image_artifact:
            properties['sw_image_data'].update(
                {'software_image_id': nodetemplate_name})
            sw_image_data = properties['sw_image_data']
            if 'metadata' in sw_image_artifact:
                sw_image_data.update({'metadata':
                    sw_image_artifact['metadata']})
            return sw_image_data


def _populate_flavour_data(tosca):
    flavours = []
    for tp in tosca.nested_tosca_templates_with_topology:
        sw_image_list = []

        # Setting up flavour data
        flavour_id = tp.substitution_mappings.properties.get('flavour_id')
        if flavour_id:
            flavour = {'flavour_id': flavour_id}
        else:
            flavour = {}
        instantiation_levels = _get_instantiation_levels(tp.policies)
        if instantiation_levels:
            flavour.update({'instantiation_levels': instantiation_levels})
        for template_name, node_tpl in tp.tpl.get('node_templates').items():
            # check the flavour property in vnf data
            _update_flavour_data_from_vnf(tp.custom_defs, node_tpl, flavour)

            # Update the software image data
            sw_image = _get_software_image(tp.custom_defs, template_name,
                                           node_tpl)
            if sw_image:
                sw_image_list.append(sw_image)

        # Add software images for flavour
        if sw_image_list:
            flavour.update({'sw_images': sw_image_list})

        if flavour:
            flavours.append(flavour)

    return flavours


def _get_instantiation_levels_from_policy(tpl_policies):
    """Get defined instantiation levels

    Getting instantiation levels defined under policy type
    'tosca.policies.nfv.InstantiationLevels'.
    """

    levels = []
    for policy in tpl_policies:
        for key, value in policy.items():
            if value.get('type') == 'tosca.policies.nfv.InstantiationLevels'\
                    and value.get('properties', {}).get('levels', {}):
                levels = value.get('properties').get('levels').keys()
                default_level = value.get(
                    'properties').get('default_level')

                if default_level and default_level not in levels:
                    error_msg = "Level {} not found in defined levels" \
                                " {}".format(default_level,
                                             ",".join(sorted(levels)))
                    raise exceptions.InvalidCSAR(error_msg)
    return levels


def _validate_instantiation_levels(policy, instantiation_levels):
    expected_policy_type = ['tosca.policies.nfv.VduInstantiationLevels',
                            'tosca.policies.nfv.'
                            'VirtualLinkInstantiationLevels']
    for policy_name, policy_tpl in policy.items():
        if policy_tpl.get('type') not in expected_policy_type:
            return

        if not instantiation_levels:
            msg = ('Policy of type'
                   ' "tosca.policies.nfv.InstantiationLevels is not defined.')
            raise exceptions.InvalidCSAR(msg)
        if policy_tpl.get('properties'):
            levels_in_policy = policy_tpl.get(
                'properties').get('levels')

            if levels_in_policy:
                invalid_levels = set(levels_in_policy.keys()) - set(
                    instantiation_levels)
            else:
                invalid_levels = set()

            if invalid_levels:
                error_msg = "Level(s) {} not found in defined levels" \
                            " {}".format(",".join(sorted(invalid_levels)),
                                         ",".join(sorted(instantiation_levels)
                                                  ))
                raise exceptions.InvalidCSAR(error_msg)


def _validate_sw_image_data_for_artifact(node_tpl, template_name):
    artifact_type = []
    artifacts = node_tpl.get('artifacts')
    if artifacts:
        for key, value in artifacts.items():
            if value.get('type') == 'tosca.artifacts.nfv.SwImage':
                artifact_type.append(value.get('type'))

        if len(artifact_type) > 1:
            error_msg = ('artifacts of type "tosca.artifacts.nfv.SwImage"'
                         ' is added more than one time for'
                         ' node %(node)s.') % {'node': template_name}
            raise exceptions.InvalidCSAR(error_msg)

        if artifact_type and node_tpl.get('properties'):
            if not node_tpl.get('properties').get('sw_image_data'):
                error_msg = ('Node property "sw_image_data" is missing for'
                             ' artifact type %(type)s for '
                             'node %(node)s.') % {
                    'type': artifact_type[0], 'node': template_name}
                raise exceptions.InvalidCSAR(error_msg)


def _validate_sw_image_data_for_artifacts(tosca):
    for tp in tosca.nested_tosca_templates_with_topology:
        for template_name, node_tpl in tp.tpl.get('node_templates').items():
            _validate_sw_image_data_for_artifact(node_tpl, template_name)

    for template in tosca.nodetemplates:
        _validate_sw_image_data_for_artifact(
            template.entity_tpl, template.name)


def _get_data_from_csar(tosca, context, id):
    for tp in tosca.nested_tosca_templates_with_topology:
        levels = _get_instantiation_levels_from_policy(tp.tpl.get("policies"))
        for policy_tpl in tp.tpl.get("policies"):
            _validate_instantiation_levels(policy_tpl, levels)

    _validate_sw_image_data_for_artifacts(tosca)
    vnf_data = _get_vnf_data(tosca.nodetemplates)
    if not vnf_data:
        error_msg = "VNF properties are mandatory"
        raise exceptions.InvalidCSAR(error_msg)

    flavours = _populate_flavour_data(tosca)
    if not flavours:
        error_msg = "No VNF flavours are available"
        raise exceptions.InvalidCSAR(error_msg)

    return vnf_data, flavours


def _extract_csar_zip_file(file_path, extract_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            zf.extractall(extract_path)
    except (RuntimeError, zipfile.BadZipfile) as exp:
        with excutils.save_and_reraise_exception():
            LOG.error("Error encountered while extracting "
                      "csar zip file %(path)s. Error: %(error)s.",
                      {'path': file_path,
                      'error': encodeutils.exception_to_unicode(exp)})
            exp.reraise = False
            raise exceptions.InvalidZipFile(path=file_path)


def load_csar_data(context, package_uuid, zip_path):

    extract_zip_path = os.path.join(CONF.vnf_package.vnf_package_csar_path,
                                    package_uuid)
    _extract_csar_zip_file(zip_path, extract_zip_path)

    try:
        tosca = ToscaTemplate(zip_path, None, True)
        return _get_data_from_csar(tosca, context, package_uuid)
    except exceptions.InvalidCSAR as exp:
        with excutils.save_and_reraise_exception():
            LOG.error("Error processing CSAR file %(path)s for vnf package"
                      " %(uuid)s: Error: %(error)s. ",
                      {'path': zip_path, 'uuid': package_uuid,
                    'error': encodeutils.exception_to_unicode(exp)})
    except Exception as exp:
        with excutils.save_and_reraise_exception():
            LOG.error("Tosca parser failed for vnf package %(uuid)s: "
                      "Error: %(error)s. ", {'uuid': package_uuid,
                      'error': encodeutils.exception_to_unicode(exp)})
            exp.reraise = False
            raise exceptions.InvalidCSAR(encodeutils.exception_to_unicode
                                         (exp))


def delete_csar_data(package_uuid):
    # Remove zip and folder from the vnf_package_csar_path
    csar_zip_temp_path = os.path.join(CONF.vnf_package.vnf_package_csar_path,
                                      package_uuid)
    csar_path = os.path.join(CONF.vnf_package.vnf_package_csar_path,
                 package_uuid + ".zip")

    try:
        shutil.rmtree(csar_zip_temp_path)
        os.remove(csar_path)
    except OSError as exc:
        exc_message = encodeutils.exception_to_unicode(exc)
        msg = _('Failed to delete csar folder: '
                '%(csar_path)s, Error: %(exc)s')
        LOG.warning(msg, {'csar_path': csar_path, 'exc': exc_message})
