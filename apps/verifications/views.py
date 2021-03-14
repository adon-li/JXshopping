from django.shortcuts import HttpResponse

# Create your views here.
from django.views import View
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
class ImageCode(View):
    def get(self,request,uuid):
        text,image = captcha.generate_captcha()
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_%s' % uuid, 300, text)
        return HttpResponse(image,content_type='image/jpeg')
