import psycopg2
import psycopg2.extensions

from apminsight import constants
from apminsight.agentfactory import get_agent
from apminsight.util import is_non_empty_string

from .wrapper import default_wrapper


class Psycopg2CursorWrapper(psycopg2.extensions.cursor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._apm_check_and_wrap('execute')
        self._apm_check_and_wrap('executemany')

    def _apm_extract_query(self, tracker, args=(), kwargs={}, return_value=None):
        tracker.set_info(
            {
                'host': self.connection.info.host,
                'port': self.connection.info.port
            }
        )
        threshold = get_agent().get_threshold()
        if threshold.is_sql_capture_enabled() is not True:
            return

        if isinstance(args, (list, tuple)) and len(args)>0:
            if is_non_empty_string(args[0]):
                tracker.set_info({'query' : args[0]})

    def _apm_check_and_wrap(self, attr):
        if hasattr(self, attr):
            attr_info = {
                constants.method_str : attr,
                constants.component_str : 'Postgresql',
                constants.extract_info : self._apm_extract_query,
                constants.is_db_tracker : True
            }

            wrapper = default_wrapper(getattr(self, attr), 'Cursor', attr_info)
            setattr(self, attr, wrapper)


class Psycopg2Wrapper():
    @staticmethod
    def instrument_conn(original, module, method_info):
        def conn_wrapper(*args, **kwargs):
            conn = original(*args, **kwargs)
            if not conn:
                return conn

            conn.cursor_factory = Psycopg2CursorWrapper

            return conn

        return conn_wrapper