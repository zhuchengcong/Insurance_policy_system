from django.db import models

# Create your models here.
'''
模型字段类型：
models.CharField() # 字符串类型
models.TextField() # 文本类型
models.IntegerField() # int类型
models.BooleanField() # bool类型
models.NullBooleanField() # 允许为空的bool类型
models.DateField() # 日期类型 年月日
models.DecimalField() # 金额类型 可以指定长度和小数位数 max_digits=15, decimal_places=2, 总长度15位，小数位为2
models.EmailField() # 邮箱类型
models.FloatField() # 浮点数类型
models.TimeField() # 时间类型
'''

# channel_type_name = models.CharField(max_length=255, verbose_name='种类名', blank=True, null=True)
# 解释：channel_type_name 数据库字段名, max_length 最大长度, verbose_name 对应字段中文民, blank=True 允许键为空，指定的字段可以不传, null=True 允许值为空

# class Meta:
#        db_table = 'channel_rate_one'
#        verbose_name = '渠道费率表1'
#        verbose_name_plural = verbose_name

# 解释：db_table 对应数据库中的表名， verbose_name 对应数据库表中文名


# 渠道费率表1
from django.db import models
from soft_delete_new.models import SoftDeleteModel

from base.models import BaseModel


# 手续费表
class HandlingFee(SoftDeleteModel, BaseModel):
    jiaoqiang_insurance_fee = models.DecimalField(verbose_name='交强险手续费比例', max_digits=15, decimal_places=2,
                                                  blank=True, null=True)

    commercial_insurance_fee = models.DecimalField(verbose_name='商业险手续费', max_digits=15, decimal_places=2,
                                                   blank=True, null=True)

    maintenance_fee = models.DecimalField(verbose_name='维护费', max_digits=15, decimal_places=2,
                                          blank=True, null=True)
    customer_experience_fee = models.DecimalField(verbose_name='客户体验费', max_digits=15, decimal_places=2,
                                                  blank=True, null=True)

    insurance_tax = models.DecimalField(verbose_name='保单税费', max_digits=15, decimal_places=2,
                                        blank=True, null=True)

    handling_fee_tax = models.DecimalField(verbose_name='手续费税率', max_digits=15, decimal_places=2,
                                           blank=True, null=True)
    maintenance_fee_tax = models.DecimalField(verbose_name='维护费税率', max_digits=15, decimal_places=2,
                                              blank=True, null=True)

    customer_experience_fee_tax = models.DecimalField(verbose_name='客户体验费税率', max_digits=15, decimal_places=2,
                                                      blank=True, null=True)

    class Meta:
        db_table = 'handling_fee'
        verbose_name = '手续费'
        verbose_name_plural = verbose_name


class Settlements(SoftDeleteModel, BaseModel):
    # 实际结算手续费
    # 实际结算时，可能会选取部门同一渠道不同出单日期的保单，同时进行结算！
    # 实际结算时一个结算单可能对应多个保单  可勾选多个保单同时结算

    actual_settlement_fee = models.DecimalField(verbose_name='实际结算手续费', max_digits=15, decimal_places=2, blank=True,
                                                null=True)
    settlement_date = models.DateTimeField(verbose_name='结算日期', blank=True, null=True)

    settlement_method = models.CharField(max_length=255, verbose_name='结算方式', blank=True, null=True)

    note = models.CharField(max_length=255, verbose_name='备注', blank=True, null=True)

    receiving_account = models.CharField(max_length=255, verbose_name='收款账号', blank=True, null=True)

    class Meta:
        db_table = 'settlements'
        verbose_name = '结算表'
        verbose_name_plural = verbose_name
    # 后续字段暂定


# 打款明细表
class Remit(SoftDeleteModel, BaseModel):
    # 指向外键的数据删除时，不删除，但是此条已无意义
    settlement = models.ForeignKey(Settlements, on_delete=models.PROTECT, verbose_name='结算表id',
                                   blank=True, null=True)
    mode_of_payment = models.CharField(max_length=255, verbose_name='支付方式', blank=True, null=True)
    amount = models.CharField(max_length=255, verbose_name='支付金额', blank=True, null=True)
    acount = models.CharField(max_length=255, verbose_name='支付账户名', blank=True, null=True)
    acount_tail = models.CharField(max_length=255, verbose_name='支付账户尾号', blank=True, null=True)
    note = models.CharField(max_length=255, verbose_name='备注', blank=True, null=True)

    class Meta:
        db_table = 'remit'
        verbose_name = '打款明细'
        verbose_name_plural = verbose_name


# 费率字段表
class FeeField(BaseModel):
    name = models.CharField(max_length=255, verbose_name='费率字段名', blank=True, null=True)
    fee = models.DecimalField(verbose_name='费率', max_digits=15, decimal_places=2, blank=True,
                              null=True)

    class Meta:
        db_table = 'fee_field'
        verbose_name = '费率字段表'
        verbose_name_plural = verbose_name


# 渠道表
class ChannelRate(SoftDeleteModel, BaseModel):
    chanel = models.CharField(max_length=255, verbose_name='渠道', blank=True, null=True)

    class Meta:
        db_table = 'channel_rate'
        verbose_name = '渠道表'
        verbose_name_plural = verbose_name


# 渠道 生效时间 表
class ChannelEffectiveTime(SoftDeleteModel, BaseModel):
    chanel_id = models.ForeignKey(ChannelRate, on_delete=models.PROTECT, verbose_name='渠道id',
                                  blank=True,
                                  null=True)
    fee_field = models.ManyToManyField(FeeField, blank=True, null=True)
    time_start = models.DateField(verbose_name='生效时间', blank=True, null=True)
    time_end = models.DateField(verbose_name='效期终止时间', blank=True, null=True)


