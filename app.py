import  streamlit as st
import  datetime
import  requests
import  json
import  pandas as pd

page = st.sidebar.selectbox('choose your page',['users','rooms','bookings'])
if page == 'users':
    st.title("ユウザー登録画面")

    with st.form(key='user'):  # formの開始
        #user_id: int = random.randint(0, 10)test用自動採番に変更
        username: str = st.text_input("ユーザー名", max_chars=12)
        data = {
            #"user_id": user_id,
            "username": username
        }
        submit_button = st.form_submit_button(label='ユーザー登録')  # form専用送信ボタン

    if submit_button:
        url = "http://127.0.0.1:8000/users/"
        res = requests.post(url, json=data)  # ← jsonで送る（これが正解）

        if res.status_code ==200:
            st.success("ユーザー登録完了")
        st.json(res.json())

elif page == 'rooms':
    st.title("会議室登録画面")

    with st.form(key='room'):#formの開始
        #room_id : int = random.randint(0,10)
        room_name : str = st.text_input("会議室名",max_chars=12)
        capacity : int = st.number_input("収容人数",step=1)
        data = {
            #"room_id": room_id,
            "room_name": room_name,
            "capacity": capacity
        }
        submit_button = st.form_submit_button(label='会議室登録')#form専用送信ボタン

    if submit_button:
        url = "http://127.0.0.1:8000/rooms/"
        res = requests.post(
            url,
            data=json.dumps(data)
        )  # ← jsonで送る（これが正解）
        if res.status_code ==200:
            st.success("会議室登録完了")
        st.write("status:", res.status_code)
        st.json(res.json())

elif page == 'bookings':
    st.title("会議室予約画面")
    #ユーザー一覧取得
    url_users = "http://127.0.0.1:8000/users/"
    res = requests.get(url_users)
    users = res.json()

    #ユーザー名をキー、ユーザーIDをバリューにした辞書作成
    user_name = { }
    for user in users:
        user_name[user["username"]] = user["user_id"]
    #会議室一覧取得
    url_rooms = "http://127.0.0.1:8000/rooms/"
    res = requests.get(url_rooms)
    rooms = res.json()

    rooms_name = {}
    for room in rooms:
        rooms_name[room["room_name"]] = {
            "room_id": room["room_id"],
            "capacity": room["capacity"]
        }

    st.write("###会議室一覧")
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ["会議室名","定員","会議室ID"]
    st.table(df_rooms)#静的なテーブル

    url_bookings = "http://127.0.0.1:8000/bookings/"
    res = requests.get(url_bookings)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)#panndasuデータフレームに変換

    users_id = {}
    for user in users:
        users_id[user["user_id"]] = user["username"]#予約一覧のIDから名前に変換するための辞書

    rooms_id = {}
    for room in rooms:
        rooms_id[room["room_id"]] = {
            "room_name": room["room_name"],#予約一覧のIDから会議室名に変換するための辞書
            "capacity": room["capacity"],
        }

    #ＩＤを各値に変換 ラムダ関数
    to_username = lambda x: users_id[x]
    to_room_name = lambda x: rooms_id[x]["room_name"]
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime("%Y/%m/%d %H:%M")#datetime型に変換してから文字列に変換

    #特定の列に適用
    df_bookings["user_id"] = df_bookings["user_id"].map(to_username)#IDを名前に書き込む（上書きできる）
    df_bookings["room_id"] = df_bookings["room_id"].map(to_room_name)
    df_bookings["start_datetime"] = df_bookings["start_datetime"].map(to_datetime)
    df_bookings["end_datetime"] = df_bookings["end_datetime"].map(to_datetime)

    df_bookings =df_bookings.rename(columns={
        "user_id": "予約者名",
        "room_id": "会議室名",
        "booked_num": "予約人数",
        "start_datetime": "開始時刻",
        "end_datetime": "終了時刻",
        "booking_id": "予約番号"
    })
    st.write("###予約一覧")
    st.table(df_bookings)


    with st.form(key='booking'):
        username: str = st.selectbox("予約者名",user_name.keys())
        room_name: str = st.selectbox("会議室名", rooms_name.keys())
        booked_num : int = st.number_input("予約人数",step=1,min_value=1)
        date = st.date_input("予約日", min_value=datetime.date.today())
        start_time = st.time_input("開始時刻",value = datetime.time( hour=9,minute=0))
        end_time = st.time_input("終了時刻",value = datetime.time( hour=20,minute=0))
        submit_button = st.form_submit_button(label='予約登録')#form専用送信ボタン

    if submit_button:
        user_id: int = user_name[username]
        room_id: int = rooms_name[room_name]["room_id"]
        room_capacity: int = rooms_name[room_name]["capacity"]

        data = {
             "user_id": user_id,
            "room_id": room_id,
            "booked_num": booked_num,
            "start_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute
            ).isoformat(),
            "end_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat()
        }
        #定員より多い予約人数の場合
        if booked_num > room_capacity:
            st.error(f"{room_name}の定員は{room_capacity}名です。")
        #開始時刻 ＞＝ 終了時刻
        elif start_time >= end_time:
            st.error("開始時刻が終了時刻を超えています。")
        elif start_time < datetime.time(9, 0) or end_time > datetime.time(20, 0):
            st.error("予約可能時間は9:00～20:00です。")

        else:
            #会議室予約
            url = "http://127.0.0.1:8000/bookings/"
            res = requests.post(
                url,
                json=data)  # ← jsonで送る（これが正解）
            if res.status_code ==200:
                st.success("予約登録完了")
            elif res.status_code ==409 and res.json()["detail"] == "Already booked":
                st.error("指定の時間は既に予約ありです。")






