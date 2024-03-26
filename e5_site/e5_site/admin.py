from django.contrib import admin
from e5_app.models import *


class MyAdminSite(admin.AdminSite):
    def get_app_list(self, request, app_label=None):
        order = [News, Event,Vacancy, Partner, Visitor, Mailing, Employee, Work]
        app_list = admin.AdminSite.get_app_list(self, request)
        for app in app_list:
            if app.get('app_label') == 'e5_app':
                app["models"].sort(key=lambda x: order.index(x['model']) if x['model'] in order else len(order))

        return app_list
