## Background
The AWS platform allows you to log API calls using [AWS CloudTrail](https://aws.amazon.com/cloudtrail).

You can use tools like [AWS Config](https://aws.amazon.com/config/) and [CaptialOne's CloudCustodian](https://github.com/cloud-custodian/cloud-custodian) 
to create security controls that react to these events.

## The problem 
There is not much documentation on the structure of the events.  

## What is this?
The structure of the events from CloudTrail are similar to responses seen when using boto3.  
Boto3 is powered by the botocore library.  
The botocore library contains a data directory that describes the API calls (requests and responses).
This library allows you to interact with the data directories of botocore to see the API request and responses.
This is to help you write custom AWS Config rules and or CloudCustodian policies.

## Examples
Running ```cloudtrail-schema``` with no arguements will list the services/sources:
```yaml
Services:
- acm
- acm-pca
- alexaforbusiness
- amplify
- apigateway
- apigatewaymanagementapi
- apigatewayv2
```

Running ```cloudtrail-schema iam``` with a service will list the operations/events:
```yaml
Operations:
- AddClientIDToOpenIDConnectProvider
- AddRoleToInstanceProfile
- AddUserToGroup
- AttachGroupPolicy
- AttachRolePolicy
- AttachUserPolicy
- ChangePassword
```

Running with a service and event ```cloudtrail-schema iam.CreatePolicy.output``` give the following output:
```
Description
------
<p>Creates a new managed policy for your AWS account.</p> <p>This operation creates a policy version with a version identifier of <code>v1</code> and sets v1 as the policy's default version. For more information about policy versions, see <a href="http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html">Versioning for Managed Policies</a> in the <i>IAM User Guide</i>.</p> <p>For more information about managed policies in general, see <a href="http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html">Managed Policies and Inline Policies</a> in the <i>IAM User Guide</i>.</p>


Result
------
{
    "policy": {
        "policyName": {
            "type": "string",
            "max": 128,
            "min": 1,
            "pattern": "[\\w+=,.@-]+"
        },
        "policyId": {
            "type": "string",
            "max": 128,
            "min": 16,
            "pattern": "[\\w]+"
        },
        "arn": {
            "type": "string",
            "documentation": "<p>The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.</p> <p>For more information about ARNs, go to <a href=\"http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html\">Amazon Resource Names (ARNs) and AWS Service Namespaces</a> in the <i>AWS General Reference</i>. </p>",
            "max": 2048,
            "min": 20
        },
        "path": {
            "type": "string",
            "pattern": "((/[A-Za-z0-9\\.,\\+@=_-]+)*)/"
        },
        "defaultVersionId": {
            "type": "string",
            "pattern": "v[1-9][0-9]*(\\.[A-Za-z0-9-]*)?"
        },
        "attachmentCount": {
            "type": "integer"
        },
        "permissionsBoundaryUsageCount": {
            "type": "integer"
        },
        "isAttachable": {
            "type": "boolean"
        },
        "description": {
            "type": "string",
            "max": 1000
        },
        "createDate": {
            "type": "timestamp"
        },
        "updateDate": {
            "type": "timestamp"
        }
    }
}
```


### Writing a CloudCustodian policy
When you view a event response using this tool you can translate it easily into a a CloudCustodian policy:

```
# cloudtrail-schema iam.CreatePolicy.output

Description
------
<p>Creates a new managed policy for your AWS account.</p> <p>This operation creates a policy version with a version identifier of <code>v1</code> and sets v1 as the policy's default version. For more information about policy versions, see <a href="http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html">Versioning for Managed Policies</a> in the <i>IAM User Guide</i>.</p> <p>For more information about managed policies in general, see <a href="http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html">Managed Policies and Inline Policies</a> in the <i>IAM User Guide</i>.</p>


Result
------
{
    "policy": {
        "policyName": {
            "type": "string",
            "max": 128,
            "min": 1,
            "pattern": "[\\w+=,.@-]+"
        },
        "policyId": {
            "type": "string",
            "max": 128,
            "min": 16,
            "pattern": "[\\w]+"
        },
        "arn": {
            "type": "string",
            "documentation": "<p>The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.</p> <p>For more information about ARNs, go to <a href=\"http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html\">Amazon Resource Names (ARNs) and AWS Service Namespaces</a> in the <i>AWS General Reference</i>. </p>",
            "max": 2048,
            "min": 20
        },
        "path": {
            "type": "string",
            "pattern": "((/[A-Za-z0-9\\.,\\+@=_-]+)*)/"
        },
        "defaultVersionId": {
            "type": "string",
            "pattern": "v[1-9][0-9]*(\\.[A-Za-z0-9-]*)?"
        },
        "attachmentCount": {
            "type": "integer"
        },
        "permissionsBoundaryUsageCount": {
            "type": "integer"
        },
        "isAttachable": {
            "type": "boolean"
        },
        "description": {
            "type": "string",
            "max": 1000
        },
        "createDate": {
            "type": "timestamp"
        },
        "updateDate": {
            "type": "timestamp"
        }
    }
}

```

You use the argument to decide the mode.events.source and mode.events.event:

source: iam.amazonaws.com
event: CreatePolicy

Full example:

```yaml
policies:
  - name: iam-has-allow-all-policy
    description: |
      Notify when a policy is created using allow all
    resource: iam-policy
    mode:
      type: cloudtrail
      events:
        - source: iam.amazonaws.com
          event: CreatePolicy
          ids: "responseElements.policy.policyId"

```

The json returned from the app can be used to write filters.  The json returned
is the same as the structure available from responseElements.  You can write the 
following policy as an example:

Running: ```cloudtrail-schema ec2.CreateVpcPeeringConnection.output``` results in

```
Description
------
<p>Requests a VPC peering connection between two VPCs: a requester VPC that you own and an accepter VPC with which to create the connection. The accepter VPC can belong to another AWS account and can be in a different Region to the requester VPC. The requester VPC and accepter VPC cannot have overlapping CIDR blocks.</p> <note> <p>Limitations and rules apply to a VPC peering connection. For more information, see the <a href="http://docs.aws.amazon.com/AmazonVPC/latest/PeeringGuide/vpc-peering-basics.html#vpc-peering-limitations">limitations</a> section in the <i>VPC Peering Guide</i>.</p> </note> <p>The owner of the accepter VPC must accept the peering request to activate the peering connection. The VPC peering connection request expires after 7 days, after which it cannot be accepted or rejected.</p> <p>If you create a VPC peering connection request between VPCs with overlapping CIDR blocks, the VPC peering connection has a status of <code>failed</code>.</p>


Result
------
{
    "vpcPeeringConnection": {
        "accepterVpcInfo": {
            "cidrBlock": {
                "type": "string"
            },
            "ipv6CidrBlockSet": {
                "type": "list",
                "member": {
                    "shape": "Ipv6CidrBlock",
                    "locationName": "item"
                }
            },
            "cidrBlockSet": {
                "type": "list",
                "member": {
                    "shape": "CidrBlock",
                    "locationName": "item"
                }
            },
            "ownerId": {
                "type": "string"
            },
            "peeringOptions": {
                "allowDnsResolutionFromRemoteVpc": {
                    "type": "boolean"
                },
                "allowEgressFromLocalClassicLinkToRemoteVpc": {
                    "type": "boolean"
                },
                "allowEgressFromLocalVpcToRemoteClassicLink": {
                    "type": "boolean"
                }
            },
            "vpcId": {
                "type": "string"
            },
            "region": {
                "type": "string"
            }
        },
        "expirationTime": {
            "type": "timestamp"
        },
        "requesterVpcInfo": {
            "cidrBlock": {
                "type": "string"
            },
            "ipv6CidrBlockSet": {
                "type": "list",
                "member": {
                    "shape": "Ipv6CidrBlock",
                    "locationName": "item"
                }
            },
            "cidrBlockSet": {
                "type": "list",
                "member": {
                    "shape": "CidrBlock",
                    "locationName": "item"
                }
            },
            "ownerId": {
                "type": "string"
            },
            "peeringOptions": {
                "allowDnsResolutionFromRemoteVpc": {
                    "type": "boolean"
                },
                "allowEgressFromLocalClassicLinkToRemoteVpc": {
                    "type": "boolean"
                },
                "allowEgressFromLocalVpcToRemoteClassicLink": {
                    "type": "boolean"
                }
            },
            "vpcId": {
                "type": "string"
            },
            "region": {
                "type": "string"
            }
        },
        "status": {
            "code": {
                "type": "string",
                "enum": [
                    "initiating-request",
                    "pending-acceptance",
                    "active",
                    "deleted",
                    "rejected",
                    "failed",
                    "expired",
                    "provisioning",
                    "deleting"
                ]
            },
            "message": {
                "type": "string"
            }
        },
        "tags": {
            "type": "list",
            "member": {
                "shape": "Tag",
                "locationName": "item"
            }
        },
        "vpcPeeringConnectionId": {
            "type": "string"
        }
    }
}

```
You can use this response to write a complex event filter.  Everything from the detail.responseElements downwards is
what was was returned from the app.
```yaml
policies:
 - name: vpc-peering-cross-account-checker-real-time
   resource: peering-connection
   mode:
      type: cloudtrail
      events:
         - source: ec2.amazonaws.com
           event: CreateVpcPeeringConnection
           ids: 'responseElements.vpcPeeringConnection.vpcPeeringConnectionId'
      timeout: 90
      memory: 256
      role: arn:aws:iam::{account_id}:role/Cloud_Custodian_EC2_Lambda_Role
   description: |
     When a new peering connection is created the Accepter and Requester account
     numbers are compared and if they aren't both internally owned accounts then the
     cloud and security teams are notified to investigate and delete the peering connection.
   filters:
     - or:
         - type: event
           key: "detail.responseElements.vpcPeeringConnection.accepterVpcInfo.ownerId"
           op: not-in
           value_from:
             url: s3://s3bucketname/AccountNumbers.csv
             format: csv2dict
         - type: event
           key: "detail.responseElements.vpcPeeringConnection.requesterVpcInfo.ownerId"
           op: not-in
           value_from:
             url: s3://s3bucketname/AccountNumbers.csv
             format: csv2dict
```
