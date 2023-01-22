# Dropbox to github
- Simple script that takes the current state of a public/private dropbox folder and commits it to a public/private repo hosted on github
- Intention when writing this is so it can be used as a lambda function that can be triggered to an a schedule using a cron expression (via EventBridge) to keep personal in dropbox backed up in a version controlled way
- Assumptions
  - The repo already exists and there is a github [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with permissions to make changes
  - There exists a [DBX Platform app](https://www.dropbox.com/developers/reference/getting-started#app%20console) created
  - Access to aws from the cli

____
## Variables and secrets 
- `DROPBOX_CLIENT_ID` and `DROPBOX_CLIENT_ID` are the client credentials of the dropbox app.
- `DROPBOX_REFRESH_TOKEN` is generated using the `authorization_code` flow using the client id and secret . Step by step details for obtaining it [here](https://www.dropboxforum.com/t5/Dropbox-API-Support-Feedback/Get-refresh-token-from-access-token/td-p/596739)
- `DROPBOX_FOLDER_PATH`  is the absolute path of the folder in dropbox to be moved to github
- `GITHUB_TOKEN` is the [github personal access token](https://github.com/settings/tokens)
- `GITHUB_REPO_NAME` is the repo name where the dropbox files will be located

____
## Lambda infrastructure and deployment
### Create infrastructure and deploy lambda
```Bash
export \
  TF_VAR_DROPBOX_CLIENT_ID=value \
  TF_VAR_DROPBOX_CLIENT_SECRET=value \
  TF_VAR_DROPBOX_FOLDER_PATH=value \
  TF_VAR_DROPBOX_REFRESH_TOKEN=value \
  TF_VAR_GITHUB_REPO_NAME=value \
  TF_VAR_GITHUB_TOKEN=value \
  TF_VAR_GITHUB_USER_NAME=value \
  && sh ./deploy_iac.sh
```

### Deploy an updated lambda

```Bash
sh ./deploy_code.sh
```