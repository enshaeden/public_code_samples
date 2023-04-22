# JAMF Command Line Management
## Service Desk Support options

This support tool is designed to allow Service Desk users to facilitate basic managmeent actions in a specific range of tasks.

Primarily, users should be able to do the following:

- Lock computer
- Erase computer
- Lock mobile device
- Add device to group
- Remove device from group

Policy membership is not included as policy membership should be relegated to Group membership.

Users will need a service account for authorisation at this time until session tokens or okta auth is added.
For enhanced security it is recommended that username/password combos should not be written directly into the code.
Instead, users should set their username and password as environment variables in their ~/.*profile or ~/.*rc files.

`JSS_USER="serviceaccount_username"`

`JSS_PASS="serviceaccountpasswordsareriskyinthisformat"`

`export JSS_USER`

`export JSS_PASS`

Alternatively, though less secure, users can hard-code the credentials directly into the jssAuth file as follows:

`username = "serviceaccount_username"`

`password = "thisisevenmorerisky"`
