[![NPM version](https://badge.fury.io/js/cdk-serverless-lamp.svg)](https://badge.fury.io/js/cdk-serverless-lamp)
[![PyPI version](https://badge.fury.io/py/cdk-serverless-lamp.svg)](https://badge.fury.io/py/cdk-serverless-lamp)
![Build](https://github.com/aws-samples/cdk-serverless-lamp/workflows/Build/badge.svg)

# Welcome to cdk-serverless-lamp

`cdk-serverless-lamp` is a JSII construct library for AWS CDK that allows you to deploy the [New Serverless LAMP Stack](https://aws.amazon.com/tw/blogs/compute/introducing-the-new-serverless-lamp-stack/) running PHP Laravel Apps by specifying the local `laravel` directory.

By deploying the `ServerlessLaravel` and `DatabaseCluster`, the following resources will be created:

1. Amazon API Gateway HTTP API
2. AWS Lambda custom runtime with [Bref runtime](https://bref.sh/docs/runtimes/) support
3. Amazon Aurora for MySQL database cluster with RDS proxy enabled

## Howto

Create a new Laravel project with AWS CDK

```sh
$ mkdir serverless-lamp && cd serverless-lamp
# create cdk and codebase directories for AWS CDK and Laravel project
$ mkdir cdk codebase
# create the new Laravel project with docker
$ docker run --rm -ti \
  --volume $PWD:/app \
  composer create-project --prefer-dist laravel/laravel ./codebase
# install bref/bref and bref/laravel-bridge in the vendor
$ cd codebase
$ docker run --rm -ti \
  --volume $PWD:/app \
  composer require bref/bref bref/laravel-bridge
# initialize the AWS CDK project
$ cd ../cdk
$ cdk init -l typescript
# install the cdk-severless-lamp npm module
$ yarn add cdk-serverless-lamp
```

Now your directories should look like this:

```
.
├── cdk
└── codebase
```

where `cdk` is for the AWS CDK and `codebase` for Laravel project.

# AWS CDK sample

Building your serverless Laravel with `ServerlessLaravel` construct:

Update `./cdk/lib/cdk-stack.ts`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
import path as path
from cdk_serverless_lamp import ServerlessLaravel

class CdkStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        ServerlessLaravel(self, "ServerlessLaravel",
            bref_layer_version="arn:aws:lambda:us-east-1:209497400698:layer:php-74-fpm:12",
            laravel_path=path.join(__dirname, "../../codebase")
        )
```

deploy the CDK stack:

```sh
# see the difference before the deployment
$ cdk diff
# deploy it
$ cdk deploy
```

On deploy complete, the API Gateway URL will be returned in the Output. Click the URL and you will see the Laravel landing page:

![laravel-welcome](./images/laravel.png)

## Amazon Aurora support

Use `DatabaseCluster` to create the your database cluster:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from aws_cdk.aws_ec2 import InstanceType, Vpc
import path as path
from cdk_serverless_lamp import ServerlessLaravel, DatabaseCluster

class CdkStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        vpc = Vpc(self, "Vpc", max_azs=3, nat_gateways=1)

        # the DatabaseCluster sharing the same vpc with the ServerlessLaravel
        db = DatabaseCluster(self, "DatabaseCluster",
            vpc=vpc,
            instance_type=InstanceType("t3.small"),
            rds_proxy=True
        )

        # the ServerlessLaravel
        ServerlessLaravel(self, "ServerlessLaravel",
            bref_layer_version="arn:aws:lambda:us-east-1:209497400698:layer:php-74-fpm:12",
            laravel_path=path.join(__dirname, "../../codebase"),
            vpc=vpc,
            database_config={
                "writer_endpoint": db.rds_proxy.endpoint
            }
        )
```

## Local Development

Create `docker-compose.yml` with the following content:

```docker-compose
version: "3.5"
services:
  web:
    image: bref/fpm-dev-gateway
    ports:
      - "8000:80"
    volumes:
      - ./laravel:/var/task
    depends_on:
      - php
    environment:
      HANDLER: public/index.php
  php:
    image: bref/php-74-fpm-dev
    volumes:
      - ./laravel:/var/task
```

and run this command `docker-compose up -d` and now you can access [http://localhost:8000](http://localhost:8000).

*(more information can be found in [bref documentation](https://bref.sh/docs/local-development.html))*
