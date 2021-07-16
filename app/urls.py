from django.urls import path
# current directory
from . import views
from django.conf.urls import url



urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'^signup/', views.signup, name = 'signup'),
    url(r'^validate_email', views.validate_email, name="vaildate_email"),
    url(r'^account-settings', views.account_settings, name="account-settings"),
    url(r'^listing-emails', views.listing_emails, name="listing-emails"),
    url(r'^change-password', views.change_password, name="change-password"),
    url(r'^logout/', views.logout, name = 'logout'),
    url(r'^agents/', views.agents, name = 'agents'),
    url(r'^aboutus/', views.aboutus, name = 'aboutus'),
    url(r'^contact/', views.contact, name = 'contact'),
    path(r'^<type>/properties/', views.properties, name="properties"),
    path(r'^<id>/property/', views.property, name="property"),
    url(r'^search-results/', views.search_results, name="search-results"),
    url(r'^package-list/', views.package_list, name="package-list"),
    url(r'^checkout/', views.checkout, name="checkout"),
    url(r'^orderCompleted/', views.orderCompleted, name="orderCompleted"),
    url(r'^success/', views.success, name="success"),
    url(r'^my-listing/', views.my_listing, name="my-listing"),
    url(r'^header-search/', views.header_search, name="header-search"),
    url(r'^add-property/', views.add_property, name="add-property"),
    url(r'^addAgent/admin/', views.addAgent, name="addAgent"),
    path(r'^<id>/updateAgent/admin/', views.updateAgent, name="updateAgent"),
    url(r'^allAgents/admin/', views.allAgents, name="allAgents"),
    url(r'^addProperty/admin/', views.addProperty, name="addProperty"),
    path(r'^<id>/individualProperty/', views.individualProperty, name="individualProperty"),
    path(r'^<id>/individualAgent/', views.individualAgent, name="individualAgent"),
    path(r'^<id>/deleteProperty/', views.deleteProperty, name="deleteProperty"),
    url(r'^allProperty/admin/', views.allProperty, name="allProperty"),
    url(r'^adminDashboard/', views.adminDashboard, name = 'adminDashboard'),
    url(r'^admin/', views.admin, name = 'admin'),
    url(r'^adminInbox/', views.adminInbox, name = 'adminInbox'),
    path(r'^<id>/deleteAgent/', views.deleteAgent, name = 'deleteAgent'),
    path(r'^<id>/deleteMessage/', views.deleteMessage, name = 'deleteMessage'),
    path(r'^<id>/message/', views.message, name = 'message'),
    url(r'^adminLogout/', views.adminLogout, name = 'adminLogout'),




]