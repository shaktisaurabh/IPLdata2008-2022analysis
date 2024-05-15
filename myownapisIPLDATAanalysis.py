import numpy as np 
import pandas as pd 
ipl_ball_by_ball=pd.read_csv(r"C:\Users\LENOVO\Downloads\IPL_Ball_by_Ball_2008_2022 - IPL_Ball_by_Ball_2008_2022.csv")
ipl_matches=pd.read_csv(r"C:\Users\LENOVO\Downloads\IPL_Matches_2008_2022 - IPL_Matches_2008_2022.csv") 
dk1=ipl_ball_by_ball.merge(ipl_matches,on='ID') 
dk1['bowling_team']=dk1['Team1']+dk1['Team2'] 
dk1['bowling_team']=dk1[['BattingTeam','bowling_team']].apply(lambda x:str(x.values[1]).replace(x.values[0],''),axis=1)

def isbowler_run(x):
    if x[1] in ['legbyes','byes','penalty']:
        return 0 
    else:
        return x[0]
dk1['bowler_run']=dk1[['total_run','extra_type']].apply(isbowler_run,axis=1) 

def isbowler_wicket(x):
    if x[0] in ['caught','caught and bowled','bowled','stumped','lbw','hit wicket']:
        return x[1] 
    else:
        return 0 
dk1['bowler_wicket']=dk1[['kind','isWicketDelivery']].apply(isbowler_wicket,axis=1) 

def teamlist():
    a1=list(ipl_ball_by_ball['BattingTeam'].unique()) 
    return {
        'team_list':str(a1)
    }

def team1Vteam2(team1,team2):
    dhammi=ipl_matches[((ipl_matches['Team1']==team1)&(ipl_matches['Team2']==team2))|((ipl_matches['Team1']==team2)&(ipl_matches['Team2']==team1))]
    if dhammi.empty:
        return {
            'total_matches':str(0),
            team1:str(0),
            team2:str(0),
            'no_result':str(0)
        }
    else:
        try:
            win_team1=dhammi['WinningTeam'].value_counts()[team1] 
        except:
            win_team1=0
        try:
            win_team2=dhammi['WinningTeam'].value_counts()[team2]
        except:
            win_team2=0
        no_result=dhammi['WinningTeam'].isnull().sum() 
        total_matches=dhammi.shape[0] 
        return {
            'total_matches':str(total_matches),
            team1:str(win_team1),
            team2:str(win_team2),
            'no_result':str(no_result)
        } 
    
def all_record(team1):
    dhammi1=ipl_matches[((ipl_matches['Team1']==team1)|(ipl_matches['Team2']==team1))] 
    total_matches=dhammi1.shape[0] 
    won=dhammi1[dhammi1['WinningTeam']==team1].shape[0] 
    no_result=dhammi1['WinningTeam'].isnull().sum() 
    lost=total_matches-(won+no_result)
    titles=dhammi1[(dhammi1['MatchNumber']=='Final')&(dhammi1['WinningTeam']==team1)].shape[0] 
    return {
        'total_matches':str(total_matches),
        'won':str(won),
        'lost':str(lost),
        'no_result':str(no_result),
        'titles':str(titles)
    }

def teamAPI(team1):
    dhammi1=ipl_matches[((ipl_matches['Team1']==team1)|(ipl_matches['Team2']==team1))] 
    self_record=all_record(team1)
    TEAMS=dhammi1['Team1'].unique() 
    vs_each_team={team2:team1Vteam2(team1,team2) for team2 in TEAMS} 
    overall_record={
        'overall_record':self_record,
        'against':vs_each_team
    }
    return overall_record

def player_record(player,df=dk1):
    if df.empty:
        return np.nan
    a1=df[df['batter']==player]
    if a1.empty:
        return np.nan
    num_innings=len(a1['ID'].unique())
    runs=a1['batsman_run'].sum() 
    fours=a1[a1['batsman_run']==4].shape[0]
    sixes=a1[a1['batsman_run']==6].shape[0]
    average=(a1['batsman_run'].sum())/(a1[a1['player_out']==player].shape[0]) 
    strike_rate=(a1['batsman_run'].sum())/(a1[~(a1['extra_type']=='wides')].shape[0])*100 
    ok=a1.groupby('ID')['batsman_run'].sum() 
    fifties=ok[ok>=50].shape[0] 
    hundreds=ok[ok>=100].shape[0]
    high_score=ok.sort_values(ascending=False).head(1).values[0]
    outs=a1[a1['player_out']==player].shape[0] 
    not_outs=len(ok)-outs 
    mom=df[df['Player_of_Match']==player].drop_duplicates('ID',keep='first').shape[0] 
    return {
        'num_innings':str(num_innings), 
        'runs':str(runs),
        'fours':str(fours),
        'sixes':str(sixes),
        'average':str(average),
        'strike_rate':str(strike_rate),
        'fifties':str(fifties),
        'hundreds':str(hundreds),
        'high_score':str(high_score),
        'outs':str(outs),
        'not_outs':str(not_outs),
        'mom':str(mom)
    }

def batsmanvsteam(batsman,team):
    anb=dk1[dk1['bowling_team']==team] 
    return player_record(batsman,anb) 

def bowler_record(bowler,df=dk1):
    if df.empty:
        return np.nan 
    a1=df[df['bowler']==bowler] 
    if a1.empty:
        return np.nan 
    tot_innings=a1['ID'].unique().shape[0] 
    wickets=a1['bowler_wicket'].sum() 
    nballs=a1[~(a1['extra_type'].isin(['wides','noballs']))].shape[0] 
    runs=a1['bowler_run'].sum() 
    if nballs:
        eco=(runs/nballs)*6 
    else:
        eco=0 
    if wickets:
        avg=runs/wickets 
    else:
        avg=0 
    if wickets:
        strike_rate=nballs/wickets 
    else:
        strike_rate=np.nan 
    fours=a1[a1['batsman_run']==4].shape[0]
    sixes=a1[a1['batsman_run']==6].shape[0]
    gb1=a1.groupby('ID')[['bowler_run','bowler_wicket']].sum() 
    g2=gb1.sort_values(['bowler_wicket','bowler_run'],ascending=(False,True)).head(1) 
    best_figure=f"{g2['bowler_wicket'].values[0]}/{g2['bowler_run'].values[0]}" 
    g3=gb1.sort_values(['bowler_wicket','bowler_run'],ascending=(False,True)) 
    w3=g3[g3['bowler_wicket']>=3].shape[0]
    total_mom=a1[a1['Player_of_Match']==bowler].drop_duplicates('ID',keep='first').shape[0] 
    return {
        'total_innings':str(tot_innings),
        'wickets':str(wickets),
        'economy':str(eco),
        'average':str(avg),
        'strikeRate':str(strike_rate),
        'fours':str(fours),
        'sixes':str(sixes),
        'best_figure':str(best_figure),
        '3+w':str(w3),
        'mom':str(total_mom)
    } 

def bowlervsteam(bowler,team):
    aq=dk1[dk1['BattingTeam']==team] 
    return bowler_record(bowler,aq) 

    