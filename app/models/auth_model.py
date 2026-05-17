import hashlib

from app import mysql


# =====================================================
# Hash Password
# =====================================================

def hash_password(password):

    return hashlib.sha256(

        password.encode()

    ).hexdigest()


# =====================================================
# Get User By Username
# =====================================================

def get_user_by_username(
    username
):

    cur = mysql.connection.cursor()

    cur.execute(

        """
        SELECT *
        FROM users
        WHERE username = %s
        """,

        (username,)
    )

    user = cur.fetchone()

    cur.close()

    return user


# =====================================================
# Create User
# =====================================================

def create_user(
    username,
    password,
    name
):

    hashed_password = hash_password(
        password
    )

    cur = mysql.connection.cursor()

    cur.execute(

        """
        INSERT INTO users
        (
            username,
            password,
            name
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        """,

        (
            username,
            hashed_password,
            name
        )
    )

    mysql.connection.commit()

    cur.close()


# =====================================================
# Validate Login
# =====================================================

def validate_user_login(
    username,
    password
):

    user = get_user_by_username(
        username
    )

    if not user:

        return None

    hashed_password = hash_password(
        password
    )

    if user["password"] == hashed_password:

        return user

    return None