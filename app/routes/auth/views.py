from flask import Blueprint, jsonify, request, g, current_app
from functools import wraps

from app.routes.auth.auth import hash_password, verify_password, new_session_token, session_expiry

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_connector():
    return current_app.config["connector"]

def _get_bearer_token():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[len("Bearer "):].strip()
    return None

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = _get_bearer_token() or request.cookies.get("session")
        if not token:
            return jsonify({"error": "Missing session"}), 401

        with get_connector().connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT s.token, s.user_id, u.email
                    FROM financial.sessions s
                    JOIN financial.users u ON u.id = s.user_id
                    WHERE s.token = %s AND s.expires_at > now()
                    """,
                    (token,),
                )
                row = cur.fetchone()

        if not row:
            return jsonify({"error": "Invalid or expired session"}), 401

        # If your cursor returns tuples, use indexes:
        # token_val, user_id, email = row
        # If it returns dict rows, use keys:
        try:
            user_id = row["user_id"]
            email = row["email"]
        except TypeError:
            # tuple fallback
            _, user_id, email = row

        g.user = {"id": user_id, "email": email}
        g.session_token = token
        return fn(*args, **kwargs)
    return wrapper


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    if len(password) < 8:
        return jsonify({"error": "password must be at least 8 characters"}), 400

    pw_hash = hash_password(password)

    try:
        with get_connector().connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO financial.users (email, password_hash)
                    VALUES (%s, %s)
                    RETURNING id, email
                    """,
                    (email, pw_hash),
                )
                user = cur.fetchone()

        try:
            return jsonify({"id": user["id"], "email": user["email"]}), 201
        except TypeError:
            return jsonify({"id": user[0], "email": user[1]}), 201
    except Exception:
        return jsonify({"error": "User already exists"}), 409


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    with get_connector().connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, email, password_hash FROM financial.users WHERE email = %s",
                (email,),
            )
            user = cur.fetchone()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    try:
        user_id = user["id"]
        pw_hash = user["password_hash"]
        email_val = user["email"]
    except TypeError:
        user_id, email_val, pw_hash = user

    if not verify_password(password, pw_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    token = new_session_token()
    expires = session_expiry()

    with get_connector().connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO financial.sessions (token, user_id, expires_at)
                VALUES (%s, %s, %s)
                """,
                (token, user_id, expires),
            )

    return jsonify({
        "session": token,
        "expires_at": expires.isoformat(),
        "user": {"id": user_id, "email": email_val},
    })


@auth_bp.route("/me", methods=["GET"])
@require_auth
def me():
    return jsonify({"user": g.user})


@auth_bp.route("/logout", methods=["POST"])
@require_auth
def logout():
    token = g.session_token
    with get_connector().connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM financial.sessions WHERE token = %s", (token,))
    return jsonify({"ok": True})


@auth_bp.route("/cleanup_sessions", methods=["POST"])
def cleanup_sessions():
    with get_connector().connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM financial.sessions WHERE expires_at <= now()")
            deleted = cur.rowcount
    return jsonify({"deleted": deleted})
