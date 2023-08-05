# coding=utf-8
# *** WARNING: this file was generated by pulumi-gen-eks. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import errno
from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call


class InstallPluginCommand(install):
    def run(self):
        install.run(self)
        try:
            check_call(['pulumi', 'plugin', 'install', 'resource', 'eks', '0.22.0'])
        except OSError as error:
            if error.errno == errno.ENOENT:
                print("""
                There was an error installing the eks resource provider plugin.
                It looks like `pulumi` is not installed on your system.
                Please visit https://pulumi.com/ to install the Pulumi CLI.
                You may try manually installing the plugin by running
                `pulumi plugin install resource eks 0.22.0`
                """)
            else:
                raise


def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(name='pulumi_eks',
      version='0.22.0',
      description="Pulumi Amazon Web Services (AWS) EKS Components.",
      long_description=readme(),
      long_description_content_type='text/markdown',
      cmdclass={
          'install': InstallPluginCommand,
      },
      keywords='pulumi aws eks',
      url='https://pulumi.com',
      project_urls={
          'Repository': 'https://github.com/pulumi/pulumi-eks'
      },
      license='Apache-2.0',
      packages=find_packages(),
      package_data={
          'pulumi_eks': [
              'py.typed',
          ]
      },
      install_requires=[
          'parver>=0.2.1',
          'pulumi>=2.15.5,<3.0.0',
          'pulumi-aws>=3.18.0,<4.0.0',
          'pulumi-kubernetes>=2.7.3,<3.0.0',
          'semver>=2.8.1'
      ],
      zip_safe=False)
