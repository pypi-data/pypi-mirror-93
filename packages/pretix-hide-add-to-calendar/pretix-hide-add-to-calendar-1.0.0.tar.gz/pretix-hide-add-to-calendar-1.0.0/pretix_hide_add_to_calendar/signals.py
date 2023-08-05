from django.dispatch import receiver
from django.template.loader import get_template
from pretix.presale.signals import html_head


@receiver(html_head, dispatch_uid="hide_add_to_calendar_html_head")
def html_head_presale(sender, request=None, **kwargs):
    template = get_template("pretix_hide_add_to_calendar/presale_head.html")
    ctx = {}
    return template.render(ctx)
