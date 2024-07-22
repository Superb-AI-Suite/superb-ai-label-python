<!-- <p align="center">
  <a href="http://suite-api.superb-ai.com/" target="blank"><img src="logo/cool-tree.png" width="200" height="200" alt="Cool-Tree Logo" /></a>
</p> -->

# `superb-ai-label`

[Build](https://github.com/Superb-AI-Suite/superb-ai-label/workflows/Build/badge.svg)
[![Version](https://img.shields.io/pypi/v/superb-ai-label)](https://pypi.org/project/superb-ai-label/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`superb-ai-label` is the Software Development Kit for managing Label with [Superb Platform](https://superb-ai.com/).

## Installation

```shell
pip install --upgrade superb-ai-label
```

### Requirements

Python 3.8+

## Documentation

You can also find the documentation for `superb-ai-label` [on the website](https://docs.superb-ai.com/reference/super-ai-python-sdk-overview).

* [Introduction](https://docs.superb-ai.com/reference/super-ai-python-sdk-overview)
* [Tutorial](https://docs.superb-ai.com/reference/sdk-workflow-and-examples)

## Authentication

An Access Key is required to use the python client. This can be generated from the Settings > Access menu on the Superb AI Curate website. For more details on access key issuance and management, you can check the Access Key Management documentation. The Team Name refers to the organization name that your personal account belongs to.

```python
import os
from spb_label import sdk

project_name="Project Name"
team_name = os.environ.get("TEAM_NAME")
access_key = os.environ.get("ACCESS_KEY")
client = sdk.Client(project_name=project_name, team_name=team_name, access_key=access_key)
```

## Resource Description

### Projects

```python
from spb_label import sdk

client = sdk.Client()
# Get all projects
count, projects = client.get_projects()
# Set project to client what to handle
client.set_project(projects[0])
# Get project name and id
client.get_project_name()
client.get_project_id()

# Get all project users
count, users = client.get_project_users()

# Get project tags
count, tags = client.get_project_tags()
```

### Labels

```python
from spb_label import sdk
from spb_label.utils import SearchFilter

client = sdk.Client()
client.set_project(name="YOUR PROJECT NAME")

# Get labels
filter = SearchFilter(project=client.project)

# Status filter
filter.status_is_any_one_of = ["WORKING", "SKIPPED"]
# Assignee filter
filter.assignee_is_any_one_of = ["ASSIGNEE EMAIL"]
# Tag filter
filter.tag_name_all = ["TAG NAME"]

count, labels, next = client.get_labels(
  filter=filter,
  cursor=next
)
```

## Contributing

Feel free to report issues and suggest improvements.  
Please email us at <support@superb-ai.com>

## License

The MIT License (MIT)

Copyright (c) 2020, Superb AI, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
