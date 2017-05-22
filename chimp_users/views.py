# django import 

from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View, generic

#local import 

from . forms import SignUpForm, SignInForm, EditUserProfileForm, ChangePasswordForm
from .models import UserProfile
from campaign.models import UserCampaign
from campaign import urls



class SignUpView(generic.FormView):
	""" 
	User registration View 
	"""
	success_url = reverse_lazy('campaign:dashboard')
	form_class = SignUpForm
	template_name = 'chimp_users/sign_up.html'
	
	def get(self, *args, **kwargs):
		"""
		check if user already logged in redirect to dashboard
		"""

		if self.request.user.is_authenticated():
			return redirect('campaign:dashboard')

		return super(SignUpView, self).get(*args, **kwargs)

	def form_valid(self,form):
		"""
		split first_name and last_name form name and save in user and objects
		"""

		username = form.cleaned_data.get('username')
		name = form.cleaned_data.get('name')
		password = form.cleaned_data.get('password')
		business_name = form.cleaned_data.get('business_name')
		email = form.cleaned_data.get('email_id')
		package = form.cleaned_data.get('package')
		first_name = name.split()[0]
		last_name = ''

		try:
			last_name=name.split()[1]
		except:
			pass

		user = User(username = username, first_name = first_name, last_name = last_name, email = email)
		user.set_password(password)
		user.save()
		userprofile = UserProfile(user = user, business_name = business_name, package = package , email = email)
		userprofile.save()
		messages.success(self.request, 'User Register Successfully')
		return redirect(self.success_url)
		#return HttpResponseRedirect("user register successfully")


class SignInView(generic.FormView):
	"""
	user sign-up view
	"""
	template_name='chimp_users/sign_in.html'
	form_class=SignInForm
	success_url=reverse_lazy('campaign:dashboard')

	def get(self, *args, **kwargs):
		"""
		check if user is already loggedin then redirect to dashboard
		"""

		if self.request.user.is_authenticated():
			return redirect('campaign:dashboard')
		return super(SignInView, self).get(*args, **kwargs)

	def form_valid(self,form):
		"""
		check if username and password is valid then login the user
		"""
		username =form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		user=authenticate(username=username,password=password)
		
		# if user is authenticate then login the user		
		if user.is_active:
			login(self.request, user)
			return redirect('campaign:dashboard')


class LogoutView(LoginRequiredMixin, generic.View):
	"""
	User logout View
	"""

	def get(self,request):
		"""
		logout the request
		"""
		logout(request)
		
		return redirect('chimp_users:sign_in')


class EditUserProfileView(LoginRequiredMixin, generic.FormView):
	"""
	Edit User Profile View
	"""		
	
	template_name='chimp_users/edit_user_profile.html'
	form_class=EditUserProfileForm
	success_url=reverse_lazy('campaign:dashboard')
	
	def get(self, *args, **kwargs):
		u = User.objects.get(pk=kwargs['pk'])
		if u.id != self.request.user.id:
			messages.success(self.request, 'The Profile you are trying to reach is not authenticated')
			return redirect('campaign:dashboard')
		return super(EditUserProfileView, self).get(*args, **kwargs)
	
	def get_initial(self):
		"""
		get initail data of object
		"""
		initial={"username":self.request.user.username, "name":self.request.user.get_full_name(), "email_id":self.request.user.email, "business_name":UserProfile.objects.get(user=self.request.user).business_name}
		
		return initial.copy()
	
	def form_valid(self,form):
		"""
		edit UserProfile object
		"""

		name =form.cleaned_data.get('name')
		business_name =form.cleaned_data.get('business_name')
		email_id = form.cleaned_data.get('email_id')
		first_name=name.split()[0]
		last_name = ''
	
		try:
			last_name=name.split()[1]
		except:
			pass
		u = UserProfile.objects.get(user=self.request.user)
		u.business_name=business_name

		u.save()

		self.request.user.first_name = first_name
		self.request.user.last_name = last_name
		self.request.user.email= email_id
		self.request.user.save()
		messages.success(self.request,'User Profile Edited successfully')
		
		return super(EditUserProfileView, self).form_valid(form)

	def get_form_kwargs(self):
		"""
		pass request to EditUserProfileForm
		"""
		kwargs = super(EditUserProfileView, self).get_form_kwargs()
		kwargs['request'] = self.request
		
		return kwargs



class ChangePasswordView(LoginRequiredMixin, generic.FormView):
	"""
	Change password view
	"""
	form_class = ChangePasswordForm
	template_name='chimp_users/change.html'
	success_url = reverse_lazy('campaign:dashboard')
	success_message = 'password changed successfully'
	
	def form_valid(self,form):
		"""
		check if old password if valid then change the password
		"""
		
		old_password=form.cleaned_data.get('old_password')
		new_password=form.cleaned_data.get('new_password')
		
		if self.request.user.check_password(old_password):
			self.request.user.set_password(new_password)
			self.request.user.save()
		# else:
		# 	print('Invalid password')

		return super(ChangePasswordView, self).form_valid(form)

	def get_form_kwargs(self):
		"""
		pass request to EditUserProfileForm
		"""
		kwargs = super(ChangePasswordView, self).get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs


class UserProfileView(LoginRequiredMixin, generic.ListView):
	template_name ='chimp_users/user_profile.html'

	def get_queryset(self):
		"""
		send object of UserProfile of authenticated user
		"""
		return UserProfile.objects.filter(user=self.request.user)
