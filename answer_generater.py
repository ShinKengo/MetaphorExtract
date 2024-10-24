import os
from openai import OpenAI
from dotenv import load_dotenv

def gpt4o_mini_response(user_input):
    load_dotenv()
    client = OpenAI()

    with open("system_prompt.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 入力テキストを25000文字ずつに分割
    chunks = [user_input[i:i + 25000] for i in range(0, len(user_input), 25000)]
    result = []

    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 仮にGPT-4を指定しています
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
    user_query = input("文章を入力してください: ")
    answer = gpt4o_mini_response(user_query)
    print(answer)
