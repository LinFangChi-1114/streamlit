import requests
import streamlit as st

def getAllBookstore() ->list:
    url = 'https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    res = response.json()  # 將 response 轉換成 json 格式
    return res# 回傳值


def getCountyOption(items) ->list:
    optionList = []
    for item in items:
        name = item['cityName'][0:3]
        if name not in optionList:
            optionList.append(name)
    return optionList

def getSpecificBookstore(items, county, districts):
    specificBookstoreList = []
    for item in items:
        name = item['cityName']
        if county not in name: continue
        for district in districts:
            if district not in name: continue
            specificBookstoreList.append(item)
    return specificBookstoreList

def getDistrictOption(items, target) ->list:
    optionList = []
    for item in items:
        name = item['cityName']
        if target not in name: 
            continue
	
        name.strip()
        district = name[5:]
        if len(district) == 0: 
            continue
		
        if district not in optionList:# 如果 district 不在 optionList 裡面，將 district 放入 optionList
            optionList.append(district)# hint: 使用 if-else 判斷式並使用 append 將內容放入 optionList
    return optionList

def getBookstoreInfo(items):
    expanderList = []
    for item in items:
        expander = st.expander(item['name'])
        expander.image(item['representImage'])
        expander.metric('hitRate', item['hitRate'])
        expander.subheader('Introduction')
        expander.write(item['intro'])
        expander.subheader('Address')
        expander.write(item['address'])
        expander.subheader('Open Time')
        expander.write(item['openTime'])
        expander.subheader('Email')
        expander.write(item['email'])
        expanderList.append(expander)
    return expanderList

def app():
    bookstoreList = getAllBookstore()

    countyOption = getCountyOption(bookstoreList)

    st.header('特色書店地圖')
    st.metric('Total bookstore', len(bookstoreList))
    county = st.selectbox('請選擇縣市', countyOption)
    districtOption = getDistrictOption(bookstoreList, county)
    district = st.multiselect('請選擇區域', districtOption)

    specificBookstore = getSpecificBookstore(bookstoreList, county, district)
    num = len(specificBookstore)
    st.write(f'總共有{num}項結果', num)

    specificBookstore.sort(key = lambda item: item['hitRate'], reverse=True)
    bookstoreInfo = getBookstoreInfo(specificBookstore)
    

if __name__ == '__main__':
    app()


