# python imports

# django imports
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

# Third party imports

# Locals imports
from campaign.models import UserCampaign, MailingList, Template


class ValidCampaignMixin(object):
	"""
	View Mixin which validate and authenticate the user for campaign
	"""

	def dispatch(self, request, *args, **kwargs):
		if UserCampaign.objects.filter(pk=kwargs['pk']).exists():
			camp = UserCampaign.objects.get(pk=kwargs['pk'])
			if camp.user.id != self.request.user.id:
				messages.success(self.request, 'The campaign you are trying to reach does not authenticated')
				return redirect('campaign:show_campaign')
		else:
			messages.success(self.request, 'The campaign you are trying to reach does not exists' )
			return redirect('campaign:show_campaign')

		return super(ValidCampaignMixin, self).dispatch(request, *args, **kwargs)


class ValidMailingListMixin(object):
	"""
	View Mixin which validate and authenticate the user for campaign
	"""

	def dispatch(self, request, *args, **kwargs):
		if MailingList.objects.filter(pk=kwargs['pk']).exists():
			mlist = MailingList.objects.get(pk=kwargs['pk'])
			if mlist.user.id != self.request.user.id:
				messages.success(self.request, 'The MailingList you are trying to reach does not authenticated')
				return redirect('campaign:show_mailing_list')
		else:
			messages.success(self.request, 'The MailingList you are trying to reach does not exists' )
			return redirect('campaign:show_campaign')

		return super(ValidMailingListMixin, self).dispatch(request, *args, **kwargs)


