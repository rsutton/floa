# TODO
- export/import to/from json

- bulk update/multiple item selection in UI

- maybe move init_app to Library from __init__.py or an App object

- multiple user/libraries?
  - library.catalog belongs in LoA - only need 1 instance
  - library.library is associated with a user
  - LoA checks for updates from website on startup (and daily?)
  - when user logon, check catalog and apply updates to library.library
    - don't need to use compare, just process entire catalog against library
    since 'add' logic will only change missing entries. 
  - oauth
  - user db as simply hash table

- rebuild my library list from json