from enum import StrEnum
class EditorialStatus(StrEnum):
    DRAFT = "draft"
    IMPORTED_UNVERIFIED = "imported_unverified"
    IN_REVIEW = "in_review"
    REVIEWED = "reviewed"
    PUBLISHED = "published"
    ARCHIVED = "archived"
class Visibility(StrEnum):
    PUBLIC = "public"
    COMMUNITY = "community"
    RESTRICTED = "restricted"
