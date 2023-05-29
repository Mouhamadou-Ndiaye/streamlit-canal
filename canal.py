import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import plotly.express as px

from PIL import Image


# Functions

# ---------------------Data Observation-----------------------------------------#

def data_observation(data):
    st.markdown("---")
    df = pd.read_csv(data + '.csv', encoding='utf-8', delimiter=",")
    st.subheader(data + ' data')
    code_1 = data + '''.head(10)'''
    st.code(code_1, language='python')
    st.dataframe(df.head(10))
    st.subheader('Description of the data')
    st.table(df.describe())



def count_rows(rows):
    return len(rows)


def drop_col(hyconiq) :
    hyconiq_drop = hyconiq
    for x in range(1,17) :
        hyconiq_drop = hyconiq_drop.drop(columns = [rf'taggedFullName{x}',rf'taggedUsername{x}'])
    hyconiq_drop = hyconiq_drop.drop(columns = ['playCount','videoDuration','query','caption','profileUrl','query','location','locationId','viewCount','username','postId','postUrl','videoUrl','imgUrl','fullName','likedByViewer'])
    pd.DataFrame((hyconiq_drop))
    return hyconiq_drop

from datetime import datetime


def get_weekday(dt):
    return dt.weekday()


def get_hour(dt):
    return dt.hour


def get_month(dt):
    return dt.month


def get_dom(dt):
    return dt.day


def time_gestion(data):
    data['pubDate'] = data['pubDate'].map(pd.to_datetime)
    data['weekday'] = data['pubDate'].map(get_weekday)
    data['hour'] = data['pubDate'].map(get_hour)
    data['month'] = data['pubDate'].map(get_month)
    data['day'] = data['pubDate'].map(get_dom)
    return data


def typeconvert(study_data):
    study_data['type'] = (study_data['type']).apply(lambda x: str(x))
    study_data['isSidecar'] = (study_data['isSidecar']).apply(lambda x: str(x))
    return study_data

def initializing(study_data):
    hycoviz = study_data.drop(columns=['pubDate', 'timestamp'])
    hycoviz = hycoviz.drop_duplicates()
    return hycoviz


def frequency(study_data, freq, var):
    fig = px.bar(study_data, x=study_data[freq], y=study_data[var], color=study_data['month'], title= var + ' by ' + freq)
    st.plotly_chart(fig)


def frequecy_list(study_data):

    col1, col2 = st.columns(2)

    sf = col1.selectbox(
        "Sélectionner",  # Drop Down Menu Name
        [
            'likeCount',
            'commentCount',
        ]
    )

    sd = col2.selectbox(
        "Sélectionner votre temporalité",  # Drop Down Menu Name
        [
            'hour',
            'day',
            'weekday',
            'month',
        ]
    )

    frequency(study_data, sd, sf)

def typestudy(study_data, freq, var, type):
    fig = px.bar(study_data, x=study_data[freq], y=study_data[var], color=study_data[type], barmode="group", title= var + ' of ' + type + ' by ' + freq)
    st.plotly_chart(fig)

def type_list(study_data):

    col1, col2, col3 = st.columns(3)

    sf = col1.selectbox(
        "Sélectionner",  # Drop Down Menu Name
        [
            'likeCount',
            'commentCount',
        ]
    )

    se = col2.selectbox(
        "Sélectionner",  # Drop Down Menu Name
        [
            'type',
            'isSidecar',
        ]
    )

    sd = col3.selectbox(
        "Sélectionner votre temporalité",  # Drop Down Menu Name
        [
            'hour',
            'day',
            'weekday',
            'month',
        ]
    )

    typestudy(study_data, sd, sf,se)

def top10liked (pub_stat) :
    pub_stat_like_top10 = pub_stat.sort_values(by = ['likeCount'], ascending=False).head(20)
    fig = px.pie(pub_stat_like_top10,values = pub_stat_like_top10['likeCount'] , names = pub_stat_like_top10['description'],title='Top Like Post of your account', color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)


