import datetime
from rest_framework import serializers
from atomichabits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Habit
        fields = (
            'id', 'user', 'place', 'time', 'action',
            'is_pleasurable', 'linked_habit', 'frequency',
            'reward', 'execution_time', 'is_public'
        )
        read_only_fields = ('id',)

    def validate(self, data):
        linked_habit = data.get('linked_habit')
        reward = data.get('reward')
        execution_time = data.get('execution_time')
        is_pleasurable = data.get('is_pleasurable')
        frequency = data.get('frequency')

        if linked_habit and reward:
            raise serializers.ValidationError(
                "Связанную привычку и награду указать нельзя"
            )

        if execution_time is not None and \
           execution_time > datetime.time(hour=0, minute=2):
            raise serializers.ValidationError(
                "Время выполнения не может быть больше 120 секунд"
            )

        if linked_habit and not linked_habit.is_pleasurable:
            raise serializers.ValidationError(
                "Только приятные привычки можно добавить в связанные"
            )

        if is_pleasurable and (reward or linked_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть награды/привычки"
            )

        if frequency is not None and frequency < 7:
            raise serializers.ValidationError(
                "Периодичность не может быть меньше 7 дней"
            )

        return data
