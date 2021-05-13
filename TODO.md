# TODO

- Out of Stock (or Out of Print) status
  - Refactor status as binary digits so that an item may have multiple status'
    - show oos as a separate status
    - status rule engine
  - catalog update reads details of each item to search for 'out of stock'
    string 
    <div class="detail-content__overview" style="opacity: 1;">
                <p><strong><font color="blue">This title is out of stock</font>
                
  - should not be changeable by user
  - new column between status and volume id or perhaps change the volume id appearance

- TLS certificate for localhost
- Dockerize - how to handle data persistence - local mount?

- bulk update/multiple item selection in UI

- new user signup
  - create new user
~~  - initialize empty library, don't show items as new~~

- sort and filter, change existing views into 'quick filters'
  - volume id is default
  - title
  - author? many volumes are collections of several authors


- update help page with Login/Signup 

- db admin tool
  - view and edit records
  - backup, import/export db
- try sqlite3

- Bug
  - ~~user library does not update if logged in when a new catalog item is added~~