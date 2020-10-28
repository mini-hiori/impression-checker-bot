import re
import traceback

import requests
from bs4 import BeautifulSoup, Comment

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'


class ImpressionFetcher:
    def __init__(self, event_id, bms_id):
        self.raw_html = ""
        self.soup = None
        self.event_id = event_id
        self.bms_id = bms_id

    def fetch_bms_info(self):
        "event_idとbms_idで指定したbmsの登録ページにアクセスして情報をとってくる"
        url = "http://manbow.nothing.sh/event/event.cgi?action=More_def&num={0}&event={1}".format(
            self.bms_id, self.event_id)
        try:
            response = requests.get(
                url, timeout=20, headers={
                    'User-Agent': USER_AGENT})
            response.encoding = "cp932"
            if response.status_code == 200:
                self.raw_html = response.text
                self.soup = BeautifulSoup(self.raw_html, "lxml")
            else:
                self.raw_html = ""
                self.soup = None
                return None
        except BaseException:
            traceback.print_exc()
            # もうちょっと細分化した方がいい タイムアウトとか...
            self.raw_html = ""
            self.soup = None
            return None

    def get_genre(self):
        "ジャンル取得"
        genre = self.soup.find_all("h4")
        if genre:
            return genre[0].text
        else:
            return ""

    def get_title(self):
        "bmsタイトル取得"
        title = self.soup.find_all("h2")
        if title:
            return title[0].text
        else:
            return ""

    def get_artist(self):
        "作者名取得"
        artist = self.soup.find_all("h3")
        if artist:
            return artist[0].text
        else:
            return ""

    def get_total(self):
        "総得点取得(vote込み)"
        total = self.soup.find_all(id="score_total")
        if total:
            return total[0].text
        else:
            return ""

    def get_impression_count(self):
        "インプレ数取得(vote込み)"
        impression_count = self.soup.find_all(id="score_imp")
        if impression_count:
            return impression_count[0].text
        else:
            return ""

    def get_median(self):
        "総得点取得(vote込み？)"
        median = self.soup.find_all(id="score_med")
        if median:
            return median[0].text
        else:
            return ""

    def get_average(self):
        "平均点取得(vote込み？)"
        average = self.soup.find_all(id="score_ave")
        if average:
            return average[0].text
        else:
            return ""

    def get_download_link(self):
        "ダウンロードリンク取得"
        # div1個足されたら終わりなので、もうちょっと正規表現とかでアレしたい
        selector = "#content > div:nth-child(2) > div > div.col_full > div.col_two_third.col_last > blockquote > p > a"
        link = self.soup.select(selector)
        if link:
            return link[0].get('href')
        else:
            return ""

    def get_recent_short_impression(self):
        "1行インプレを直近10件取得"
        impressions = self.soup.find_all(
            class_="spost clearfix nomarginbottom")
        impressions = [i for i in impressions if i.find(
            class_="points_oneline")][:10]
        # 1行インプレだけ残す
        for ind in range(len(impressions)):
            score = impressions[ind].find(class_="points_oneline").text.strip()
            player = impressions[ind].find("strong").text.strip()
            text = impressions[ind].find_all(
                class_="entry-title")[-1].text.strip()
            impressions[ind] = (score, player, text)
        return impressions

    def get_recent_long_impression(self):
        "長文インプレを直近10件取得"
        info = self.soup.find_all(class_="spost clearfix nomarginbottom")
        info = [i for i in info if i.find(class_="entry-meta") and i.find(class_="points_normal")][:10]
        text_all = self.soup.find_all(class_="event-desc-detail")
        text_all = [i for i in text_all if not i.find(class_="event-desc-time")][:10]
        # 長文インプレはタグが別れてる
        if len(info) != len(text_all):
            print("htmlが怪しいです")
            return []
        impressions = []
        for ind in range(len(info)):
            score = info[ind].find(class_="points_normal").text.strip()
            player = info[ind].find(
                class_="entry-title").text.split("\xa0")[0].strip()
            text = text_all[ind].text.strip()
            impressions.append((score, player, text))
        return impressions


