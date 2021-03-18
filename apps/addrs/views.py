from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.addrs.models import addrs
from django.http import JsonResponse
from django.core.cache import cache
class Areas(View):
    def get(self,request):
        #先查询缓存数据
        province_list = cache.get('province')
        if province_list is None:
            provinces = addrs.objects.filter(parent=None)
            #查询出来的数据集是queryset,需要返回json数据，所以要queryset数据转为json数据
            province_list = []
            for province in provinces:
                province_list.append({
                    'id':province.id,
                    'name':province.name
                })
            #保存缓存数据
            cache.set('province',province_list,24*3600)
        return JsonResponse({'code':0,'errmsg':'OK','province_list':province_list})

class SubAreas(View):
    def get(self,reuqest,city_id):
        city_list = cache.get('city_%s'%city_id)
        if city_list is None:
            # cities = addrs.objects.filter(parent=city_id)
            province = addrs.objects.get(id=city_id)
            cities = province.subs.all()
            city_list = []
            for city in cities:
                city_list.append({
                    'id': city.id,
                    'name': city.name
                })
            cache.set('city_%s'%city_id, city_list, 24 * 3600)
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'sub_data': {'subs':city_list}})