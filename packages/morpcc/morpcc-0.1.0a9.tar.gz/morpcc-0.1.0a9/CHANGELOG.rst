0.1.0a9 (2021-01-31)
--------------------

- hide reference panel if no permission to view
- excluding results from datatable search creates odd pagination, 
  show item as restricted instead
- display state column by default if statemachine exists
- added transition guarding capability
- `site/+term-search` is now using `ViewHome` permission


0.1.0a8 (2021-01-31)
--------------------

- Reference widget can now filter by selection from different field
- relocate `/api/v1/` to `/api`
- improvement in permission rule resolution
- fixed permission inheritance
- utilize config based permission rule configuration from morpfw
- added default permissions for notifications
- added default permissions for site root
- automatically activate user if no email verification needed


0.1.0a7 (2021-01-27)
--------------------

- removed Through-the-web development components
- relicense to GPLv3 considering TTW components no longer in this package
- notification system is functional with normally expected views now


0.1.0a6 (2021-01-14)
--------------------

- fix issue with apikey model have renamed 'label' field to 'name'


0.1.0a5 (2020-12-24)
--------------------

- improve documentation
- reduce default database string column length
- compare types when generating updates
- fixed issue with deleting dictionary entity
- show user source in user listing
- validate reference data in display form
- added AGPL license notification page
- added AGPL exception agreement license enforcement hooks
- added type referencing/backreferencing UI
- added initial data visualization library
- use ESCapableRequest by default
- various UI fixes


0.1.0a4 (2020-11-23)
--------------------

- First release with changelog