def top10Commented (pub_stat) :
    pub_stat_comment_top10 = pub_stat.sort_values(by = ['commentCount'], ascending=False).head(20)
    fig = px.pie(pub_stat_comment_top10,values = pub_stat_comment_top10['commentCount'] , names = pub_stat_comment_top10['description'], title = 'Top Comment post of your account', color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

def heatmap(data_drop):
    fig = plt.figure(figsize=(10, 4))
    datag = data_drop.groupby(['weekday', 'hour']).apply(count_rows).unstack()
    heatmap = sns.heatmap(datag, linewidths=.5)
    plt.title('Heatmap by Hour and weekdays', fontsize=15)
    heatmap.set_yticklabels(('Lun Mar Mer Jeu Ven Sam Dim').split(), rotation='horizontal')
    st.pyplot(fig)
# In this function we're going to look at the data and his missing values

# ---------------------Data Processing-----------------------------------------#
# How to manage the columns in my data
# In this function we're going to delete the column we don't use in our dataviz and rename the columns


if __name__ == "__main__":

    with st.sidebar:
        selected = option_menu("CanalViz",
                               ["Presentation", "Transforming the Data", "Frequency", "Type Study", "Top 10"
                                   , "n._mouhamadou_", "621565314", "mouhamadou.ndiaye@efrei.net"
                                ],
                               icons=['instagram', 'gear', 'calendar', 'search', 'file-bar-graph', 'instagram', 'telephone', 'envelope'
                                      ], menu_icon="cast", default_index=1)

    st.title("Welcome to my CanalViz ✨")

    if selected == "Presentation":

        from PIL import Image

        orangeImage = Image.open('canal.png')
        orangeImage2 = Image.open('canal1.jpg')


        st.image(orangeImage, width=700)
        st.title("Presentation 🎤")
        st.markdown("Canal qui est une chaîne de télévision française créé depuis 1984 propose des contenus adaptés à leurs clients. "
                    "La réussite de cette entreprise s'est effectuée grâce à la compréhension et à l'anticipation des attentes de ses clients. De nos jours, cette prévision peut s'améliorer "
                    "grâce à l'analyse des données des plateformes d'interaction client comme Instagram.")
        st.image(orangeImage2,width=700)

        st.markdown('La data visualisation que je vais vous présenter se base sur votre compte instagram, et montre des statistiques sur le nombre de likes ou de comments '
                    ', le comportement de ces derniers à travers les jours et heures, et bien plus encore ...  Bonne visualisation ❤️.')

    if selected == "Transforming the Data":
        from PIL import Image

        st.title("Discovering the data 📚")
        discover = Image.open('discover.jpg')
        st.image(discover)
        st.title('Canal Data')
        st.markdown('Voici la base de données sur laquelle je vais faire ma data visualisation.')
        data_observation('canal')

        st.markdown('---')

        st.title("Transforming the data 📚")
        process = Image.open('process.jpg')
        st.image(process)
        st.subheader('Data Drop')

        st.write(
            'Comme vous pouvez le voir il y a des colonnes qui on des valeurs manquantes et des colonnes répititives. '
            'Je vais donc supprimer ces colonnes afin de procéder à la visualisation')

        hermes = pd.read_csv('canal.csv')

        st.subheader('Canal data after transformation')
        hermes= drop_col(hermes)
        st.dataframe(hermes.head(10))
        st.subheader('Rajout des colonnes jour, mois, heure')
        st.markdown(
            'Ici nous avons rajouté les colonnes day, month et hour afin de pouvoir une étude temporelle des posts')
        hermes = time_gestion(hermes)
        hermes  = initializing(hermes)
        st.dataframe(hermes.head(10))

    if selected == "Frequency":
        hermes = pd.read_csv('canal.csv')
        hermes = drop_col(hermes)
        hermes = time_gestion(hermes)
        hermes = typeconvert(hermes)
        hermes = initializing(hermes)

        st.title('Statistiques de like et de comments par post')
        st.markdown(
            'Dans cette visualisation, découvrez les statistiques des likes et comments de vos posts selon le jour, l heure ou le mois')

        post = Image.open('post.jpg')
        st.image(post)

        frequecy_list(hermes)

    if selected == "Type Study":
        hermes = pd.read_csv('canal.csv')
        hermes = drop_col(hermes)
        hermes = time_gestion(hermes)
        hermes = typeconvert(hermes)
        hermes = initializing(hermes)

        st.title('Statistiques de like et de comments par type de post')
        st.markdown(
            'Il est aussi important de connaître le type de post qui touche le plus de client, par le type de post que ça soit une photo, une vidéo ou un carrousel')

        media = Image.open('media.jpg')
        st.image(media)

        type_list(hermes)

    if selected == "Top 10":
        hermes = pd.read_csv('canal.csv')
        hermes = drop_col(hermes)
        hermes = time_gestion(hermes)
        hermes = typeconvert(hermes)
        hermes = initializing(hermes)

        st.title('Top 10')
        top = Image.open('top.jpg')
        st.image(top)

        st.title('Top 10 Liked post')
        st.markdown('Ici découvrez vos 10 posts qui ont le plus eu de likes')
        top10liked(hermes)

        st.title('Top 10 Commented post')
        st.markdown('Ici découvrez vos 10 posts qui ont le plus eu de comments')
        top10Commented(hermes)

        st.title('Bonus Correlation')
        heatmap(hermes)






