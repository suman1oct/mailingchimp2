from django import forms
from django.contrib.auth.models import User
from . validation import validateEmail
from . choices import PACKAGE_CHOICES
from django.contrib.auth import authenticate


class SignUpForm(forms.Form):
	"""
	User SignUp form
	"""
	username = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'placeholder': 'Username'}))
	name = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'placeholder': 'Name'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Password'}))
	business_name = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'placeholder': 'Business'}))
	email_id = forms.CharField(widget = forms.EmailInput(attrs = {'placeholder': 'email id'}), validators = [validateEmail])
	package = forms.CharField(max_length = 10,label = 'Package',widget = forms.Select(choices = PACKAGE_CHOICES),)

	def clean_username(self):
		#check whether username already exist or not if exist raise username already exist error
		if User.objects.filter(username = self.cleaned_data['username']).exists():
			raise forms.ValidationError('Username already exist')
		return self.cleaned_data['username']

	def clean_email_id(self):
		#check whether email address already exist or not if exist raise email already register error
		email = self.cleaned_data.get('email_id')
		if email and User.objects.filter(email=email).exists():
			raise forms.ValidationError(u'Email address already registered.')
		return email
	
	def clean(self):
		name = self.cleaned_data.get('name')
		password = self.cleaned_data.get('password')
		business_name = self.cleaned_data.get('business_name')
		package = self.cleaned_data.get('package')
		return self.cleaned_data


class SignInForm(forms.Form):
	"""
	User SignIn form
	"""
	username = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'placeholder': 'Username'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Password'}))
	
	def clean(self):
		username = self.cleaned_data.get('username')
		password= self.cleaned_data.get('password')
		user=authenticate(username=username, password=password)
		if not user or not user.is_active:
			raise forms.ValidationError("Not a Valid Username Or Password")
		return self.cleaned_data

class EditUserProfileForm(forms.Form):	
	"""
	Edit User Profile Form
	"""
	name =forms.CharField(max_length=100, widget=forms.TextInput())
	business_name=forms.CharField(max_length=100, widget=forms.TextInput())
	email_id = forms.CharField(widget = forms.EmailInput(), validators = [validateEmail])

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditUserProfileForm, self).__init__(*args, **kwargs)

	def clean_username(self):
		#check whether username already exist if exist raise validation error
		if User.objects.filter(username=self.cleaned_data['username']).exists():
			raise forms.ValidationError('user already exist')
		return self.cleaned_data['username']

	def clean_email_id(self):
		#check whether email address already exist or not if exist raise email already register error
		email = self.cleaned_data.get('email_id')
		if email and User.objects.filter(email=email).exclude(email=self.request.user.email).exists():
			raise forms.ValidationError(u'Email address already register.')
		return email


class ChangePasswordForm(forms.Form):		
	"""
	Change Password Form
	"""
	old_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'old Password'}))
	new_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
	confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ChangePasswordForm, self).__init__(*args, **kwargs)


	def clean(self):
		old_password=self.cleaned_data.get('old_password')
		if not self.request.user.check_password(old_password):
			raise forms.ValidationError('invalid old password')
		new_password=self.cleaned_data.get('new_password')
		confirm_password=self.cleaned_data.get('confirm_password')
		if new_password and new_password!=confirm_password:
			raise forms.ValidationError('New password and Confirm password are not matched')
		return self.cleaned_data
