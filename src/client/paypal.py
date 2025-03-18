import httpx

from projetopython import settings



async def get_access_token() -> str:
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
        'Content-Type': 'application/json',
    }
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET_ID)
    data = {'grant_type': 'client_credentials'}

    async with httpx.AsyncClient() as client:
        resp_data = (await client.post(
            settings.PAYPAL_AUTH_URL,
            auth = auth,
            headers = headers,
            data = data,
        )).json()
        return resp_data['access_token']


async def cancel_subscription(
    access_token: str,
    subscription_id: str,
    reason = 'Not specified',
):
    bearer_token = f'Bearer {access_token}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
        'Accept': 'application/json',
    }
    url = f'{settings.PAYPAL_BILLING_SUBSCRIPTIONS_URL}/{subscription_id}/cancel'
    data = { 'reason': reason }
    async with httpx.AsyncClient() as client:
        resp = (await client.post(url, headers=headers))
        print(f'[+] {resp.status_code}')