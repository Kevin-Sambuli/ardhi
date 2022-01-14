# Generated by Django 3.2.3 on 2021-11-20 10:25

from django.db import migrations


def create_groups(apps, schema_migration):
    # User = apps.get_model('accounts', 'Account')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    view_landowner = Permission.objects.get(codename='view_landowner')
    add_account = Permission.objects.get(codename='add_account')
    view_account = Permission.objects.get(codename='view_account')
    change_account = Permission.objects.get(codename='change_account')
    process_surveys = Permission.objects.get(codename='can_process_survey')

    agent_surveyors = Permission.objects.get(codename='agent_surveyors')
    agent_landowners = Permission.objects.get(codename='agent_landowners')

    # creating land owners group and its permissions
    land_group, created = Group.objects.get_or_create(name='landowners')

    land_perms = [
        add_account,
        view_account,
        change_account,
        view_landowner,
    ]

    land_group.permissions.set(land_perms)

    # creating surveyors group and its permissions
    surveyors_perms = [
        add_account,
        view_account,
        change_account,
        process_surveys,
    ]

    survey_group, created = Group.objects.get_or_create(name='surveyors')
    survey_group.permissions.set(surveyors_perms)

    agents_perms = [
        add_account,
        view_account,
        change_account,
        view_landowner,
        process_surveys,
        agent_landowners,
        agent_surveyors,
    ]

    # creating agents group and its permissions
    agents_group, created = Group.objects.get_or_create(name='agents')
    agents_group.permissions.set(agents_perms)

    managers, created = Group.objects.get_or_create(name='managers')
    manager_perms = Permission.objects.filter(codename__contains='manage')
    managers.permissions.set(manager_perms)
    managers.permissions.set(agents_perms)


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
