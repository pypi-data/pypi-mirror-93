# Foolish Authentication App
If use this APP as django rest framework authenticator, It only check the HTTP
header for FOOLISH_AUTH.
If the Header attribute is not None, it would create a in-memory user with
the header attribute value as the username.
