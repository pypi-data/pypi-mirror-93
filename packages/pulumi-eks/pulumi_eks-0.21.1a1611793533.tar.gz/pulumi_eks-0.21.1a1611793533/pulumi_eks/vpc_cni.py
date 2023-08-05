# coding=utf-8
# *** WARNING: this file was generated by pulumi-gen-eks. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from . import _utilities, _tables

__all__ = ['VpcCni']


class VpcCni(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 custom_network_config: Optional[pulumi.Input[bool]] = None,
                 eni_config_label_def: Optional[pulumi.Input[str]] = None,
                 eni_mtu: Optional[pulumi.Input[int]] = None,
                 external_snat: Optional[pulumi.Input[bool]] = None,
                 image: Optional[pulumi.Input[str]] = None,
                 kubeconfig: Optional[Any] = None,
                 log_file: Optional[pulumi.Input[str]] = None,
                 log_level: Optional[pulumi.Input[str]] = None,
                 node_port_support: Optional[pulumi.Input[bool]] = None,
                 veth_prefix: Optional[pulumi.Input[str]] = None,
                 warm_eni_target: Optional[pulumi.Input[int]] = None,
                 warm_ip_target: Optional[pulumi.Input[int]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        VpcCni manages the configuration of the Amazon VPC CNI plugin for Kubernetes by applying its YAML chart.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] custom_network_config: Specifies that your pods may use subnets and security groups (within the same VPC as your control plane resources) that are independent of your cluster's `resourcesVpcConfig`.
               
               Defaults to false.
        :param pulumi.Input[str] eni_config_label_def: Specifies the ENI_CONFIG_LABEL_DEF environment variable value for worker nodes. This is used to tell Kubernetes to automatically apply the ENIConfig for each Availability Zone
               Ref: https://docs.aws.amazon.com/eks/latest/userguide/cni-custom-network.html (step 5(c))
               
               Defaults to the official AWS CNI image in ECR.
        :param pulumi.Input[int] eni_mtu: Used to configure the MTU size for attached ENIs. The valid range is from 576 to 9001.
               
               Defaults to 9001.
        :param pulumi.Input[bool] external_snat: Specifies whether an external NAT gateway should be used to provide SNAT of secondary ENI IP addresses. If set to true, the SNAT iptables rule and off-VPC IP rule are not applied, and these rules are removed if they have already been applied.
               
               Defaults to false.
        :param pulumi.Input[str] image: Specifies the container image to use in the AWS CNI cluster DaemonSet.
               
               Defaults to the official AWS CNI image in ECR.
        :param Any kubeconfig: The kubeconfig to use when setting the VPC CNI options.
        :param pulumi.Input[str] log_file: Specifies the file path used for logs.
               
               Defaults to "stdout" to emit Pod logs for `kubectl logs`.
        :param pulumi.Input[str] log_level: Specifies the log level used for logs.
               
               Defaults to "DEBUG"
               Valid values: "DEBUG", "INFO", "WARN", "ERROR", or "FATAL".
        :param pulumi.Input[bool] node_port_support: Specifies whether NodePort services are enabled on a worker node's primary network interface. This requires additional iptables rules and that the kernel's reverse path filter on the primary interface is set to loose.
               
               Defaults to true.
        :param pulumi.Input[str] veth_prefix: Specifies the veth prefix used to generate the host-side veth device name for the CNI.
               
               The prefix can be at most 4 characters long.
               
               Defaults to "eni".
        :param pulumi.Input[int] warm_eni_target: Specifies the number of free elastic network interfaces (and all of their available IP addresses) that the ipamD daemon should attempt to keep available for pod assignment on the node.
               
               Defaults to 1.
        :param pulumi.Input[int] warm_ip_target: Specifies the number of free IP addresses that the ipamD daemon should attempt to keep available for pod assignment on the node.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['custom_network_config'] = custom_network_config
            __props__['eni_config_label_def'] = eni_config_label_def
            __props__['eni_mtu'] = eni_mtu
            __props__['external_snat'] = external_snat
            __props__['image'] = image
            if kubeconfig is None and not opts.urn:
                raise TypeError("Missing required property 'kubeconfig'")
            __props__['kubeconfig'] = kubeconfig
            __props__['log_file'] = log_file
            __props__['log_level'] = log_level
            __props__['node_port_support'] = node_port_support
            __props__['veth_prefix'] = veth_prefix
            __props__['warm_eni_target'] = warm_eni_target
            __props__['warm_ip_target'] = warm_ip_target
        super(VpcCni, __self__).__init__(
            'eks:index:VpcCni',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VpcCni':
        """
        Get an existing VpcCni resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return VpcCni(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

