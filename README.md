# Dropbox to github
- Simple script that takes the current state of a public/private dropbox folder and commits it a repo hosted on github
- Assumes that the repo already exists and a regiestered app with dropbox with a valid client id/secret
- Intention when writing this is so it can be used as a lambda function that can be triggered on a schedule (via EventBridge) to keep personal docs in dropbox backed up but in a version controlled way. I also assumed that I won't be making changes to the git repo directly as any changes will be overritten by changes coming from dropbox whenever this script runs.

____
## Secrets and variables 
- `DROPBOX_CLIENT_ID` and `DROPBOX_CLIENT_ID` are obtained upon [creating an app in dropbox](https://www.dropbox.com/developers/apps/create)
- `DROPBOX_REFRESH_TOKEN` is generated using the `authorization_code` flow using the client id and secret . Step by step details for obtaining it [here](https://www.dropboxforum.com/t5/Dropbox-API-Support-Feedback/Get-refresh-token-from-access-token/td-p/596739)
- `DROPBOX_FOLDER_PATH`  is the absolute path of the folder in dropbox to be moved to github
- `GITHUB_TOKEN` token is the [github personal access token](https://github.com/settings/tokens) needed to assess and update github.
  - This token has an expiration.
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
./deploy_code.sh
```
