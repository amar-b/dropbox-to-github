import dropbox_to_github
import json
import traceback

def lambda_handler(event, context):
  try:
    return dropbox_to_github.update_github_from_dropbox()
  except Exception as ex:
    print(ex)
    traceback.print_stack()
    raise ex