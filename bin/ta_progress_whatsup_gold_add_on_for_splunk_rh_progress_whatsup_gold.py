
import ta_progress_whatsup_gold_add_on_for_splunk_declare

from splunktaucclib.rest_handler.endpoint import (
    field,
    validator,
    RestModel,
    DataInputModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunk_aoblib.rest_migration import ConfigMigrationHandler

util.remove_http_proxy_env_vars()


fields = [
    field.RestField(
        'interval',
        required=True,
        encrypted=False,
        default=None,
        validator=validator.Pattern(
            regex=r"""^\-[1-9]\d*$|^\d*$""", 
        )
    ), 
    field.RestField(
        'index',
        required=True,
        encrypted=False,
        default='default',
        validator=validator.String(
            min_len=1, 
            max_len=80, 
        )
    ), 
    field.RestField(
        'device_reports',
        required=False,
        encrypted=False,
        default='cpu-utilization~ping-availability~state-change~disk-utilization~interface-utilization~memory-utilization',
        validator=None
    ), 
    field.RestField(
        'time_range',
        required=True,
        encrypted=False,
        default='today',
        validator=None
    ), 
    field.RestField(
        'range_n',
        required=True,
        encrypted=False,
        default='1',
        validator=None
    ), 
    field.RestField(
        'debug',
        required=False,
        encrypted=False,
        default=None,
        validator=None
    ), 

    field.RestField(
        'disabled',
        required=False,
        validator=None
    )

]
model = RestModel(fields, name=None)



endpoint = DataInputModel(
    'progress_whatsup_gold',
    model,
)


if __name__ == '__main__':
    admin_external.handle(
        endpoint,
        handler=ConfigMigrationHandler,
    )
