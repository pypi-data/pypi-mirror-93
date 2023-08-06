# mongoengine-arrow

## Description

[Arrow](https://github.com/arrow-py/arrow) datetime support for [MongoEngine](https://github.com/MongoEngine/mongoengine)

## Install

```bash
pip3 install --upgrade mongoengine-arrow
```

## How it works

Feed it datetime with or without timezone info in any format Arrow supports.
To confirm whether it will work, feed it to `arrow.get()` function.

## Usage example

```python3
# Import the field
from mongoengine_arrow import ArrowDateTimeField

...

# Define model
class MyModel(Document):
    timestamp = ArrowDateTimeField(required=True)

...

# Get instance
myinstance = MyModel.objects.first()

# Get timestamp in local time
timestamp = myinstance.timestamp.to("local")

# Set timestamp in any timezone
myinstance.timestamp = arrow.get(2021, 1, 1, tzinfo="UTC")

# Set timestamp from datetime
from datetime import datetime
myinstance.timestamp = datetime(2021, 1, 1)

# Set timestamp from datetime that has tzinfo
from datetime import datetime
from dateutil.tz import gettz
myinstance.timestamp = datetime(2021, 1, 1, tzinfo=gettz("UTC+5"))
```
