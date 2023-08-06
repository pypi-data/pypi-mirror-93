## DatCat
Simple data catalogue api.
Please note this is an alpha version and still in active development.

###Convensions
Location: /datcat/catalogue/schemas \
Filetype: .json \
Naming: your_schema_name_v1.json \
Platform: bigquery

###Format of a Simple Schema
```json
[
  {
    "description": "Unique Identifier",
    "mode": "REQUIRED",
    "name": "MY_UNIQUE_ID",
    "type": "INT64"
  },  {
    "description": "Favourite Colour",
    "mode": "REQUIRED",
    "name": "MY_FAVOURITE_COLOUR",
    "type": "STRING"
  }
]
```

### .env.example
```bash
#settings
SCHEMAS_PATH=catalogue/schemas
METADATA_PATH=catalogue/metadata
MAPPINGS_FILEPATH=catalogue/mappings/schema_topic_subscription.json

CATALOGUE_SCHEME=http
CATALOGUE_HOST=0.0.0.0
CATALOGUE_PORT=50000
CATALOGUE_DEBUG=False
```
### Build and Run it Inside a Docker Container Example

```bash
source .env
poetry build --format wheel
docker build --tag dc .
docker run --hostname datcat \
  --env-file .env \
  --publish "${CATALOGUE_PORT}":"${CATALOGUE_PORT}" \
  --detach dc:latest
```

Now go to: http://0.0.0.0.8080 to see it

### Test Coverage
```bash
pytest --cov=. tests/ | grep -v .env
```
