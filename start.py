import math

from handlers.users.media import lang
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot

chat_id = "-1001818918192"


# @dp.message_handler(state=['*', 'start'], content_types=types.ContentTypes.ANY)
# async def start(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer(message.photo[-1].file_id)

@dp.message_handler(commands='start', state=['*', 'start'])
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Please, choose the language/Будь ласка, виберіть мову",
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=[[
                             types.KeyboardButton(text='🇬🇧ENGLISH🇬🇧'),
                             types.KeyboardButton(text='🇺🇦УКРАЇНСЬКА🇺🇦')
                         ]
                         ], resize_keyboard=True))
    await state.set_state('Начать')


@dp.message_handler(state='Начать')
async def become_a_model(message: types.Message, state: FSMContext):
    if message.text != '🇬🇧ENGLISH🇬🇧' and message.text != '🇺🇦УКРАЇНСЬКА🇺🇦':
        await message.answer("I did not understand you/Я вас не зрозумів"
                             "\n\n"
                             "Please, choose the language/Будь ласка, виберіть мову")
    else:
        if message.text == '🇬🇧ENGLISH🇬🇧':
            text = lang.dictionary.get("eng")
        else:
            text = lang.dictionary.get("ukr")
        buttons = text.get("buttons")
        await state.update_data({"dict": text})
        await message.answer(text.get("START"),
                             reply_markup=types.ReplyKeyboardMarkup(keyboard=[[
                                 types.KeyboardButton(text=buttons.get("APPLY_but")),
                                 types.KeyboardButton(text=buttons.get("ABOUT_US_but"))
                             ]
                             ], resize_keyboard=True))
        await state.set_state("Model")


@dp.message_handler(state='Model')
async def model(message: types.Message, state: FSMContext):
    data = await state.get_data()
    dictionary: dict = data.get("dict")
    buttons = dictionary.get("buttons")
    if message.text == buttons.get("ABOUT_US_but"):
        await message.answer(dictionary.get("ABOUT_US"))
    elif message.text == buttons.get("APPLY_but"):
        await bot.send_photo(caption=dictionary.get("APPLY"),
                             photo='AgACAgUAAxkBAAOPY1mjY_rjsmcHgbsD15EGH8ktUGoAArm4MRtunMhWrutVkbv9DmcBAAMCAAN5AAMqBA',
                             chat_id=message.chat.id, reply_markup=types.ReplyKeyboardRemove())
        await state.set_state("SNAPS")


@dp.message_handler(state='SNAPS')
async def snaps(message: types.Message, state: FSMContext):
    await state.update_data({"information": message.text})
    data = await state.get_data()
    dictionary = data.get("dict")
    await message.answer(dictionary.get("SNAPS1"))
    media = types.MediaGroup(
        [
            types.InputMediaVideo(media="BAACAgUAAxkBAAO0Y1mktq57qbC-BRbiFbLN5Bsow6UAAmMGAAJunMhW8QiqtoRcOQ8qBA",
                                  caption=dictionary.get("SNAPS2")),
            types.InputMediaVideo(media="BAACAgUAAxkBAAO2Y1mk3fsLAAHO3aFbuiwz-gqXgbIXAAJkBgACbpzIVvKFZV-N6FVUKgQ"),
            types.InputMediaPhoto(
                media="AgACAgUAAxkBAAO6Y1mlPWOGVufV_MmVgpH1v5t40kkAAsi4MRtunMhWq8gfkL2hS5oBAAMCAAN5AAMqBA"),
            types.InputMediaPhoto(
                media="AgACAgUAAxkBAAO8Y1mlW54Fn2sAASdR9BEnR4Gytw4cAALJuDEbbpzIVq_s4DdHW3EbAQADAgADeQADKgQ"),
            types.InputMediaPhoto(
                media="AgACAgUAAxkBAAO-Y1mlZem0esgT6KcriksM-niS1XgAAsq4MRtunMhWg4FjntMZiQ0BAAMCAAN5AAMqBA"),
            types.InputMediaPhoto(
                media="AgACAgUAAxkBAAPAY1mleW1_WYNUvHVCIry39hNqdFoAAsu4MRtunMhWR0CwaWgZLH8BAAMCAAN5AAMqBA"),
            types.InputMediaPhoto(
                media="AgACAgUAAxkBAAPCY1mlgco0OJv778tqQ9tGNRMDWkIAAsy4MRtunMhWWnXh7BwkowgBAAMCAAN5AAMqBA"),
            types.InputMediaPhoto(
                media="AgACAgUAAxkBAAPEY1mliO8gYM-4bFmkJRb6W5qn1_QAAs24MRtunMhWpXw93gc3GioBAAMCAAN5AAMqBA"),
            types.InputMediaPhoto(
                media="AgACAgUAAxkBAAPGY1mlj3yg-hu58LhIgVU2bqTTXBwAAs64MRtunMhWby7KYiHLJ80BAAMCAAN5AAMqBA"),
        ]
    )
    await bot.send_media_group(chat_id=message.chat.id, media=media)
    await state.set_state("SNAPS_END")


