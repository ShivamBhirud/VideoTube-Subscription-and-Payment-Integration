from . import views
from django.urls import path, include
from subscriptions.views import (
    PlanView, HomeView, SubscriptionsView, PaymentView)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('plans', PlanView.as_view(), name='plans'), 
    path('update_plan/<int:id>', PlanView.as_view(), name='update_plan'),
    path('subscribed', SubscriptionsView.as_view(), name='subscribed'),
    path('checkout/<int:charges>/<int:id>/', PaymentView.as_view(), name='checkout'),
]