import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import Classes.Cherwell_Interpreter as Handler
from string import punctuation
from collections import Counter
from heapq import nlargest

raw_cherwell_file = './Data/Source/converted_csv.json'
cherwell_data = Handler.read_json(raw_cherwell_file)
nlp = spacy.load("en_core_web_lg")
stop_words = list(STOP_WORDS)
punctuation = punctuation + '\n'

def find_agents(cherwell_data):
    agents = {}
    for row in cherwell_data:
        ticket = Handler.Ticket_Details(row)

        if ticket.assignee not in agents:
            agents[ticket.assignee] = {}

    return agents

def get_scores(cherwell_data):
    agent_list = find_agents(cherwell_data)
    for row in cherwell_data:
        ticket = Handler.Ticket_Details(row)

        assignee = ticket.assignee
        score = ticket.csat_score

        for agent in agent_list:
            if assignee == agent:
                if score != "":
                    agent_list[agent][score] = []
    return agent_list


def get_summaries(cherwell_data):
    agents_and_scores = get_scores(cherwell_data)

    for row in cherwell_data:
        ticket = Handler.Ticket_Details(row)

        assignee = ticket.assignee
        score = ticket.csat_score
        summary = ticket.csat_summary

        for agent in agents_and_scores:
            if assignee == agent:
                for value in agents_and_scores[agent]:
                    if score == value:
                        if summary != "":
                            agents_and_scores[agent][score].append(summary)
                        if summary == "":
                            agents_and_scores[agent][score].append("No comment")
    
    return agents_and_scores


def get_word_frequencies(agent_scores_and_summaries):
    agent_data = agent_scores_and_summaries
    
    weighted_scores = {}
    
    for agent in agent_data:
        weighted_scores[agent] = {}
        for score in agent_data[agent]:
            weighted_scores[agent][score] = {}
            score_word_freq = {}
            for summary in agent_data[agent][score]:
                if summary != "No comment":
                    doc = nlp(summary)

                    for word in doc:
                        if word.text.lower() not in stop_words:
                            if word.text.lower() not in punctuation:
                                if word.pos_ != "PROPN":
                                    if word.text not in score_word_freq.keys():
                                        score_word_freq[word.text] = 1
                                    else:
                                        score_word_freq[word.text] += 1
           
            weighted_scores[agent][score] = score_word_freq
    
    return weighted_scores


def get_normalised_word_frequencies(word_frequencies):
    for agent in word_frequencies:
        for score in word_frequencies[agent]:
            if score != "":
                for word in word_frequencies[agent][score]:
                    word_frequencies[agent][score][word] = word_frequencies[agent][score][word] / max(word_frequencies[agent][score].values())
    return word_frequencies


def get_sentence_scores(agents_scores_and_summaries, normalised_word_scores):
    sentence_scores = {}

    for agent in agents_scores_and_summaries:
        sentence_scores[agent] = {}
        for score in agents_scores_and_summaries[agent]:
            sentence_scores[agent][score] = {}
            score_word_freq = {}
            for summary in agents_scores_and_summaries[agent][score]:
                if summary != "No comment":
                    doc = nlp(summary)

                    sentence_tokens = [sent for sent in doc.sents]
                    # print(sentence_tokens)
                    for sent in sentence_tokens:
                        for word in sent:
                            if word.text.lower() in normalised_word_scores[agent][score].keys():
                                if sent not in sentence_scores.keys():
                                    sentence_scores[agent][score][sent] = normalised_word_scores[agent][score][word.text.lower()]
                                else:
                                    sentence_scores[agent][score][sent] += normalised_word_scores[agent][score][word.text.lower()]
    return sentence_scores



if __name__ == "__main__":
    agents_scores_and_summaries = get_summaries(cherwell_data)
    word_frequencies = get_word_frequencies(agents_scores_and_summaries)
    normalised_word_scores = get_normalised_word_frequencies(word_frequencies)
    sentence_scores = get_sentence_scores(agents_scores_and_summaries, normalised_word_scores)

    for agent in sentence_scores:
        print(f"{agent}")
        for score in sentence_scores[agent]:
            summary = nlargest(n = 3, iterable = sentence_scores[agent][score], key = sentence_scores[agent][score].get)

            print(f"{score}: {summary}")