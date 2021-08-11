import requests
from bs4 import BeautifulSoup
import re
import csv
import re

rootURL = 'https://www.pro-football-reference.com/'
playerURL_list = []
player_list = []

ppr = 1
ppf = 0


# HTML cleaner
def _strip_html(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', str(text))

url = 'https://www.pro-football-reference.com/years/2020/scrimmage.htm'
## Scrape for RB stats
res = requests.get(url)
soup = BeautifulSoup(res.text,features="html.parser")

parsed = soup.findAll(
    'table', {
        'id': 'receiving_and_rushing'
    }
)

rows = parsed[0].findAll('td')

column_len = 30

grouped_rows = [
    rows[i:i+column_len] for i in range(0, len(rows), column_len)
]


for i in grouped_rows:
    fullSTR = str(i)
    trimmed = re.search('href="(.*).htm">',fullSTR)
    playerURL = trimmed.group(1)
    playerURL = rootURL + playerURL + '.htm'
    playerURL_list.append(playerURL)

table = [map(lambda x: _strip_html(x), row) for row in grouped_rows]

for i in table:
    player_list.append(list(i))

def player_fetch(z,name):
    url = playerURL_list[z]
    player_career = []
    num_rows = 0
    pos = ''
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, features="html.parser")

        parsed = soup.findAll(
            'table', {
                'id': 'rushing_and_receiving'
            }
        )

        pos = 'RB'

        rows = parsed[0].findAll('td')
        num_rows = len(rows)/31

        column_len = 31

        grouped_rows = [
            rows[i:i + column_len] for i in range(0, len(rows)-(1*column_len), column_len)
        ]

        table = [map(lambda x: _strip_html(x), row) for row in grouped_rows]



    except:
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, features="html.parser")

            parsed = soup.findAll(
                'table', {
                    'id': 'receiving_and_rushing'
                }
            )

            pos = 'WR'

            rows = parsed[0].findAll('td')
            num_rows = len(rows)/31

            column_len = 31

            grouped_rows = [
                rows[i:i + column_len] for i in range(0, len(rows) - (1 * column_len), column_len)
            ]

            table = [map(lambda x: _strip_html(x), row) for row in grouped_rows]

        except:
            return None, None

    num_teams = 0
    teams = []
    iter = 0

    if(name == 'Marvin Jones '):
        num_rows = num_rows + 3
    
    for i in table:
        season_row = list(i)

        if(iter < (num_rows - num_teams))or(name == 'Raheem Mostert'):

            if(season_row[1] == 'Missed season - Contract dispute'):
                season_row = season_row[2:]
                if(season_row[0] =='27'):
                    if(season_row[1] =='NYJ'):
                        season_row.append('1')
                        season_row.append('')
            elif(season_row[1] =='Missed season - Violation of league substance abuse policy'):
                if(name == 'Josh Gordon'):
                    season_row = season_row[4:]
                    season_row.append('335')
                    season_row.append('1')
                    season_row.append('0')
                    season_row.append('2')
            elif(name == 'Josh Gordon'):
                if(season_row[0] == '335'):
                    season_row = season_row[4:]
                    season_row.append('737')
                    season_row.append('4')
                    season_row.append('0')
                    season_row.append('7')
                elif (season_row[0] == '737'):
                    season_row = season_row[4:]
                    season_row.append('17')
                    season_row.append('1')
                    season_row.append('0')
                    season_row.append('0')
                elif (season_row[0] == '17'):
                    season_row = season_row[4:]
                    season_row.append('720')
                    season_row.append('3')
                    season_row.append('0')
                    season_row.append('7')
                elif (season_row[0] == '720'):
                    season_row = season_row[4:]
                    season_row.append('427')
                    season_row.append('1')
                    season_row.append('0')
                    season_row.append('')


            player_career.append(season_row)

            if(season_row[1]) not in teams:
                teams.append(season_row[1])
                if(season_row[1] == '2TM'):
                    pass
                elif(num_teams == 1):
                    if(name != "Todd Gurley"):
                        num_teams = num_teams + 2
                else:
                    if (name != "Todd Gurley"):
                        num_teams = num_teams + 1
        iter = iter + 1

    z = 0
    team2_1 = 0
    team2_2 = 0

    team3_1 = 0
    team3_2 = 0
    team3_3 = 0
    twoteam_flag = 0
    threeteam_flag = 0
    dos = 0
    dos_list = []
    for i in player_career:
        z = z + 1
        if(i[1] == '2TM'):
            if(twoteam_flag==1):
                dos = 1
                dos_list.append(team2_1)
                dos_list.append(team2_2)
                dos_list.append(z)
                dos_list.append(z+1)
            else:
                twoteam_flag = 1
                team2_1 = z
                team2_2 = z+1
        elif(i[1] == '3TM'):
            threeteam_flag = 1
            team3_1 = z
            team3_2 = z+1
            team3_3 = z+2


    if(twoteam_flag == 1):
        if(dos == 1):
            del player_career[dos_list[0]]
            del player_career[dos_list[1]-1]
            del player_career[dos_list[2] - 2]
        elif(name == 'Mack Hollins'):
            del player_career[team2_1]
        else:
            del player_career[team2_1]
            del player_career[team2_2-1]
    if(threeteam_flag == 1):
        del player_career[team3_1]
        del player_career[team3_2-1]
        if(name != 'Zach Zenner') and (name != "Eric Tomlinson"):
            del player_career[team3_3-2]

    if(name == 'Todd Gurley'):
        del player_career[6]
        del player_career[6]
        
    if(name == 'Raheem Mostert'):
        del player_career[6]
        del player_career[6]
        del player_career[6]
        del player_career[6]
        del player_career[6]

    if(name == 'Marvin Jones '):
        player_career[2] = ['25', 'CIN', 'WR', '82', '16', '13', '103', '65', '816', '12.6', '4', '34', '47', '4.1', '51.0', '63.1%', '7.9', '5', '33', '0', '3', '30', '6.6', '2.1', '0.3', '70', '12.1', '849', '4','0','9']
        player_career[3] = ['26', 'DET', 'WR', '11', '15', '15', '103', '55', '930', '16.9', '4', '41', '73', '3.7', '62.0', '53.4%', '9.0', '1', '3', '0', '0', '3', '3.0', '0.2', '0.1', '56', '16.7', '933', '4','0','8']
        player_career[4] = ['27', 'DET', 'WR', '11', '16', '16', '107', '61', '1101', '18.0', '9', '44', '58', '3.8', '68.8', '57.0%', '10.3', '', '', '', '', '', '', '', '', '61', '18.0', '1101', '9','0','9']
        player_career[5] = ['28', 'DET', 'WR', '11', '9', '9', '62', '35', '508', '14.5', '5', '27', '39', '3.9', '56.4', '56.5%', '8.2', '', '', '', '', '', '', '', '', '35', '14.5', '508', '5','0','4']
        player_career[6] = ['29', 'DET', 'WR', '11', '13', '11', '91', '62', '779', '12.6', '9', '41', '47', '4.8', '59.9', '68.1%', '8.6', '2', '0', '0', '0', '4', '0.0', '0.0', '0.2', '64', '12.2', '779', '9','0','6']
        player_career[7] = ['30', 'DET', 'WR', '11', '16', '16', '115', '76', '978', '12.9', '9', '52', '43', '4.8', '61.1', '66.1%', '8.5', '', '', '', '', '', '', '', '', '76', '12.9', '978', '9','0','0']

    if(name == "Le'Veon Bell"):
        player_career[6] = ['28', '2TM', '', '', '11', '4', '82', '328', '2', '21', '16', '4.0', '29.8', '7.5', '20', '16', '138', '8.6', '0', '7', '30', '1.5', '12.5', '80.0%', '6.9', '98', '4.8', '466', '2','1','0']
        del player_career[7]

    if(name == "Mack Hollins"):
        del player_career[2]

    if(name == "Dontrelle Inman"):
        del player_career[6]

    if(name == "Jason Witten"):
        player_career[15] = ['37', 'DAL', 'TE', '82', '16', '16', '83', '63', '529', '8.4', '4', '27', '33', '3.9', '33.1', '75.9%', '6.4', '', '', '', '', '', '', '', '', '63', '8.4', '529', '4','1','4']
        player_career[16] = ['38', 'LVR', 'te', '82', '16', '7', '17', '13', '69', '5.3', '2', '8', '15', '0.8', '4.3', '76.5%', '4.1', '', '', '', '', '', '', '', '', '13', '5.3', '69', '2','0','0']

    if(name == 'Dez Bryant'):
        player_career[8] = ['32', 'BAL', '', '88', '6', '0', '11', '6', '47', '7.8', '2', '3', '16', '1.0', '7.8', '54.5%', '4.3', '', '', '', '', '', '', '', '', '6', '7.8','47','2','0','0']
        del player_career[9]

    if(name == 'Mohamed Sanu'):
        del player_career[9]

    #for i in player_career:
        #print(i)
            
    # To evaluate previous years
    # player_career = player_career[:-1]
    return player_career, pos

