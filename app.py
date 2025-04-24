# 環境変数の読み込み
from dotenv import load_dotenv
load_dotenv()

# 必要なライブラリのインポート
from langchain.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate)
from langchain_openai import ChatOpenAI
import streamlit as st
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

# チャットプロンプト
system_template = "あなたは、{genre}に詳しいAIです。ユーザーからの質問に100文字以内で回答してください。"
human_template = "{question}"
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template(human_template),
])

# Streamlit UI
st.title("LLM質問アプリ")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["モード1: フィットネスに詳しいAI", "モード2: 食事に詳しいAI"]
)

input_message = st.text_input(label="AIへの質問を入力してください。")

if st.button("実行"):
    if not input_message:
        st.error("質問を入力してから「実行」ボタンを押してください。")
    else:
        # モードに応じたジャンル設定
        mode_genre = "フィットネス" if selected_item == "モード1: フィットネスに詳しいAI" else "食事"

        # メッセージ生成
        messages = prompt.format_prompt(
            genre=mode_genre,
            question=input_message
        ).to_messages()

        # LLM呼び出し
        result = llm.invoke(messages)

        # 結果表示
        st.divider()
        st.write(result.content)