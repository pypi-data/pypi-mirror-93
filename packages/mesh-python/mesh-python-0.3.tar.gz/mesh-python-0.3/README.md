### A python client for Mesh Queries

#### Installation

`pip install mesh-python`

#### Usage

```python
from mesh import MeshClient

credentials = {
    "username":"Your username",
    "password":"Your password"
    }
client = MeshClient(**credentials)
query = "$UNIV2.DPI_WETH.DPI_PRICE"

result = client.engine(query)
```