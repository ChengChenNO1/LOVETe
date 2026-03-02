import streamlit as st
import requests
import time

# 替换成你刚才在 npoint.io 申请到的地址
API_URL = "https://api.npoint.io/acacdc9eb5d982857ff4"


def get_remote_data():
    """获取云端 JSON 数据"""
    response = requests.get(API_URL)
    return response.json()


def update_remote_data(room_id, user_role, choice):
    """更新云端数据"""
    data = get_remote_data()
    if room_id not in data:
        data[room_id] = {"user_a": None, "user_b": None}

    # 根据角色更新 0 或 1
    data[room_id][user_role] = choice
    requests.post(API_URL, json=data)


st.title("✨ 默契信号灯")

# 1. 基础设置
room_id = st.text_input("输入暗号 (例如: love2026)", value="love2026")
role = st.radio("你的身份", ["user_a", "user_b"], captions=["发起者", "受邀者"])

# 2. 选择与提交
choice = st.selectbox("你的选择 (双方均看不到对方选择)", [None, 0, 1], index=0)

if st.button("锁定选择"):
    if choice is not None:
        update_remote_data(room_id, role, choice)
        st.success("已发送至云端，等待信号交汇...")
    else:
        st.warning("请先选一个数字")

# 3. 结果判定
if st.button("揭晓答案"):
    with st.spinner("正在接收信号..."):
        data = get_remote_data()
        room_data = data.get(room_id, {})

        a = room_data.get("user_a")
        b = room_data.get("user_b")

        if a is None or b is None:
            st.info("还有一方没选呢，别急~")
        elif a == 0 and b == 0:
            st.balloons()  # 基础气球
            # 这里可以放你的烟花组件
            st.markdown("### 🎆 信号达成！砰砰砰！")
        else:
            st.error("信号未对上，下次再试试？")
            if st.button("重置房间"):
                update_remote_data(room_id, "user_a", None)
                update_remote_data(room_id, "user_b", None)
                st.rerun()