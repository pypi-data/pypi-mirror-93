"""
deploy.py

Deploy services in either Google Cloud Run or CDF Functions. 
Model registry uses CDF Files.
""" 
import os
from importlib import import_module, resources as importlib_resources
import shutil
import sys
import subprocess
from functools import partial


from akerbp.mlops.cdf.helpers import download_model_version, set_up_cdf_client
from akerbp.mlops.utils import logger 

logging=logger.get_logger(name='MLOps')

# Read environmental variables
ENV = os.environ['ENV'] # Must be set
SERVICE_NAME = os.environ['SERVICE_NAME']
LOCAL_DEPLOYMENT = os.getenv('LOCAL_DEPLOYMENT') # Optional

deployment_platform = 'cdf' # 'cdf'

def replace_string_file(s_old, s_new, file):
    with open(file) as f:
        s = f.read()
        if s_old not in s:
            logging.warning(f"Didn't find '{s_old}' in {file}")

    with open(file, 'w') as f:
        s = s.replace(s_old, s_new)
        f.write(s)


def set_test_mlops_import(req_file):
    # Some packages may not available in testpypi, so we give the standard
    # index as alternative
    old = 'akerbp.mlops'
    new = """
    akerbp.mlops
    """
    replace_string_file(old, new, req_file)
    logging.debug("Modified requirements.txt to install test akerbp.mlops")


def read_config():
    logging.info(f"Read project configuration")
    from mlops_settings import model_names, model_files, model_req_files
    from mlops_settings import model_artifact_folders, infos, model_test_files
    return zip(
        model_names, 
        model_files, 
        model_req_files, 
        model_artifact_folders,
        infos,
        model_test_files
    )


def get_top_folder(s):
    return s.split(os.sep)[0]


def to_import_path(file_path):
    if file_path:
        return file_path.replace(os.sep,'.').replace('.py','')
    else:
        logging.debug(f"Empty file path -> empty import path returned")


def to_folder(path, folder_path):
    """
    Copy folders, files or package data to a given folder
    Input:
      - path (string): supported parths are
            - folder path: e,g, "my/folder" 
            - file path: e.g. "my/file" (string)
            - module file: e.g. "module.Dockerfile" or "module.code_file" 
                where "code_file" is a python file (note that ".py" should 
                be omitted)  
    """
    if os.path.isdir(path):
        shutil.copytree(
            path, 
            os.path.join(folder_path, path), 
            dirs_exist_ok=True
        )
    elif os.path.isfile(path):
        shutil.copy(path, folder_path)
    else:
        module_path, file_name = path.rsplit('.',1)
        if not importlib_resources.is_resource(module_path, file_name):
            file_name += '.py'
        elif not importlib_resources.is_resource(module_path, file_name):
            raise Exception(f"Didn't find {file_name} in {module_path}")
        with importlib_resources.path(module_path, file_name) as file_path:
            shutil.copy(file_path, folder_path)


def run_tests(test_path, path_type='file'):
    """
    Run tests with pytest
    Input
      - test_path: path to tests with pytest (string or a list of strings) All
        should have the same format (see next parameter)
      - path_type: either 'file' (test_path refers then to files/folders) or
        'module' (test_path refers then to modules)
    """
    command = [sys.executable, "-m", "pytest"]
    if path_type == 'module':
        command.append("--pyargs")
    if isinstance(test_path, str):
        command.append(test_path)
    elif isinstance(test_path, list):
        command += test_path
    else:
        raise ValueError("Input should be string or list of strings")
    logging.info(f"Run tests: {test_path}")
    subprocess.check_call(command)


