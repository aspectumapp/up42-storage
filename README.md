# up42-storage
Storage block for integrating data with UP42 Platform

<p align="center">
  <img width="100%" src="https://lh3.googleusercontent.com/GiebGqsc8xmaURoG4kTvIzy-NrvsI3IlU5gScTU-y7tZdeWsRMzLcH8D-OQBywn3jXG7UVcPOkwmxiaYJft6sQiJFYyzD86j-LAu0RBvkGruu5rYuVzr1mT9haWjjYi8iOoGqUHILgrZbcV_TNmXWVg7mitIRduhngETWzdXk_b_a9jO_3n1VPQd3c6rCSnKvyLZ63fmv-bsGFxAuahkrFmnNMKNbLRV9IMI3cBtP8G-iu7YopmdDDHVL42eAv3mDf9RAq3kRjUnq9PJotLArDw1u5K7jQAJie6gO1lT7gTuxW6rQ7FC6kKg2304cApbvL-JvUAiIZTGKtBHzTdmb42-zR2SenttwhIOmMZW5d6KO7hvVF_gYpQ_R-SSXdwwT5KuIZdbvwEUcm-ZRfs9nT2-eZ6CeQH7GuOqa3Kv0mKYT36vFyY6VYxrKUgm8fQ_0tSHbyg1yMoM80B6PKHvuog1cMsDaKt7nRcIwOaJOb0xas1U8eTqVfdR-8vbZgpq1tLSHare9KeHX-ZL63d_-qLZzrk_3FdH5T6w36il7axqoULOl0Ckmax2qhN-MZf6DUT9fzGapbx5s5ml_P4ySLvpz4WTCef6xT0NdzQdwdhPoVjsdq9ny3imnYYyzYycA7pjxLWn9-KWMxgBaaNkyycqMvcl4kFloOnwHyRIODmJ18dg7PfK1-0BIigiDQmoTYzJF7-ISknA3GpHfj9Udm74MSk1SaIM4-HUrWrQonUIzbdi=w657-h428-no">
</p>


