# Dropbox to github
- Simple script that takes the current state of a public/private dropbox folder and commits it a repo hosted on github
- Assumes that the repo already exists and an
- Intention when writing this is so it can be used as a lambda function that can be triggered to an a schedule using a cron expression (via EventBridge) 

## Running Locally
The environment variables are set by updated the values in `dropbox_to_github.py`

____
## Secrets 
- `GITHUB_TOKEN` token is the [github personal access token](https://github.com/settings/tokens) needed to assess and update github.
  - This token has an expiration.
- `DROPBOX_REFRESH_TOKEN` is generated using the `authorization_code` flow. Step by step details for obtaining it [here](https://www.dropboxforum.com/t5/Dropbox-API-Support-Feedback/Get-refresh-token-from-access-token/td-p/596739)

____
## Lambda Infrastructure + Deployment
### Package and deploy a new lambda lambda to aws
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