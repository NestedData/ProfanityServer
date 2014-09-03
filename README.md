## Usage Profanity Library `src/Profanity`

```python
from .profanity import Filter

# create a new filter
# if the filter_id exists, the doc will be retrieved
# if it doesn't exist, it will be created and persisted to the db
MSUFilter = Filter("drizzle:mississippi-state-university")

# grab an existing filter, don't create it if it doesn't exist yet
LSUFilter = Filter("drizzle:lsu", create=False)


# Filters have a small public api. Each method updates the blacklist
# in memory and persists the change to the database
MSUFilter.set_blacklist(["a", "b"])

# extends the existing blacklist with the new blacklist
MSUFilter.add_to_blacklist(["c", "d"])

# removing terms that don't exist causes no problem
# store=False makes the change locally without persisting it to the db
MSUFilter.remove_from_blacklist(["a", "c", "e"], store=False)

# remove the filter from the db entirely
MSUFilter.destroy()

# get the blacklist from the filter as an array of terms
MSUFilter.black_list

# persist the filter to the db
MSUFilter.save()
```


## Usage: Server API

### Managing filters

#### POST /filters

Creates a new filter

##### request body

```python
data = {
  "filter_id": "slug-style-string"
}
```

##### Response - JSON

Echos filter_id back on success or returns an error.

```json
{
  "filter_id: "slug-style-string"
}
```

or

```json
{
  "error": "Failed to create filter for filter_id: 'slug-style-string'"
}
```

#### GET /filters/:filter_id

Returns the filter info. Expects no request body

##### Response - JSON

```json
{
  "filter_id": "slug-style-string",
  "black_list": ["a", "b"]
}
```

#### PUT /filters/:filter_id

Update the filter.

##### Request body

If the blacklist key isn't present or none of the sub keys are set then no change will be made to the filter.

The `add` key will add terms to the existing black_list.

The `remove` key will remove terms from the existing black_list.

The `init` key will replace the black_list in place.

`init` is processed first, followed `remove` and ending with `add`.

```json
{
  "black_list": {
    "init": ["a", "c"],
    "remove": ["a"],
    "add": ["z", "y", "x"]
  }
}
```

##### Response - JSON

```json
{
  "filter_id": "slug-style-string",
  "black_list": ["a", "b"]
}
```

#### DELETE /filters/:filter_id

Destroys the filter. Doesn't expect a request body.

##### Response - JSON

```json
{
  "filter_id": "slug-style-string"
}
```

### Codify Text

#### POST /filters/:filter_id/codify

##### Request body

```python
data = {
  text: "A string to check for profanity"
}
```

##### Response - JSON

```json
{
  "profane": False
}
```