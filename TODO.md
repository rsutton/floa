# TODO

- ~~library update only happens at login or on status change. if there are new items
and the user is already authenticated, those items will not be added to the 
  library correctly, i.e. missing status value. Need a call to library.update()
  if new items are found in loa.check_for_updates() for the current user.~~

- ~~remove anonymous user check status=0 from home page. handle the anon user in code.~~

- ~~anonymous user should be able to 'try' the app, meaning that item status 
changes persist between pages. currently the bookshelf page does a full load
and clears any changes.~~

- bulk update/multiple item selection in UI

- ~~LoA checks for updates on startup. For long running server this~~
    ~~needs to be at least daily.~~
    - ~~set 12 hour interval, will check whenever / is hit~~

- multiple user/libraries?
  - ~~at user logon, check catalog and apply updates to their library~~
  - oauth - make Google connection
  - new user signup
  - ~~anonymous can view catalog and 'create' bookshelf but it doesn't save the changes~~
  - ~~logout link~~

- ~~save user updates~~
- update help page with Login/Signup 

- db admin tool
  - view and edit records
  - backup, import/export db
- ~~db index to speed up queries~~
- ~~private data member instead of reading file on every query~~
- 