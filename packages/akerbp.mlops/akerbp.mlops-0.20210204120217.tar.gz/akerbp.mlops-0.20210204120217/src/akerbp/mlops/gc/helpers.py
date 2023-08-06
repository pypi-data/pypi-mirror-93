"""
helpers.py

Functionality built on top of Google SDK (bash or python)
Requirement: SDK activated and GOOGLE_APPLICATION_CREDENTIALS defined
(see install_gc_sdk.sh)
"""

import subprocess
import os

import requests
import json
from google.cloud import secretmanager

from akerbp.mlops.core import logger 

logging=logger.get_logger(name='gc_helper')

project_id = os.getenv("GOOGLE_PROJECT_ID")


def create_service_account(service_account):
    """
    Create a service account if it doesn't exist
    """
    try:
        subprocess.check_call(
            f"gcloud iam service-accounts list | grep {service_account}",
            shell=True
        )
        logging.debug(f"Found service account {service_account}")
    except subprocess.CalledProcessError:
        subprocess.check_call(
            f"gcloud iam service-accounts create {service_account}",
            shell=True
        )
        logging.debug(f"Created service account {service_account}")


def access_secret_version(secret_id, version_id="latest"):
    """
    Read a secret

    See https://codelabs.developers.google.com/codelabs/secret-manager-python/index.html?index=..%2F..index#5
    See https://dev.to/googlecloud/serverless-mysteries-with-secret-manager-libraries-on-google-cloud-3a1p
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    # Access the secret version.
    response = client.access_secret_version(name=name)
    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')


def create_image(image_name, folder='.'):
    """
    Build an image
    """
    subprocess.check_call(
        f"gcloud builds submit {folder} \
            --tag gcr.io/{project_id}/{image_name}",
        shell=True
    )


def allow_access_to_secrets(service_account, secret_names=["mlops-cdf-keys"]):
    """
    Give a service account access to secrets stored in Secret Manager
    """
    s_a_id = f"{service_account}@{project_id}.iam.gserviceaccount.com"
    for secret_name in secret_names:
        subprocess.check_call(
            f"gcloud secrets add-iam-policy-binding {secret_name} \
            --member serviceAccount: {s_a_id}\
            --role roles/secretmanager.secretAccessor"
        )


def run_container(image_name, service_account):
    """
    Run container with a service account
    """
    subprocess.check_call(
        f"gcloud run deploy {image_name} \
            --image gcr.io/{project_id}/{image_name} \
            --platform managed \
            --region=europe-north1 \
            --no-allow-unauthenticated \
            --memory=512M \
            --service-account {service_account}",
        shell=True
    )


def deploy_function(
    function_name,
    folder='.',
    **kwargs
):
    """
    Deploys a Google Cloud Run function from a folder. 

    Inputs:
      - function_name: name of the function to create
      - folder: path where the source code is located
      - handler_path: path to the handler file
      - kwargs: accept `handler_path` and possibly other args required by CDF
            but not GC
    """
    service_account = f"{function_name}-acc"
    logging.debug(f"Deploy function {function_name}")
    create_service_account(service_account)
    allow_access_to_secrets(service_account)
    create_image(function_name, folder)
    run_container(function_name, service_account)


def read_function_url(function_name):
    # Read service url
    return subprocess.check_output(
        f"""gcloud run services list \
            --platform managed \
            --filter="metadata.name='{function_name}'" \
            --format="value(URL)") """,
        shell=True
    )


def call_function(function_name, data):
    """
    Call a function deployed in Google Cloud Run
    """
    url = read_function_url(function_name)
    requests.post(url, json={'data': json.dumps(data)})

    return {"status":"ok"}


def test_function(function_name, data):
    """
    Call a function with data and verify that the response's 
    status is 'ok'
    """
    logging.debug(f"Test function {function_name}")
    output = call_function(function_name, data)
    assert output['status'] == 'ok'
    logging.info(f"Test call was successful :)")