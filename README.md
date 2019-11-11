# HT Pipeline

A repository for common commands and tasks carried out in day to day job.


#### Manage EC2 Instances

It can be common to start and stop instances of AWS EC2 instances so there are some common commands that can be 
used to manage these.

To start and instance you can use -

`python -m app.adhoc.manage_ec2 "Instance Name" start`

And to stop and instance, you use -

`python -m app.adhoc.manage_ec2 "Instance Name" stop`

If you attempt to start an instance that is already running or stop an instance that has already 
stopped, you will get a message telling you so, otherwise it will start the process of starting/stopping
the instance and give regular updates of the status until the action has completed.


#### Manage NHBC Plot Files

For the NHBC plot files, there can be a lot of file movement between workspaces, local machines and S3. To
make this a bit easier, there are a couple of commands that can be used to -

To upload the latest files to S3, you can use -

`python -m app.adhoc.manage_plot_files -a upload [YYYYMM]`

This will upload to S3 the files found in `\\property.local\shared\HOMETRACK_ROOT\Techdev\Raw Data\020_NHBCNewBuildDataset\data`
for the optionally given month. Where the month is not given it will use the current month.
The files will be uploaded to to S3 `nhbc-eu-west-2-318016054559/raw/YYYYMM/` where they can then be used by the NHBC
process to create the transformed plots file.

To download the transformed plots file, you can use

`python -m app.adhoc.manage_plot_files -a download [YYYYMM]`

This will download the transformed file from S3 path `nhbc-eu-west-2-318016054559/transformed/plots/month=YYYYMM/`
for the optionally given month. Where the month is not given it will use the current month.


#### Download Land Reg CSV

To easily download the latest Land Registry file from `landregistry.gov.uk` you can use -

`python -m app.adhoc.download_land_reg`

This will download the latest file from `http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv`
and save it to `S:\\HOMETRACK_ROOT\\Techdev\\Raw Data\\084_LandRegistry\\latest\\pp-complete.csv`


#### Create and Run Comparables Build Config

To create the build config you can use the following arguments to create, show and run the build config
for Comparables -


```python -m app.process.comparables.build_config

optional arguments:
  -h, --help            show this help message and exit
  -a {build,show,run}, --action {build,show,run}
                        Action to build config, show config, or run comps
                        config
  -as AS_OF_DATE, --asof AS_OF_DATE
                        As of date for the config
  -o OS_VERSION, --os_version OS_VERSION
                        OS data version to use for the config
  -b BASED_ON_VERSION, --based_on_version BASED_ON_VERSION
                        Comps version based on to use for the config
  -c COMPARED_TO_VERSION, --compared_to_version COMPARED_TO_VERSION
                        Comps version compared to to use for the config
  -r REBUILD, --rebuild REBUILD
                        Whether comps build is rebuild or not
  -u UPDATE, --update UPDATE
                        Whether comps build is update or not
  -d BUILD_DESCRIPTION, --description BUILD_DESCRIPTION
                        Build description
  -i IS_RELEASE_BUILD, --is_release_build IS_RELEASE_BUILD
                        Whether comps build is release build or not
```

###### Build
You can build the config by running the following in the command line and swapping the relevant variables -
```
python -m app.process.comparables.build_config --action build ^
--asof 20191101 ^
--os_version 80 ^
--based_on_version 672 ^
--compared_to_version 672 ^
--rebuild True ^
--update False
```

This will save a local version of the build configuration as well as output it to the console.
You will need to run this before you can run the config.


###### Show

This will output to the console the current saved config that was run by the build command.

`python -m app.process.comparables.build_config -a show`

If the config has been created, this will raise an error.


###### Run

You can run the current config by running -

```
python -m app.process.comparables.build_config --action run ^
--description "Comps Build description" ^
--is_release False
```

This will run the current config against LON-SQL-02.

NOTE: Currently there is an issue with double hop issue so the run command will output the sql to
the console, where it can be copied to be run on the relevant server/instance.