def player_recur(pos,writer,name,table):
    data = []
    seasons = len(table)

    if (seasons >= 1):
        last_season = table[seasons - 1]
        actual = 0


        print(name + " ", end='')
        if (pos == 'RB'):
            is_rb = True
            if(last_season[15] == ''):
                last_season[15] = 0
            if(last_season[20] == ''):
                last_season[20] = 0
            if(last_season[9] == ''):
                last_season[9] = 0
            if(last_season[14] == ''):
                last_season[14] = 0
            actual = (float(last_season[27])) / 10 + (float(last_season[28]) * 6) - (float(last_season[29]) * 2) + (float(last_season[15]) * ppr) + (float(last_season[9]) + float(last_season[20]))*ppf    
        if (pos == 'WR'):
            is_rb = False
            if(last_season[20] == ''):
                last_season[20] = 0
            if(last_season[11] == ''):
                last_season[11] = 0
            if(last_season[6] == ''):
                last_season[6] = 0
            actual = (float(last_season[27])) / 10 + (float(last_season[28]) * 6) - (float(last_season[29]) * 2) + (float(last_season[7]) * ppr) + (float(last_season[11]) + float(last_season[20]))*ppf

        data.append(name)

        print("- " + str(actual))

        table.pop()

        # Calculate career averages
        games = 0
        games_count = 0
        for i in table:
            if (i[4] != ''):
                games = games + float(i[4])
                games_count = float(i[4])

        

        age = 0
        for i in table:
            age = age + float(i[0])

        att = 0
        if (pos == 'RB'):
            for i in table:
                if (i[6] != ''):
                    att = att + float(i[6])
        elif (pos == 'WR'):
            for i in table:
                if (i[17] != ''):
                    att = att + float(i[17])

        scrim = 0
        for i in table:
            scrim = scrim + float(i[27])

        tot_td = 0
        for i in table:
            tot_td = tot_td + float(i[28])

        fmbl = 0
        for i in table:
            fmbl = fmbl + float(i[29])

        rec = 0
        if (pos == 'RB'):
            for i in table:
                if (i[15] != ''):
                    rec = rec + float(i[15])
        elif (pos == 'WR'):
            for i in table:
                if (i[7] != ''):
                    rec = rec + float(i[7])

        tgt = 0
        if (pos == 'RB'):
            for i in table:
                if (i[14] != ''):
                    tgt = tgt + float(i[14])
        elif (pos == 'WR'):
            for i in table:
                if (i[6] != ''):
                    tgt = tgt + float(i[6])

        rush_yds = 0
        if (pos == 'RB'):
            for i in table:
                if (i[7] != ''):
                    rush_yds = rush_yds + float(i[7])
        elif (pos == 'WR'):
            for i in table:
                if (i[18] != ''):
                    rush_yds = rush_yds + float(i[18])

        rec_yds = 0
        if (pos == 'RB'):
            for i in table:
                if (i[16] != ''):
                    rec_yds = rec_yds + float(i[16])
        elif (pos == 'WR'):
            for i in table:
                if (i[8] != ''):
                    rec_yds = rec_yds + float(i[8])

        yds_rec = 0
        if (pos == 'RB'):
            for i in table:
                if (i[17] != ''):
                    yds_rec = yds_rec + float(i[17])
        elif (pos == 'WR'):
            for i in table:
                if (i[9] != ''):
                    yds_rec = yds_rec + float(i[9])

        rec_td = 0
        if (pos == 'RB'):
            for i in table:
                if (i[18] != ''):
                    rec_td = rec_td + float(i[18])
        elif (pos == 'WR'):
            for i in table:
                if (i[10] != ''):
                    rec_td = rec_td + float(i[10])

        rec_first = 0
        if (pos == 'RB'):
            for i in table:
                if (i[19] != ''):
                    rec_first = rec_first + float(i[19])
        elif (pos == 'WR'):
            for i in table:
                if (i[11] != ''):
                    rec_first = rec_first + float(i[11])

        catch = 0
        if (pos == 'RB'):
            for i in table:
                if (i[23] != ''):
                    myString = i[23]
                    myString = myString[:-1]
                    catch = catch + float(myString)
        elif (pos == 'WR'):
            for i in table:
                if (i[15] != ''):
                    myString = i[15]
                    myString = myString[:-1]
                    catch = catch + float(myString)

        rush_td = 0
        if (pos == 'RB'):
            for i in table:
                if (i[8] != ''):
                    rush_td = rush_td + float(i[8])
        elif (pos == 'WR'):
            for i in table:
                if (i[19] != ''):
                    rush_td = rush_td + float(i[19])

        rush_first = 0
        if (pos == 'RB'):
            for i in table:
                if (i[9] != ''):
                    rush_first = rush_first + float(i[9])
        elif (pos == 'WR'):
            for i in table:
                if (i[20] != ''):
                    rush_first = rush_first + float(i[20])

        rush_long = 0
        if (pos == 'RB'):
            for i in table:
                if (i[10] != ''):
                    rush_long = rush_long + float(i[10])
        elif (pos == 'WR'):
            for i in table:
                if (i[21] != ''):
                    rush_long = rush_long + float(i[21])

        rec_long = 0
        if (pos == 'RB'):
            for i in table:
                if (i[20] != ''):
                    rec_long = rec_long + float(i[20])
        elif (pos == 'WR'):
            for i in table:
                if (i[12] != ''):
                    rec_long = rec_long + float(i[12])

        yards_att = 0
        if (pos == 'RB'):
            for i in table:
                if (i[11] != ''):
                    yards_att = yards_att + float(i[11])
        elif (pos == 'WR'):
            for i in table:
                if (i[22] != ''):
                    yards_att = yards_att + float(i[22])

        touch = 0
        for i in table:
            if i[25] != '':
                touch = touch + float(i[25])

        yards_touch = 0
        for i in table:
            if i[26] != '':
                yards_touch = yards_touch + float(i[26])

        data.append(actual)

        # Normalize
        if (games == 0):
            return None
        else:
            scrim = scrim / games
            tot_td = tot_td / games
            fmbl = fmbl / games
            rec = rec / games
            tgt = tgt / games
            att = att / games
            age = age / (seasons - 1)
            rush_yds = rush_yds / games
            rec_yds = rec_yds / games
            yds_rec = yds_rec / (seasons - 1)
            rec_td = rec_td / games
            rec_first = rec_first / games
            catch = catch / (seasons - 1)
            rush_td = rush_td / games
            rush_first = rush_first / games
            rush_long = rush_long / (seasons - 1)
            rec_long = rec_long / (seasons - 1)
            yards_att = yards_att / (seasons - 1)
            touch = touch / games
            yards_touch = yards_touch / (seasons - 1)

        # Append to row
        data.append(scrim)
        data.append(tot_td)
        data.append(fmbl)
        data.append(rec)
        data.append(tgt)
        data.append(att)
        data.append(age)
        data.append(rush_yds)
        data.append(rec_yds)
        data.append(yds_rec)
        data.append(rec_td)
        data.append(rec_first)
        data.append(catch)
        data.append(rush_td)
        data.append(rush_first)
        data.append(rush_long)
        data.append(rec_long)
        data.append(yards_att)
        data.append(touch)
        data.append(yards_touch)

        # Reset variables
        age = 0
        rush_yds = 0
        rec_yds = 0
        yds_rec = 0
        rec_td = 0
        rec_first = 0
        catch = 0
        rush_td = 0
        rush_first = 0
        rush_long = 0
        rec_long = 0
        yards_att = 0
        touch = 0
        yards_touch = 0
        games = 0
        scrim = 0
        fmbl = 0
        rec = 0
        tgt = 0
        att = 0

        # Enter last season stats
        if (table[-1][4] != ''):
            games = float(table[-1][4])
        scrim = float(table[-1][27])
        tot_td = float(table[-1][28])
        fmbl = float(table[-1][29])

        if (pos == 'RB'):
            if (table[-1][15] != ''):
                rec = float(table[-1][15])
        elif (pos == 'WR'):
            if (table[-1][7] != ''):
                rec = float(table[-1][7])

        if (pos == 'RB'):
            if (table[-1][14] != ''):
                tgt = float(table[-1][14])
        elif (pos == 'WR'):
            if (table[-1][6] != ''):
                tgt = float(table[-1][6])

        if (pos == 'RB'):
            if (table[-1][6] != ''):
                att = float(table[-1][6])
        elif (pos == 'WR'):
            if (table[-1][17] != ''):
                att = float(table[-1][17])

        age = table[-1][0]

        # Rush yds
        if (pos == 'RB'):
            if (table[-1][7] != ''):
                rush_yds = float(table[-1][7])
        elif (pos == 'WR'):
            if (table[-1][18] != ''):
                rush_yds = float(table[-1][18])

        # Rec yds
        if (pos == 'RB'):
            if (table[-1][16] != ''):
                rec_yds = float(table[-1][16])
        elif (pos == 'WR'):
            if (table[-1][8] != ''):
                rec_yds = float(table[-1][8])

        # Yards/rec
        if (pos == 'RB'):
            if (table[-1][17] != ''):
                yds_rec = float(table[-1][17])
        elif (pos == 'WR'):
            if (table[-1][9] != ''):
                yds_rec = float(table[-1][9])

        # Rec TD
        if (pos == 'RB'):
            if (table[-1][18] != ''):
                rec_td = float(table[-1][18])
        elif (pos == 'WR'):
            if (table[-1][10] != ''):
                rec_td = float(table[-1][10])

        # Rec 1D
        if (pos == 'RB'):
            if (table[-1][19] != ''):
                rec_first = float(table[-1][19])
        elif (pos == 'WR'):
            if (table[-1][11] != ''):
                rec_first = float(table[-1][11])

        # Catch
        if (pos == 'RB'):
            if (table[-1][23] != ''):
                myString = table[-1][23]
                myString = myString[:-1]
                catch = catch + float(myString)
        elif (pos == 'WR'):
            if (table[-1][15] != ''):
                myString = table[-1][15]
                myString = myString[:-1]
                catch = catch + float(myString)

        # Rush TD
        if (pos == 'RB'):
            if (table[-1][8] != ''):
                rush_td = float(table[-1][8])
        elif (pos == 'WR'):
            if (table[-1][19] != ''):
                rush_td = float(table[-1][19])

        # Rush 1D
        if (pos == 'RB'):
            if (table[-1][9] != ''):
                rush_first = float(table[-1][9])
        elif (pos == 'WR'):
            if (table[-1][20] != ''):
                rush_first = float(table[-1][20])

        # Rush long
        if (pos == 'RB'):
            if (table[-1][10] != ''):
                rush_long = float(table[-1][10])
        elif (pos == 'WR'):
            if (table[-1][21] != ''):
                rush_long = float(table[-1][21])

        # Rec long
        if (pos == 'RB'):
            if (table[-1][20] != ''):
                rec_long = float(table[-1][20])
        elif (pos == 'WR'):
            if (table[-1][12] != ''):
                rec_long = float(table[-1][12])

        # Yds/att
        if (pos == 'RB'):
            if (table[-1][11] != ''):
                yards_att = float(table[-1][11])
        elif (pos == 'WR'):
            if (table[-1][22] != ''):
                yards_att = float(table[-1][22])

        # Touch
        if (pos == 'RB'):
            if (table[-1][25] != ''):
                touch = float(table[-1][25])
        elif (pos == 'WR'):
            if (table[-1][25] != ''):
                touch = float(table[-1][25])

        # Yards/Touch
        if (pos == 'RB'):
            if (table[-1][26] != ''):
                yards_touch = float(table[-1][26])
        elif (pos == 'WR'):
            if (table[-1][26] != ''):
                yards_touch = float(table[-1][26])

        # Noramlize
        if (games != 0):
            scrim = scrim / games
            tot_td = tot_td / games
            fmbl = fmbl / games
            rec = rec / games
            tgt = tgt / games
            att = att / games
            age = age
            rush_yds = rush_yds / games
            rec_yds = rec_yds / games
            yds_rec = yds_rec
            rec_td = rec_td / games
            rec_first = rec_first / games
            catch = catch
            rush_td = rush_td / games
            rush_first = rush_first / games
            rush_long = rush_long
            rec_long = rec_long
            yards_att = yards_att
            touch = touch / games
            yards_touch = yards_touch

        data.append(scrim)
        data.append(tot_td)
        data.append(fmbl)
        data.append(rec)
        data.append(tgt)
        data.append(att)
        data.append(age)
        data.append(rush_yds)
        data.append(rec_yds)
        data.append(yds_rec)
        data.append(rec_td)
        data.append(rec_first)
        data.append(catch)
        data.append(rush_td)
        data.append(rush_first)
        data.append(rush_long)
        data.append(rec_long)
        data.append(yards_att)
        data.append(touch)
        data.append(yards_touch)

        writer.writerow(data)

        if (len(table) >= 1):
            player_recur(pos,writer, name, table)
        else:
            return None

