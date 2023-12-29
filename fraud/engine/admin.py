from django.contrib import admin
from .models import Request, Blacklist, Whitelist, Condition, Rule , Action 


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'card_number', 'ip_address', 'email', 'phone', 'country', 'datetime', 'amount', 'currency', 'transaction_type', 'status', 'fraud_details')
    list_filter = ('status', 'transaction_type', 'currency')
    search_fields = ('card_number', 'ip_address', 'email', 'phone')

@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = ('type', 'value')

@admin.register(Whitelist)
class WhitelistAdmin(admin.ModelAdmin):
    list_display = ('type', 'value')

@admin.register(Condition)
class ConditionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'variable', 'operator', 'value', 'details')
    list_filter = ('type', 'variable', 'operator')

@admin.register(Rule)
class RulesAdmin(admin.ModelAdmin):
    list_display = ('id', 'priority', 'actions')
    list_filter = ('priority', 'actions')



admin.site.register(Action)