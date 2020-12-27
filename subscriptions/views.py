from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import status
from subscriptions.serializers import SubscriptionSerializer
from rest_framework.views import APIView
from .models import Subscriptions
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db.models import Q
import stripe



stripe_pubkey = settings.STRIPE_PUBLIC_KEY
stripe_privkey = settings.STRIPE_PRIVATE_KEY
stripe.api_key = stripe_privkey


# Render Home Page and delete a user's expired plans
class HomeView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        # Delete the expired plans on user login
        user = User.objects.get(id=request.user.id)
        Subscriptions.objects.filter(
            Q(id=user.id, expiry_date__lte=timezone.datetime.now()) |
            Q(id=user.id, is_paid=False)).delete()
        return render(request, 'subscriptions/home.html')


# Serve POST request to store data in Subscription Model using DRF
class SubscriptionsView(APIView):
    serializer_class = SubscriptionSerializer

    @method_decorator(login_required(login_url='login'))
    def post(self, request, *args, **kwargs):
        subscription_data = request.data
        try:
            # DB entry for the plan choosen by user
            new_subscription = Subscriptions.objects.create(
            plan=subscription_data['plan'], logged_user=request.user
            )
            new_subscription.save()
            serializer = SubscriptionSerializer(new_subscription)
            if subscription_data['plan'] == '1':
                charges = 2000
            elif subscription_data['plan'] == '2':
                charges = 4000
            else:
                charges = 6000
            return render(request, 'subscriptions/pay.html',
            {'status':status.HTTP_201_CREATED,'data':serializer.data,
            'charges':charges, 'key': stripe_pubkey})
        except Exception as e:
            return render(request, 'subscriptions/pay.html',
            {'status':status.HTTP_400_BAD_REQUEST})


# Payment success and failure view
class PaymentView(View):
    def post(self, request, charges, id):
        customer = stripe.Customer.create(
            email = request.POST['stripeEmail'],
            source = request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer = customer.id,
            amount = charges,
            currency = 'USD',
            description = 'subscription payment to VideoTube'
        ) 
        if charge['status'] == 'succeeded':
            subscription = Subscriptions.objects.get(id=id)
            months = subscription.plan
            subscription.is_paid = True
            subscription.is_active = True
            subscription.expiry_date = timezone.datetime.now() + relativedelta(
                months=+months)
            subscription.save()
            return HttpResponseRedirect('/plans')
        else:
            error = str('Payment NOT done. Next time please check the' +
            'credentials carefully before submitting.')
            return render(request, 'subscriptions/home.html', {'msg':error})


# Manage subscription plan related views
class PlanView(View):
    # Show all active and paused plans
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        subscription = Subscriptions.objects.filter(
            logged_user=user.id, is_paid=True  
        )
        serializer = SubscriptionSerializer(subscription, many=True)
        print(serializer.data)
        return render(request, 'subscriptions/show_plans.html',
        {'data':serializer.data})
    
    # Pause or resume a plan
    def post(self, request, id):
        plan_status = request.POST['plan_status']
        # On Pause update DB
        if plan_status == 'pause':
            subscription = Subscriptions.objects.get(id=id)
            tz_info = subscription.expiry_date.tzinfo
            delta = subscription.expiry_date - timezone.datetime.now(tz_info)
            print(delta)
            print(delta.days)
            subscription.remaining_days = delta.days
            subscription.is_active = False
            subscription.is_paused = True
            subscription.expiry_date = None
            subscription.save()
            msg = str('Plan details updated successfully!')
        # On Activate update DB
        elif plan_status == 'activate':
            subscription = Subscriptions.objects.get(id=id)
            subscription.expiry_date = timezone.datetime.now() + relativedelta(
                days=+subscription.remaining_days+1)
            subscription.remaining_days = None
            subscription.is_active = True
            subscription.is_paused = False
            subscription.save()
            msg = str('Plan details updated successfully!')
        else:
            msg = str('Couldn\'t Update Plan Details!')
        
        return HttpResponseRedirect('/plans', 
        {'msg':msg})
            




        








