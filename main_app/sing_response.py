from utils import *
import argparse
#from utils import parse_config

logger = setup_logger(__name__)

general_params=None
device=None
seed=None
debug=None
generation_pipeline_kwargs=None
generator_kwargs=None
prior_ranker_weights=None
cond_ranker_weights=None
chatbot_params=None
max_turns_history=None
generation_pipeline=None
ranker_dict=None
turns = []

# def main():
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '--type',
    type=str,
    default='telegram',
    help="Type of the conversation to run: telegram, console or dialogue"
)
arg_parser.add_argument(
    '--config',
    type=str,
    default='my_chatbot.cfg',
    help="Path to the config"
)
args = arg_parser.parse_args()
config_path = args.config#string is the pfile path of my_config.cfg and can be set manually
config = parse_config(config_path)


def start_message():
    print("Bot:",
          "Just start texting me. "
          "If I'm getting annoying, type \"/reset\". "
          )


def reset_message():
    print("Bot:", "Beep beep!")


def initialize(**kwargs):
    """Run the console bot."""
    global general_params
    global device
    global seed
    global debug
    global generation_pipeline_kwargs
    global generator_kwargs
    global prior_ranker_weights
    global cond_ranker_weights
    global chatbot_params
    global max_turns_history
    global generation_pipeline
    global ranker_dict
    global turns
    # Extract parameters
    general_params = kwargs.get('general_params', {})
    device = general_params.get('device', -1)
    seed = general_params.get('seed', None)
    debug = general_params.get('debug', False)

    generation_pipeline_kwargs = kwargs.get('generation_pipeline_kwargs', {})
    generation_pipeline_kwargs = {**{
        'model': 'microsoft/DialoGPT-medium'
    }, **generation_pipeline_kwargs}

    generator_kwargs = kwargs.get('generator_kwargs', {})
    generator_kwargs = {**{
        'max_length': 1000,
        'do_sample': True,
        'clean_up_tokenization_spaces': True
    }, **generator_kwargs}

    prior_ranker_weights = kwargs.get('prior_ranker_weights', {})
    cond_ranker_weights = kwargs.get('cond_ranker_weights', {})

    chatbot_params = kwargs.get('chatbot_params', {})
    max_turns_history = chatbot_params.get('max_turns_history', 2)

    # Prepare the pipelines
    generation_pipeline = load_pipeline('text-generation', device=device, **generation_pipeline_kwargs)
    ranker_dict = build_ranker_dict(device=device, **prior_ranker_weights, **cond_ranker_weights)

    # Run the chatbot
    logger.info("Running the console bot...")

    turns = []
    start_message()

#if args.type == 'console':
initialize(**config)

def bot_response(prompt) :

    global general_params
    global device
    global seed
    global debug
    global generation_pipeline_kwargs
    global generator_kwargs
    global prior_ranker_weights
    global cond_ranker_weights
    global chatbot_params
    global max_turns_history
    global generation_pipeline
    global ranker_dict
    global turns

    try:
        #while True:
            #prompt = input("User: ")
        if max_turns_history == 0:
            turns = []
        if prompt.lower() == '/start':
            start_message()
            turns = []
            #continue
        if prompt.lower() == '/reset':
            reset_message()
            turns = []
            #continue
        elif prompt.startswith('/'):
            print('Command not recognized.')
            #continue
        # A single turn is a group of user messages and bot responses right after
        turn = {
            'user_messages': [],
            'bot_messages': []
        }
        turns.append(turn)#pass by value not reference
        turn['user_messages'].append(prompt)
        # Merge turns into a single prompt (don't forget delimiter)
        prompt = ""
        from_index = max(len(turns) - max_turns_history - 1, 0) if max_turns_history >= 0 else 0
        for turn in turns[from_index:]:
            # Each turn begins with user messages
            for user_message in turn['user_messages']:
                prompt += clean_text(user_message) + generation_pipeline.tokenizer.eos_token
            for bot_message in turn['bot_messages']:
                prompt += clean_text(bot_message) + generation_pipeline.tokenizer.eos_token

        # Generate bot messages
        bot_messages = generate_responses(
            prompt,
            generation_pipeline,
            seed=seed,
            debug=debug,
            **generator_kwargs
        )
        if len(bot_messages) == 1:
            bot_message = bot_messages[0]
        else:
            bot_message = pick_best_response(
                prompt,
                bot_messages,
                ranker_dict,
                debug=debug
            )
        turn['bot_messages'].append(bot_message)
        return bot_message
    except KeyboardInterrupt:
        exit()
    except:
        raise

