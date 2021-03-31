from engine.application import Application


def update_scroll_value(elem, scroll_value):
    app = Application.instance()

    label = app.get_ui_element('Label')
    elem.scroll_value = min(50, scroll_value)
    label.text = str(scroll_value)
    label.enabled = bool(scroll_value % 2)
    label.ysize = 5 + min(50, scroll_value)
    label.layer = scroll_value

    panel = app.get_ui_element('Panel')
    panel.layer = -scroll_value

    window = app.get_ui_element('Window')
    window.layer = scroll_value
    window.xposition = 50 + scroll_value
