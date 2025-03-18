from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user
from common.auth import aclient_required, ensure_for_current_user
from common.django_utils import arender, alogout
from .models import Subscription, PlanChoices
from django.core.exceptions import ObjectDoesNotExist
from writer.models import Article
from asgiref.sync import sync_to_async
from django.contrib.auth import update_session_auth_hash
from . import paypal as sub_manager
from .forms import UpdateUserForm
# Create your views here.

# async def dashboard(request: HttpRequest) -> HttpResponse:
#    return render(request, 'client/dashboard.html')

async_update_session_auth_hash = sync_to_async(update_session_auth_hash)

@aclient_required
async def dashboard(request: HttpRequest) -> HttpResponse:
    user = await aget_user(request)
    try:
        subscription = await Subscription.objects.aget(user=user, is_active=True)
        has_subscription = True
        subscription_name = (await subscription.aplan_choice()).name
        subscription_plan = 'premium' if await subscription.ais_premium() else 'standard'
    except ObjectDoesNotExist:
        has_subscription = False
        subscription_plan = 'none'
        subscription_name = 'No subscription yet'

    context = {
        'has_subscription': has_subscription,
        'subscription_plan': subscription_plan,
        'subscription_name': subscription_name
    }
    return await arender(request, 'client/dashboard.html', context)

@aclient_required
async def browse_articles(request: HttpRequest) -> HttpResponse:
    user = await aget_user(request)
    try:
        subscription = await Subscription.objects.aget(user = user, is_active = True)
        has_subscription = True
        subscription_plan = 'premium' if await subscription.ais_premium() else 'standard'
        if not await subscription.ais_premium():
            articles = Article.objects.filter(is_premium = False).select_related('user')
        else:
            articles = Article.objects.all().select_related('user')
    except ObjectDoesNotExist:
        has_subscription = False
        subscription_plan = 'none'
        articles = []

    context = {
        'has_subscription': has_subscription, 
        'articles': articles,
        'subscription_plan': subscription_plan,
    }
    return await arender(request, 'client/browse-articles.html', context)

@aclient_required
async def subscribe_plan(request: HttpRequest) -> HttpResponse:
    user = await aget_user(request)
    if await Subscription.afor_user(user):
        return redirect('client-dashboard')
    context = {'plan_choices': PlanChoices.objects.filter(is_active = True)}
    return await arender(request, 'client/subscribe-plan.html', context)


@aclient_required
async def update_user(request: HttpRequest) -> HttpResponse:
    user = await aget_user(request)
    
    # Inicializa o formulário para GET e só substitui para POST se necessário
    form = UpdateUserForm(instance=user)
    
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance = user)
        if await form.ais_valid():
            await form.asave()
            # Adiciona mensagem de sucesso usando a função auxiliar
            return redirect('update-client')
        else:
            # Adiciona mensagem de erro usando a função auxiliar
         
            form = UpdateUserForm(instance = user)
    try:
        subscription = await Subscription.objects.aget(user = user, is_active = True)
        has_subscription = True
        subscription_plan = 'premium' if await subscription.ais_premium() else 'standard'
        subscription_name = (await subscription.aplan_choice()).name
    except ObjectDoesNotExist:
        subscription = None
        has_subscription = False
        subscription_plan = 'none'
        subscription_name = 'No subscription yet'

    context = {
        'has_subscription': has_subscription,
        'subscription_plan': subscription_plan,
        'subscription_name': subscription_name,
        'subscription': subscription,
        'update_user_form': form,
    }
    return await arender(request, 'client/update-client.html', context)
 
@aclient_required
async def create_subscription(
    request: HttpRequest,
    sub_id: str,
    plan_code: str,
) -> HttpResponse:
    user = await aget_user(request)

    if await Subscription.afor_user(user):
        return redirect('client-dashboard')

    plan_choice = await PlanChoices.afrom_plan_code(plan_code)
    await Subscription.objects.acreate(
        plan_choice = plan_choice,
        cost = plan_choice.cost,
        external_subscription_id = sub_id,
        is_active = True,
        user = user,
    )

    return redirect('update-client')


@aclient_required
@ensure_for_current_user(Subscription, redirect_if_missing = 'client-dashboard')
async def cancel_subscription(request: HttpRequest, id: int) -> HttpResponse:
    subscription = id

    if request.method == 'POST':
        # Cancel the subscription in PayPal
        access_token = await sub_manager.get_access_token()
        sub_id = subscription.external_subscription_id
        await sub_manager.cancel_subscription(access_token, sub_id)

        # Update the subscription in the database
        await subscription.adelete()
        


        # Redirecionar para a página de atualização do usuário
        return redirect('update-client')

    context = {'subscription_plan': (await subscription.aplan_choice()).name}
    return await arender(request, 'client/cancel-subscription.html', context)