"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""
from test.testlib.testcase import BaseTestCase
from cfnlint import Transform
from cfnlint.decode import cfn_yaml


class TestTransform(BaseTestCase):
    """Test Transform Parsing """

    def test_parameter_for_autopublish_version(self):
        """Test Parameter is created for autopublish version run"""
        filename = 'test/fixtures/templates/good/transform/auto_publish_alias.yaml'
        region = 'us-east-1'
        template = cfn_yaml.load(filename)
        transformed_template = Transform(filename, template, region)
        transformed_template.transform_template()
        self.assertDictEqual(transformed_template._parameters, {
                             'Stage1': 'Alias', 'Stage2': 'Alias'})
        self.assertDictEqual(
            transformed_template._template.get('Resources').get(
                'SkillFunctionAliasAlias').get('Properties'),
            {
                'Name': 'Alias',
                'FunctionName': {'Ref': 'SkillFunction'},
                'FunctionVersion': {'Fn::GetAtt': ['SkillFunctionVersion55ff35af87', 'Version']}
            })

    def test_conversion_of_step_function_definition_uri(self):
        """ Tests that the a serverless step function can convert a local path to a s3 path """
        filename = 'test/fixtures/templates/good/transform/step_function_local_definition.yaml'
        region = 'us-east-1'
        template = cfn_yaml.load(filename)
        transformed_template = Transform(filename, template, region)
        transformed_template.transform_template()
        self.assertDictEqual(
            transformed_template._template.get('Resources').get(
                'StateMachine').get('Properties').get('DefinitionS3Location'),
            {
                'Bucket': 'bucket',
                'Key': 'value'
            })

    def test_parameter_for_autopublish_version_bad(self):
        """Test Parameter is created for autopublish version run"""
        filename = 'test/fixtures/templates/bad/transform/auto_publish_alias.yaml'
        region = 'us-east-1'
        template = cfn_yaml.load(filename)
        transformed_template = Transform(filename, template, region)
        transformed_template.transform_template()
        self.assertDictEqual(transformed_template._parameters, {})

    def test_test_function_using_image_good(self):
        """Test Parameter is created for autopublish version run"""
        filename = 'test/fixtures/templates/good/transform/function_using_image.yaml'
        region = 'us-east-1'
        template = cfn_yaml.load(filename)
        transformed_template = Transform(filename, template, region)
        transformed_template.transform_template()
        self.assertDictEqual(transformed_template._parameters, {})
