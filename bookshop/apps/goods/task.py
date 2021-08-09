from celery_task.celery import app


@app.task
def banner_update():
    from goods.serializer import BannerSerializer
    from goods.models import Banner
    from django.core.cache import cache
    queryset_banner = Banner.objects.filter(is_delete=False, is_show=True).order_by('index')[:3]
    serializer_banner = BannerSerializer(instance=queryset_banner, many=True)
    for banner in serializer_banner.data:
        banner['image'] = 'http://127.0.0.1:8000' + banner['image']
    cache.set('banner_list', serializer_banner.data)
    return True