# 费用数据
# 交强险手续费比例	商业险手续费	                                                               有计算公式
# 维护费	客户体验费	保单税费	手续费税率	维护费税率	客户体验费税率	综合费用合计	公司结算净费	   暂无计算公式
# 客户类型（直接/代理）	实际支付商业手续费	实际支付交强手续费	客户实际支付保费	代理实际支付             暂无计算公式

# 保单表
class InsurancePolicy(SoftDeleteModel, BaseModel):
    note = models.CharField(max_length=255, verbose_name='备注', blank=True, null=True)
    nature_of_use = models.CharField(max_length=255, verbose_name='使用性质', blank=True, null=True)
    generation_date = models.DateTimeField(verbose_name='保单生成日期', blank=True, null=True)
    jiaoqiang_insure_no = models.CharField(max_length=255, verbose_name='交强投保单号', blank=True, null=True, )
    commercial_insure_no = models.CharField(max_length=255, verbose_name='商业投保单号', blank=True, null=True, )
    jiaoqiang_insurance_start_date = models.DateTimeField(max_length=255, verbose_name='交强起保日期', blank=True, null=True)
    jiaoqiang_insurance_end_date = models.DateTimeField(max_length=255, verbose_name='交强终止日期', blank=True, null=True)
    commercial_insurance_start_date = models.DateTimeField(max_length=255, verbose_name='商业险起保日期', blank=True,
                                                           null=True)
    commercial_insurance_end_date = models.DateTimeField(max_length=255, verbose_name='商业险终止日期', blank=True, null=True)
    commercial_insurance_no = models.CharField(max_length=255, verbose_name='商业险保单号', blank=True, null=True,
                                               )
    jiaoqiang_insurance_no = models.CharField(max_length=255, verbose_name='交强险保单号', blank=True, null=True, )
    applicant_certificate_number = models.CharField(max_length=255, verbose_name='投保人证件号码', blank=True, null=True)
    applicant = models.CharField(max_length=255, verbose_name='投保人', blank=True, null=True)
    insured = models.CharField(max_length=255, verbose_name='被保险人', blank=True, null=True)
    vehicel_owner = models.CharField(max_length=255, verbose_name='车主', blank=True, null=True)
    license_plate = models.CharField(max_length=255, verbose_name='车牌', blank=True, null=True)
    chassis_number = models.CharField(max_length=255, verbose_name='车架号', blank=True, null=True)
    engine_number = models.CharField(max_length=255, verbose_name='发动机号', blank=True, null=True)
    commercial_insurance_amount = models.DecimalField(verbose_name='商业险金额', max_digits=15, decimal_places=2, blank=True,
                                                      null=True)
    jiaoqiang_insurance_amount = models.DecimalField(verbose_name='交强险金额', max_digits=15, decimal_places=2, blank=True,
                                                     null=True)
    vehicel_and_vessel_tax = models.DecimalField(verbose_name='车船税', max_digits=15, decimal_places=2, blank=True,
                                                 null=True)
    total_premium = models.DecimalField(verbose_name='保费合计', max_digits=15, decimal_places=2, blank=True, null=True)
    salesman = models.CharField(max_length=255, verbose_name='业务员', blank=True, null=True)
    business_source = models.CharField(max_length=255, verbose_name='业务来源', blank=True, null=True)
    channel = models.CharField(max_length=255, verbose_name='渠道', blank=True, null=True)

    settlement_status = models.BooleanField(verbose_name='结算状态', blank=True, null=True, default=False)

    # 后续属性 暂定

    # 应结算手续费
    # 公式：”保单录入”商业险金额 ? "渠道管理"对应渠道、对应使用性质的商业险手续费率?”保单录入”交强险金额 ? "渠道管理"对应渠道、对应使用性质的交强险手续费率
    settlement_fee_payable = models.DecimalField(verbose_name='应结算手续费', max_digits=15, decimal_places=2, blank=True,
                                                 null=True)

    # 对应结算id   保单 对应 结算 关系  多对一
    settlements_id = models.ForeignKey(Settlements, on_delete=models.PROTECT, verbose_name='对应保单id', blank=True,
                                       null=True)

    # 对应渠道费率表1
    # 渠道费率id只能有一个，另一个为空，计算时提取不为空的渠道费率进行计算
    chanel_rate_id = models.ForeignKey(ChannelRate, on_delete=models.PROTECT, verbose_name='对应渠道id',
                                       blank=True,
                                       null=True)

    @property
    def total_premium_(self):
        # 保费合计 返回 商业险金额 + 交强险金额 + 车船税
        return self.commercial_insurance_amount + self.jiaoqiang_insurance_amount + self.vehicel_and_vessel_tax

    class Meta:
        db_table = 'insurance_policy'
        verbose_name = '保单表'
        verbose_name_plural = verbose_name


# 满足 三个字段就匹配对应渠道
class ChannelMatch(SoftDeleteModel, BaseModel):
    channel_name = models.CharField(max_length=255, verbose_name='渠道', blank=True, null=True)
    applicant = models.CharField(max_length=255, verbose_name='投保人', blank=True, null=True)
    insured = models.CharField(max_length=255, verbose_name='被保险人', blank=True, null=True)
    vehicel_owner = models.CharField(max_length=255, verbose_name='车主', blank=True, null=True)

    class Meta:
        db_table = 'channel_match'
        verbose_name = '渠道匹配表'
        verbose_name_plural = verbose_name
