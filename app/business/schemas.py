
REQUIRED_BUSINESS_FIELDS = [
    "mobile",
    "name",
    "location",
    "category"
]

USER_DEFINED_BUSINESS_FIELDS = [
    *REQUIRED_BUSINESS_FIELDS
]

VALID_BUSINESS_FIELDS = [
    *USER_DEFINED_BUSINESS_FIELDS,
    "owner"
]


REQUIRED_REVIEW_FIELDS = [
    "heading",
    "body",
    "author_id",
    "business_id"
]
