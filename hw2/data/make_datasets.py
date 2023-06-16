import pandas as pd
import ast

characters = pd.read_csv('raw/movie_characters_metadata.tsv', sep='\t', on_bad_lines='skip', header=None,
                         names=['characterID', 'character', 'movieID', 'movie_title', 'gender', 'position'])
conversations = pd.read_csv('raw/movie_conversations.tsv', sep='\t', on_bad_lines='skip', header=None,
                            names=['characterID_1', 'characterID_2', 'movieID', 'chrono'])
lines = pd.read_csv('raw/movie_lines.tsv', sep='\t', on_bad_lines='skip', header=None,
                    names=['lineID', 'characterID', 'movieID', 'character', 'text'])
titles = pd.read_csv('raw/movie_titles_metadata.tsv', sep='\t', on_bad_lines='skip', header=None,
                     names=['movieID', 'movie_title', 'movie_year', 'rating', 'imdb_votes', 'genres'])

characters.dropna(inplace=True)
conversations.dropna(inplace=True)
lines.dropna(inplace=True)
titles.dropna(inplace=True)


def map_vals(col1, col2):
    map_val = dict(zip(col1, col2))
    return map_val


lines_id_character = map_vals(lines.lineID, lines.characterID)
lines_id_text = map_vals(lines.lineID, lines.text)
characters_id_names = map_vals(characters.characterID, characters.character)
characters_id_gender = map_vals(characters.characterID, characters.gender)


def delim(string):
    nstring = ast.literal_eval(string)
    res = ['L' + i for i in nstring[0].split('L')[1:]]
    return res


titles['genres'] = titles['genres'].apply(lambda x: [i[1:-1] for i in x.strip('][').split(' ')])
conversations['chrono'] = conversations['chrono'].apply(lambda x: delim(x))
conversations['characters'] = conversations['chrono'].apply(lambda x: [
    lines_id_character[i] if i in lines_id_character.keys() else 'unknown_character' for i in x])
conversations['genders'] = conversations['characters'].apply(lambda x: [
    characters_id_gender[i] if i in characters_id_gender.keys() else '?' for i in x])
conversations['replics'] = conversations['chrono'].apply(lambda x: [
    lines_id_text[i] if i in lines_id_text.keys() else 'unknown_text' for i in x])
conversations['names'] = conversations['characters'].apply(lambda x: [
    characters_id_names[i] if i in characters_id_names.keys() else 'unknown_character ' for i in x])

df_dump = conversations.drop(columns=['characterID_1', 'characterID_2'])
df = df_dump.merge(titles, on='movieID', how='left')
df = df.drop(columns=['movie_year', 'rating', 'imdb_votes'])

df['text_length'] = df['replics'].apply(lambda x: len(''.join(eval(str(x)))))
dff = df.loc[((df['text_length'] > 150) & (df['text_length'] < 201))]


if __name__ == "__main__":
    df.to_csv('processed/films_data.csv', index=False) # merged df
    dff.to_csv('processed/films_data_to_label.csv', index=False) # df for labeling
    print(df.info(memory_usage='deep'))
    print(df.shape)
    print(dff.info(memory_usage='deep'))
    print(dff.shape)