def player_2020(pos,writer,name,table):
    data = []
    seasons = len(table)
    if(seasons < 1):
        return None
    last_season = table[-1]

    print(name)

    data.append(name)

    # Calculate career averages
    games = 0
    for i in table:
        if (i[4] != ''):
            games = games + float(i[4])

    scrim = 0
    for i in table:
        scrim = scrim + float(i[27])

    tot_td = 0
    for i in table:
        tot_td = tot_td + float(i[28])

    fmbl = 0
    for i in table:
        fmbl = fmbl + float(i[29])

    rec = 0
    if (pos == 'RB'):
        is_rb = True
        for i in table:
            if (i[15] != ''):
                rec = rec + float(i[15])
    elif (pos == 'WR'):
        is_rb = False
        for i in table:
            if (i[7] != ''):
                rec = rec + float(i[7])

    tgt = 0
    if (pos == 'RB'):
        for i in table:
            if (i[14] != ''):
                tgt = tgt + float(i[14])
    elif (pos == 'WR'):
        for i in table:
            if (i[6] != ''):
                tgt = tgt + float(i[6])

    att = 0
    if (pos == 'RB'):
        for i in table:
            if (i[6] != ''):
                att = att + float(i[6])
    elif (pos == 'WR'):
        for i in table:
            if (i[17] != ''):
                att = att + float(i[17])

    age = 0
    for i in table:
        if(name == 'Penny Hart'):
            i[0] = 24
        age = age + float(i[0])

    rush_yds = 0
    if (pos == 'RB'):
        for i in table:
            if (i[7] != ''):
                rush_yds = rush_yds + float(i[7])
    elif (pos == 'WR'):
        for i in table:
            if (i[18] != ''):
                rush_yds = rush_yds + float(i[18])

    rec_yds = 0
    if (pos == 'RB'):
        for i in table:
            if (i[16] != ''):
                rec_yds = rec_yds + float(i[16])
    elif (pos == 'WR'):
        for i in table:
            if (i[8] != ''):
                rec_yds = rec_yds + float(i[8])

    yds_rec = 0
    if (pos == 'RB'):
        for i in table:
            if (i[17] != ''):
                yds_rec = yds_rec + float(i[17])
    elif (pos == 'WR'):
        for i in table:
            if (i[9] != ''):
                yds_rec = yds_rec + float(i[9])

    rec_td = 0
    if (pos == 'RB'):
        for i in table:
            if (i[18] != ''):
                rec_td = rec_td + float(i[18])
    elif (pos == 'WR'):
        for i in table:
            if (i[10] != ''):
                rec_td = rec_td + float(i[10])

    rec_first = 0
    if (pos == 'RB'):
        for i in table:
            if (i[19] != ''):
                rec_first = rec_first + float(i[19])
    elif (pos == 'WR'):
        for i in table:
            if (i[11] != ''):
                rec_first = rec_first + float(i[11])

    catch = 0
    if (pos == 'RB'):
        for i in table:
            if (i[23] != ''):
                myString = i[23]
                myString = myString[:-1]
                catch = catch + float(myString)
    elif (pos == 'WR'):
        for i in table:
            if (i[15] != ''):
                myString = i[15]
                myString = myString[:-1]
                catch = catch + float(myString)

    rush_td = 0
    if (pos == 'RB'):
        for i in table:
            if (i[8] != ''):
                rush_td = rush_td + float(i[8])
    elif (pos == 'WR'):
        for i in table:
            if (i[19] != ''):
                rush_td = rush_td + float(i[19])

    rush_first = 0
    if (pos == 'RB'):
        for i in table:
            if (i[9] != ''):
                rush_first = rush_first + float(i[9])
    elif (pos == 'WR'):
        for i in table:
            if (i[20] != ''):
                rush_first = rush_first + float(i[20])

    rush_long = 0
    if (pos == 'RB'):
        for i in table:
            if (i[10] != ''):
                rush_long = rush_long + float(i[10])
    elif (pos == 'WR'):
        for i in table:
            if (i[21] != ''):
                rush_long = rush_long + float(i[21])

    rec_long = 0
    if (pos == 'RB'):
        for i in table:
            if (i[20] != ''):
                rec_long = rec_long + float(i[20])
    elif (pos == 'WR'):
        for i in table:
            if (i[12] != ''):
                rec_long = rec_long + float(i[12])

    yards_att = 0
    if (pos == 'RB'):
        for i in table:
            if (i[11] != ''):
                yards_att = yards_att + float(i[11])
    elif (pos == 'WR'):
        for i in table:
            if (i[22] != ''):
                yards_att = yards_att + float(i[22])

    touch = 0
    for i in table:
        if i[25] != '':
            touch = touch + float(i[25])

    yards_touch = 0
    for i in table:
        if i[26] != '':
            yards_touch = yards_touch + float(i[26])

    # Normalize
    if (games == 0):
        return None
    else:
        scrim = scrim / games
        tot_td = tot_td / games
        fmbl = fmbl / games
        rec = rec / games
        tgt = tgt / games
        att = att / games
        age = age / (seasons)
        rush_yds = rush_yds / games
        rec_yds = rec_yds / games
        yds_rec = yds_rec / (seasons)
        rec_td = rec_td / games
        rec_first = rec_first / games
        catch = catch / (seasons)
        rush_td = rush_td / games
        rush_first = rush_first / games
        rush_long = rush_long / (seasons)
        rec_long = rec_long / (seasons)
        yards_att = yards_att / (seasons)
        touch = touch / games
        yards_touch = yards_touch / (seasons)

    # Append to row
    data.append(scrim)
    data.append(tot_td)
    data.append(fmbl)
    data.append(rec)
    data.append(tgt)
    data.append(att)
    data.append(age)
    data.append(rush_yds)
    data.append(rec_yds)
    data.append(yds_rec)
    data.append(rec_td)
    data.append(rec_first)
    data.append(catch)
    data.append(rush_td)
    data.append(rush_first)
    data.append(rush_long)
    data.append(rec_long)
    data.append(yards_att)
    data.append(touch)
    data.append(yards_touch)

    # Reset variables
    age = 0
    rush_yds = 0
    rec_yds = 0
    yds_rec = 0
    rec_td = 0
    rec_first = 0
    catch = 0
    rush_td = 0
    rush_first = 0
    rush_long = 0
    rec_long = 0
    yards_att = 0
    touch = 0
    yards_touch = 0
    games = 0
    scrim = 0
    fmbl = 0
    rec = 0
    tgt = 0
    att = 0

    # Enter last season stats
    if (table[-1][4] != ''):
        games = float(table[-1][4])
    scrim = float(table[-1][27])
    tot_td = float(table[-1][28])
    fmbl = float(table[-1][29])

    if (pos == 'RB'):
        if (table[-1][15] != ''):
            rec = float(table[-1][15])
    elif (pos == 'WR'):
        if (table[-1][7] != ''):
            rec = float(table[-1][7])

    if (pos == 'RB'):
        if (table[-1][14] != ''):
            tgt = float(table[-1][14])
    elif (pos == 'WR'):
        if (table[-1][6] != ''):
            tgt = float(table[-1][6])

    if (pos == 'RB'):
        if (table[-1][6] != ''):
            att = float(table[-1][6])
    elif (pos == 'WR'):
        if (table[-1][17] != ''):
            att = float(table[-1][17])

    age = table[-1][0]

    # Rush yds
    if (pos == 'RB'):
        if (table[-1][7] != ''):
            rush_yds = float(table[-1][7])
    elif (pos == 'WR'):
        if (table[-1][18] != ''):
            rush_yds = float(table[-1][18])

    # Rec yds
    if (pos == 'RB'):
        if (table[-1][16] != ''):
            rec_yds = float(table[-1][16])
    elif (pos == 'WR'):
        if (table[-1][8] != ''):
            rec_yds = float(table[-1][8])

    # Yards/rec
    if (pos == 'RB'):
        if (table[-1][17] != ''):
            yds_rec = float(table[-1][17])
    elif (pos == 'WR'):
        if (table[-1][9] != ''):
            yds_rec = float(table[-1][9])

    # Rec TD
    if (pos == 'RB'):
        if (table[-1][18] != ''):
            rec_td = float(table[-1][18])
    elif (pos == 'WR'):
        if (table[-1][10] != ''):
            rec_td = float(table[-1][10])

    # Rec 1D
    if (pos == 'RB'):
        if (table[-1][19] != ''):
            rec_first = float(table[-1][19])
    elif (pos == 'WR'):
        if (table[-1][11] != ''):
            rec_first = float(table[-1][11])

    # Catch
    if (pos == 'RB'):
        if (table[-1][23] != ''):
            myString = table[-1][23]
            myString = myString[:-1]
            catch = catch + float(myString)
    elif (pos == 'WR'):
        if (table[-1][15] != ''):
            myString = table[-1][15]
            myString = myString[:-1]
            catch = catch + float(myString)

    # Rush TD
    if (pos == 'RB'):
        if (table[-1][8] != ''):
            rush_td = float(table[-1][8])
    elif (pos == 'WR'):
        if (table[-1][19] != ''):
            rush_td = float(table[-1][19])

    # Rush 1D
    if (pos == 'RB'):
        if (table[-1][9] != ''):
            rush_first = float(table[-1][9])
    elif (pos == 'WR'):
        if (table[-1][20] != ''):
            rush_first = float(table[-1][20])

    # Rush long
    if (pos == 'RB'):
        if (table[-1][10] != ''):
            rush_long = float(table[-1][10])
    elif (pos == 'WR'):
        if (table[-1][21] != ''):
            rush_long = float(table[-1][21])

    # Rec long
    if (pos == 'RB'):
        if (table[-1][20] != ''):
            rec_long = float(table[-1][20])
    elif (pos == 'WR'):
        if (table[-1][12] != ''):
            rec_long = float(table[-1][12])

    # Yds/att
    if (pos == 'RB'):
        if (table[-1][11] != ''):
            yards_att = float(table[-1][11])
    elif (pos == 'WR'):
        if (table[-1][22] != ''):
            yards_att = float(table[-1][22])

    # Touch
    if (pos == 'RB'):
        if (table[-1][25] != ''):
            touch = float(table[-1][25])
    elif (pos == 'WR'):
        if (table[-1][25] != ''):
            touch = float(table[-1][25])

    # Yards/Touch
    if (pos == 'RB'):
        if (table[-1][26] != ''):
            yards_touch = float(table[-1][26])
    elif (pos == 'WR'):
        if (table[-1][26] != ''):
            yards_touch = float(table[-1][26])

    # Noramlize
    if (games != 0):
        scrim = scrim / games
        tot_td = tot_td / games
        fmbl = fmbl / games
        rec = rec / games
        tgt = tgt / games
        att = att / games
        age = age
        rush_yds = rush_yds / games
        rec_yds = rec_yds / games
        yds_rec = yds_rec
        rec_td = rec_td / games
        rec_first = rec_first / games
        catch = catch
        rush_td = rush_td / games
        rush_first = rush_first / games
        rush_long = rush_long
        rec_long = rec_long
        yards_att = yards_att
        touch = touch / games
        yards_touch = yards_touch

    data.append(scrim)
    data.append(tot_td)
    data.append(fmbl)
    data.append(rec)
    data.append(tgt)
    data.append(att)
    data.append(age)
    data.append(rush_yds)
    data.append(rec_yds)
    data.append(yds_rec)
    data.append(rec_td)
    data.append(rec_first)
    data.append(catch)
    data.append(rush_td)
    data.append(rush_first)
    data.append(rush_long)
    data.append(rec_long)
    data.append(yards_att)
    data.append(touch)
    data.append(yards_touch)

    writer.writerow(data)

