
ENTITY_CONFIG = {
    'tags': {
        'className': 'Tag',
        'key': 'tag'
    }, 'triggers': {
        'className': 'Trigger',
        'key': 'trigger'
    }, 'variables': {
        'className': 'Variable',
        'key': 'variable'
    }, 'built_in_variables': {
        'className': 'BuiltInVariable',
        'key': 'builtInVariable'
    }, 'folders': {
        'className': 'Folder',
        'key': 'folder'
    }, 'templates': {
        'className': 'Template',
        'key': 'template',
        'importKey':"customTemplate"
    }

}

DEFAULT_BUILT_IN_VARIABLES = {
    "event" :{
        "name": "Event",
        "exportName":"EVENT",
    },
    "pageHostname":{
        "name": "Page Hostname",
        "exportName":"PAGE_HOSTNAME",
    },
    "pagePath":{
        "name": "Page Path",
        "exportName":"PAGE_PATH",
    },
    "pageUrl":{
        "name": "Page URL",
        "exportName":"PAGE_URL",
    },
    "clickUrl":{
        "name": "Click URL",
        "exportName":"CLICK_URL",
    },
    "clickClasses":{
        "name": "Click Classes",
        "exportName":"CLICK_CLASSES",
    },
    "clickId":{
        "name": "Click ID",
        "exportName":"CLICK_ID",
    },
}