def deploy(model_settings):

    for setting in model_settings:
        (model_name, model_file, model_req_file, model_artifact_folder,
        info, model_test_file) = setting
        
        logging.info(f"Deploy model {model_name}")

        deployment_folder =f'mlops_{model_name}'
        function_name=f"{model_name}-{SERVICE_NAME}-{ENV}"
        
        model_code_folder = get_top_folder(model_file)

        logging.info("Create deployment folder and move required files/folders")
        os.mkdir(deployment_folder)
        to_deployment_folder = partial(to_folder, folder_path=deployment_folder)
        logging.debug("model code => deployment folder")
        to_deployment_folder(model_code_folder)
        logging.debug("handler => deployment folder")
        to_deployment_folder(f'akerbp.mlops.{SERVICE_NAME}.handler')
        logging.debug("project config => deployment folder")
        to_deployment_folder('mlops_settings.py')
        if deployment_platform == 'gc':
            logging.debug("Dockerfile => deployment folder")
            to_deployment_folder("akerbp.mlops.gc.Dockerfile")
        if (
            ENV=='dev' and 
            SERVICE_NAME == 'prediction' and 
            os.path.isdir(model_artifact_folder)
        ):
            logging.info("artifact folder => deployment folder")
            to_deployment_folder(model_artifact_folder)

        logging.debug(f"cd {deployment_folder}")
        base_path = os.getcwd()
        os.chdir(deployment_folder)

        if SERVICE_NAME == 'prediction':
            if not os.path.isdir(model_artifact_folder):
                # This will always be executed in the test and prod env,
                # assuming artifact folder is not committed to repo
                logging.info("Download serialized model")
                os.mkdir(model_artifact_folder)
                model_id = download_model_version(
                    model_name, 
                    ENV, 
                    model_artifact_folder)
            elif ENV=='dev':
                logging.info(f"Use model artifacts in {model_artifact_folder=}")
                model_id=f'{model_name}/dev/1'
            else:
                raise Exception("Model artifact folder in Test or Prod")
        else:
            model_id = None

        logging.info("Write service settings file")
        model_import_path = to_import_path(model_file)
        test_import_path = to_import_path(model_test_file)

        mlops_settings=dict(
            model_name=model_name,
            model_artifact_folder=model_artifact_folder,
            model_import_path=model_import_path,
            model_code_folder=model_code_folder,
            env=ENV,
            model_id=model_id,
            test_import_path=test_import_path
        )
        # File name can't be mlops_settings.py, or there will be an importing
        # error when the service test is run (user settings <- model test <-
        # service test)
        with open('service_settings.py', 'w') as config:
            config.write(f'{mlops_settings=}')
        
        logging.info("Create CDF requirement file")
        shutil.move(model_req_file, 'requirements.txt')
        if ENV in ["dev", "test"]:
            pass
            #set_test_mlops_import('requirements.txt')
        if ENV != "dev":
            logging.info(f"Install python requirements from model {model_name}")
            subprocess.check_call(["pip", "install", "-r", 'requirements.txt'])

        # * Dependencies: (user settings <- model test). Either run before going
        #   to the dep. folder or copy project config to dep. folder. 
        # * It is important to run tests after downloading model artifacts, in
        #   case they're used to test prediction service.
        # * Tests need the model requirements installed!
        logging.info(f"Run model and service tests")
        if model_test_file:
            run_tests(model_test_file)
            run_tests('akerbp.mlops.tests', path_type='module')
        else:
            logging.warning("Model test file is missing! " \
                            "Didn't run tests")
        # Project settings file isn't needed anymore
        os.remove('mlops_settings.py')

        if ENV != "dev" or LOCAL_DEPLOYMENT:
            logging.info(f"Deploy {function_name} to {deployment_platform}")
            
            if deployment_platform == 'cdf':
                from akerbp.mlops.cdf.helpers import deploy_function
                from akerbp.mlops.cdf.helpers import test_function

            elif deployment_platform == 'gc': 
                from akerbp.mlops.gc.helpers import deploy_function
                from akerbp.mlops.gc.helpers import test_function
            else:
                message = f"Expected 'cdf' or 'gc', got {deployment_platform=}"
                raise ValueError(message)
            
            logging.info("Deploy function")
            deploy_function(function_name, info=info[SERVICE_NAME])
            
            if test_import_path:
                logging.info("Test call")
                ServiceTest=import_module(test_import_path).ServiceTest  
                input = getattr(ServiceTest(), f"{SERVICE_NAME}_input")
                test_function(function_name, input)
            else:
                logging.warning("No test file was set up. " \
                                 "End-to-end test skipped!")
        
        logging.debug(f"cd ..")
        os.chdir(base_path)
        logging.debug(f"Delete deployment folder")
        shutil.rmtree(deployment_folder)


if __name__ == '__main__':
    set_up_cdf_client(context='deploy')
    model_settings = read_config()
    deploy(model_settings)