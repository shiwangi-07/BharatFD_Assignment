"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
# @ Importing necessary modules. `op` is used for generating schema migrations, `sa` is the SQLAlchemy module.
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# @ Revision identifiers for Alembic migrations: `revision` is the current migration ID, `down_revision` is the previous migration ID.
# @ `branch_labels` and `depends_on` are additional identifiers for managing branching and dependencies between migrations.
revision: str = ${repr(up_revision)}  # @ Unique identifier for this migration.
down_revision: Union[str, None] = ${repr(down_revision)}  # @ The identifier of the migration this one depends on.
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}  # @ Optional labels for the migration branch.
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}  # @ Optional dependencies for this migration.

# @ `upgrade` function to define operations that will be applied to upgrade the database schema.
def upgrade() -> None:
    ${upgrades if upgrades else "pass"}  # @ Placeholder for database schema changes (e.g., adding columns, tables).

# @ `downgrade` function to define operations that will be applied to downgrade the database schema, undoing `upgrade` actions.
def downgrade() -> None:
    ${downgrades if downgrades else "pass"}  # @ Placeholder for reversing changes made in the `upgrade` function.
