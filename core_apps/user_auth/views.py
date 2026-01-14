from django.http import JsonResponse
from django.views import View
from loguru import logger



class TestLoggingView(View):
    def get(self,request):
        logger.debug("This is a debug message from TestLoggingView")
        logger.info("This is an info message from TestLoggingView")
        logger.warning("This is a warning message from TestLoggingView")
        logger.error("This is an error message from TestLoggingView")
        logger.critical("This is a critical message from TestLoggingView")
        return JsonResponse({"message": "Logging test completed. Check the logs for messages."})
  
