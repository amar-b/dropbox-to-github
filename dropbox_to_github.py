import dropbox
import os
import shutil
import zipfile
import requests
import time
import json
from requests.auth import HTTPBasicAuth
from dulwich import porcelain

def get_dropbox_sl_token(env):
  data = {
    "grant_type": "refresh_token",
    "refresh_token": env["DROPBOX_REFRESH_TOKEN"]
  }
  auth = HTTPBasicAuth(env["DROPBOX_CLIENT_ID"], env["DROPBOX_CLIENT_SECRET"])

  return requests.post("https://api.dropbox.com/oauth2/token", data=data, auth=auth).json()["access_token"]

def clean(env):
  for d in ["repo", "git", "temp", "temp.zip"]:
    path = f'{env["DBX_TO_GH_TMP_PATH"]}/{d}'
    if os.path.exists(path):
      if os.path.isfile(path):
        os.remove(path)
      else:
        shutil.rmtree(path)


def read_env_vars():
  return {key: os.environ[key] for key in [
    "DBX_TO_GH_TMP_PATH",
    "GITHUB_TOKEN", 
    "GITHUB_USER_NAME",
    "GITHUB_REPO_NAME",
    "DROPBOX_FOLDER_PATH",
    "DROPBOX_CLIENT_ID",
    "DROPBOX_CLIENT_SECRET",
    "DROPBOX_REFRESH_TOKEN"
  ]}


def clone_repo(env):
  token, user_name, repo_name =  env["GITHUB_TOKEN"], env["GITHUB_USER_NAME"], env["GITHUB_REPO_NAME"]

  return porcelain.clone(f'https://user:{token}@github.com/{user_name}/{repo_name}', f'{env["DBX_TO_GH_TMP_PATH"]}/repo')


def update_repo(env):
  local_base_path = env["DBX_TO_GH_TMP_PATH"]
  dropbox_path = env["DROPBOX_FOLDER_PATH"][1:] if env["DROPBOX_FOLDER_PATH"][0] == '/' else env["DROPBOX_FOLDER_PATH"]
  
  dbx = dropbox.Dropbox(get_dropbox_sl_token(env))
  dbx.files_download_zip_to_file(f'{local_base_path}/temp.zip', f'/{dropbox_path}')

  with zipfile.ZipFile(f'{local_base_path}/temp.zip', "r") as zip_ref:
      zip_ref.extractall(f'{local_base_path}/temp')

  src = f'{local_base_path}/temp/{dropbox_path}'
  dtn = f'{local_base_path}/repo'

  for f in set(os.listdir(src) + os.listdir(dtn) ):
    if ".git" in f:
      continue
    src_path = os.path.join(src, f)
    dst_path = os.path.join(dtn, f)

    if os.path.exists(dst_path):
      if os.path.isfile(dst_path):
        os.remove(dst_path)
      else:
        shutil.rmtree(dst_path)
    
    if os.path.exists(src_path):
      shutil.move(src_path, dst_path)

def commit_repo(env, repo):
  token, user_name, repo_name =  env["GITHUB_TOKEN"], env["GITHUB_USER_NAME"], env["GITHUB_REPO_NAME"]
  repo_path = f'{env["DBX_TO_GH_TMP_PATH"]}/repo/'

  local_paths = [f'{dp}/{f}' for dp, dn, filenames in os.walk(repo_path) for f in filenames if ".git" not in dp and ".git" not in f]
  tracked_paths = [repo_path + l.decode("utf-8")  for l in porcelain.ls_files(repo)]
  paths = list(set(local_paths+tracked_paths))

  porcelain.add(repo, paths = paths)
  porcelain.commit(repo, f'dropbox-to-github app - {time.ctime()}')
  porcelain.push(repo, f'https://user:{token}@github.com/{user_name}/{repo_name}', force=True)

  return len(paths)

def update_github_from_dropbox():
  env = read_env_vars()
  clean(env)
  repo = clone_repo(env)
  update_repo(env)
  count = commit_repo(env, repo)
  clean(env)

  return f'Updated {count} files in {env["GITHUB_REPO_NAME"]}'


# local
if __name__ == "__main__":
  os.environ["DBX_TO_GH_TMP_PATH"] = "."

  os.environ["GITHUB_TOKEN"] = ""
  os.environ["GITHUB_USER_NAME"] = ""
  os.environ["GITHUB_REPO_NAME"] = ""

  os.environ["DROPBOX_FOLDER_PATH"] =  ""
  os.environ["DROPBOX_CLIENT_ID"] =  ""
  os.environ["DROPBOX_CLIENT_SECRET"] =  ""
  os.environ["DROPBOX_REFRESH_TOKEN"] =  ""

  print(update_github_from_dropbox())