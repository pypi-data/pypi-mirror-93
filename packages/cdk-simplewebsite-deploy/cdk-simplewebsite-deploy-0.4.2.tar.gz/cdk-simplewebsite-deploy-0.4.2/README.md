[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)
![Build](https://github.com/SnapPetal/cdk-simplewebsite-deploy/workflows/Build/badge.svg)
![Release](https://github.com/SnapPetal/cdk-simplewebsite-deploy/workflows/Release/badge.svg?branch=main)

# cdk-simplewebsite-deploy

This is an AWS CDK Construct to simplify deploying a single-page website using either S3 buckets or CloudFront distributions.

## Installation and Usage

### [CreateBasicSite](https://github.com/snappetal/cdk-simplewebsite-deploy/blob/main/API.md#cdk-cloudfront-deploy-createbasicsite)

#### Creates a simple website using S3 buckets with a domain hosted in Route 53.

##### Typescript

```console
npm install cdk-simplewebsite-deploy
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_simplewebsite_deploy import CreateBasicSite

class PipelineStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        CreateBasicSite(stack, "test-website",
            website_folder="./src/build",
            index_doc="index.html",
            hosted_zone="example.com"
        )
```

##### C#

```console
dotnet add package ThonBecker.CDK.SimpleWebsiteDeploy
```

```cs
using Amazon.CDK;
using ThonBecker.CDK.SimpleWebsiteDeploy;

namespace SimpleWebsiteDeploy
{
    public class PipelineStack : Stack
    {
        internal PipelineStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            new CreateBasicSite(scope, "test-website", new BasicSiteConfiguration()
            {
                WebsiteFolder = "./src/build",
                IndexDoc = "index.html",
                HostedZone = "example.com",
            });
        }
    }
}
```

### [CreateCloudfrontSite](https://github.com/snappetal/cdk-simplewebsite-deploy/blob/main/API.md#cdk-cloudfront-deploy-createcloudfrontsite)

#### Creates a simple website using a CloudFront distribution with a domain hosted in Route 53.

##### Typescript

```console
npm install cdk-simplewebsite-deploy
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_simplewebsite_deploy import CreateCloudfrontSite

class PipelineStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        CreateCloudfrontSite(stack, "test-website",
            website_folder="./src/dist",
            index_doc="index.html",
            hosted_zone="example.com",
            sub_domain="www.example.com"
        )
```

##### C#

```console
dotnet add package ThonBecker.CDK.SimpleWebsiteDeploy
```

```cs
using Amazon.CDK;
using ThonBecker.CDK.SimpleWebsiteDeploy;

namespace SimpleWebsiteDeploy
{
    public class PipelineStack : Stack
    {
        internal PipelineStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            new CreateCloudfrontSite(scope, "test-website", new CloudfrontSiteConfiguration()
            {
                WebsiteFolder = "./src/build",
                IndexDoc = "index.html",
                HostedZone = "example.com",
                SubDomain = "www.example.com",
            });
        }
    }
}
```

## License

Distributed under the [Apache-2.0](./LICENSE) license.
