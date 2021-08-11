import requests
from bs4 import BeautifulSoup
import re
import csv
import re
import sys

rootURL = 'https://www.pro-football-reference.com/'
playerURL_list = []
player_list = []

ppr = 0
ppf = 0.5


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
            return None, None, None

    num_teams = 0
    teams = []
    iter = 0

    page_string = str(soup)
    url_search = re.search('https://www.sports-reference.com/(.*).html">',page_string)
    if(url_search == None):
        print(name)
        return None, None, None
    
    college_url = url_search.group(1)
    college_url = 'https://www.sports-reference.com/' + college_url + '.html'
    

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
    
    return player_career, pos, college_url

def prep_train(name,player_career,college_url,pos):
    print(name)

    if(college_url == None):
        return None
    if('https://www.sports-reference.com/cbb/players/' in college_url):
        return None
    if(name == 'Logan Thomas'):
        return None
    if(name == 'Taysom Hill'):
        return None
    if(name == 'Greg Ward'):
        return None
    if(name == 'Julian Edelman'):
        return None
    if(name == 'Blake Bell'):
        return None        
    if(name == 'Keith Smith'):
        return None
    if(name == 'Jakob Johnson'):
        return None
    if(name == 'Dominique Dafney'):
        return None
    if(name == 'Tommy Stevens '):
        return None
    if(name == 'Anthony Sherman'):
        return None
    if(name == 'Logan Woodside '):
        return None
    if(name == 'Bruce Miller'):
        return None
    if(name == 'Kendall Lamm'):
        return None
    
    rookie_year = player_career[0]

    scrim = 0
    rec = 0
    rrtd = 0
    rush_first = 0
    rec_first = 0
    
    if(pos == 'RB'):
        if(rookie_year[27] != ''):
            scrim = int(rookie_year[27])
            
        if (rookie_year[15] != ''):
            rec = int(rookie_year[15])

        if (rookie_year[28] != ''):
            rrtd = int(rookie_year[28])

        if (rookie_year[9] != ''):
            rush_first = int(rookie_year[9])

        if (rookie_year[19] != ''):
            rec_first = int(rookie_year[19])
            
    elif (pos == 'WR'):
        
        if(rookie_year[27] != ''):
            scrim = int(rookie_year[27])
            
        if (rookie_year[7] != ''):
            rec = int(rookie_year[7])

        if (rookie_year[28] != ''):
            rrtd = int(rookie_year[28])

        if (rookie_year[11] != ''):
            rush_first = int(rookie_year[11])

        if (rookie_year[20] != ''):
            rec_first = int(rookie_year[20])
            
    rookie_points = (0.1*scrim)+(ppr*rec)+(rrtd*6)+((rush_first+rec_first)*ppf)

    res = requests.get(college_url)
    soup = BeautifulSoup(res.text, features="html.parser")


    parsed = soup.findAll(
        'table', {
            'id': 'rushing'
                }
            )

    college_pos = 'RB'

    if not parsed:
            parsed = soup.findAll(
                'table', {
                    'id': 'receiving'
                }
            )

            college_pos = 'WR'

    rows = parsed[0].findAll('td')

    column_len = 17

    grouped_rows = [
    rows[i:i+column_len] for i in range(0, len(rows), column_len)]

    table = [map(lambda x: _strip_html(x), row) for row in grouped_rows]

    college_list = []
    for i in table:
        college_list.append(list(i))

    # Remove table totals
    college_list.pop()

    if(name == 'Jonathan Taylor'):
        college_list.pop()
    if(name == 'Gus Edwards '):
        del(college_list[2])
        college_list.pop()
        college_list.pop()
    if(name == 'Marquez Valdes-Scantling '):
        del(college_list[2])
        college_list.pop()
        college_list.pop()
    if(name == 'Jalen Guyton'):
        del(college_list[0])
        college_list.pop()
        college_list.pop()
    if(name == 'Gerald Everett'):
        college_list.pop()
        college_list.pop()        
    if (name == 'Preston Williams'):
        college_list.pop()
        college_list.pop()
    if(name == 'Van Jefferson '):
        del(college_list[0])
        college_list.pop()
        college_list.pop()
    if(name == "Ke'Shawn Vaughn "):
        college_list.pop()
        college_list.pop()
    if(name == "De'Michael Harris"):
        college_list.pop()
    if(name == 'Jace Sternberger'):
        del(college_list[0])
        college_list.pop()
        college_list.pop()        
    if(name == 'Jordan Howard'):
        college_list.pop()
        college_list.pop()
    if(name == 'Devin Asiasi '):
        college_list.pop()
        college_list.pop()
    if(name == 'Jonathan Williams'):
        college_list.pop()
    if(name == 'Keith Kirkwood'):
        college_list.pop()
        college_list.pop()
    if(name == 'Gehrig Dieter '):
        college_list.pop()
        college_list.pop()
        college_list.pop()
        
    career_games = 0
    career_att = 0
    career_rush_yds = 0
    career_rush_avg = 0
    career_rush_td = 0
    career_rec = 0
    career_rec_yds = 0
    career_rec_avg = 0
    career_rec_td = 0
    career_touch = 0
    career_scrim = 0
    career_yards_touch = 0
    career_rrtd = 0
    
    for i in college_list:
        print(i)
        if(i[4] != ''):
            career_games = career_games + int(i[4])
        if(college_pos == 'RB'):
            if(i[5] != ''):
                career_att = career_att + int(i[5])
            if(i[6] != ''):
                career_rush_yds = career_rush_yds + int(i[6])
            if(i[8] != ''):           
                career_rush_td = career_rush_td + int(i[8])
            if(i[9] != ''):           
                career_rec = career_rec + int(i[9])
            if(i[10] != ''):           
                career_rec_yds = career_rec_yds + int(i[10])
            if(i[12] != ''):           
                career_rec_td = career_rec_td + int(i[12])
            if(i[13] != ''):           
                career_touch = career_touch + int(i[13])
            if(i[14] != ''):           
                career_scrim = career_scrim + int(i[14])
            if(i[16] != ''):           
                career_rrtd = career_rrtd + int(i[16])
        else:
            if(i[9] != ''):
                career_att = career_att + int(i[9])
            if(i[10] != ''):
                career_rush_yds = career_rush_yds + int(i[10])
            if(i[12] != ''):           
                career_rush_td = career_rush_td + int(i[12])
            if(i[5] != ''):           
                career_rec = career_rec + int(i[5])
            if(i[6] != ''):           
                career_rec_yds = career_rec_yds + int(i[6])
            if(i[8] != ''):           
                career_rec_td = career_rec_td + int(i[8])
            if(i[13] != ''):           
                career_touch = career_touch + int(i[13])
            if(i[14] != ''):           
                career_scrim = career_scrim + int(i[14])
            if(i[16] != ''):           
                career_rrtd = career_rrtd + int(i[16])

    # Normalize stats           
    if(career_att != 0):
        career_rush_avg = career_rush_yds/career_att
    else:
        career_rush_avg = 0

    if(career_rec != 0):
        career_rec_avg = career_rec_yds/career_rec
    else:
        career_rec_avg = 0

    career_yards_touch = career_scrim/career_touch
    career_att = career_att/career_games
    career_rush_yds = career_rush_yds/career_games
    career_rush_td = career_rush_td/career_games
    career_rec = career_rec/career_games
    career_rec_yds = career_rec_yds/career_games
    career_rec_td = career_rec_td/career_games
    career_touch = career_touch/career_games
    career_scrim = career_scrim/career_games
    career_rrtd = career_rrtd/career_games

    last_season = college_list.pop

    games = 0
    att = 0
    rush_yds = 0
    rush_td = 0
    rec = 0
    rec_yds = 0
    rec_td = 0
    touch = 0
    scrim = 0
    yards_touch = 0
    rrtd = 0
    rush_avg = 0
    rec_avg = 0

    if(i[4] != ''):
        games = int(i[4])
    if(i[13] != ''):           
        touch = int(i[13])
    if(i[14] != ''):           
        scrim = int(i[14])
    if(i[16] != ''):           
        rrtd = int(i[16])

    if(college_pos == 'RB'):
        if(i[5] != ''):
            att = int(i[5])
        if(i[6] != ''):
            rush_yds = int(i[6])
        if(i[8] != ''):           
            rush_td = int(i[8])
        if(i[9] != ''):           
           rec = career_rec + int(i[9])
        if(i[10] != ''):           
            rec_yds = int(i[10])
        if(i[12] != ''):           
            rec_td = int(i[12])
    else:
        if(i[9] != ''):
            att = career_att + int(i[9])
        if(i[10] != ''):
            rush_yds = int(i[10])
        if(i[12] != ''):           
           rush_td = int(i[12])
        if(i[5] != ''):           
            rec = int(i[5])
        if(i[6] != ''):           
           rec_yds =  int(i[6])
        if(i[8] != ''):           
            rec_td = int(i[8])

    # Normalize last season
    if(att != 0):
        rush_avg = rush_yds/att
    if(rec != 0):
        rec_avg = rec_yds/rec
    if(touch !=0):
        yards_touch = scrim/touch

    att = att/games
    rush_yds = rush_yds/games
    rush_td = rush_td/games
    rec = rec/games
    rec_yds = rec_yds/games
    rec_td = rec_td/games
    touch = touch/games
    scrim = scrim/games
    rrtd = rrtd/games
    
    final_row = []
    final_row = [name, rookie_points, career_att, career_rush_yds, career_rush_avg, career_rush_td, career_rec, career_rec_yds, career_rec_avg, career_rec_td, career_touch, career_scrim, career_yards_touch, career_rrtd, att, rush_yds, rush_avg, rush_td, rec, rec_yds, rec_avg, rec_td, touch, scrim, yards_touch, rrtd] 
        
    #exit()
    return final_row 

