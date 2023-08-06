# app.py
# Bash: install httpie, then:
#   http -v POST http://127.0.0.1:8000/train data='{"x": [1,-1],"y":[1,0]}'
# Python: challenging when posting nested json with requests. This works:
#   import requests, json
#   data = {"x":[1,-1], "y":[1,0]}
#   requests.post(model_api, json={'data': json.dumps(data)})
#   

from fastapi import FastAPI
from pydantic import Json, BaseModel

from akerbp.mlops.gc.helpers import access_secret_version
from akerbp.mlops.training.service import service
from akerbp.mlops.core import logger

logging=logger.get_logger()


secrets_string = access_secret_version('mlops-cdf-keys') 
secrets = eval(secrets_string)


app = FastAPI()

class Data(BaseModel):
    data: Json

@app.post(f'/train')
def api(input: Data):
    data = input.data
    logging.debug(f"{data=}")
    try:
        return service(data, secrets)
    except Exception as error:
      error_type = type(error).__name__
      error_message = f"Training service failed. {error_type}: {error}"
      logging.critical(error_message)
      return dict(status='error', error_message=error_message)
