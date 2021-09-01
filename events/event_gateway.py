from core.utils.database import model_as_dict


def create_event(**attributes):
    from events.models import Event

    created_event = Event.objects.create(**attributes)
    return model_as_dict(created_event)
