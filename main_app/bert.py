import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer


def generateResponse(question,paragraph):
    question = '''what is your daily ritual?'''

    paragraph = '''is 5-minute Friday on attention sharpening tools part 2 of 2 a mattress 5-minute Friday I introduced the concept that mindfulness training or a formal meditation practice are fundamentally nothing more than honing your attentional capacity I talked about two tools the guided meditation app headspace and the Brain sensing headband Muse that I used together as a part of my daily meditation ritual going back now many years at the end of the episode I disclosed that the coronavirus pandemic unexpectedly led to a recent dramatic acceleration in my commitment to deliver it might as well as a corresponding dramatic acceleration inattentional benefits let's dig into that now after a few months of covid-19 down I was in an emotionally challenging. I'm a highly social person I love hanging out with groups of friends and I even love going into the office to spend time with my witty and fascinating colleagues so while I've been meditating daily for years but typically for only up to 10 minutes a day I had a sense that I needed to deepen my meditation practice further to confront he's challenging lockdown related emotions. For several months now along with being sure to use my muse brain wave feedback headband every single day while digesting a headspace guided meditation I've also been gradually lengthening my meditation sessions more specifically in the summer of 2020 I began using the headspace 365 pack which was the original 365 days series of meditations that featured in the app when it was first launched many years ago attack of the 365 pack in part because I had already completed every other pack of medications that are available in the headspace app but also because I knew it would force me to after 6 years of dealing from his training extend the length of my daily sessions the headspace 365 pack starts with 10 10 minute sessions then goes on to 15 15 minute sessions and then for the remaining 340 days in the 365-day pack 20-minute long sessions now I don't have time every single day or more accurately I don't get time every single day for 20 minutes of meditation so I do a 20-minute session from the 365 pack on a half of days and for the sake of maintaining my daily ritual of doing every some structured mindfulness training on the other half of days I do the quote-unquote today's meditation from the headspace app home screen reset for 3 or 5 or at most a 10 minute session it's on the days where I do the 20-minute meditation however that I've noticed the dramatic acceleration in benefits I noticed that I am now committed to three days a week where I do a particularly long session the guided headspace 365 session always ends after 20 minutes but I set the Muse headband to continue sending my brain waves for unguided meditation simply bring my attention back to my breath whenever a drift away for one minute longer each week so two weeks ago I was doing a 28 minute long session 3 days a week last week I was doing 20 minute sessions three days a week and this week I did three half hour sessions over the course of the week I'm going to continue experimenting with adding another minute each week until I noticed that the benefits start. So maybe that'll be around the 45-minute Mark or something like that but I really don't know the point is that by doing these longer sessions even after years of meditating without missing a day I've noticed a huge impact on my attention span challenges suddenly seem trivial in manageable I fly through my to do list during the day I don't waste time I do become consumed by distracting or unhelpful thoughts about you relevant events happening on the internet I'm present with my senses in my body in the moment I'm more creative I'm more confident and I'm even more patient for empathetic and loving it really it really has been a journey as he might now guess I highly recommend training your attention I believe it can ask you benefits on your data science career and more generally in your life I recommend starting small with training your attention with a structured guided mindfulness practice but block off the time on your calendar for it in advance or put it is a daily to-do item that workers on your phone consistency is the key to Habit formation in the beginning not the duration of the sessions initially you could start with one minute meditations every day for a week and then maybe just stay there but it's a minute starts to feel Wheezy then in the second week go up to two minutes every day and so on these small incremental changes in eventually accumulate too long and hugely beneficial sessions although even those shorts sessions and whatever you do finish the session reward yourself have a piece of chocolate or have a cup of coffee whatever you find intrinsically satisfying by rewarding yourself Force the behavior and it will become easier and easier to maintain a daily mindfulness practice with will grow more and more as I detailed already I've been using headspace reviews for many years now I do think they're outstanding and I highly recommend them but I don't have any paid sponsorships or anything like that I'm not partial to go to tools for any reason other than my personal positive experience with some other apps that I've experimented with more briefly or have been recommended to me it's seem to be really great our Sam Harris waking up 10% happier calm and if you're looking for something completely free you can check out insight timer all right that's it those are my tips in tools for sharpening your attention Happy Trails and catch you next week for another episode of 5-minute Friday'''

    encoding = tokenizer.encode_plus(text=question,text_pair=paragraph)
    inputs = encoding['input_ids']
    sentence_embedding = encoding['token_type_ids']
    tokens = tokenizer.convert_ids_to_tokens(inputs) 
    tokenized_sentence = tokenizer.encode(text = question, text_pair = paragraph, padding=True, truncation=True,max_length=50, add_special_tokens = True)

    start_scores, end_scores = model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]),return_dict=False)

    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)

    answer = ' '.join(tokens[start_index:end_index+1])

    corrected_answer = ''

    for word in answer.split():
        #If it's a subword token
        if word[0:2] == '##':
            corrected_answer += word[2:]
        else:
            corrected_answer += ' ' + word
    print(corrected_answer)
    return corrected_answer


#Model
# model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
#Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
x = generateResponse('abc','pqr')