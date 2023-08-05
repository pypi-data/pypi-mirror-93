# Global Imports
import json
from collections import defaultdict

# Metaparser
from genie.metaparser import MetaParser

# =============================================
# Collection for '/mgmt/tm/sys/turboflex/features' resources
# =============================================


class SysTurboflexFeaturesSchema(MetaParser):

    schema = {}


class SysTurboflexFeatures(SysTurboflexFeaturesSchema):
    """ To F5 resource for /mgmt/tm/sys/turboflex/features
    """

    cli_command = "/mgmt/tm/sys/turboflex/features"

    def rest(self):

        response = self.device.get(self.cli_command)

        response_json = response.json()

        if not response_json:
            return {}

        return response_json
