from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def preflop_ai_feedback(card1, card2):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Assume I am playing Texas hold em. You will be provided with my two cards making up my hand and your task is to generate 20 words or less response for tips, summary, what to look for, or other advice on how to play given these cards."
            },

            {
                "role": "user",
                "content": f"First Card: {card1}\n    Second Card: {card2}."
            }
        ],
        temperature=0.8,
        max_tokens=64,
        top_p=1   
    )
    return response.choices[0].message.content

def final_ai_feedback(card1, card2, card3, card4, card5, card6, card7):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Assume I am playing Texas hold em and all 5 cards are on the table. You will be provided with my two cards making up my hand along with 5 community cards within the table and your task is to give advice on the analysis of the strength of my 5 best cards, what to look out for, and if I have a likely shot of winning the pot in a table of 5 other players. Generate this response in 50 words or less please."
            },   

            {
                "role": "user",
                "content": f"My Hand: {card1},{card2}\n    Community Cards: {card3}, {card4}, {card5}, {card6}, and {card7}."
            }
        ],
        temperature=0.8,
        max_tokens=64,
        top_p=1   
    )
    return response.choices[0].message.content