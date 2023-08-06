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

from tacker.common import exceptions
from tacker import context
from tacker.db.db_sqlalchemy import models
from tacker import objects
from tacker.objects import vnf_package
from tacker.tests.unit.db.base import SqlTestCase
from tacker.tests.unit.objects import fakes as fake_data
from tacker.tests.unit.vnfpkgm import fakes


class TestVnfPackage(SqlTestCase):

    def setUp(self):
        super(TestVnfPackage, self).setUp()
        self.context = context.get_admin_context()
        self.vnf_package = self._create_vnf_package()
        self.vnf_deployment_flavour = self._create_vnf_deployment_flavour()

    def _create_vnf_package(self):
        vnfpkgm = objects.VnfPackage(context=self.context,
                                     **fake_data.vnf_package_data)
        vnfpkgm.create()
        return vnfpkgm

    def _create_vnf_deployment_flavour(self):
        flavour_data = fake_data.vnf_deployment_flavour
        flavour_data.update({'package_uuid': self.vnf_package.id})
        vnf_deployment_flavour = objects.VnfDeploymentFlavour(
            context=self.context, **flavour_data)
        vnf_deployment_flavour.create()
        return vnf_deployment_flavour

    def test_add_user_defined_data(self):
        vnf_package_db = models.VnfPackage()
        vnf_package_db.update(fakes.fake_vnf_package())
        vnf_package_db.save(self.context.session)
        result = vnf_package._add_user_defined_data(
            self.context, vnf_package_db.id, vnf_package_db.user_data)
        self.assertEqual(None, result)

    def test_vnf_package_get_by_id(self):
        result = vnf_package._vnf_package_get_by_id(
            self.context, self.vnf_package.id,
            columns_to_join=['vnf_deployment_flavours'])
        self.assertEqual(self.vnf_package.id, result.id)
        self.assertTrue(result.vnf_deployment_flavours)

    def test_vnf_package_create(self):
        result = vnf_package._vnf_package_create(self.context,
                                                 fakes.fake_vnf_package())
        self.assertTrue(result.id)

    def test_vnf_package_list(self):
        result = vnf_package._vnf_package_list(
            self.context, columns_to_join=['vnf_deployment_flavours'])
        self.assertTrue(isinstance(result, list))
        self.assertTrue(result)

    def test_vnf_package_update(self):
        update = {'user_data': {'test': 'xyz'}}
        result = vnf_package._vnf_package_update(
            self.context, self.vnf_package.id, update)
        self.assertEqual({'test': 'xyz'}, result.user_data)

    def test_destroy_vnf_package(self):
        vnf_package._destroy_vnf_package(self.context,
                                         self.vnf_package.id)
        self.assertRaises(
            exceptions.VnfPackageNotFound,
            objects.VnfPackage.get_by_id, self.context,
            self.vnf_package.id)

    def test_make_vnf_packages_list(self):
        response = vnf_package._vnf_package_list(self.context)
        vnf_pack_list_obj = objects.VnfPackagesList(self.context)
        result = vnf_package._make_vnf_packages_list(
            self.context, vnf_pack_list_obj, response, None)
        self.assertTrue(isinstance(result, objects.VnfPackagesList))
        self.assertTrue(result.objects[0].id)
