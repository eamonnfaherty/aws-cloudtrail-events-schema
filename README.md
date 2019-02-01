## Background
The AWS platform allows you to log API calls using [AWS CloudTrial](https://aws.amazon.com/cloudtrail).

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

Running ```cloudtrail-schema iam.CreatePolicy.output``` give the following output:
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