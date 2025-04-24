import pandas as pd
from datetime import datetime
sheet_url = "https://docs.google.com/spreadsheets/d/1QJqNYWfSz_C-jq3jGAzdPUeTHSxaAfGFDXy8lDMICPg/export?format=csv"
today = datetime.now().strftime('%d-%m-%Y')

df = pd.read_csv(sheet_url)
df.columns = [col.strip().lower() for col in df.columns]
today_rows = df[df['date'] == today]
print(today_rows)


from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key="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",
    model_name="mistralai/mistral-7b-instruct"
)

template = """
You are a professional LinkedIn content writer.

Write a short and engaging LinkedIn post on the topic: "{topic}" without using emoji

- Keep it professional and helpful
- Make it sound human and authentic
- Do NOT use hashtags
- Add a personal or motivational touch

Only return the post text. Don't add quotation marks or markdown.
"""

prompt = PromptTemplate(
    input_variables=["topic"],
    template=template,
)

post_chain = LLMChain(llm=llm, prompt=prompt)


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=chrome_options)


driver.get("https://www.linkedin.com/login")

time.sleep(3)

from selenium.webdriver.common.by import By
email_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")


email_field.send_keys("daskumarbiman2020@gmail.com")
password_field.send_keys("Biman@707")
password_field.send_keys(Keys.RETURN)

time.sleep(5)

import pickle
pickle.dump(driver.get_cookies(), open("linkedin_cookies.pkl", "wb"))


cookies = pickle.load(open("linkedin_cookies.pkl", "rb"))

driver.get("https://www.linkedin.com/feed/")

time.sleep(3)

for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()

time.sleep(5)


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def post_on_linkedin(post_content):
    driver.get("https://www.linkedin.com/feed/")

    # start a post button
    try:
        post_button = driver.find_element( By.XPATH, "//button[contains(@id,'ember37') and .//span[contains(@class,'artdeco-button__text')]//strong[text()='Start a post']]")


        post_button.click()
    except Exception as e:
        print("❌ Failed to click 'Start a post' button:", e)
        return

    # type content portion
    try:
        post_text_area = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'ql-editor') and @contenteditable='true' and @role='textbox']"
            ))
        )
        post_text_area.click()
        post_text_area.send_keys(post_content)
    except Exception as e:
        print("❌ Failed to type post content:", e)
        return

    # post button
    try:
        post_button_final = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@class,'share-actions__primary-action') and not(@disabled)]"
            ))
        )
        post_button_final.click()
    except Exception as e:
        print("❌ Failed to click Post button:", e)
        return


for idx, row in today_rows.iterrows():
    topic = row['topic']
    print(f"\n📝 Generating post for topic: {topic}")
    result = post_chain.run(topic=topic)
    # result="test"
    print("Generated Post:")
    print(result)

    post_on_linkedin(result)
