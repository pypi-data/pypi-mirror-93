"""
# CDK Bucket Deployment Expirator

![build](https://github.com/kcwinner/cdk-bucket-deployment-expirator/workflows/Build/badge.svg)
[![codecov](https://codecov.io/gh/kcwinner/cdk-bucket-deployment-expirator/branch/main/graph/badge.svg)](https://codecov.io/gh/kcwinner/cdk-bucket-deployment-expirator)
[![dependencies Status](https://david-dm.org/kcwinner/cdk-bucket-deployment-expirator/status.svg)](https://david-dm.org/kcwinner/cdk-bucket-deployment-expirator)
[![npm](https://img.shields.io/npm/dt/cdk-bucket-deployment-expirator)](https://www.npmjs.com/package/cdk-bucket-deployment-expirator)

[![npm version](https://badge.fury.io/js/cdk-bucket-deployment-expirator.svg)](https://badge.fury.io/js/cdk-bucket-deployment-expirator)
[![PyPI version](https://badge.fury.io/py/cdk-bucket-deployment-expirator.svg)](https://badge.fury.io/py/cdk-bucket-deployment-expirator)

## Why This Package

I've been having issues with my React deployments to AWS S3 while using Cloudfront due to browsers caching and attempting to load chunks that were unavailable after using [CDK Bucket Deployment](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-s3-deployment-readme.html).

I had been using `prune: true` to clean up the bucket and this was causing all previous chunks to be deleted. However, the reality is we want to support N number of older chunks, just in case, and provide a mechanism for alerting the user that a new version is available (not part of this construct).

## Must Be Used With CDK Bucket Deployment

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_s3_deployment import BucketDeployment, Source

bucket = Bucket(self, "SourceBucket")
now = Date().get_time()

bucket_deployment = BucketDeployment(self, "deploy-spa",
    sources=[Source.asset("path/to/assets")],
    destination_bucket=bucket,
    metadata=UserDefinedObjectMetadata(deployed=now.to_string()),
    prune=False
)

BucketDeploymentExpirator(self, "expirator",
    bucket_deployment=bucket_deployment, # need this to add cfn depends on
    source_bucket=bucket
)
```

## Versioning

I will *attempt* to align the major and minor version of this package with [AWS CDK], but always check the release descriptions for compatibility.

This currently supports [![GitHub package.json dependency version (prod)](https://img.shields.io/github/package-json/dependency-version/kcwinner/cdk-bucket-deployment-expirator/@aws-cdk/core)](https://github.com/aws/aws-cdk)

## References

* [CDK Bucket Deployment](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-s3-deployment-readme.html)
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_iam
import aws_cdk.aws_s3
import aws_cdk.aws_s3_deployment
import aws_cdk.core


class BucketDeploymentExpirator(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-bucket-deployment-expirator.BucketDeploymentExpirator",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        bucket_deployment: aws_cdk.aws_s3_deployment.BucketDeployment,
        source_bucket: aws_cdk.aws_s3.IBucket,
        deployments_to_keep: typing.Optional[jsii.Number] = None,
        meta_lookup_key: typing.Optional[builtins.str] = None,
        remove_unmarked: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param bucket_deployment: The CDK Bucket Deployment Construct. Required to addDependency
        :param source_bucket: The S3 bucket to remove old deployments from.
        :param deployments_to_keep: The number of old deployments to keep. Default: 3
        :param meta_lookup_key: The S3 metadata key to look for as a timestamp. Default: "deployed"
        :param remove_unmarked: Whether or not to remove items without a metadata key. Default: false
        :param role: Execution role associated with this function. Default: - A role is automatically created
        """
        props = BucketDeploymentExpiratorProps(
            bucket_deployment=bucket_deployment,
            source_bucket=source_bucket,
            deployments_to_keep=deployments_to_keep,
            meta_lookup_key=meta_lookup_key,
            remove_unmarked=remove_unmarked,
            role=role,
        )

        jsii.create(BucketDeploymentExpirator, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-bucket-deployment-expirator.BucketDeploymentExpiratorProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_deployment": "bucketDeployment",
        "source_bucket": "sourceBucket",
        "deployments_to_keep": "deploymentsToKeep",
        "meta_lookup_key": "metaLookupKey",
        "remove_unmarked": "removeUnmarked",
        "role": "role",
    },
)
class BucketDeploymentExpiratorProps:
    def __init__(
        self,
        *,
        bucket_deployment: aws_cdk.aws_s3_deployment.BucketDeployment,
        source_bucket: aws_cdk.aws_s3.IBucket,
        deployments_to_keep: typing.Optional[jsii.Number] = None,
        meta_lookup_key: typing.Optional[builtins.str] = None,
        remove_unmarked: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """
        :param bucket_deployment: The CDK Bucket Deployment Construct. Required to addDependency
        :param source_bucket: The S3 bucket to remove old deployments from.
        :param deployments_to_keep: The number of old deployments to keep. Default: 3
        :param meta_lookup_key: The S3 metadata key to look for as a timestamp. Default: "deployed"
        :param remove_unmarked: Whether or not to remove items without a metadata key. Default: false
        :param role: Execution role associated with this function. Default: - A role is automatically created
        """
        self._values: typing.Dict[str, typing.Any] = {
            "bucket_deployment": bucket_deployment,
            "source_bucket": source_bucket,
        }
        if deployments_to_keep is not None:
            self._values["deployments_to_keep"] = deployments_to_keep
        if meta_lookup_key is not None:
            self._values["meta_lookup_key"] = meta_lookup_key
        if remove_unmarked is not None:
            self._values["remove_unmarked"] = remove_unmarked
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def bucket_deployment(self) -> aws_cdk.aws_s3_deployment.BucketDeployment:
        """The CDK Bucket Deployment Construct.

        Required to addDependency
        """
        result = self._values.get("bucket_deployment")
        assert result is not None, "Required property 'bucket_deployment' is missing"
        return result

    @builtins.property
    def source_bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The S3 bucket to remove old deployments from."""
        result = self._values.get("source_bucket")
        assert result is not None, "Required property 'source_bucket' is missing"
        return result

    @builtins.property
    def deployments_to_keep(self) -> typing.Optional[jsii.Number]:
        """The number of old deployments to keep.

        :default: 3
        """
        result = self._values.get("deployments_to_keep")
        return result

    @builtins.property
    def meta_lookup_key(self) -> typing.Optional[builtins.str]:
        """The S3 metadata key to look for as a timestamp.

        :default: "deployed"
        """
        result = self._values.get("meta_lookup_key")
        return result

    @builtins.property
    def remove_unmarked(self) -> typing.Optional[builtins.bool]:
        """Whether or not to remove items without a metadata key.

        :default: false
        """
        result = self._values.get("remove_unmarked")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Execution role associated with this function.

        :default: - A role is automatically created
        """
        result = self._values.get("role")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketDeploymentExpiratorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BucketDeploymentExpirator",
    "BucketDeploymentExpiratorProps",
]

publication.publish()
