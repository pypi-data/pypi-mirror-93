import logging

# import pyximport
# pyximport.install()

from ...functions import lists_differs

logger = logging.getLogger('django_sso_app.core.apps.groups')


def update_profile_groups(profile, actual_groups_list):
    previous_groups_list = list(profile.groups.order_by('name').values_list('name', flat=True))

    if lists_differs(previous_groups_list, actual_groups_list):
        logger.info('Must update profile groups for "{}"'.format(profile))

        # try to add profile to new groups
        for group_name in actual_groups_list:
            if group_name not in previous_groups_list:
                logger.info('Adding user profile to group {}'.format(group_name))
                profile.add_to_group(group_name)

        # try to remove profile from removed groups
        for group_name in previous_groups_list:
            if group_name not in actual_groups_list:
                logger.info('Removing user profile from group {}'.format(group_name))
                profile.remove_from_group(group_name)
