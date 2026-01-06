import pytest

from services.notification_service.app.rendering import TemplateRenderer
from services.notification_service.app.schemas import Channel, Notification


def build_notification(alert_type: str, **metadata: str) -> Notification:
    metadata.setdefault("service", "api")
    metadata["type"] = alert_type
    return Notification(
        title="System Alert",
        message="Service latency is above threshold",
        severity="critical",
        metadata=metadata,
    )


@pytest.mark.parametrize(
    "alert_type, channel, expected",
    [
        ("incident", Channel.email, "Incident critique"),
        ("maintenance", Channel.slack, "Maintenance planifiée"),
        ("recovery", Channel.sms, "RECOVERY"),
    ],
)
def test_template_renderer_for_each_type(alert_type, channel, expected):
    renderer = TemplateRenderer()
    notification = build_notification(alert_type, window="22:00-23:00", duration="5m")

    rendered = renderer.render(channel, notification)

    assert expected in rendered
    assert notification.title in rendered
    assert notification.message in rendered
