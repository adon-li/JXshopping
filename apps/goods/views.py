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