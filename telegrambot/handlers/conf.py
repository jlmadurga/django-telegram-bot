from django.conf.urls import url

def command(command, view):
    return url(r'^/%s(\s)*(?P<param>\w*)' % command, view)

def unknown_command(view):
    return url(r'^/(?P<unknown_command>\w+).*', view)

def regex(pattern, view):
    return url(pattern, view)

def message(view):
    return url(r'^(?P<message>.*)', view)