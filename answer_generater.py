import os
from openai import OpenAI
from dotenv import load_dotenv

def gpt4o_mini_response(user_input=None, input_file=None):
    load_dotenv()
    client = OpenAI()

    with open("system_prompt.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 入力が指定されていない場合、input_fileから内容を読み込む
    if user_input is None and input_file is not None:
        with open(input_file, "r", encoding="utf-8") as f:
            user_input = f.read()
    elif user_input is None:
        raise ValueError("user_inputかinput_fileのいずれかを指定してください")

    # 入力テキストを25000文字ずつに分割
    chunks = [user_input[i:i + 25000] for i in range(0, len(user_input), 25000)]
    result = []

    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chunk},
            ],
            max_tokens=1000,
        )

        answer = response.choices[0].message.content

        lines = answer.strip().split("\n")

        for line in lines:
            parts = line.split("説明:")
            metaphor = parts[0].replace("メタファー:", "").strip()
            explanation = parts[1].strip() if len(parts) > 1 else ""
            result.append([metaphor, explanation])

    return result

if __name__ == "__main__":
    input_method = input("入力方法を選択してください (1: コンソール入力, 2: ファイル入力): ")
    if input_method == "1":
        user_query = input("文章を入力してください: ")
        answer = gpt4o_mini_response(user_input=user_query)
    elif input_method == "2":
        file_name = input("ファイル名を入力してください: ")
        answer = gpt4o_mini_response(input_file=file_name)
    else:
        raise ValueError("無効な入力方法が選択されました")
    
    print(answer)
