from apminsight import constants
from apminsight.instrumentation.psycopg2_wrapper import Psycopg2Wrapper


module_info = {
    'psycopg2' : [
        {
            constants.method_str : 'connect',
            constants.component_str : constants.postgres_comp,
            constants.wrapper_str : Psycopg2Wrapper.instrument_conn,
            constants.default_host : constants.localhost,
            constants.default_port : '5432'
        }
    ]
}

