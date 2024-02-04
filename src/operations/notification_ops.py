

from ..models.common import SubTypeEnum


def send_email(email_address: str, content: str):
    """Send Email"""
    pass


def send_sns(mobile: str, content: str):
    """Send sns"""
    pass


def send_newsletter(sub_type: SubTypeEnum, sub_address: str, content: str):
    """Send newsletter based on subscription type"""
    if sub_type == SubTypeEnum.email:
        send_email(sub_address, content)
    elif sub_type == SubTypeEnum.sns:
        send_sns(sub_address, content)
    else:
        raise ValueError(f"Unsupportable subscription type: {sub_type}")
