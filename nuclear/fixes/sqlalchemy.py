from ..reactivity.patch import UNPATCHABLE_TYPES

import sqlalchemy

def fix_sqlalchemy():
    UNPATCHABLE_TYPES.extend([
        sqlalchemy.orm.attributes.QueryableAttribute
    ])
    