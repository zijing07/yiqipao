from django.db import models
from django.contrib import admin

class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    run_length = models.FloatField(default=0)
    is_admin = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class RunLog(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    distance = models.FloatField(null=False)
    picture = models.FileField(upload_to="upload_pictures")
    witness = models.CharField(max_length=200)
    info = models.CharField(max_length=1024)

    ACCEPT, REJECT, PENDING = 'accept', 'reject', 'pending'
    ITEM_STATUS = (
        (ACCEPT, "accept"),
        (REJECT, "reject"),
        (PENDING, "pending"))
    status = models.CharField(max_length=10,
                              choices=ITEM_STATUS,
                              default=PENDING)

    def __unicode__(self):
        return ('runlog from %s' % self.user.name)

class Notification(models.Model):
    run_log = models.ForeignKey(RunLog)
    has_seen = models.BooleanField(default=False)

    def __unicode__(self):
        return ('notification to runlog %d' % self.run_log.id)

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'run_length', 'is_admin')

class RunLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'distance', 'picture', 'witness', 'info', 'status')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('run_log', 'has_seen')
