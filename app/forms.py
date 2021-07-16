from django import forms
from .models import Contact, UserProfile, Agent, Property, PropertyImages,Orders
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'phone',
            'subject',
            'message',


        ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
           'user_name',

        ]


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['website', 'bioInfo', 'mobile']


    def save(self, commit=True):
        profile = self.instance
        profile.website = self.cleaned_data['website']
        profile.bioInfo = self.cleaned_data['bioInfo']
        profile.mobile = self.cleaned_data['mobile']

        if commit:
            profile.save()
        return profile

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['username',
                  'agentId',
                  'phone',
                  'address',
                  'email',
                  'company',
                  'website',
                  'facebook',
                  'twitter',
                  'instagram',
                  'photo'
                  ]

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['type',
                  'status',
                  'no_of_beds',
                  'no_of_bathrooms',
                  'pets',
                  'parking_area',
                  'area',
                  'lot_size',
                  'property_id',
                  'title',
                  'price',
                  'price_per_area',
                  'community',
                  'description',
                  'city',
                  'state',
                  'location',
                  'photo',
                  'agent',
                  'latitude',
                  'longitude'

        ]


class PropertyImagesForm(forms.ModelForm):
    class Meta:
        model = PropertyImages
        fields = ['property',
                  'photo',]


class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['package_id','user_id','method']

class UpdateAgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['username',
                  'agentId',
                  'phone',
                  'address',
                  'email',
                  'company',
                  'website',
                  'facebook',
                  'twitter',
                  'instagram',
                  'photo'
                  ]


def save(self, commit=True):
    agent = self.instance
    agent.username = self.cleaned_data['username']
    agent.agentId = self.cleaned_data['agentId']
    agent.phone = self.cleaned_data['phone']
    agent.email = self.cleaned_data['email']
    agent.website = self.cleaned_data['wesbite']
    agent.facebook = self.cleaned_data['facebook']
    agent.twitter = self.cleaned_data['twitter']

    if self.cleaned_data['photo']:
        agent.photo = self.cleaned_data['photo']

    if commit:
        agent.save()
    return agent

