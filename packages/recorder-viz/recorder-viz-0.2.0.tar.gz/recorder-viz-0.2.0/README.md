recorder-viz
=============

This is a python package which contains tools for processing [Recorder](https://github.com/uiuc-hpc/Recorder) traces.

Usage
--------

Install it using pip: `pip install recorder-viz`


Below is a simple code snippet shows how to use the provided class `RecorderReader`. 

Copy it to test.py and `run python test.py [path/to/Recorder traces folder]`

```python

#!/usr/bin/env python
# encoding: utf-8

import sys
from recorder_viz import RecorderReader

reader = RecorderReader(sys.argv[1])

for rank in range(reader.GM.total_ranks):
    LM = reader.LMs[rank]
    print("Rank: %d, Number of trace records: %d" %(rank, LM.total_records))
```

Details
--------

```python
class LocalMetadata(Structure):
    _fields_ = [
            ("start_timestamp", c_double),
            ("end_timestamp", c_double),
            ("num_files", c_int),
            ("total_records", c_int),
            ("filemap", POINTER(c_char_p)),
            ("file_sizes", POINTER(c_size_t)),
            ("function_count", c_int*256),
    ]

class GlobalMetadata(Structure):
    _fields_ = [
            ("time_resolution", c_double),
            ("total_ranks", c_int),
            ("compression_mode", c_int),
            ("peephole_window_size", c_int),
    ]


class Record(Structure):
    _fields_ = [
            ("status", c_char),
            ("tstart", c_double),
            ("tend", c_double),
            ("func_id", c_ubyte),
            ("arg_count", c_int),
            ("args", POINTER(c_char_p)),
            ("res", c_int),
    ]
```

The above three classes are Python wrappers of C structures. They can be accessed through the
Python class `RecorderReader` as the simple example shown at the begining.

```python
class RecorderReader:
    self.GM: instance of GlobalMetadata
    self.LMs: list of LocalMetadata objects, one for each rank
    self.records: list of list, self.records[i] is a list of Record objects of rank i.

```
