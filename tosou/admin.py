from django.contrib import admin
from .models import customer_voice_model,user_meta,qa_model,catalog_model,message_table_model,message_user_model,account_meta,code_model,c_v_model
# Register your models here.

admin.site.register(customer_voice_model)
admin.site.register(user_meta)
admin.site.register(qa_model)
admin.site.register(catalog_model)
admin.site.register(message_table_model)
admin.site.register(message_user_model)
admin.site.register(account_meta)
admin.site.register(code_model)
admin.site.register(c_v_model)