z = 0
pos = ''

#Gather training data
with open('train.csv',mode='w') as train:
    writer = csv.writer(train, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    labels = ['Player','Actual','Career Att','Career Rush Yards','Career Rush Avg','Career Rush TD','Career Rec','Career Rec Yards','Career Rec Avg','Career Rec TD','Career Touches','Career Scrimmage Yards','Career yards/touch','Career TOT TDs','Last Season Att','Last Season Rush Yards','Last Season Rush Avg','Last Season Rush TD','Last Season Rec','Last Season Rec Yards','Last Season Rec Avg','Last Season Rec TD','Last Season Touches','Last Season Scrimmage Yards','Last Season Yards/Touch','Last Season TOT TDs']
    writer.writerow(labels)
    for i in player_list:
        name = i[0].replace("*","")
        table, pos, url = player_fetch(z,name)
        x = prep_train(name,table,url,pos)
        if(x != None):
            writer.writerow(x)
        z=z+1

z = 0
# Gather testing data
with open('test.csv',mode='w') as test:
    writer = csv.writer(test, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    labels = ['Player','Career Att','Career Rush Yards','Career Rush Avg','Career Rush TD','Career Rec','Career Rec Yards','Career Rec Avg','Career Rec TD','Career Touches','Career Scrimmage Yards','Career yards/touch','Career TOT TDs','Last Season Att','Last Season Rush Yards','Last Season Rush Avg','Last Season Rush TD','Last Season Rec','Last Season Rec Yards','Last Season Rec Avg','Last Season Rec TD','Last Season Touches','Last Season Scrimmage Yards','Last Season Yards/Touch','Last Season TOT TDs']
    writer.writerow(labels)

    rookie_names = []
    rookie_list = []
    rootURL = 'https://www.sports-reference.com'
    
    rec_url = 'https://www.sports-reference.com/cfb/years/2020-receiving.html'
    ## Scrape for rec stats
    res = requests.get(rec_url)
    soup = BeautifulSoup(res.text,features="html.parser")

    parsed = soup.findAll(
        'table', {
            'id': 'receiving'
        }
    )
    
    rows = parsed[0].findAll('td')

    column_len = 16

    grouped_rows = [
        rows[i:i+column_len] for i in range(0, len(rows), column_len)
    ]

    playerURL_list = []

    for i in grouped_rows:
        fullSTR = str(i)
        trimmed = re.search('href="(.*).html',fullSTR)
        playerURL = trimmed.group(1)
        playerURL = rootURL + playerURL 
        playerURL = playerURL.split(".html",1)[0] + '.html'
        playerURL_list.append(playerURL)

    rec_table = [map(lambda x: _strip_html(x), row) for row in grouped_rows]

    for i in rec_table:
        rookie_list.append(list(i))

    for i in rookie_list:
        name = i[0].replace("*","")
        rookie_names.append(name)
        url = playerURL_list[z]
        res = requests.get(url)
        soup = BeautifulSoup(res.text, features="html.parser")
        if (': QB' in str(soup)):
            z = z + 1
            continue
        z=z+1
        print('---------------------------')


        parsed = soup.findAll(
            'table', {
                'id': 'rushing'
                    }
                )

        college_pos = 'RB'

        if not parsed:
                parsed = soup.findAll(
                    'table', {
                        'id': 'receiving'
                    }
                )

                college_pos = 'WR'

        try:
            rows = parsed[0].findAll('td')
        except:
            print('---')

        print(college_pos)
            
        column_len = 17

        grouped_rows = [
        rows[i:i+column_len] for i in range(0, len(rows), column_len)]

        table = [map(lambda x: _strip_html(x), row) for row in grouped_rows]

        college_list = []
        
        for i in table:
            k = list(i)
            college_list.append(k)

        # Remove table totals
        college_list.pop()

        print()
        print('"'+ name + '"')
        print()
        
        teams = []
        b = 0
        for i in college_list:
            if(i[0] not in teams):
                teams.append(i[0])
                b = b+1

        while(b > 1):
            college_list.pop()
            b = b - 1

                
                
        career_games = 0
        career_att = 0
        career_rush_yds = 0
        career_rush_avg = 0
        career_rush_td = 0
        career_rec = 0
        career_rec_yds = 0
        career_rec_avg = 0
        career_rec_td = 0
        career_touch = 0
        career_scrim = 0
        career_yards_touch = 0
        career_rrtd = 0

        print( '"' + college_list[-1][4] + '"')

        junior_status = 0
        for i in college_list:
            print(i[2])
            if((i[2] == 'JR') or (i[2] == 'SR')):
                junior_status = 1

        if(junior_status != 1):
            continue


        while(college_list[-1][4] == ''):
            college_list.pop()
        
        print(junior_status)

        for i in college_list:
            print(i)
            if(i[4] != ''):
                career_games = career_games + int(i[4])
            if(college_pos == 'RB'):
                if(i[5] != ''):
                    career_att = career_att + int(i[5])
                if(i[6] != ''):
                    career_rush_yds = career_rush_yds + int(i[6])
                if(i[8] != ''):           
                    career_rush_td = career_rush_td + int(i[8])
                if(i[9] != ''):           
                    career_rec = career_rec + int(i[9])
                if(i[10] != ''):           
                    career_rec_yds = career_rec_yds + int(i[10])
                if(i[12] != ''):           
                    career_rec_td = career_rec_td + int(i[12])
                if(i[13] != ''):           
                    career_touch = career_touch + int(i[13])
                if(i[14] != ''):           
                    career_scrim = career_scrim + int(i[14])
                if(i[16] != ''):           
                    career_rrtd = career_rrtd + int(i[16])
            else:
                if(i[9] != ''):
                    career_att = career_att + int(i[9])
                if(i[10] != ''):
                    career_rush_yds = career_rush_yds + int(i[10])
                if(i[12] != ''):           
                    career_rush_td = career_rush_td + int(i[12])
                if(i[5] != ''):           
                    career_rec = career_rec + int(i[5])
                if(i[6] != ''):           
                    career_rec_yds = career_rec_yds + int(i[6])
                if(i[8] != ''):           
                    career_rec_td = career_rec_td + int(i[8])
                if(i[13] != ''):           
                    career_touch = career_touch + int(i[13])
                if(i[14] != ''):           
                    career_scrim = career_scrim + int(i[14])
                if(i[16] != ''):           
                    career_rrtd = career_rrtd + int(i[16])

        # Normalize stats           
        if(career_att != 0):
            career_rush_avg = career_rush_yds/career_att
        else:
            career_rush_avg = 0

        if(career_rec != 0):
            career_rec_avg = career_rec_yds/career_rec
        else:
            career_rec_avg = 0

        career_yards_touch = career_scrim/career_touch
        career_att = career_att/career_games
        career_rush_yds = career_rush_yds/career_games
        career_rush_td = career_rush_td/career_games
        career_rec = career_rec/career_games
        career_rec_yds = career_rec_yds/career_games
        career_rec_td = career_rec_td/career_games
        career_touch = career_touch/career_games
        career_scrim = career_scrim/career_games
        career_rrtd = career_rrtd/career_games
            
        last_season = college_list.pop

        games = 0
        att = 0
        rush_yds = 0
        rush_td = 0
        rec = 0
        rec_yds = 0
        rec_td = 0
        touch = 0
        scrim = 0
        yards_touch = 0
        rrtd = 0
        rush_avg = 0
        rec_avg = 0

        if(i[4] != ''):
            games = int(i[4])
        if(i[13] != ''):           
            touch = int(i[13])
        if(i[14] != ''):           
            scrim = int(i[14])
        if(i[16] != ''):           
            rrtd = int(i[16])

        if(college_pos == 'RB'):
            if(i[5] != ''):
                att = int(i[5])
            if(i[6] != ''):
                rush_yds = int(i[6])
            if(i[8] != ''):           
                rush_td = int(i[8])
            if(i[9] != ''):           
               rec = career_rec + int(i[9])
            if(i[10] != ''):           
                rec_yds = int(i[10])
            if(i[12] != ''):           
                rec_td = int(i[12])
        else:
            if(i[9] != ''):
                att = career_att + int(i[9])
            if(i[10] != ''):
                rush_yds = int(i[10])
            if(i[12] != ''):           
               rush_td = int(i[12])
            if(i[5] != ''):           
                rec = int(i[5])
            if(i[6] != ''):           
               rec_yds =  int(i[6])
            if(i[8] != ''):           
                rec_td = int(i[8])

        # Normalize last season
        if(att != 0):
            rush_avg = rush_yds/att
        if(rec != 0):
            rec_avg = rec_yds/rec
        if(touch !=0):
            yards_touch = scrim/touch

        att = att/games
        rush_yds = rush_yds/games
        rush_td = rush_td/games
        rec = rec/games
        rec_yds = rec_yds/games
        rec_td = rec_td/games
        touch = touch/games
        scrim = scrim/games
        rrtd = rrtd/games
    
        final_row = []
        final_row = [name, career_att, career_rush_yds, career_rush_avg, career_rush_td, career_rec, career_rec_yds, career_rec_avg, career_rec_td, career_touch, career_scrim, career_yards_touch, career_rrtd, att, rush_yds, rush_avg, rush_td, rec, rec_yds, rec_avg, rec_td, touch, scrim, yards_touch, rrtd] 

        writer.writerow(final_row)

    rookie_list = []
    z = 0
    rush_url = 'https://www.sports-reference.com/cfb/years/2020-rushing.html'
    ## Scrape for rushing stats
    res = requests.get(rush_url)
    soup = BeautifulSoup(res.text,features="html.parser")
    

    parsed = soup.findAll(
        'table', {
            'id': 'rushing'
        }
    )
    
    rows = parsed[0].findAll('td')

    column_len = 16

    grouped_rows = [
        rows[i:i+column_len] for i in range(0, len(rows), column_len)
    ]

    playerURL_list = []

    for i in grouped_rows:
        fullSTR = str(i)
        trimmed = re.search('href="(.*).html',fullSTR)
        playerURL = trimmed.group(1)
        playerURL = rootURL + playerURL 
        playerURL = playerURL.split(".html",1)[0] + '.html'
        playerURL_list.append(playerURL)

    rush_table = [map(lambda x: _strip_html(x), row) for row in grouped_rows]

    for i in rush_table:
        rookie_list.append(list(i))

    for i in rookie_list:
        name = i[0].replace("*","")
        if(name in rookie_names):
            z = z+1
            continue
        url = playerURL_list[z]
        res = requests.get(url)
        soup = BeautifulSoup(res.text, features="html.parser")

        if (': QB' in str(soup)):
            z = z + 1
            continue
        z=z+1

        print('---------------------------')


        parsed = soup.findAll(
            'table', {
                'id': 'rushing'
                    }
                )

        college_pos = 'RB'

        if not parsed:
                parsed = soup.findAll(
                    'table', {
                        'id': 'receiving'
                    }
                )

                college_pos = 'WR'

        try:
            rows = parsed[0].findAll('td')
        except:
            print('---')

        print(college_pos)
            
        column_len = 17

        grouped_rows = [
        rows[i:i+column_len] for i in range(0, len(rows), column_len)]

        table = [map(lambda x: _strip_html(x), row) for row in grouped_rows]

        college_list = []
        
        for i in table:
            k = list(i)
            college_list.append(k)

        # Remove table totals
        college_list.pop()

        print()
        print('"'+ name + '"')
        print()

        print(url)
        
        teams = []
        b = 0
        for i in college_list:
            if(i[0] not in teams):
                teams.append(i[0])
                b = b+1

        while(b > 1):
            college_list.pop()
            b = b - 1

        print( '"' + college_list[-1][4] + '"')     
                
        career_games = 0
        career_att = 0
        career_rush_yds = 0
        career_rush_avg = 0
        career_rush_td = 0
        career_rec = 0
        career_rec_yds = 0
        career_rec_avg = 0
        career_rec_td = 0
        career_touch = 0
        career_scrim = 0
        career_yards_touch = 0
        career_rrtd = 0

        junior_status = 0
        for i in college_list:
            if((i[2] == 'JR') or (i[2] == 'SR')):
                junior_status = 1

        if(junior_status != 1):
            continue

        while(college_list[-1][4] == ''):
            college_list.pop()   
    
        for i in college_list:
            print(i)
            if(i[4] != ''):
                career_games = career_games + int(i[4])
            if(college_pos == 'RB'):
                if(i[5] != ''):
                    career_att = career_att + int(i[5])
                if(i[6] != ''):
                    career_rush_yds = career_rush_yds + int(i[6])
                if(i[8] != ''):           
                    career_rush_td = career_rush_td + int(i[8])
                if(i[9] != ''):           
                    career_rec = career_rec + int(i[9])
                if(i[10] != ''):           
                    career_rec_yds = career_rec_yds + int(i[10])
                if(i[12] != ''):           
                    career_rec_td = career_rec_td + int(i[12])
                if(i[13] != ''):           
                    career_touch = career_touch + int(i[13])
                if(i[14] != ''):           
                    career_scrim = career_scrim + int(i[14])
                if(i[16] != ''):           
                    career_rrtd = career_rrtd + int(i[16])
            else:
                if(i[9] != ''):
                    career_att = career_att + int(i[9])
                if(i[10] != ''):
                    career_rush_yds = career_rush_yds + int(i[10])
                if(i[12] != ''):           
                    career_rush_td = career_rush_td + int(i[12])
                if(i[5] != ''):           
                    career_rec = career_rec + int(i[5])
                if(i[6] != ''):           
                    career_rec_yds = career_rec_yds + int(i[6])
                if(i[8] != ''):           
                    career_rec_td = career_rec_td + int(i[8])
                if(i[13] != ''):           
                    career_touch = career_touch + int(i[13])
                if(i[14] != ''):           
                    career_scrim = career_scrim + int(i[14])
                if(i[16] != ''):           
                    career_rrtd = career_rrtd + int(i[16])

        # Normalize stats           
        if(career_att != 0):
            career_rush_avg = career_rush_yds/career_att
        else:
            career_rush_avg = 0

        if(career_rec != 0):
            career_rec_avg = career_rec_yds/career_rec
        else:
            career_rec_avg = 0
            
        career_yards_touch = career_scrim/career_touch
        career_att = career_att/career_games
        career_rush_yds = career_rush_yds/career_games
        career_rush_td = career_rush_td/career_games
        career_rec = career_rec/career_games
        career_rec_yds = career_rec_yds/career_games
        career_rec_td = career_rec_td/career_games
        career_touch = career_touch/career_games
        career_scrim = career_scrim/career_games
        career_rrtd = career_rrtd/career_games

        last_season = college_list.pop

        games = 0
        att = 0
        rush_yds = 0
        rush_td = 0
        rec = 0
        rec_yds = 0
        rec_td = 0
        touch = 0
        scrim = 0
        yards_touch = 0
        rrtd = 0
        rush_avg = 0
        rec_avg = 0

        if(i[4] != ''):
            games = int(i[4])
        if(i[13] != ''):           
            touch = int(i[13])
        if(i[14] != ''):           
            scrim = int(i[14])
        if(i[16] != ''):           
            rrtd = int(i[16])

        if(college_pos == 'RB'):
            if(i[5] != ''):
                att = int(i[5])
            if(i[6] != ''):
                rush_yds = int(i[6])
            if(i[8] != ''):           
                rush_td = int(i[8])
            if(i[9] != ''):           
               rec = career_rec + int(i[9])
            if(i[10] != ''):           
                rec_yds = int(i[10])
            if(i[12] != ''):           
                rec_td = int(i[12])
        else:
            if(i[9] != ''):
                att = career_att + int(i[9])
            if(i[10] != ''):
                rush_yds = int(i[10])
            if(i[12] != ''):           
               rush_td = int(i[12])
            if(i[5] != ''):           
                rec = int(i[5])
            if(i[6] != ''):           
               rec_yds =  int(i[6])
            if(i[8] != ''):           
                rec_td = int(i[8])

        # Normalize last season
        if(att != 0):
            rush_avg = rush_yds/att
        if(rec != 0):
            rec_avg = rec_yds/rec
        if(touch !=0):
            yards_touch = scrim/touch

        att = att/games
        rush_yds = rush_yds/games
        rush_td = rush_td/games
        rec = rec/games
        rec_yds = rec_yds/games
        rec_td = rec_td/games
        touch = touch/games
        scrim = scrim/games
        rrtd = rrtd/games
    
        final_row = []
        final_row = [name, career_att, career_rush_yds, career_rush_avg, career_rush_td, career_rec, career_rec_yds, career_rec_avg, career_rec_td, career_touch, career_scrim, career_yards_touch, career_rrtd, att, rush_yds, rush_avg, rush_td, rec, rec_yds, rec_avg, rec_td, touch, scrim, yards_touch, rrtd] 

        writer.writerow(final_row)
 







