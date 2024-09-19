import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import TOKEN, CAPTION, PIC, API_ID, API_HASH
from IMDb import search_movies, fetch_movie_details

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = InlineKeyboardMarkup()
    row1 = [
        InlineKeyboardButton("Channel", url='https://t.me/botsupports_og'),
        InlineKeyboardButton("Group", url='https://t.me/+uetvaBu_d5k5MTU1')
    ]
    keyboard.add(*row1)
    keyboard.add(InlineKeyboardButton("🍿 Updates", url='https://t.me/Hollywood_in_HindiHD'))
    bot.send_photo(chat_id=message.chat.id, photo=PIC, caption=CAPTION, parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(commands=['movie'])
def handle_movie_command(message):
    bot.send_message(message.chat.id, "Send me a movie name to get details.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text
    if query:
        results = search_movies(query)
        if results:
            keyboard = InlineKeyboardMarkup()
            for result in results:
                movie_id = result.movieID
                title = result.get('title', 'N/A')
                year = result.get('year', 'N/A')
                keyboard.add(InlineKeyboardButton(f"{title} ({year})", callback_data=movie_id))
            bot.send_message(message.chat.id, "Select a movie:", reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "No results found.")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    movie_id = call.data
    movie_details = fetch_movie_details(movie_id)

    if movie_details:
        title = movie_details['title']
        rating = movie_details['rating']
        year = movie_details['year']
        duration = movie_details['duration']
        languages = movie_details['languages']
        genres = movie_details['genres']
        plot = movie_details['plot']
        directors = movie_details['directors']
        actors = movie_details['actors']
        writers = movie_details['writers']
        poster_url = movie_details['poster_url']

        # Create the movie info string with HTML formatting
        movie_info = (
            f"🎪 <b>Movie:</b> {title}\n"
            f"🏆 <b>User Ratings:</b> {rating}\n"
            f"🗓 <b>Release Info:</b> {year}\n"
            f"🕰 <b>Duration:</b> {duration}\n"
            f"🎧 <b>Language:</b> {languages}\n"
            f"🎭 <b>Genres:</b> {genres}\n"
            f"📋 <b>Storyline:</b> <i>{plot}</i>\n"
            f"🎥 <b>Director:</b> {directors}\n"
            f"🎎 <b>Actors:</b> {actors}\n"
            f"✍️ <b>Writers:</b> {writers}\n"
        )

        # Truncate caption if too long
        MAX_CAPTION_LENGTH = 1024
        if len(movie_info) > MAX_CAPTION_LENGTH:
            movie_info = movie_info[:MAX_CAPTION_LENGTH - 3] + "..."

        # Prepare InlineKeyboardMarkup with two buttons
        keyboard = InlineKeyboardMarkup()
        imdb_button = InlineKeyboardButton("Check IMDB", url=f"https://www.imdb.com/title/tt{movie_id}/")
        download_button = InlineKeyboardButton("Download Movie", url="https://t.me/botsupports_og")
        keyboard.add(imdb_button, download_button)

        if poster_url:
            bot.send_photo(call.message.chat.id, poster_url, caption=movie_info, parse_mode='HTML', reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, movie_info, parse_mode='HTML', reply_markup=keyboard)

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    else:
        bot.send_message(call.message.chat.id, "Movie details not found.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
