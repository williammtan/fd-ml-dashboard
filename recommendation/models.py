from django.db import models

class TopicRecommendation(models.Model):
    user_id = models.IntegerField(blank=False, null=False)
    keyword = models.CharField(max_length=100)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'meaningful_topics'