@dp.message_handler(state='SNAPS_END',
                    content_types=types.ContentTypes.VIDEO | types.ContentTypes.PHOTO | types.ContentTypes.TEXT | types.ContentTypes.DOCUMENT)
async def snaps_end(message: types.Message, state: FSMContext):
    data = await state.get_data()
    dictionary = data.get("dict")
    buttons = dictionary.get("buttons")
    if message.text == buttons.get("PHOTO_but"):
        text = f'Модель: {message.from_user.full_name}\n' \
               f'username: {"@" + message.from_user.username if message.from_user.username else "Немає"} \n' \
               f'відправила такі данні: \n\n"{data.get("information")}"'

        media = []
        counter = 0
        media_dict = data.get("media")
        for file_id in media_dict:
            if counter > 0:
                kwargs = {"media": file_id}
                type_media = media_dict[file_id]
                if type_media == "photo":
                    media.append(types.InputMediaPhoto(**kwargs))
                elif type_media == "video":
                    media.append(types.InputMediaVideo(**kwargs))
                else:
                    pass
            else:
                kwargs = {"caption": text, "media": file_id}
                type_media = media_dict[file_id]
                if type_media == "photo":
                    media.append(types.InputMediaPhoto(**kwargs))
                elif type_media == "video":
                    media.append(types.InputMediaVideo(**kwargs))
                else:
                    pass
                counter = counter + 1
                
        quantity_pages = math.ceil(len(media) / 10)
        for page in range(quantity_pages):
            page = page + 1
            first_element = page * 10 - 10
            past_element = first_element + 9
            await bot.send_media_group(chat_id=chat_id, media=media[first_element:past_element])
        
        await state.set_state("END")
        await message.answer(dictionary.get("END2"),
                             reply_markup=types.ReplyKeyboardMarkup(keyboard=[[
                                 types.KeyboardButton(text=buttons.get("DONE_but")),
                                 types.KeyboardButton(text=buttons.get("MESSAGE_but"))
                             ]
                             ], resize_keyboard=True))
    elif message.photo:
        media = data.get("media") if data.get("media") else {}
        media.update({message.photo[-1].file_id: "photo"})
        await state.update_data({"media": media})
        await message.answer(dictionary.get("END"), reply_markup=types.ReplyKeyboardMarkup(keyboard=[[
            types.KeyboardButton(text=buttons.get("PHOTO_but"))
        ]
        ], resize_keyboard=True))
    elif message.video:
        media = data.get("media") if data.get("media") else {}
        media.update({message.video.file_id: "video"})
        await state.update_data({"media": media})
        await message.answer(dictionary.get("END"), reply_markup=types.ReplyKeyboardMarkup(keyboard=[[
            types.KeyboardButton(text=buttons.get("PHOTO_but"))
        ]
        ], resize_keyboard=True))
    elif message.document:
        kwargs = {"text": "Ви відправили документ, відправте відео або фото/"
                          "You have sent a document, send a video or photo"} if data.get("media") is None else {
            "text": "Ви відправили документ, відправте відео або фото/"
                    "You have sent a document, send a video or photo",
            "reply_markup": types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text=buttons.get('PHOTO_but'))]], resize_keyboard=True)}
        await message.answer(**kwargs)
    else:
        kwargs = {"text": "Відправте ваші фото і відео по одному/"
                          "Send your photos and videos one at a time"} if data.get("media") is None else {
            "text": "Відправте ваші фото і відео по одному/"
                    "Send your photos and videos one at a time",
            "reply_markup": types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text=buttons.get('PHOTO_but'))]], resize_keyboard=True)}
        await message.answer(**kwargs)


@dp.message_handler(state='END')
async def end(message: types.Message, state: FSMContext):
    data = await state.get_data()
    dictionary: dict = data.get("dict")
    buttons = dictionary.get("buttons")
    if message.text == buttons.get("DONE_but"):
        await message.answer(dictionary.get("SNAPS_END"), reply_markup=types.ReplyKeyboardRemove())
        # await start(message=message, state=state)
    elif message.text == buttons.get("MESSAGE_but"):
        await state.set_state('MESSAGE')
        await message.answer(dictionary.get("MESSAGE"), reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state='MESSAGE')
async def mes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    dictionary: dict = data.get("dict")
    await bot.send_message(chat_id=chat_id, text=f'Нове повідомлення від користувача: {message.from_user.full_name}\n'
                                                 f'username: {"@" + message.from_user.username if message.from_user.username else "Немає"}\n\n'
                                                 f'"{message.text}"')
    await message.answer(dictionary.get("SNAPS_END"))
    await state.set_state('HOME')
