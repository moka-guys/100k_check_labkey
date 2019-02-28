# 100k_check_labkey v1.0

## About
Get data from the Genomics England LabKey API for a given participant ID. The API is accessed using the HTTP interface.

The class LabKey_HTTP() contains methods for accessing data. Calling the script prints the following to the console for the input PID:
"<NAME>,<DATE_OF_BIRTH\[DAY/MONTH/YEAR\]>,<NHS NUMBER>"

This module requires a ~/.netrc file with a user's LabKey login credentials. Details of this file format can be found in the [LabKey API Docs on creating a netrc file](https://www.labkey.org/Documentation/wiki-page.view?name=netrc).

## Usage

Requirements:
* Python 3.6+
* pytest
* requests

On `SV-TE-GENAPP01` activate the `jellypy_py3` conda environment so that above requirements are met:

```
source activate jellypy_py3
```
Then run the script...
```
LabKey.py --pid 1234567 -u [ labkey username ] -p [ labkey password ]

Arguments:
    pid: A GEL participant ID
    username;password: Optional labkey credentials
```

## Objects
Class LabKey_HTTP(pid, username=None, password=None) : Returns an object with LabKey data for a given GEL participant ID.

## Tests
Tests are defined in test_labkey.py
Rename `example_test_data.txt` to `test_data.txt` and add in the details of a patient in labkey for use in testing. Format is...
```
GeL participant ID
DOB
NHS number
```
To ensure the correct version of python is used when running pytest, use `python -m pytest` from the environment the script will be run in.