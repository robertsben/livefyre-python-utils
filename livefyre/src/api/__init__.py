def get_lf_token_header(core, user = None):
    token = None;
    if user is not None:
        token = core.build_user_auth_token(user, '', core.DEFAULT_EXPIRES)
        
    return {
            'Authorization': 'lftoken ' + (core.build_livefyre_token() if token is None else token),
            'Accepts': 'application/json'
    }