# Package and deploy
```Bash
./deploy.sh
```

# Secrets
- Secrets are added in aws as env variables
- Git access token expires every year. So env variable must be updates
  + https://github.com/settings/tokens?type=beta
- Dropbox refresh token is generated using the auth code and authcoode is generated by calling /authorize with offline grant type