z = 0
pos = ''

# Gather training data
with open('train.csv',mode='w') as train:
    writer = csv.writer(train, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    labels = ['Player','Actual','Scrim yds','TOT TD','Fmbl','Rec','Tgt','Att','Age','Rush yds','Rec yds','Yds/rec','Rec TD','Rec 1D','Catch %','Rushing TD','Rush 1D','Rush long','Rec long','Yards/att','Touch','Yards/touch','Scrim yds','TOT TD','Fmbl','Rec','Tgt','Att','Age','Rush yds','Rec yds','Yds/rec','Rec TD','Rec 1D','Catch %','Rushing TD','Rush 1D','Rush long','Rec long','Yards/att','Touch','Yards/touch']
    writer.writerow(labels)
    for i in player_list:
        name = i[0].replace("*","")
        table, pos = player_fetch(z,name)
        if(type(table) == list):
            player_recur(pos,writer,name,table)

        z=z+1

z = 0
# Gather testing data
with open('test.csv',mode='w') as test:
    writer = csv.writer(test, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    labels = ['Player','Scrim yds','TOT TD','Fmbl','Rec','Tgt','Att','Age','Rush yds','Rec yds','Yds/rec','Rec TD','Rec 1D','Catch %','Rushing TD','Rush 1D','Rush long','Rec long','Yards/att','Touch','Yards/touch','Scrim yds','TOT TD','Fmbl','Rec','Tgt','Att','Age','Rush yds','Rec yds','Yds/rec','Rec TD','Rec 1D','Catch %','Rushing TD','Rush 1D','Rush long','Rec long','Yards/att','Touch','Yards/touch']
    writer.writerow(labels)

    for i in player_list:
        name = i[0].replace("*","")
        table, pos = player_fetch(z,name)
        if(type(table) == list):
            player_2020(pos,writer,name,table)

        z=z+1





