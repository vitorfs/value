from .models import ApplicationSetting


def application_settings(request):
    settings = ApplicationSetting.get()
    return {
        'jira_is_enabled': settings.get(ApplicationSetting.JIRA_INTEGRATION_FLAG)
    }
