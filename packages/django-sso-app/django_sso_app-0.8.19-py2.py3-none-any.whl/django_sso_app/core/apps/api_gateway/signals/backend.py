import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.db.models.signals import pre_delete, pre_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from allauth.account.adapter import get_adapter

from ....permissions import is_django_staff
from ...devices.models import Device
from ...groups.models import Group
from ...profiles.models import Profile
from ...profiles.utils import get_or_create_user_profile
from ..utils import delete_apigw_consumer, create_apigw_consumer_jwt, delete_apigw_consumer_jwt, \
                    create_apigw_consumer_acl, delete_apigw_consumer_acl, get_profile_apigw_consumer_id, \
                    get_apigw_consumer_acls

logger = logging.getLogger('django_sso_app.core.apps.api_gateway')

User = get_user_model()
adapter = get_adapter()


# device

@receiver(pre_save, sender=Device)
def create_device_apigw_jwt(sender, instance, **kwargs):
    device = instance
    profile = device.profile
    user = profile.user

    if not is_django_staff(user):
        logger.info('Profile "{}" has apigw_consumer_id "{}"'.format(profile, profile.apigw_consumer_id))

        apigateway_consumer_id = get_profile_apigw_consumer_id(profile)
        logger.info('apigateway_consumer_id "{}" on device create'.format(apigateway_consumer_id))

        if instance._state.adding:
            logger.info('Creating apigw JWT for Device "{}"'.format(device))

            status_code, r1 = create_apigw_consumer_jwt(profile)
            if status_code != 201:
                # delete_apigw_consumer(username)
                logger.error(
                    'Error ({}) creating apigw consumer JWT, "{}"'.format(
                        status_code, r1))
                raise Exception(
                    'Error ({}) creating apigw consumer jwt'.format(status_code))

            device.apigw_jwt_id = r1.get('id')
            device.apigw_jwt_key = r1.get('key')
            device.apigw_jwt_secret = r1.get('secret')


@receiver(pre_delete, sender=Device)
def delete_device_api_jwt(sender, instance, **kwargs):
    device = instance
    logger.info('Deleting apigw JWT for Device "{}", jwt_id: "{}"'.format(device, device.apigw_jwt_id))

    status_code, r1 = delete_apigw_consumer_jwt(device.profile, device.apigw_jwt_id)
    logger.info('Kong JWT deleted ({0}), {1}'.format(status_code, r1))
    if status_code >= 300:
        if status_code != 404:
            # delete_apigw_consumer(username)
            logger.error('Error ({}) Deleting apigw JWT for Device "{}", "{}"'.format(status_code, device, r1))

            raise Exception(
                "Error deleting apigw consumer jwt, {}".format(status_code))


# profile

@receiver(pre_delete, sender=Profile)
def delete_apigw_profile_consumer(sender, instance, **kwargs):
    profile = instance
    user = profile.user

    if not is_django_staff(user):
        logger.info('Profile "{}" will be deleted, removing api gateway consumer'.format(profile))

        status_code, r1 = delete_apigw_consumer(profile)
        logger.info('Api gateway consumer deletion: ({0}), {1}'.format(status_code, r1))

        if status_code >= 300:
            if status_code != 404:
                # delete_apigw_consumer(username)
                logger.error(
                    'Error ({0}) Deleting apigw consumer for User {1}, {2}'.format(
                        status_code, profile, r1))
                raise Exception(
                    "Error deleting apigw consumer, {}".format(status_code))


# group

@receiver(m2m_changed, sender=Profile.groups.through)
def api_gateway_signal_handler_when_profile_is_added_to_or_removed_from_group(action, instance, pk_set, **kwargs):

    profile = instance
    user = profile.user

    if not is_django_staff(user):
        is_loaddata = getattr(user, '__dssoa__loaddata', False)

        if action == 'pre_add':

            # do not create acl groups for signing up users
            if user.last_login is None:
                logger.info('do not create acl groups while user never logged in')
                return

            for pk in pk_set:
                group = Group.objects.get(id=pk)

                logger.info('creating api gateway acl group "{}" for profile "{}"'.format(group, profile))

                status_code, resp = create_apigw_consumer_acl(profile, group.name)

                if status_code < 400:
                    logger.info('api gateway acl group created {}, {}'.format(status_code, resp))

                    if not is_loaddata:
                        profile.update_rev(True)
                else:
                    logger.exception('error ({}) creating api gateway acl group'.format(status_code))

        elif action == 'pre_remove':
            for pk in pk_set:
                group = Group.objects.get(id=pk)
                logger.info('deleting apigw acl group "{}" for "{}"'.format(group, profile))

                status_code, resp = delete_apigw_consumer_acl(profile, group.name)

                if status_code < 400:
                    logger.info('"{}" DELETED, updating profile sso_rev'.format(group))

                    if not is_loaddata:
                        profile.update_rev(True)
                else:
                    logger.exception('error ({}) deleting api gateway acl group'.format(status_code))


@receiver(user_logged_in)
def post_user_login(**kwargs):
    user = kwargs['user']

    if not is_django_staff(user):
        profile = get_or_create_user_profile(user, commit=True)
        apigateway_consumer_id = get_profile_apigw_consumer_id(profile)

        logger.info('apigateway_consumer_id on login "{}"'.format(apigateway_consumer_id))

        _status, apigateway_acl_response = get_apigw_consumer_acls(profile)
        actual_acl_groups = list(map(lambda x: x['group'], apigateway_acl_response['data']))

        for group in profile.groups.exclude(name__in=actual_acl_groups):
            # try create apigw consumer acls for logged in user

            status_code, resp = create_apigw_consumer_acl(profile, group.name)

            if status_code < 400:
                logger.info('apigateway acl group "{}" created on login'.format(group.name))

            else:
                logger.exception('apigateway acl group "{}" not created on login ({})'.format(group.name, status_code))
