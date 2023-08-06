# handler.py
import warnings
warnings.simplefilter("ignore")

from akerbp.mlops.prediction.service import service
from akerbp.mlops.utils import logger
from akerbp.mlops import __version__ as version

logging=logger.get_logger()

logging.debug(f"MLOps framework version {version}")

def handle(data, secrets):
   try:
      return service(data, secrets)
   except Exception as error:
      error_type = type(error).__name__
      error_message = f" Prediction service failed. {error_type}: {error}"
      logging.critical(error_message)
      return dict(status='error', error_message=error_message)
