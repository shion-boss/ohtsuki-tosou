from django.contrib import admin
from .models import customer_voice_model,user_meta,qa_model,catalog_model
# Register your models here.

admin.site.register(customer_voice_model)
admin.site.register(user_meta)
admin.site.register(qa_model)
admin.site.register(catalog_model)
