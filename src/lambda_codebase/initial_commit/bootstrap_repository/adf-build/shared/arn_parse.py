# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""Helper module to assist in the parsing of ARNS and AWS Partitions."""

from dataclasses import InitVar, asdict, dataclass, field

from errors import MalformedArnError


@dataclass
class Arn:
    """Parses Amazon Resource Names (ARNs) and returns its parts."""
    arn: InitVar[str]
    partition: str = field(init=False)
    service: str = field(init=False)
    region: str = field(init=False)
    account_id: str = field(init=False)
    resource_type: str = field(init=False)
    resource_id: str = field(init=False)

    def __post_init__(self, arn):
        if not arn.startswith('arn:'):
            raise MalformedArnError

        elements = arn.split(':')
        self.partition = elements[1]
        self.service = elements[2]
        self.region = elements[3]
        self.account_id = elements[4]

        if len(elements) == 6:
            res_elements = elements[5].split('/')
            if len(res_elements) == 1:
                self.resource_type = ""
                self.resource_id = elements[5]
            else:
                self.resource_type = res_elements[0]
                self.resource_id = '/'.join(res_elements[1:])

        if len(elements) == 7:
            self.resource_type = elements[5]
            self.resource_id = elements[6]

    def as_dict(self):
        return asdict(self)


def set_aws_partition(region: str) -> str:
    """Returns the proper partition for Commercial and GovCloud.

    :param region: Current region as a string.
    :return: String containing either the commercial or GovCloud partition.
    """
    if region.startswith('us-gov'):
        return 'aws-us-gov'
    else:
        return 'aws'
