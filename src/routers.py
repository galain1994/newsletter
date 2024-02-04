

import logging
from typing import Optional
from fastapi import APIRouter, Request
from .operations import subscription_ops
from .schemas.subscription import SubscriptionBase as SubscriptionBaseSchema, \
    UnsubscribeSchema, RespSubSchema, RespMultiSubSchema, RespUnsubSchema


sub_router = APIRouter(
    prefix="/api/v1",
)


@sub_router.get(
    "/subscriptions", 
    response_model=RespMultiSubSchema
)
async def get_subscriptions(
        request: Request,
        user_identifier: Optional[str] = None, email: Optional[str] = None, mobile: Optional[str] = None
    ):
    """Get by subscriptions by user_identifier, mobile or email

    :param request: HttpRequest
    :type request: Request
    :param user_identifier: search subscription by user_identifier
    :type user_identifier: Optional[str]
    :param email: search subscription by email
    :type email: Optional[str]
    :param mobile: search subscription by mobile
    :type mobile: Optional[str]
    """
    records = subscription_ops.search_subscription(request.state.db_session, user_identifier, email, mobile)
    return {'data': records, 'msg': 'success', 'err_code': '0'}


# Action

@sub_router.post(
    "/subscribe",
    response_model=RespSubSchema
)
async def subscribe(request: Request, subscription: SubscriptionBaseSchema):
    """Create or update subscription"""
    # if already subscribe in specified type then update the exists
    # else create new subscription
    logging.info(f"[ModifySubscription] {subscription}")
    subscription.is_active = True
    subscription_obj = subscription_ops.create_or_update_subscription(
        request.state.db_session, subscription
    )
    return {
        'data': subscription_obj,
        'msg': 'success',
        'err_code': '0'
    }


@sub_router.post(
    "/unsubscribe",
    response_model=RespUnsubSchema
)
async def unsubscribe(
        request: Request,
        body: UnsubscribeSchema,
    ):
    """Unsubscribe newsletter"""
    logging.info(f"[UnsubscribeSubscription] {body}")
    
    subscriptions = subscription_ops.search_subscription(
        request.state.db_session, body.user_identifier, body.email, body.mobile
    )
    if not subscriptions:
        return {'data': [], 'msg': "No subscriptions", "err_code": '404'}
    subscription_ops.unsubscribe(request.state.db_session, subscriptions)
    return {'data': [sub.id for sub in subscriptions], 'msg': 'success', 'err_code': '0'}


# RESTful

# @sub_router.post(
#     '/subscriptions/{subscription_id}'
# )
# async def update_subscription(subscription_id: int):
#     pass


# @sub_router.put(
#     '/subscription'
# )
# async def add_subscription():
#     pass


# Create send task
# support both sync and async method, async could use Celery

# @sub_router.post(
#     '/task'
# )
# async def modify_task(request: Request, body):
#     """Create or update task"""
#     pass
