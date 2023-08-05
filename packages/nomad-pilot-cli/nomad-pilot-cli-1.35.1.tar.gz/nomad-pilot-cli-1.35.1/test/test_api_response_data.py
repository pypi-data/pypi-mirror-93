# coding: utf-8

"""
    Nomad Pilot

    This is the API descriptor for the Nomad Pilot API, responsible for shipping and logistics processing. Developed by [Samarkand Global](https://www.samarkand.global/) in partnership with [SF Express](https://www.sf-express.com/), [eSinotrans](http://air.esinotrans.com/), [sto](http://sto-express.co.uk/). Read the documentation online at [Nomad API Suite](https://api.samarkand.io/). - Install for node with `npm install nomad_pilot_cli` - Install for python with `pip install nomad-pilot-cli` - Install for Maven users `groupId, com.gitlab.samarkand-nomad; artifactId, nomad-pilot-cli`  # noqa: E501

    The version of the OpenAPI document: 1.35.1
    Contact: paul@samarkand.global
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import nomad_pilot_cli
from nomad_pilot_cli.models.api_response_data import ApiResponseData  # noqa: E501
from nomad_pilot_cli.rest import ApiException

class TestApiResponseData(unittest.TestCase):
    """ApiResponseData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ApiResponseData
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = nomad_pilot_cli.models.api_response_data.ApiResponseData()  # noqa: E501
        if include_optional :
            return ApiResponseData(
                waybill_id = '0', 
                order_sn = '0', 
                order_ref = '0', 
                seller_order_ref = '0', 
                domestic_delivery_company = 'YTO', 
                delivery_status = '0', 
                delivery_note = '0', 
                delivery_slip_url = '0', 
                tracking_url = '0', 
                check_points = ["@accept_time 2020-05-01 04:59:38; @accept_address 伦敦; @remark 寄方准备快件中,当前地点: 【GB London Delivery Centre (英國倫敦收派中心)】; @opcode 647; @zoneGmt 1","...","@accept_time 2020-05-13 09:10:49; @accept_address 江门市;  @remark 在官网'运单资料&签收图',可查看签收人信息; @opcode 8000; @stayWhyCode  1; @zoneGmt 8"]
            )
        else :
            return ApiResponseData(
        )

    def testApiResponseData(self):
        """Test ApiResponseData"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
