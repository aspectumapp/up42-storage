# up42-storage
Storage block for integrating data with UP42 Platform

## Introduction
The block enables UP42 users to run processing algorithms on top of their data. The concept of the block came from the case where [Cars Detection](https://marketplace.up42.com/block/7d8dda9f-db1e-4645-9c1b-e056e0bdc698) algorithm should have been run on previously acquired imagery for further [visualization and processing in Aspectum](https://aspectum.com/app/maps/shared/5abe7981-fe40-4cf5-b3ba-257f202261d4?theme=dark).

## Requirements
This example requires the Mac or Ubuntu bash. In order to bring this example block or your own custom block to the UP42 platform the following tools are required:
 - [UP42](https://up42.com) account -  Sign up for free!
 - [AWS](https://aws.amazon.com/) account with bucket created
 - [Python 3.7](https://python.org/downloads)
 - A virtual environment manager e.g. [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
 - [git](https://git-scm.com/)
 - [docker engine](https://docs.docker.com/engine/)
 - [GNU make](https://www.gnu.org/software/make/)


## Instructions

### Clone the repository
```
git clone https://github.com/aspectumapp/up42-storage.git
```

Then navigate to the folder via `cd up42-storage`.


### Installing the required libraries

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
### Set up parameters
To use the block you should provide [your AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html). 
Open the `Makefile`. Edit the code below by inserting your AWS credentials:

```
AWS_ACCESS_KEY :=
AWS_SECRET_ACCESS_KEY :=
AWS_REGION :=
AWS_BUCKET_NAME :=
AWS_PUBLIC_BUCKET_NAME :=
```

## Pushing the block to the UP42 platform

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
  <img width="500" src="https://i.ibb.co/YpmwxY2/custom-block-successfully-uploaded.png">
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
1. To use the block in UP42 Platform, you should provide the filename of the imagery stored on the bucket.
Сюди скріншот

2. Zoom level is required parameter. To understand zoom levels and scales check [this article](https://wiki.openstreetmap.org/wiki/Zoom_levels). I.e. for using Pleiades data with a resolution ~50cm zoom level 18 is prefeded.

3. Run the job! Now your file has been used as an input for the following processing and/or visualization.
**Important: The imagery should be in EPSG:3857 coordinate system. For transforming the coordinate system of geotiff you could use GIS software: [QGIS](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/gdal/rasterprojections.html) or [ArcGIS](https://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/defining-or-modifying-a-raster-coordinate-system.htm) examples.**

