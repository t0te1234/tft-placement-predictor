from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import csv

driver = webdriver.Chrome()
driver.get("https://www.metatft.com/match-history")
players = []
na_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'NA')]"))
)
na_tab.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "LeaderboardPlayerLink"))
)
links = driver.find_elements(By.CLASS_NAME, "LeaderboardPlayerLink")
for link in links:
    name = driver.execute_script(
        "let t=''; for (const n of arguments[0].childNodes) "
        "{ if (n.nodeType===3 && n.nodeValue.trim()) { t=n.nodeValue.trim(); break; } } return t;",
        link,
    )
    tagline = link.find_element(By.CLASS_NAME, "PlayerTagline")
    
    tag = driver.execute_script(
        "let count = 0, t = ''; "
        "for (const n of arguments[0].childNodes) { "
        "  if (n.nodeType === 3 && n.nodeValue.trim()) { "
        "    count++; "
        "    if (count === 2) { t = n.nodeValue.trim(); break; } "
        "  } "
        "} "
        "return t;",
        tagline,
    )
    players.append({"name": name, "href": link.get_attribute("href"), "tag": tag})
print (players)

df = pd.DataFrame(players)
df.to_csv("players.csv", index=False)
        
driver.quit()
'''
statistics = []
for p in players:
    driver.get(p["href"])
    matches = driver.find_elements(By.CLASS_NAME, "PlayerGameMatchInfo")
    for match in matches:
        stats = match.find_elements(By.CLASS_NAME, "PlayerMatchStatText")

        values = []
        for stat in stats:
            value = driver.execute_script(
                "let t=''; for (const n of arguments[0].childNodes) "
                "{ if (n.nodeType===3 && n.nodeValue.trim()) { t=n.nodeValue.trim(); break; } } return t;",
                stat,
            )
            if value:
                values.append(value)
        placement = match.find_element(By.CLASS_NAME, "PlayerMatchSummaryPlacement").text.strip()
        record = {
            "placement": placement,
            "damage": values[0] if len(values) > 0 else None,
            "gold": values[1] if len(values) > 1 else None
        }
        statistics.append(record)
'''
