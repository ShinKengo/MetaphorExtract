from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_novel_text(url) -> str:
    # Chromeドライバーのセットアップ
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "contentMain-header-workTitle")))
        title_body = driver.find_element(By.ID, "contentMain-header-workTitle")
        title = title_body.text
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        driver.quit()
        return None

    try:
        file_name = f"{title}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            while url:
                # 指定されたURLを開く
                driver.get(url)

                # ページが完全に読み込まれるのを待機（動的に要素が表示されるまで待つ）
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "widget-episodeBody")))

                # クラス名"widget-episodeBody"でタグがつけられたdivの配下にあるすべてのテキストを取得
                episode_body = driver.find_element(By.CLASS_NAME, "widget-episodeBody")
                f.write(episode_body.text + "\n")

                # 次のエピソードのリンクを確認
                try:
                    next_episode = driver.find_element(By.ID, "contentMain-nextEpisode")
                    next_link = next_episode.find_element(By.TAG_NAME, "a").get_attribute("href")
                    url = next_link
                except Exception:
                    # 次のエピソードが存在しない場合はループを終了
                    url = None

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

    finally:
        driver.quit()

    return file_name

if __name__ == "__main__":
    url = "https://kakuyomu.jp/works/16818093080924239434/episodes/16818093080924331976"
    result = scrape_novel_text(url)
    if result:
        print(f"出力ファイル: {result}")
