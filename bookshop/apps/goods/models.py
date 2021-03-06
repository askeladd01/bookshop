from django.db import models


# Create your models here.
class BaseModel(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    is_delete = models.BooleanField('是否删除', default=False)
    is_show = models.BooleanField('是否展示', default=False)

    class Meta:
        abstract = True


class GoodsCategory(BaseModel):
    """
    商品多级分类
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    # 设置目录树的级别
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="父类目级别",
                                        related_name="sub_cat", db_constraint=False)

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(BaseModel):
    """
    某一大类下的宣传商标
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.SET_NULL, related_name='brands', null=True, blank=True,
                                 db_constraint=False, verbose_name="商品类目")
    name = models.CharField(default="", max_length=30, verbose_name="品牌名", help_text="品牌名")
    desc = models.TextField(default="", max_length=200, verbose_name="品牌描述", help_text="品牌描述")
    image = models.ImageField(max_length=200, upload_to="brands/")

    class Meta:
        verbose_name = "宣传品牌"
        verbose_name_plural = verbose_name
        db_table = "goods_brand"

    def __str__(self):
        return self.name


class Goods(BaseModel):
    """
    商品
    """
    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号")
    name = models.CharField(max_length=100, verbose_name="商品名")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="商品销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    goods_brief = models.TextField(max_length=32, verbose_name="出版社")
    goods_desc = models.TextField(verbose_name="内容", default='')
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    # 首页中展示的商品封面图
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")

    category = models.ForeignKey(GoodsCategory, null=True, blank=True, on_delete=models.SET_NULL, db_constraint=False,
                                 verbose_name="商品类目")

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(BaseModel):
    """
    商品轮播
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品", related_name="images")
    image = models.ImageField(upload_to="goods/detail/", verbose_name="图片", null=True, blank=True)

    class Meta:
        verbose_name = '商品轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(BaseModel):
    """
    首页轮播
    """
    name = models.CharField(max_length=32, verbose_name='图片名字')
    image = models.ImageField(upload_to="banner", verbose_name="轮播图", null=True, blank=True)
    link = models.CharField(max_length=32, verbose_name='跳转连接')
    info = models.TextField(verbose_name='图片简介')
    index = models.IntegerField(default=0, verbose_name="轮播顺序")

    class Meta:
        verbose_name = '首页轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IndexAd(BaseModel):
    """
    首页类别标签右边展示的七个商品广告
    """
    category = models.ForeignKey(GoodsCategory, null=True, db_constraint=False, on_delete=models.SET_NULL,
                                 related_name='category', verbose_name="商品类目")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='goods')

    class Meta:
        verbose_name = '首页广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(BaseModel):
    """
    搜索栏下方热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")

    class Meta:
        verbose_name = '热搜排行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords
