import pandas as pd
import streamlit as st


df = pd.read_csv("data/processed/films_data.csv")

emotions = ["Positive","Neutral", "Negative", "Happy", "Satisfied",
            "Sad", "Betrayed", "Motivated", "Hopeful", "Sarcastic",
            "Philosophical", "Mischievous"]


def app():
    st.title("Dialogue Emotion Annotation Tool")
    movies = df["movie_title"].unique()
    movie = st.selectbox("Select a movie", movies, key='movie_select')

    data = df[df["movie_title"] == movie].copy()
    data["emotions"] = [[] for _ in range(len(data))]

    # Display the dialogues for the selected movie
    for i, row in data.iterrows():
        names = eval(row["names"])
        replics = eval(row["replics"])
        dialogues = [f"{name}: {replic}" for name, replic in zip(names, replics)]
        dialogue_text = "\n\n".join(dialogues)
        st.write(f"**Dialogue {i + 1}** \n\n {dialogue_text}")

        emotions_selected = []
        for j, replic in enumerate(replics):
            emotion = st.multiselect(f"Select emotion(s) for replic {j+1}", emotions, key=f'emotions_select_{i}_{j}')
            emotions_selected.append(emotion)

        st.write("Selected emotions:", emotions_selected)

        data.at[i, "emotions"] = emotions_selected

        st.markdown("---")

    if st.button("Save labeled data"):
        data.to_csv("films_data_labeled.csv", index=False)


if __name__ == "__main__":
    app()
