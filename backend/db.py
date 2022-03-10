import bcrypt


# Fake user database
USERS_DB = {
    221977809462502706358095104732309094260: {
        "username": "test@user.com",
        "password": bcrypt.hashpw(
            "s3cr3t".encode(), bcrypt.gensalt()
        ),  # obviously, you normally want to store the already computed hash
    }
}
