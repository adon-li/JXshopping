from django.shortcuts import render

# Create your views here.

# from fdfs_client.client import Fdfs_client

#修改配置文件，创建客户端
# client = Fdfs_client('D:/pycharm/JXshopping/venv/client.conf')
# #2上传文件
# client.upload_by_filename('D:\pycharm\JXshopping\JX-front_end\images\cat.jpg')
#3获取file_id,upload_by_filename上传成功会返回字典数据，该数据中包含file_id
#getting connection
# <fdfs_client.connection.Connection object at 0x0000019BEA3F2668>
# <fdfs_client.fdfs_protol.Tracker_header object at 0x0000019BEA3F2630>
# {'Group name': 'group1', 'Remote file_id': 'group1\\M00/00/00/wKgRC2BTewyARsiOAAAQ7colEzw637.jpg', 'Status': 'Upload successed.', 'Loc
# al file name': 'D:\\pycharm\\JXshopping\\JX-front_end\\images\\cat.jpg', 'Uploaded size': '4.00KB', 'Storage IP': '192.168.17.11'}
#打开链接就可以看到图片了  ehttp://192.168.17.11:8888/group1//M00/00/00/wKgRC2BTewyARsiOAAAQ7colEzw637.jpg

from django.views import View
from utils.goods import get_categories
from apps.contents.models import ContentCategory
class Index(View):
    def get(self,request):
        #首页数据-商品分类数据
        categories = get_categories()
        #首页数据-广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request, 'index.html', context)
"""
需求：根据点击的分类，获取分类数据，排序，分页
前端：发送一个get请求，分类id在URL中，分页的页码，每页数据，排序都在请求中。
后端：接受请求数据，查询数据，将对象返回响应（json）
"""
from apps.goods.models import GoodsCategory
from django.http import JsonResponse
from utils.goods import get_breadcrumb
from apps.goods.models import SKU
from  django.core.paginator import Paginator
class ListView(View):
    def get(self,request,category_id):
        #获取前端的请求中排序的字段，用于排序
        ordering = request.GET.get('ordering')
        # 获取前端的请求中每页多少数据，用于分页
        page_size = request.GET.get('page_size')
        # 获取前端的请求中指定页数据
        page = request.GET.get('page')

        try:
            # 获取三级菜单分类信息:
            category = GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '获取mysql数据出错'})
        #获取面包屑数据
        breadcrumb = get_breadcrumb(category)
        #获取对应分类的sku数据,排序
        SKUS = SKU.objects.filter(category=category,is_launched=True).order_by(ordering)
        #分页
        paginator = Paginator(SKUS,per_page=page_size)

        page_skus = paginator.page(page)
        sku_list = []
        for sku in page_skus.object_list:
            sku_list.append({
                'id':sku.id,
                'default_image_url':sku.default_image.url,
                'name':sku.name,
                'price':sku.price
            })
        #获取总页数
        total_page = paginator.num_pages
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'breadcrumb': breadcrumb,
            'list': sku_list,
            'count': total_page
        })

