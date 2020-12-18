
- initialize new library
  - folder creation
  - get latest
- message bar for 
  - item counts
  - last update time
  - "update now" button? instead of updating on startup?
- ensure data is sorted by volume number in library, if a new item is inserted into 
catalog it should be inserted into the library at the proper location, not simply 
appended.
- refactor get_latest and update methods into a service/controller object
- 'library' only needs to be an ordered list of status numbers.
  - catalog.json + library.array = 'the library'
  - pickle catalog
  - use hash compare for catalog
  - save 'last update' timestamp in config.py
  - save 'catalog hash' in config.py
