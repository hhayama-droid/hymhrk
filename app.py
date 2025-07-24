import streamlit as st

# --- ユーザー管理 ---
if "users" not in st.session_state:
    st.session_state.users = [
        {"id": 1, "username": "admin", "role": "admin"},
        {"id": 2, "username": "user1", "role": "user"},
        {"id": 3, "username": "user2", "role": "user"},
    ]
if "current_user" not in st.session_state:
    st.session_state.current_user = None

def login():
    st.title("Login")
    usernames = [u["username"] for u in st.session_state.users]
    selected = st.selectbox("Select user", usernames)
    if st.button("Login"):
        st.session_state.current_user = next(u for u in st.session_state.users if u["username"] == selected)
        st.rerun()

def admin_panel():
    st.header("User Management")
    for user in st.session_state.users:
        col1, col2, col3, col4 = st.columns([1,2,2,2])
        col1.write(user["id"])
        col2.write(user["username"])
        if user["username"] != st.session_state.current_user["username"]:
            new_role = col3.selectbox(
                "Role", ["admin", "user"],
                index=0 if user["role"]=="admin" else 1,
                key=f"role_{user['id']}"
            )
            if new_role != user["role"]:
                user["role"] = new_role
            if col4.button("Delete", key=f"del_{user['id']}"):
                st.session_state.users = [u for u in st.session_state.users if u["id"] != user["id"]]
                st.rerun()
        else:
            col3.write(user["role"])
            col4.write("(You)")
    st.write("---")
    new_username = st.text_input("New username", key="new_username_input")
    new_role = st.selectbox("Role", ["user", "admin"], key="add_role_selectbox")
    if st.button("Add", key="add_user_btn"):
        if new_username and new_username not in [u["username"] for u in st.session_state.users]:
            new_id = max(u["id"] for u in st.session_state.users) + 1
            st.session_state.users.append({"id": new_id, "username": new_username, "role": new_role})
            st.rerun()

def timestamp_panel():
    st.header("AI Video Timestamp Generator")
    video_url = st.text_input("Enter video URL", key="video_url_input")
    if st.button("Analyze", key="analyze_btn"):
        if video_url:
            st.success("Analysis complete!")
            # ダミーのタイムスタンプ
            timestamps = [
                {"time": "00:01:23", "desc": "Intro"},
                {"time": "00:05:10", "desc": "Main Topic"},
                {"time": "00:10:45", "desc": "Summary"},
            ]
            for ts in timestamps:
                st.write(f"{ts['time']} - {ts['desc']}")
        else:
            st.error("Please enter a video URL.")

def main_panel():
    st.write(f"**Username:** {st.session_state.current_user['username']}")
    st.write(f"**Role:** {st.session_state.current_user['role']}")
    st.write("---")
    # 管理者はユーザー管理も表示
    if st.session_state.current_user["role"] == "admin":
        admin_panel()
        st.write("---")
    timestamp_panel()
    st.write("---")
    if st.button("Logout", key="logout_btn"):
        st.session_state.current_user = None
        st.rerun()

# --- アプリの流れ ---
if st.session_state.current_user is None:
    login()
else:
    main_panel()