def get_event_list():
    "イベントidと名称の組を出力 まずはここから"
    url = "http://manbow.nothing.sh/event/event.cgi"
    try:
        response = requests.get(
            url, timeout=20, headers={
                'User-Agent': USER_AGENT})
        response.encoding = "cp932"
        if response.status_code == 200:
            raw_html = response.text
            soup = BeautifulSoup(raw_html, "lxml")
            event_list = soup.find_all("tr", class_="event")
            # イベントidリスト取得 なぜか27が抜けてるので真面目に取ったほうがいい
            event_id_list = [
                i.find(
                    "td",
                    class_="eventback").text for i in event_list]
            event_id_list.reverse()
            # イベント名取得
            event_name_list = [i.find("a").text for i in event_list]
            event_name_list.reverse()
            recent_event = soup.find_all("h2")[1]
            recent_event.find("span").extract()
            event_name_list.append(recent_event.text)
            event_id_list.append(str(int(event_id_list[-1]) + 1))
            # 2000文字までしか送れないらしい つらい
            return "\n".join(
                [i + "," + j for i, j in zip(event_id_list, event_name_list)])
        else:
            return ""
    except BaseException:
        traceback.print_exc()
        # もうちょっと細分化した方がいい タイムアウトとか...
        return ""

def get_bms_list(event_id):
    "指定したイベントのbmsの登録idとタイトルを出力"
    import traceback
    url = "http://manbow.nothing.sh/event/event.cgi?action=sp&event={}".format(
        event_id)
    try:
        response = requests.get(
            url, timeout=20, headers={
                'User-Agent': USER_AGENT})
        response.encoding = "cp932"
        if response.status_code == 200:
            raw_html = response.text
            soup = BeautifulSoup(raw_html, "lxml")
            bms_list = soup.find_all("a")
            bms_list = [i.text for i in bms_list if "num=" in i.get("href")]
            bms_list_pairs = []
            for i in range(len(bms_list) // 2):
                bms_list_pairs.append(
                    bms_list[i * 2] + "," + bms_list[i * 2 + 1])
            return "\n".join(bms_list_pairs)
        else:
            return ""
    except BaseException:
        traceback.print_exc()
        # もうちょっと細分化した方がいい タイムアウトとか...
        return ""

def get_stats(event_id, bms_id):
    "指定したbmsのインプレ状況まとめを出力"
    bms_info = ImpressionFetcher(event_id, bms_id)
    result = bms_info.fetch_bms_info()
    if result:
        ret = "ジャンル: 　{}\n".format(bms_info.get_genre())
        ret += "タイトル: 　{}\n".format(bms_info.get_title())
        ret += "作者名:　 　{}\n".format(bms_info.get_artist())
        ret += "総得点:　 　{}\n".format(bms_info.get_total())
        ret += "平均点: 　　{}\n".format(bms_info.get_average())
        ret += "中央値: 　　{}\n".format(bms_info.get_median())
        ret += "インプレ数: {}\n".format(bms_info.get_impression_count())
        return ret
    else:
        return ""

def get_short_impression(event_id,bms_id):
    bms_info = ImpressionFetcher(event_id, bms_id)
    result = bms_info.fetch_bms_info()
    if result:
        impressions = bms_info.get_recent_short_impression()
        message = ""
        for imp in impressions:
            imp = ",".join(imp).strip()
            message += imp + "\n"
    else:
        message = ""
    return message

def get_long_impression(event_id,bms_id):
    bms_info = ImpressionFetcher(event_id, bms_id)
    result = bms_info.fetch_bms_info()
    if result:
        impressions = bms_info.get_recent_long_impression()
        message = ""
        for imp in impressions:
            imp = ",".join(imp).strip()
            message += imp + "\n"
    else:
        message = ""
    return message