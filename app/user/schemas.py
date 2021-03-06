REQUIRED_USER_FIELDS = [
    'username',
    'mobile',
    'first_name',
    'last_name',
    'gender',
    'email',
    'password'
]

USER_DEFINED_USER_FIELDS = [
    *REQUIRED_USER_FIELDS
]

VALID_USER_FIELDS = [
    *USER_DEFINED_USER_FIELDS,
    'businesses',
    'reviews'
]

USER_SEQUENCES = {
    'users': 'user_id_seq',
    'token': 'token_id_seq'
}
