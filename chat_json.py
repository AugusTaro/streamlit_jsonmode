import streamlit as st
import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
# os.environ["AZURE_OPENAI_API_KEY"] = "e9ba9322c15a4086bb2d31e4e91c90d2"
# os.environ["AZURE_OPENAI_ENDPOINT"] = "https://openai-jadx-01.openai.azure.com/"

deployment = os.getenv("DEPLOYMENT")
apikey = os.getenv("API_KEY")
base = os.getenv("BASE_URL")
api_version=os.getenv("API_VERSION")

# deployment = 'gpt-4-1106-preview'
# apikey = '6ac1efe20eaa47e8acdd9baf2577be0c'
# base = 'https://openai-jadx-02.openai.azure.com/'
# api_version="2023-10-01-preview"

client = AzureOpenAI(
  azure_endpoint = base,
  api_key=apikey,
  api_version=api_version
)


def init_page():
    st.set_page_config(
        page_title="プロンプトお試し",
        page_icon="😺"
    )
    st.header("プロンプトお試し 🐈")
    st.sidebar.title("Options")


def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")

def select_mode():
    model = st.sidebar.radio("Choose a mode:", ("Json", "Normal"))
    if model == "Json":
        mode_name = "json"
    elif model == "Normal":
        mode_name = "normal"

    return mode_name

def input_mail_content():
    txt = st.text_area('ターゲット',  height=150, max_chars=100000
    )
    if "mail_content" not in st.session_state:
        st.session_state["mail_content"] = "　"
    else:
        st.session_state["mail_content"] = f"{txt}"
    if "user_input" not in st.session_state:
        st.session_state["user_input"] = "　"
    else:
        st.session_state["mail_content"] = f"{txt}"
    # txt2 = st.text_area('現在入力されているメール内容', value=txt, disabled=True)
    # txt22 = st.text_area('現在入力されている入力プロンプト', value=(st.session_state["message"]), disabled=True)
    st.session_state["mail_content"] = f"{txt}"
    


#一問一答形式の解答生成
def get_answer_02(mode, message, mail_content):
    replaced_text = message.replace("{メール内容}", mail_content)
    if mode == "json":
        response = client.chat.completions.create(
        model = deployment, 
        temperature = 0.2,
        messages=[
            {"role": "user", "content": f"{replaced_text}"},
        ],   
        response_format={ "type": "json_object" }
    )
    else:
        response = client.chat.completions.create(
        model=deployment, # model = "deployment_name".
        temperature=0.2,
        messages=[
            # {"role": "system", "content": f"{mail_content}"},
            {"role": "user", "content": f"{replaced_text}"},
        ],
    )
    return (response.choices[0].message.content)

def main():
    init_page()
    mode = select_mode()
    input_mail_content()
    # init_messages()

    # ユーザーの入力を監視
    user_input = st.text_area('入力プロンプト',  height=150, max_chars=100000)
    if st.button('送信'):
        st.session_state["user_input"]=user_input
        with st.spinner("ChatGPT is typing ..."):
            answer = get_answer_02(mode,st.session_state.user_input,st.session_state.mail_content)
        st.session_state["answer"]=answer
        # st.markdown("入力プロンプト↓")

        # st.markdown(st.session_state["message"])
        if mode == "json":
            st.json(answer)
        else:
            result = is_json(answer)
            if result == True:
                st.json(answer)
            else:
                st.markdown(answer)

def is_json(json_str):
    '''
    json_strがjson.loads可能か判定
    '''
    result = False
    try:
        json.loads(json_str)
        result = True
    except json.JSONDecodeError as jde:
        result = False
    
    return result

if __name__ == '__main__':
    main()