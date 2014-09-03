## Usage `src/Profanity`

```python
from .profanity import Filter

# create a new filter
# if the client_id exists, the doc will be retrieved
# if it doesn't exist, it will be created and persisted to the db
MSUFilter = Filter("drizzle:mississippi-state-university")

# grab an existing filter, don't create it if it doesn't exist yet
LSUFilter = Filter("drizzle:lsu", create=False)


# Filters have a small public api. Each method updates the blacklist in memory and persists the change to the database

MSUFilter.set_blacklist(["a", "b"])

# extends the existing blacklist with the new blacklist
MSUFilter.add_to_blacklist(["c", "d"])

# removing terms that don't exist causes no problem
MSUFilter.remove_from_blacklist(["a", "c", "e"])
```