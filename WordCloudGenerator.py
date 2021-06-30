# Python program to generate WordCloud

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


class myWordCloud:
    comment_words = ''
    stopwords = set(STOPWORDS)

    def __init__(self, titleList):
        self.titleList = titleList

    def show(self):
        for val in self.titleList:
            val = str(val)
            tokens = val.split()
            # Converts each token into lowercase
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()
            self.comment_words += " ".join(tokens) + " "

        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              stopwords=self.stopwords,
                              min_font_size=10).generate(self.comment_words)

        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)

        plt.show()
