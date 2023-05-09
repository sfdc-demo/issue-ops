# issue-ops
## A self-service approach for managing github components/settings across multiple github instances. 

How it works:

1. Issue template created 
2. A new issue is created using the issue template and label is assigned
3. Issue triggers an action on `open`
4. Issue template is parsed
5. Validation performed for required form fields and user permissions
6. Work performed using `gh` cli tool

What's included:

### set_hostname.py
Used to set the hostname of the github instance

### validate_required_keys.py
Used to ensure that prohibited form values are not present. This will surface the prohibited values for the form field(s) so the user understands why the issue been rejected

### validate_role.py
Used to ensure the user has access to the instance and org. If the usee does not permissions this will surface a permissions error so the user understands why the issue been rejected

It be could beneficial to understand how a user may obtain credentials via this error message (e.g. bubble solutions)