## Introduction
The block enables UP42 users to run processing algorithms on top of their data. The concept of the block came from the case where [Cars Detection](https://marketplace.up42.com/block/7d8dda9f-db1e-4645-9c1b-e056e0bdc698) algorithm should have been run on previously acquired imagery for further [visualization and processing in Aspectum](https://aspectum.com/app/maps/shared/5abe7981-fe40-4cf5-b3ba-257f202261d4?theme=dark).

## Requirements
This example requires the Mac or Ubuntu bash. In order to bring this example block or your own custom block to the UP42 platform the following tools are required:
 - [UP42](https://up42.com) account -  Sign up for free!
 - [AWS](https://aws.amazon.com/) account with bucket created
 - [Python 3.7](https://python.org/downloads)
 - [git](https://git-scm.com/)
 - [docker engine](https://docs.docker.com/engine/)
 - [GNU make](https://www.gnu.org/software/make/)
 - A virtual environment manager e.g. [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) (optional for running the block locally)


## Instructions
### Clone the repository
```
git clone https://github.com/aspectumapp/up42-storage.git
```

Then navigate to the folder via `cd up42-storage`.

### Set up parameters
To use the block you should provide [your AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html). 
Open the `Makefile`. Edit the code below by inserting your AWS credentials:

```
AWS_ACCESS_KEY := #XXXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY := #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
AWS_REGION := #us-east-1
AWS_BUCKET_NAME := #your-bucket-name-with-files
```

### Pushing the block to the UP42 platform

First login to the UP42 docker registry. `me@example.com` needs to be replaced by your **UP42 username**,
which is the email address you use on the UP42 website.

```bash
make login USER=me@example.com
```

In order to push the block to the UP42 platform, you need to build the block Docker container with your
**UP42 USER-ID**. To get your USER-ID, go to the [UP42 custom-blocks menu](https://console.up42.com/custom-blocks).
Click on "`PUSH a BLOCK to THE PLATFORM`" and copy your USERID from the command shown on the last line at
"`Push the image to the UP42 Docker registry`". The USERID will look similar to this:
`63uayd50-z2h1-3461-38zq-1739481rjwia`

Pass the USER-ID to the build command:
```bash
make build UID=<UID>

# As an example: make build UID=63uayd50-z2h1-3461-38zq-1739481rjwia
```

Now you can finally push the image to the UP42 docker registry, again passing in your USER-ID:

```bash
make push UID=<UID>

# As an example: make push UID=63uayd50-z2h1-3461-38zq-1739481rjwia
```

**Success!** The block will now appear in the [UP42 custom blocks menu](https://console.up42.com/custom-blocks/) menu
and can be selected under the *Custom blocks* tab when building a workflow.

<p align="center">
  <img width="500" src="https://lh3.googleusercontent.com/5iesx5QHGsHRx9qirN1v_cpJ885L845BmwxGjnjm1MyIaVfeHw0WmAqn3ngY2WX2RhDuAfLJ7sPYXwG99IAsgRcOyeFg_WebM2bMpM6npYRYD8It4K1R9Ha9J7M70RBpl-7DofYMALXWzKfdftb2pH5Pa7XOOx1EHoRWhaMRYbr7eXW7wUlwKflkjWCuxYkwUGtnlXMPrybLgbRWjgosuf9LcEFkZCrVRK-WZpbpRQGSXQIcwxeMQSD0NUs3X_ynZU210cjORYTPhBSQ7nOXR92Mm1ABe_NtQWbHk8a5S_VMOYejaoeeJfPyzK0BruWz0z7jJIJn3NXfa9j6mfE34XX1lzrdvmIo_IVQlFAYM2CfEKJrQ-CBDCB4XcYU-coo1madaY89ihIXjJR64tsp_zwJWUMcqq58vV1yQxiQxWwjb2CINl67OCrnvo_9D-4qBNu9iP2zziQHPhJh646QqF24Fqp61XrHNwcOwv2e6kSriw0cGqT1ZlYN5bF1z7rcplQFbc_Osh14lFnodFSUGKrEyzW1Bdo46EaguIF0JFbz2opaV_knw_D2LQGKUcAKCCah32uzNX1i8pkx6gx2NyPZfRf8YZLQa5zA72ll1zrt1-W6G84H8lZ4wj1dcQb_UcRR4jS6ISiwvLm4Lcd3Ad5JFEHKeqT57fTquvVBiwKZKe2TZklAOELt65LsWrs_ZXx5Z9YA3LzrpUtzJp8eKYbDfxwAbwBwlVHyvfnLbmS2w7bt=w669-h368-no">
</p>

### Optional: Updating an existing custom block

If you want to update a custom block on UP42, you need to build the Docker container with an updated version:
The default docker tag is `up42-storage` and the version is set to `latest`.

```bash
make build UID=<UID> DOCKER_TAG=<docker tag> DOCKER_VERSION=<docker version>

# As an example: docker build UID=63uayd50-z2h1-3461-38zq-1739481rjwia DOCKER_TAG=up42-storage DOCKER_VERSION=1.0
```

Then push the block container with the updated tag and version:

```bash
make push UID=<UID> DOCKER_TAG=<docker tag> DOCKER_VERSION=<docker version>

# As an example: make push UID=63uayd50-z2h1-3461-38zq-1739481rjwia DOCKER_TAG=up42-storage DOCKER_VERSION=1.0
```

## Using the block
1. To use the block in UP42 Platform, you should provide the filename of the imagery stored on the bucket in the `file_path` parameter.

2. Choose any Bounding Box. **This parameter does not crop the image. The whole file on the S3 would be moved for the next step.**

3. Run the job! Now your file has been used as an input for the following processing and/or visualization.
**Important: The imagery should be in EPSG:3857 coordinate system. For transforming the coordinate system of geotiff you could use GIS software: [QGIS](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/gdal/rasterprojections.html) or [ArcGIS](https://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/defining-or-modifying-a-raster-coordinate-system.htm) examples.**

## Run block locally: Installing the required libraries

First create a new virtual environment called up42-aws, for example by using virtualenvwrapper:
```
mkvirtualenv --python=$(which python3.7) up42-aws
```

Activate the new environment:
```
workon up42-aws
```

Install the necessary Python libraries via:
```
make install
```
