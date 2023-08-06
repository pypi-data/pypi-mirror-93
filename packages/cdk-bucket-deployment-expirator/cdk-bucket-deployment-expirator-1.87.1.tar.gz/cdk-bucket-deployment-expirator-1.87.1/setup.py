import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-bucket-deployment-expirator",
    "version": "1.87.1",
    "description": "Opinionated CDK Bucket Deployment object pruner for maintaining N old versions",
    "license": "Apache-2.0",
    "url": "https://github.com/kcwinner/cdk-bucket-deployment-expirator.git",
    "long_description_content_type": "text/markdown",
    "author": "Ken Winner<kcswinner@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/kcwinner/cdk-bucket-deployment-expirator.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_bucket_deployment_expirator",
        "cdk_bucket_deployment_expirator._jsii"
    ],
    "package_data": {
        "cdk_bucket_deployment_expirator._jsii": [
            "cdk-bucket-deployment-expirator@1.87.1.jsii.tgz"
        ],
        "cdk_bucket_deployment_expirator": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam>=1.87.1, <2.0.0",
        "aws-cdk.aws-lambda-nodejs>=1.87.1, <2.0.0",
        "aws-cdk.aws-lambda>=1.87.1, <2.0.0",
        "aws-cdk.aws-s3-deployment>=1.87.1, <2.0.0",
        "aws-cdk.aws-s3>=1.87.1, <2.0.0",
        "aws-cdk.core>=1.87.1, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.15.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
