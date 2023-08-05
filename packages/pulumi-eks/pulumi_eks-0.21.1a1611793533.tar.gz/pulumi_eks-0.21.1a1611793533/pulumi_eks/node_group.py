# coding=utf-8
# *** WARNING: this file was generated by pulumi-gen-eks. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from . import _utilities, _tables
from .vpc_cni import VpcCni
from ._inputs import *
import pulumi_aws
import pulumi_kubernetes

__all__ = ['NodeGroup']


class NodeGroup(pulumi.ComponentResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ami_id: Optional[pulumi.Input[str]] = None,
                 auto_scaling_group_tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 bootstrap_extra_args: Optional[pulumi.Input[str]] = None,
                 cloud_formation_tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 cluster: Optional[pulumi.Input[pulumi.InputType['CoreDataArgs']]] = None,
                 cluster_ingress_rule: Optional[pulumi.Input['pulumi_aws.ec2.SecurityGroupRule']] = None,
                 desired_capacity: Optional[pulumi.Input[int]] = None,
                 encrypt_root_block_device: Optional[pulumi.Input[bool]] = None,
                 extra_node_security_groups: Optional[pulumi.Input[Sequence[pulumi.Input['pulumi_aws.ec2.SecurityGroup']]]] = None,
                 gpu: Optional[pulumi.Input[bool]] = None,
                 instance_profile: Optional[pulumi.Input['pulumi_aws.iam.InstanceProfile']] = None,
                 instance_type: Optional[pulumi.Input[str]] = None,
                 key_name: Optional[pulumi.Input[str]] = None,
                 kubelet_extra_args: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 max_size: Optional[pulumi.Input[int]] = None,
                 min_size: Optional[pulumi.Input[int]] = None,
                 node_associate_public_ip_address: Optional[pulumi.Input[bool]] = None,
                 node_public_key: Optional[pulumi.Input[str]] = None,
                 node_root_volume_size: Optional[pulumi.Input[int]] = None,
                 node_security_group: Optional[pulumi.Input['pulumi_aws.ec2.SecurityGroup']] = None,
                 node_subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 node_user_data: Optional[pulumi.Input[str]] = None,
                 node_user_data_override: Optional[pulumi.Input[str]] = None,
                 spot_price: Optional[pulumi.Input[str]] = None,
                 taints: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['TaintArgs']]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        NodeGroup is a component that wraps the AWS EC2 instances that provide compute capacity for an EKS cluster.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ami_id: The AMI ID to use for the worker nodes.
               
               Defaults to the latest recommended EKS Optimized Linux AMI from the AWS Systems Manager Parameter Store.
               
               Note: `amiId` and `gpu` are mutually exclusive.
               
               See for more details:
               - https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] auto_scaling_group_tags: The tags to apply to the NodeGroup's AutoScalingGroup in the CloudFormation Stack.
               
               Per AWS, all stack-level tags, including automatically created tags, and the `cloudFormationTags` option are propagated to resources that AWS CloudFormation supports, including the AutoScalingGroup. See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html
               
               Note: Given the inheritance of auto-generated CF tags and `cloudFormationTags`, you should either supply the tag in `autoScalingGroupTags` or `cloudFormationTags`, but not both.
        :param pulumi.Input[str] bootstrap_extra_args: Additional args to pass directly to `/etc/eks/bootstrap.sh`. Fror details on available options, see: https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh. Note that the `--apiserver-endpoint`, `--b64-cluster-ca` and `--kubelet-extra-args` flags are included automatically based on other configuration parameters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] cloud_formation_tags: The tags to apply to the CloudFormation Stack of the Worker NodeGroup.
               
               Note: Given the inheritance of auto-generated CF tags and `cloudFormationTags`, you should either supply the tag in `autoScalingGroupTags` or `cloudFormationTags`, but not both.
        :param pulumi.Input[pulumi.InputType['CoreDataArgs']] cluster: The target EKS cluster.
        :param pulumi.Input['pulumi_aws.ec2.SecurityGroupRule'] cluster_ingress_rule: The ingress rule that gives node group access.
        :param pulumi.Input[int] desired_capacity: The number of worker nodes that should be running in the cluster. Defaults to 2.
        :param pulumi.Input[bool] encrypt_root_block_device: Encrypt the root block device of the nodes in the node group.
        :param pulumi.Input[Sequence[pulumi.Input['pulumi_aws.ec2.SecurityGroup']]] extra_node_security_groups: Extra security groups to attach on all nodes in this worker node group.
               
               This additional set of security groups captures any user application rules that will be needed for the nodes.
        :param pulumi.Input[bool] gpu: Use the latest recommended EKS Optimized Linux AMI with GPU support for the worker nodes from the AWS Systems Manager Parameter Store.
               
               Defaults to false.
               
               Note: `gpu` and `amiId` are mutually exclusive.
               
               See for more details:
               - https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html
               - https://docs.aws.amazon.com/eks/latest/userguide/retrieve-ami-id.html
        :param pulumi.Input['pulumi_aws.iam.InstanceProfile'] instance_profile: The ingress rule that gives node group access.
        :param pulumi.Input[str] instance_type: The instance type to use for the cluster's nodes. Defaults to "t2.medium".
        :param pulumi.Input[str] key_name: Name of the key pair to use for SSH access to worker nodes.
        :param pulumi.Input[str] kubelet_extra_args: Extra args to pass to the Kubelet. Corresponds to the options passed in the `--kubeletExtraArgs` flag to `/etc/eks/bootstrap.sh`. For example, '--port=10251 --address=0.0.0.0'. Note that the `labels` and `taints` properties will be applied to this list (using `--node-labels` and `--register-with-taints` respectively) after to the expicit `kubeletExtraArgs`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Custom k8s node labels to be attached to each woker node. Adds the given key/value pairs to the `--node-labels` kubelet argument.
        :param pulumi.Input[int] max_size: The maximum number of worker nodes running in the cluster. Defaults to 2.
        :param pulumi.Input[int] min_size: The minimum number of worker nodes running in the cluster. Defaults to 1.
        :param pulumi.Input[bool] node_associate_public_ip_address: Whether or not to auto-assign public IP addresses on the EKS worker nodes. If this toggle is set to true, the EKS workers will be auto-assigned public IPs. If false, they will not be auto-assigned public IPs.
        :param pulumi.Input[str] node_public_key: Public key material for SSH access to worker nodes. See allowed formats at:
               https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html
               If not provided, no SSH access is enabled on VMs.
        :param pulumi.Input[int] node_root_volume_size: The size in GiB of a cluster node's root volume. Defaults to 20.
        :param pulumi.Input['pulumi_aws.ec2.SecurityGroup'] node_security_group: The security group for the worker node group to communicate with the cluster.
               
               This security group requires specific inbound and outbound rules.
               
               See for more details:
               https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html
               
               Note: The `nodeSecurityGroup` option and the cluster option`nodeSecurityGroupTags` are mutually exclusive.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] node_subnet_ids: The set of subnets to override and use for the worker node group.
               
               Setting this option overrides which subnets to use for the worker node group, regardless if the cluster's `subnetIds` is set, or if `publicSubnetIds` and/or `privateSubnetIds` were set.
        :param pulumi.Input[str] node_user_data: Extra code to run on node startup. This code will run after the AWS EKS bootstrapping code and before the node signals its readiness to the managing CloudFormation stack. This code must be a typical user data script: critically it must begin with an interpreter directive (i.e. a `#!`).
        :param pulumi.Input[str] node_user_data_override: User specified code to run on node startup. This code is expected to handle the full AWS EKS bootstrapping code and signal node readiness to the managing CloudFormation stack. This code must be a complete and executable user data script in bash (Linux) or powershell (Windows).
               
               See for more details: https://docs.aws.amazon.com/eks/latest/userguide/worker.html
        :param pulumi.Input[str] spot_price: Bidding price for spot instance. If set, only spot instances will be added as worker node.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['TaintArgs']]]] taints: Custom k8s node taints to be attached to each worker node. Adds the given taints to the `--register-with-taints` kubelet argument
        :param pulumi.Input[str] version: Desired Kubernetes master / control plane version. If you do not specify a value, the latest available version is used.
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
        if opts.id is not None:
            raise ValueError('ComponentResource classes do not support opts.id')
        else:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['ami_id'] = ami_id
            __props__['auto_scaling_group_tags'] = auto_scaling_group_tags
            __props__['bootstrap_extra_args'] = bootstrap_extra_args
            __props__['cloud_formation_tags'] = cloud_formation_tags
            if cluster is None and not opts.urn:
                raise TypeError("Missing required property 'cluster'")
            __props__['cluster'] = cluster
            __props__['cluster_ingress_rule'] = cluster_ingress_rule
            __props__['desired_capacity'] = desired_capacity
            __props__['encrypt_root_block_device'] = encrypt_root_block_device
            __props__['extra_node_security_groups'] = extra_node_security_groups
            __props__['gpu'] = gpu
            __props__['instance_profile'] = instance_profile
            __props__['instance_type'] = instance_type
            __props__['key_name'] = key_name
            __props__['kubelet_extra_args'] = kubelet_extra_args
            __props__['labels'] = labels
            __props__['max_size'] = max_size
            __props__['min_size'] = min_size
            __props__['node_associate_public_ip_address'] = node_associate_public_ip_address
            __props__['node_public_key'] = node_public_key
            __props__['node_root_volume_size'] = node_root_volume_size
            __props__['node_security_group'] = node_security_group
            __props__['node_subnet_ids'] = node_subnet_ids
            __props__['node_user_data'] = node_user_data
            __props__['node_user_data_override'] = node_user_data_override
            __props__['spot_price'] = spot_price
            __props__['taints'] = taints
            __props__['version'] = version
            __props__['auto_scaling_group_name'] = None
            __props__['cfn_stack'] = None
        super(NodeGroup, __self__).__init__(
            'eks:index:NodeGroup',
            resource_name,
            __props__,
            opts,
            remote=True)

    @property
    @pulumi.getter(name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> pulumi.Output[str]:
        """
        The AutoScalingGroup name for the Node group.
        """
        return pulumi.get(self, "auto_scaling_group_name")

    @property
    @pulumi.getter(name="cfnStack")
    def cfn_stack(self) -> pulumi.Output['pulumi_aws.cloudformation.Stack']:
        """
        The CloudFormation Stack which defines the Node AutoScalingGroup.
        """
        return pulumi.get(self, "cfn_stack")

    @property
    @pulumi.getter(name="extraNodeSecurityGroups")
    def extra_node_security_groups(self) -> pulumi.Output[Sequence['pulumi_aws.ec2.SecurityGroup']]:
        """
        The additional security groups for the node group that captures user-specific rules.
        """
        return pulumi.get(self, "extra_node_security_groups")

    @property
    @pulumi.getter(name="nodeSecurityGroup")
    def node_security_group(self) -> pulumi.Output['pulumi_aws.ec2.SecurityGroup']:
        """
        The security group for the node group to communicate with the cluster.
        """
        return pulumi.get(self, "node_security_group")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

