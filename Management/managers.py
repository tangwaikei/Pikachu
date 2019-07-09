from django.db import models


class ParametersManager(models.Manager):
    def get_objects(self, parameter_id):  # 根据parameter得到一条数据
        return self.get(user_type_id=parameter_id)