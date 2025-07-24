import streamlit as st

# Initial users
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
        st.experimental_rerun()

def admin_panel():
    st.title("User Management")
    for user in st.session_state.users:
        col1, col2, col3, col4 = st.columns([1,2,2,2])
        col1.write(user["id"])
        col2.write(user["username"])
        if user["username"] != st.session_state.current_user["username"]:
            new_role = col3.selectbox("Role", ["admin", "user"], index=0 if user["role"]=="admin" else 1, key=f"role_{user['id']}")
            if new_role != user["role"]:
                user["role"] = new_role
            if col4.button("Delete", key=f"del_{user['id']}"):
                st.session_state.users = [u for u in st.session_state.users if u["id"] != user["id"]]
                st.experimental_rerun()
        else:
            col3.write(user["role"])
            col4.write("(You)")
    st.write("---")
    new_username = st.text_input("New username")
    new_role = st.selectbox("Role", ["user", "admin"], key="add_role")
    if st.button("Add"):
        if new_username and new_username not in [u["username"] for u in st.session_state.users]:
            new_id = max(u["id"] for u in st.session_state.users) + 1
            st.session_state.users.append({"id": new_id, "username": new_username, "role": new_role})
            st.experimental_rerun()
    if st.button("Logout"):
        st.session_state.current_user = None
        st.experimental_rerun()

def user_panel():
    st.title("Welcome!")
    st.write(f"Username: {st.session_state.current_user['username']}")
    st.write(f"Role: {st.session_state.current_user['role']}")
    if st.button("Logout"):
        st.session_state.current_user = None
        st.experimental_rerun()

if st.session_state.current_user is None:
    login()
elif st.session_state.current_user["role"] == "admin":
    admin_panel()
else:
    user_panel()