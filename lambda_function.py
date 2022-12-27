import dropbox
import os
import shutil
import json
import zipfile
import requests
import time
from requests.auth import HTTPBasicAuth
from dulwich import porcelain
import traceback

def get_dropbox_sl_token(env):
  url = "https://api.dropbox.com/oauth2/token"
  client_id = env['DROPBOX_CLIENT_ID']
  client_secret = env['DROPBOX_CLIENT_SECRET']
  refresh_token = env['DROPBOX_REFRESH_TOKEN']

  return requests.post(url, data={
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token
  }, auth=HTTPBasicAuth(client_id, client_secret)).json()['access_token']

def clean(env):
  basePath = env['EFS_MNT_PATH']
  dirs = ['repo', 'git', 'temp', 'temp.zip']
  for d in dirs:
    if os.path.exists(basePath + d):
      if os.path.isfile(basePath + d):
        os.remove(basePath + d)
      else:
        shutil.rmtree(basePath + d)

def read_env():
  return {key: os.environ[key] for key in [
    'EFS_MNT_PATH',
    'GITHUB_TOKEN', 
    'DROPBOX_CLIENT_ID',
    'DROPBOX_CLIENT_SECRET',
    'DROPBOX_REFRESH_TOKEN'
  ]}
  
def clone_git_repo(env):
  token = env['GITHUB_TOKEN']
  path = env['EFS_MNT_PATH'] + 'repo'
  return porcelain.clone(f'https://user:{token}@github.com/amar-b/knowledge_repo', path)

def update_repo_from_dropbox(env):
  basePath = env['EFS_MNT_PATH']
  dbx = dropbox.Dropbox(get_dropbox_sl_token(env))
  dbx.files_download_zip_to_file(f'{basePath}temp.zip', '/knowledge_repo')
  with zipfile.ZipFile(f'{basePath}temp.zip', 'r') as zip_ref:
      zip_ref.extractall(f'{basePath}temp')

  src = f'{basePath}temp/knowledge_repo'
  dtn = f'{basePath}repo'

  for f in set(os.listdir(src) + os.listdir(dtn) ):
    if '.git' in f:
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

def update_git_repo(env, repo):
  repo_path =  env['EFS_MNT_PATH'] + 'repo/'
  token = env['GITHUB_TOKEN']
  origin = f'https://user:{token}@github.com/amar-b/knowledge_repo'

  paths = [repo_path + l.decode("utf-8")  for l in porcelain.ls_files(repo)]
  r = porcelain.add(repo, paths=paths)
  porcelain.commit(repo, 'KnowledgeRepoToGit - '+ time.ctime())
  porcelain.push(repo, origin, force=True)
  return len(paths)


def lambda_handler(event, context):
  try:
    env = read_env()
    clean(env)
    repo = clone_git_repo(env)
    update_repo_from_dropbox(env)
    cnt = update_git_repo(env, repo)
    clean(env)

    return {
      'statusCode': 200,
      'body': json.dumps(f'Successfully updated {cnt}')
    }
  
  except Exception as ex:
    print(ex)
    traceback.print_stack()
    raise ex

# local testing
if __name__ == '__main__':
  os.environ['EFS_MNT_PATH'] = ''

  os.environ['GITHUB_TOKEN'] = ''

  os.environ['DROPBOX_CLIENT_ID'] =  ''
  os.environ['DROPBOX_CLIENT_SECRET'] =  ''
  os.environ['DROPBOX_REFRESH_TOKEN'] =  ''

  print(lambda_handler(None, None))