# 新增权限菜单约束使用
from rest_framework import serializers

from insurance.models import InsurancePolicy, Settlements, HandlingFee, FeeField, ChannelRate, ChannelEffectiveTime, \
    Remit, ChannelMatch


# class ChannelRateOneSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChannelRateOne
#         fields = '__all__'


# class ChannelRateTwoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChannelRateTwo
#         fields = '__all__'

class ListChannelEffectiveTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelEffectiveTime
        fields = '__all__'
        depth = 1


class ChannelEffectiveTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelEffectiveTime
        fields = '__all__'


class ChannelRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelRate
        fields = '__all__'


class ManyChannelRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelRate
        fields = ['chanel', 'channeleffectivetime_set']
        depth = 2


class FeeFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeField
        fields = '__all__'


class ALlFeeFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeField
        fields = ['name', 'fee', 'channeleffectivetime_set', 'id']
        depth = 2


class InsurancePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePolicy
        fields = '__all__'


class ListInsurancePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePolicy
        fields = '__all__'
        depth = 1


class ManyListInsurancePolicySerializer(serializers.ModelSerializer):
    chanel_rate_id = ManyChannelRateSerializer(required=False)

    class Meta:
        model = InsurancePolicy
        fields = '__all__'
        depth = 3


class SettlementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlements
        fields = ['actual_settlement_fee', 'settlement_date', 'settlement_method', 'note', 'insurancepolicy_set',
                  'receiving_account']


class ListSettlementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlements
        fields = ['actual_settlement_fee', 'settlement_date', 'settlement_method', 'note', 'insurancepolicy_set',
                  'receiving_account', 'id']
        depth = 2


class RemitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remit
        fields = '__all__'


class HandlingFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandlingFee
        fields = '__all__'


class ChannelMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelMatch
        fields = '__all__'
