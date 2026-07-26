"""initial resource, language and sentence tables"""
from alembic import op
import sqlalchemy as sa
revision="0001"; down_revision=None; branch_labels=None; depends_on=None
def upgrade():
    op.create_table("resources", sa.Column("id",sa.String(36),primary_key=True), sa.Column("resource_type",sa.String(50),nullable=False), sa.Column("language_id",sa.String(36)), sa.Column("organization_id",sa.String(36)), sa.Column("editorial_status",sa.String(32),nullable=False), sa.Column("visibility",sa.String(20),nullable=False), sa.Column("license",sa.String(100)), sa.Column("persistent_uri",sa.String(500),unique=True), sa.Column("created_at",sa.DateTime(timezone=True),nullable=False), sa.Column("updated_at",sa.DateTime(timezone=True),nullable=False))
    op.create_table("languages", sa.Column("id",sa.String(36),sa.ForeignKey("resources.id"),primary_key=True),sa.Column("name",sa.String(200),nullable=False),sa.Column("native_name",sa.String(200)),sa.Column("iso_639_3",sa.String(3),unique=True),sa.Column("glottocode",sa.String(20),unique=True),sa.Column("description",sa.Text()))
    op.create_table("sentences",sa.Column("id",sa.String(36),sa.ForeignKey("resources.id"),primary_key=True),sa.Column("text_id",sa.String(36)),sa.Column("sequence",sa.Integer(),nullable=False),sa.Column("transcription",sa.Text(),nullable=False),sa.Column("normalized_text",sa.Text()),sa.Column("translation_pt",sa.Text()),sa.Column("translation_en",sa.Text()),sa.Column("speaker_id",sa.String(36)),sa.Column("start_ms",sa.Integer()),sa.Column("end_ms",sa.Integer()))
def downgrade():
    op.drop_table("sentences"); op.drop_table("languages"); op.drop_table("resources")
