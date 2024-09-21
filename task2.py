# -*- coding: utf-8 -*-
import requests
import matplotlib.pyplot as plt
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor



def map_function(text):
    words = text.split()
    return [(word.lower(), 1) for word in words]



def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()



def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced



def map_reduce(text):
    mapped_values = map_function(text)

    shuffled_values = shuffle_function(mapped_values)

    reduced_values = reduce_function(shuffled_values)

    return reduced_values



def visualize_top_words(word_counts, top_n=10):
    sorted_words = sorted(word_counts.items(),
                          key=lambda item: item[1], reverse=True)

    top_words = sorted_words[:top_n]

    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel('Слова')
    plt.ylabel('Частота')
    plt.title(f'Топ {top_n} найчастіше вживаних слів')
    plt.xticks(rotation=45)
    plt.show()


def fetch_text(url):
    response = requests.get(url)
    response.raise_for_status() 
    return response.text


def main(url):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(fetch_text, url)
        text = future.result()

        word_counts = map_reduce(text)

        visualize_top_words(word_counts, top_n=15)


if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/11/11-0.txt"

    main(url)
