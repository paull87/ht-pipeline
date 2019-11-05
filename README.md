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