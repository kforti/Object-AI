from collections import defaultdict

from .models import Workspace

WORKSPACES = defaultdict(list)



def create_bucket_service():
    pass


def add_data_for_annotation_service(config):
    pass


def get_workspaces(user):
    workspaces = WORKSPACES[user.cognito_username]
    return workspaces


def create_workspace_service(user):
    workspace = Workspace(
        id=200001,
        owner_id =user.cognito_username,
        name ='test-workspace-backend',
        bucket_name ='test-bucket',
        labelbox_aws_account='0909702347',
        labelbox_external_id='9832088hr39h23'
    )
    if len(WORKSPACES[user.cognito_username]) > 0:
        print('ERROR. Workspace already exists')
        return False
    WORKSPACES[user.cognito_username].append(workspace)
    return True


def _add_to_labelbox():
    pass
