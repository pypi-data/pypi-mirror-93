# Graviti python SDK

## Installation

```bash
pip3 install graviti
```

## Usage

#### Get accessKey

AccessKey is required when upload data.

Use your username and password to login to [Graviti website](https://gas.graviti.cn/),
and get accessKey on profile page.

#### Create Dataset

```python
#!/usr/bin/env python3

from graviti import GAS

ACCESS_KEY = "Accesskey-****"
DATASET_NAME = "TestDataset"

gas = GAS(ACCESS_KEY)  # register the accesskey to gas client
gas.create_dataset(DATASET_NAME)  # create a new dataset
```

#### List Datasets

```python
#!/usr/bin/env python3

from graviti import GAS

ACCESS_KEY = "Accesskey-****"

gas = GAS(ACCESS_KEY)  # register the accesskey to gas client
gas.list_datasets()  # list datasets
```

#### Upload data

This sample is for uploading dataset which only contains data collected from a single sensor.

```python
#!/usr/bin/env python3

from graviti import GAS
from graviti.dataset import Dataset, Data

ACCESS_KEY = "Accesskey-****"
DATASET_NAME = "TestDataset"
SEGMENT_NAME = "TestSegment"
THREAD_NUMBER = 8

dataset = Dataset(DATASET_NAME)  # create local dataset
segment = dataset.create_segment(SEGMENT_NAME)  # create local segment

# Add data to segment
for filename in FILE_LIST:
    data = Data(filename)
    segment.append(data)

gas = GAS(ACCESS_KEY)  # register the accesskey to gas client

# Upload local dataset to tensorbay
# Argument 'jobs' for multi-thread uploading
# Set 'skip_uploaded_files' to 'True' will skip the uploaded files
gas.upload_dataset_object(dataset, jobs=THREAD_NUMBER, skip_uploaded_files=True)
```

#### Upload fusion data

This sample is for uploading dataset which contains data collected from multiple sensors.

```python
#!/usr/bin/env python3

from graviti import GAS
from graviti.dataset import FusionDataset, Frame, Data
from graviti.sensor import Camera

ACCESS_KEY = "Accesskey-****"
DATASET_NAME = "TestFusionDataset"
SEGMENT_NAME = "TestSegment"
THREAD_NUMBER = 8

gas = GAS(ACCESS_KEY)

dataset = FusionDataset(DATASET_NAME)  # create local fusion dataset
segment = dataset.create_segment(SEGMENT_NAME)  # create local fusion segment

# Add sensor to segment
for sensor_name in SENSOR_LIST:
    camera = Camera(sensor_name)
    camera.set_translation(x=1.1, y=2.2, z=3.3)
    camera.set_rotation(w=1.1, x=2.2, y=3.3, z=4.4)
    camera.set_camera_matrix(fx=1.1, fy=2.2, cx=3.3, cy=4.4)
    camera.set_distortion_coefficients(p1=1.1, p2=2.2, k1=3.3, k2=4.4, k3=5.5)
    segment.add_sensor(camera)

# Add frame to segment
for frame_info in FRAME_LIST:
    frame = Frame()
    for sensor_name in SENSOR_LIST:
        data_info = frame_info[sensor_name]
        frame[sensor_name] = Data(data_info.filename, timestamp=data_info.timestamp)
    segment.append(frame)

gas = GAS(ACCESS_KEY)  # register the accesskey to gas client

# Upload local fusion dataset to tensorbay
# Argument 'jobs' for multi-thread uploading
# Set 'skip_uploaded_files' to 'True' will skip the uploaded files
gas.upload_dataset_object(dataset, jobs=THREAD_NUMBER, skip_uploaded_files=True)
```

#### Upload data with labels

This sample is for uploading dataset which contains labels

```python
#!/usr/bin/env python3

from graviti import GAS
from graviti.dataset import Dataset, Data
from graviti.label import LabelType, LabeledBox2D

ACCESS_KEY = "Accesskey-****"
DATASET_NAME = "TestDataset"
SEGMENT_NAME = "TestSegment"
THREAD_NUMBER = 8

dataset = Dataset(DATASET_NAME)  # create local dataset
segment = dataset.create_segment(SEGMENT_NAME)  # create local segment

# Add subcatalog
subcatalog = dataset.create_subcatalog(LabelType.BOX2D)
subcatalog.add_category(CATEGORY)

# Add data to segment
for filename, labels in zip(FILE_LIST, LABEL_LIST):
    data = Data(filename)
    data.register_label(LabelType.BOX2D)
    for label in labels:
        label = LabeledBox2D(
            label.box.xmin,
            label.box.ymin,
            label.box.xmax,
            label.box.ymax,
            category=label.category,
        )
        data.append_label(label)
    segment.append(data)

gas = GAS(ACCESS_KEY)  # register the accesskey to gas client

# Upload local dataset to tensorbay
# Argument 'jobs' for multi-thread uploading
# Set 'skip_uploaded_files' to 'True' will skip the uploaded files
gas.upload_dataset_object(dataset, jobs=THREAD_NUMBER, skip_uploaded_files=True)
```

#### Upload fusion data with labels

This sample is for uploading dataset which contains labels

```python
#!/usr/bin/env python3

from graviti import GAS
from graviti.dataset import Dataset, Data
from graviti.label import LabelType, LabeledBox2D

ACCESS_KEY = "Accesskey-****"
DATASET_NAME = "TestDataset"
SEGMENT_NAME = "TestSegment"
THREAD_NUMBER = 8

dataset = Dataset(DATASET_NAME)  # create local dataset
segment = dataset.create_segment(SEGMENT_NAME)  # create local segment

# Add subcatalog
subcatalog = dataset.create_subcatalog(LabelType.BOX2D)
subcatalog.add_category(CATEGORY)

# Add sensor to segment
for sensor_name in SENSOR_LIST:
    camera = Camera(sensor_name)
    camera.set_translation(x=1.1, y=2.2, z=3.3)
    camera.set_rotation(w=1.1, x=2.2, y=3.3, z=4.4)
    camera.set_camera_matrix(fx=1.1, fy=2.2, cx=3.3, cy=4.4)
    camera.set_distortion_coefficients(p1=1.1, p2=2.2, k1=3.3, k2=4.4, k3=5.5)
    segment.add_sensor(camera)

# Add frame to segment
for frame_info in FRAME_LIST:
    frame = Frame()
    for sensor_name in SENSOR_LIST:
        data_info = frame_info[sensor_name]

        data = Data(data_info.filename, data_info.timestamp)
        data.register_label(LabelType.BOX2D)
        for label in data_info.labels:
            label = LabeledBox2D(
                label.box.xmin,
                label.box.ymin,
                label.box.xmax,
                label.box.ymax,
                category=label.category,
            )
            data.append_label(label)

        frame[sensor_name] = data

    segment.append(frame)

gas = GAS(ACCESS_KEY)  # register the accesskey to gas client

# Upload local dataset to tensorbay
# Argument 'jobs' for multi-thread uploading
# Set 'skip_uploaded_files' to 'True' will skip the uploaded files
gas.upload_dataset_object(dataset, jobs=THREAD_NUMBER, skip_uploaded_files=True)
```

#### Commit dataset

```python
#!/usr/bin/env python3

from graviti import GAS
from graviti.dataset import Dataset, Data
from graviti.label import LabelType, LabeledBox2D

# code for load data into Dataset object
...
...

# upload_dataset_object will return the client of the uploaded dataset
dataset_client = gas.upload_dataset_object(dataset, jobs=THREAD_NUMBER, skip_uploaded_files=True)

COMMIT_MESSAGE = "Initial commit"
TAG = "v0.0.1"

# 'commit()' method will commit your dataset and return the commited dataset client
commited_dataset_client = dataset_client.commit(COMMIT_MESSAGE, TAG)
```

#### Read data and label

```python
#!/usr/bin/env python3

from graviti import GAS
from graviti.label import LabelType
from PIL import Image

ACCESS_KEY = "Accesskey-****"
DATASET_NAME = "TestDataset"
SEGMENT_NAME = "TestSegment"

gas = GAS(ACCESS_KEY)
dataset_client = gas.get_dataset(DATASET_NAME)  # Get dataset client of your dataset
segment = gas.get_segment_object(SEGMENT_NAME)  # Get segment object of your dataset

for data in segment:
    with data.open() as fp:
        img = Image.open(fp)  # Read image by PIL

    for labeled_box in data[LabelType.BOX2D]:  # Get all labeled box
        box = list(labeled_box)                # Get box which format should be [xmin, ymin, xmax, ymax]
        category = labeled_box.category        # Read the category of the labeled box
        attributes = labeled_box.attributes    # Read the attributes of the labeled box
```

## Command line

We also provide `gas` command to call SDK APIs.

Use `gas` in terminal to see the available commands as follows.

```bash
gas config
gas create
gas delete
gas publish
gas ls
gas cp
gas rm
```

#### config environment

```bash
gas config [accessKey]                   # config accesskey to default environment
gas -c [config_name] config [accessKey]  # create an environment named [config_name]
                                         # and config accesskey to it
```

#### show config

```bash
gas config         # show config information of all environments
```

#### choose environment

```bash
gas [command] [args]                           # choose default environment
gas -c [config_name] [command] [args]          # choose the environment named [config_name]
gas -k [accessKey] [command] [args]            # appoint accessKey in current command line

# '-k' has higher priority than '-c'
```

#### create dataset

```bash
gas create tb:[dataset_name]
```

#### delete dataset

```bash
gas delete tb:[dataset_name]
```

#### publish dataset

```bash
gas publish tb:[dataset_name]
```

#### list data

```bash
gas ls [Options] [tbrn]

Options:
  -a, --all      List all files under all segments. Only works when [tbrn] is tb:[dataset_name].

tbrn:
  None                                              # list all dataset names
  tb:[dataset_name]                                 # list all segment names under the dataset
  tb:[dataset_name]:[segment_name]                  # list all files under the segment
  tb:[dataset_name]:[segment_name]://[remote_path]  # list files under the remote path
```

#### upload data

```bash
gas cp [Options] [local_path1] [local_path2]... [tbrn]

Options:
  -r, --recursive     Copy directories recursively.
  -j, --jobs INTEGER  The number of threads.

tbrn:
  tb:[dataset_name]:[segment_name]                  # copy files to the segment
  tb:[dataset_name]:[segment_name]://[remote_path]  # copy files to the remote path

# [segment_name] is must required.
# If only upload one file and [remote_path] doesn't end with '/',
# then the file will be uploaded and renamed as [remote_path]
```

#### delete data

```bash
gas rm [Options] [tbrn]

Options:
  -r, --recursive  Remove directories recursively.
  -f, --force      Delete segments forcibly regardless of the nature of the dataset.
                   By default, only segments with no sensor can be deleted.
                   Once '-f' is used, sensors along with their objects will also be deleted.

tbrn:
  tb:[dataset_name]                                 # remove all segments under the dataset
  tb:[dataset_name]:[segment_name]                  # remove a segment
  tb:[dataset_name]:[segment_name]://[remote_path]  # remove files under the remote path
```

#### shell completion

Activation

For Bash, add this to ~/.bashrc:

```
eval "$(_GAS_COMPLETE=source_bash gas)"
```

For Zsh, add this to ~/.zshrc:

```
eval "$(_GAS_COMPLETE=source_zsh gas)"
```

For Fish, add this to ~/.config/fish/completions/foo-bar.fish:

```
eval (env _GAS_COMPLETE=source_fish gas)
```

See detailed info in [Click Shell Completion](https://click.palletsprojects.com/en/7.x/bashcomplete/)
