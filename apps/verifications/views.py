from django.shortcuts import HttpResponse
from django.http import JsonResponse

# Create your views here.
from django.views import View
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from random import randint
from libs.yuntongxun.sms import CCP
class ImageCode(View):
    def get(self,request,uuid):
        text,image = captcha.generate_captcha()
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_%s' % uuid, 300, text)
        return HttpResponse(image,content_type='image/jpeg')
"""
用容联云平台发送短信
平台有SDK包直接下载或者可以pip install ronglian_sms_sdk
前端：携带参数发送请求
后端：
验证用户输入的参数，验证图片验证码，生成短信验证码，保存短信验证码（后续点击注册验证使用），发送给前端短信验证码
响应：json格式
"""

class SMScode(View):
    def get(self,request,mobile):
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        if not all([image_code,uuid]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})

        redis_conn = get_redis_connection('code')
        redis_image_code = redis_conn.get('img_%s' % uuid)
        if redis_image_code is None:
            return JsonResponse({'code':400,'errmsg':'验证码已过期'})
        if redis_image_code.decode().lower() != image_code.lower() :
            return JsonResponse({'code':400,'errmsg':'验证码错误'})
        #提取保存60s的短信验证码
        send_log = redis_conn.get('send_lod%s'%mobile)
        if send_log != None:
            return JsonResponse({'code': 400, 'errmsg': '发送短信过于频繁'})

        sms_code = '%06d'% randint(0,999999)
        #保存短信验证码
        redis_conn.setex(mobile, 300, sms_code)
        #暂时保存短信验证码60
        redis_conn.setex('send_lod%s'%mobile,60,1)
        CCP().send_template_sms('15065095058',[sms_code,5],1)
        return JsonResponse({'code':0,'errmsg':'发送短信成功'})
