

from fastapi import APIRouter, Request, Response
from .models.subscription import Subscription as SubscriptionModel
from .schemas.subscription import Subscription as SubscriptionSchema, SubscriptionCreate


sub_router = APIRouter(
    prefix="/api",
)


@sub_router.get(
    "/subscriptions", 
)
async def get_subscriptions():
    # Get by subscriptions by user_identifier, mobile or email
    pass


# RESTful

@sub_router.post(
    '/subscriptions/{subscription_id}'
)
async def update_subscription(subscription_id: int):
    pass


@sub_router.put(
    '/subscription'
)
async def add_subscription():
    pass


# Action

@sub_router.post(
    "/subscribe",
    response_model=SubscriptionSchema
)
async def subscribe(request: Request, subscription: SubscriptionCreate) -> SubscriptionSchema:
    """Create or update Subscription """
    print(subscription)
    subscription_obj = SubscriptionModel.create_or_update_subscription(
        request.state.db_session, subscription
    )
    return subscription_obj


@sub_router.post(
    "/unsubscribe"
)
async def unsubscribe():
    pass

