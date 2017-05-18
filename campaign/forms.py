from django import forms
from . models import UserCampaign, MailingList
from django.contrib.auth.models import User


class CreateCampaignForm(forms.ModelForm):	
	"""
	create campaign form
	"""

	def __init__(self, *args, **kwargs):
		request = kwargs.pop("request")
		super(CreateCampaignForm, self).__init__(*args, **kwargs)
		self.fields["mail_list"].queryset = MailingList.objects.filter(user = request.user)

	class Meta:
		model = UserCampaign
		fields = ['campaign_name','mail_list','template']


class EditCampaignForm(forms.ModelForm):
	"""
	Edit campaign form
	"""

	def __init__(self, *args, **kwargs):
		request = kwargs.pop("request")
		super(EditCampaignForm, self).__init__(*args, **kwargs)
		# it will modify the only Mail_list field of form
		self.fields["mail_list"].queryset = MailingList.objects.filter(user = request.user)

	class Meta:
		model = UserCampaign
		fields = ['campaign_name','mail_list','template']


class MailingListForm(forms.ModelForm):
	"""
	Add mailing List Form
	"""
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(MailingListForm, self).__init__(*args, **kwargs)

	def clean_file(self):
		file_type = self.request.FILES['file'].content_type
		mime_type_list = ['application/vnd.ms-excel','application/msexcel','application/x-msexcel','application/x-ms-excel','application/x-excel','application/x-dos_ms_excel','application/xls','application/x-xls','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','application/vnd.ms-excel.sheet.binary.macroEnabled.12','application/vnd.openxmlformats-officedocument.spreadsheetml.template',]
		if(file_type not in  mime_type_list):
			raise forms.ValidationError('Please upload .xlsx file')
		return self.cleaned_data['file']

	def clean_mail_list_name(self):
		# Check whether user has not same mail_list_name already if has raise validation error 
		mail_list_name = self.cleaned_data.get('mail_list_name')
		u=User.objects.get(pk = self.request.user.pk)
		if mail_list_name and u.mailinglist_set.filter(mail_list_name = mail_list_name ).exists():
			raise forms.ValidationError(u'This mail list name already exists please try with another name')
		return mail_list_name
	class Meta:
		model = MailingList
		fields = ['mail_list_name','file',]

