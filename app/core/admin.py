from django.contrib import admin
from core.models import Concert,TargetInfo,QticketsSalesInfo
# Register your models here.

class ConcertAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'city', 'concert_date', 'status')
    list_display_links = ('id','name')
    search_fields = ('name', 'city', 'status')

class TargetInfoAdmin(admin.ModelAdmin):
    list_display = ('id','targetAccountID','targetCompanyID','cat')
    list_display_links = ('id',)
    search_fields = ('targetAccountID', 'targetCompanyID')

class QticketsSalesInfoAdmin(admin.ModelAdmin):
    list_display = ('id','qticketsConcertID','qticketsAccountName','cat')
    list_display_links = ('id','qticketsConcertID')
    search_fields = ('qticketsConcertID','qticketsAccountName')


admin.site.register(Concert, ConcertAdmin)
admin.site.register(TargetInfo, TargetInfoAdmin)
admin.site.register(QticketsSalesInfo, QticketsSalesInfoAdmin)