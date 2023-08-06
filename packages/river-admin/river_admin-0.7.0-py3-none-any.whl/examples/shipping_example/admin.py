from django.contrib import admin

import river_admin
from examples.shipping_example.models import Shipping


class ShippingRiverAdmin(river_admin.RiverAdmin):
    name = "Shipping Flow"
    icon = "mdi-truck"
    list_displays = ['pk', 'product', 'customer', 'shipping_status']


river_admin.site.register(Shipping, "shipping_status", ShippingRiverAdmin)


class ShippingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'customer', 'shipping_status',)
    readonly_fields = ('shipping_status',)


admin.site.register(Shipping, ShippingAdmin)
