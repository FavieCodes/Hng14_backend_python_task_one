from django.db import models


class Profile(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=50)
    gender_probability = models.FloatField()
    sample_size = models.IntegerField()
    age = models.IntegerField()
    age_group = models.CharField(max_length=20)
    country_id = models.CharField(max_length=10)
    country_probability = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'profiles'

    def to_dict(self, full=True):
        if full:
            return {
                'id': self.id,
                'name': self.name,
                'gender': self.gender,
                'gender_probability': self.gender_probability,
                'sample_size': self.sample_size,
                'age': self.age,
                'age_group': self.age_group,
                'country_id': self.country_id,
                'country_probability': self.country_probability,
                'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            }
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'age_group': self.age_group,
            'country_id': self.country_id,
        }