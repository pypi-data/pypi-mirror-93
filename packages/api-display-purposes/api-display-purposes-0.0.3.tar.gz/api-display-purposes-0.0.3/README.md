# DisplayPurposes

DisplayPurposes is a Python library for programmatically interacting with the website https://displaypurposes.com

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install displaypurposes

```bash
pip install api-display-purposes
```

## Usage

```python
from apidisplaypurposes import displaypurposes

# obtain tags similar to #happy
displaypurposes.tag('happy')
# obtain 10 tags similar to #happy
displaypurposes.tag('happy', limit=10)
# obtain 20 tags similar to #happy emulating firefox GET requests
displaypurposes.tag('happy', limit=20, browser='firefox')

# obtain tags that share an edge with #happy
displaypurposes.graph('happy')
# obtain tags that share an edge with #happy emulating firefox GET requests
displaypurposes.graph('happy', browser='firefox')

# obtain the 20 most popular tags used within the specified window
displaypurposes.map(-118.77636909484865,
                    33.23850805662313,
                    -117.04052925109865,
                    35.10400554120783,
                    zoom=14,
                    limit=20)
# obtain the 20 most popular tags used within the specified window emulating chrome GET requests
displaypurposes.map(-118.77636909484865,
                    33.23850805662313,
                    -117.04052925109865,
                    35.10400554120783,
                    zoom=14,
                    limit=20,
                    browser='chrome')
```

## Acknowledgement

Of course this project could not exist without the work of the makers of https://displaypurposes.com. Thank you for the work you put into this useful tool.

## License
[GNU](https://choosealicense.com/licenses/gpl-3.0/)
