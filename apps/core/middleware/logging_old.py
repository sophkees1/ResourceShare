import datetime
from django.conf import settings
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from apps.core.logging import Logging



logging = Logging(str(settings.BASE_DIR / "logs" / "req_res_logs.txt"))


def simple_logging_middleware(get_response):
    def middleware(request):
        http_method = request.method
        url = request.get_full_path()
        host_port = request.get_host()
        content_type = request.headers["Content-Type"]
        user_agent = request.headers['User-Agent']
        
        msg = f"{http_method} | {host_port}{url} | {content_type} | {user_agent}"
        logging.info(msg)
        
        response = get_response(request)


        headers = response.headers
        status_code = response.status_code
        
        msg = f"{status_code} | {headers}"
        logging.info(msg)

        return response
    return middleware


class ViewExcutionTimeMiddleware():
    def __init__(self,get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        start_time = timezone.now()
        
        response = self.get_response(request)
        
        end_time = timezone.now()
        total_time = end_time - start_time
        
        http_method = request.method
        url = request.get_full_path()
        host_port = request.get_host()
        msg = f"EXECUTION TIME {total_time} >> {http_method} | {host_port}{url}"
        
        logging.info(msg)
        #set time limit after which the log should have the level warning or critical
        return response
    
class ViewExecutionTimeMiddleware2(MiddlewareMixin):
    def process_request(self,request):
        request.start_time = timezone.now()
        
    def process_response(self,request, response):
        total_time = timezone.now() - request.start_time
        http_method = request.method
        url = request.get_full_path()
        host_port = request.get_host()
        msg = f"EXECUTION TIME {total_time} >> {http_method} | {host_port}{url}"
        
        ok_time = datetime.timedelta(seconds = 0.05)         
        warning_time = datetime.timedelta(seconds = 1)
        
        if total_time < ok_time:
            logging.info(msg)
        elif total_time < warning_time:
            logging.warning(msg)
        else:
            logging.critical(msg)
        
        return response
    