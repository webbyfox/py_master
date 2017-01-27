# -*- coding: utf-8 -*-
from rest_framework import serializers


class ShipSerializer(serializers.Serializer):

    name = serializers.CharField(required=True)
    imo_number = serializers.CharField(required=True)
    user_id = serializers.CharField(write_only=True, required=True)
    status = serializers.CharField(required=False, read_only=True)
    notes = serializers.CharField(required=False)

    def create(self, validated_data):
        return Ship(**validated_data)

    def update(self, instance, validate_data):
        instance.name = validated_data.get('name', instance.name)
        instance.imo_number = validated_data.get('imo_number', instance.imo_number)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.status = validated_data.get('status', instance.status)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        return instance
