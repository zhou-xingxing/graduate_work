from selenium.webdriver import Edge

def spider_hero():
    url="https://pvp.qq.com/web201605/herolist.shtml"
    browser = Edge(executable_path = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe')
    browser.get(url)
    ls=browser.find_elements_by_css_selector("body > div.wrapper > div > div > div.herolist-box > div.herolist-content > ul > li")
    hero_name=[]
    for i in ls:
        hero_name.append(i.text)

    browser.close()

    with open("hero_name.txt",'w',encoding="utf-8") as f:
        for i in hero_name:
            f.write(i)
            f.write('\n')

    print("写入完毕")


def spider_equipment():
    url="https://pvp.qq.com/web201605/item.shtml"
    browser = Edge(executable_path = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe')
    browser.get(url)
    ls=browser.find_elements_by_css_selector("#Jlist-details > li")
    equip_name=[]
    for i in ls:
        equip_name.append(i.text)

    browser.close()

    with open("equipment_name.txt",'w',encoding="utf-8") as f:
        for i in equip_name:
            f.write(i)
            f.write('\n')

    print("写入完毕")

# spider_hero()
# spider_equipment()