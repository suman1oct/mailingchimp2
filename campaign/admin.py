# django imports

from django.contrib import admin
from django import forms

#django imports

#local imports
from chimp_users.models import UserProfile
from .models import MailingList, Template, UserCampaign




class TemplateAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
    	self.request = kwargs.pop('request', None)
    	super(TemplateAdminForm, self).__init__(*args, **kwargs)
    
    def clean_file(self):
        file_type = self.request.FILES['file'].content_type
        if(file_type != 'text/html'):
            raise forms.ValidationError('Please upload . HTML file')
        return self.cleaned_data['file']
    
    def clean_template_name(self):
        if Template.objects.filter(template_name = self.cleaned_data.get('template_name')).exists():
            raise forms.ValidationError('This Template name already exists please try with another name')
        return self.cleaned_data['template_name']
    
    
    class Meta:
        model = Template
        fields = ['image','template_name','category','file']


class TemplateAdmin(admin.ModelAdmin):
    form = TemplateAdminForm
    list_display = ('image', 'template_name', 'file')
    search_fields = ('template_name',)
    list_filter=['template_name']

    def get_form(self, request, obj=None, **kwargs):

        AdminForm = super(TemplateAdmin, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return AdminFormWithRequest


class MailingListAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
    	self.request = kwargs.pop('request', None)
    	super(MailingListAdminForm, self).__init__(*args, **kwargs)
    
    def clean_file(self):
        file_type = self.request.FILES['file'].content_type
        mime_type_list = ['application/vnd.ms-excel','application/msexcel','application/x-msexcel','application/x-ms-excel','application/x-excel','application/x-dos_ms_excel','application/xls','application/x-xls','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','application/vnd.ms-excel.sheet.binary.macroEnabled.12','application/vnd.openxmlformats-officedocument.spreadsheetml.template',]
        if(file_type not in  mime_type_list):
            raise forms.ValidationError('Please upload .xlsx file')
        return self.cleaned_data['file']
    
    class Meta:
        model = MailingList
        #fields = '__all__' 
        fields = ['mail_list_name','user','file','added_date']


class MailingListAdmin(admin.ModelAdmin):
    form = MailingListAdminForm
    list_display = ('mail_list_name', 'user', 'file', 'added_date')
    search_fields = ('mail_list_name',)
    list_filter = ['mail_list_name']

    def get_form(self, request, obj = None, **kwargs):

        AdminForm = super(MailingListAdmin, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return AdminFormWithRequest


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('id','user', 'sent_email', 'remaining_email', 'business_name', 'package')
	search_fields = ('user__first_name','user__last_name')
	list_filter = ['user__first_name']


@admin.register(UserCampaign)
class CampaignAdmin(admin.ModelAdmin):
	list_display = ('id','campaign_name', 'user', 'created_date', 'mail_list', 'template')
	search_fields = ('user',)
	list_filter = ['user',]
	


admin.site.register(Template ,TemplateAdmin)
admin.site.register(MailingList , MailingListAdmin)


