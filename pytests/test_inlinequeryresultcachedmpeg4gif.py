#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2017
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
import json

import pytest

from telegram import (InlineQueryResultCachedMpeg4Gif, InlineKeyboardButton,
                      InputTextMessageContent, InlineKeyboardMarkup, InlineQueryResultCachedVoice)


@pytest.fixture(scope='class')
def inline_query_result_cached_mpeg4_gif():
    return InlineQueryResultCachedMpeg4Gif(TestInlineQueryResultCachedMpeg4Gif.id,
                                           TestInlineQueryResultCachedMpeg4Gif.mpeg4_file_id,
                                           title=TestInlineQueryResultCachedMpeg4Gif.title,
                                           caption=TestInlineQueryResultCachedMpeg4Gif.caption,
                                           input_message_content=TestInlineQueryResultCachedMpeg4Gif.input_message_content,
                                           reply_markup=TestInlineQueryResultCachedMpeg4Gif.reply_markup)


class TestInlineQueryResultCachedMpeg4Gif:
    id = 'id'
    type = 'mpeg4_gif'
    mpeg4_file_id = 'mpeg4 file id'
    title = 'title'
    caption = 'caption'
    input_message_content = InputTextMessageContent('input_message_content')
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('reply_markup')]])

    def test_expected_values(self, inline_query_result_cached_mpeg4_gif):
        assert inline_query_result_cached_mpeg4_gif.type == self.type
        assert inline_query_result_cached_mpeg4_gif.id == self.id
        assert inline_query_result_cached_mpeg4_gif.mpeg4_file_id == self.mpeg4_file_id
        assert inline_query_result_cached_mpeg4_gif.title == self.title
        assert inline_query_result_cached_mpeg4_gif.caption == self.caption
        assert inline_query_result_cached_mpeg4_gif.input_message_content.to_dict() == \
               self.input_message_content.to_dict()
        assert inline_query_result_cached_mpeg4_gif.reply_markup.to_dict() == \
               self.reply_markup.to_dict()

    def test_to_json(self, inline_query_result_cached_mpeg4_gif):
        json.loads(inline_query_result_cached_mpeg4_gif.to_json())

    def test_to_dict(self, inline_query_result_cached_mpeg4_gif):
        inline_query_result_cached_mpeg4_gif_dict = inline_query_result_cached_mpeg4_gif.to_dict()

        assert isinstance(inline_query_result_cached_mpeg4_gif_dict, dict)
        assert inline_query_result_cached_mpeg4_gif_dict['type'] == self.type
        assert inline_query_result_cached_mpeg4_gif_dict['id'] == self.id
        assert inline_query_result_cached_mpeg4_gif_dict['mpeg4_file_id'] == self.mpeg4_file_id
        assert inline_query_result_cached_mpeg4_gif_dict['title'] == self.title
        assert inline_query_result_cached_mpeg4_gif_dict['caption'] == self.caption
        assert inline_query_result_cached_mpeg4_gif_dict['input_message_content'] == \
               self.input_message_content.to_dict()
        assert inline_query_result_cached_mpeg4_gif_dict['reply_markup'] == \
               self.reply_markup.to_dict()

    def test_equality(self):
        a = InlineQueryResultCachedMpeg4Gif(self.id, self.mpeg4_file_id)
        b = InlineQueryResultCachedMpeg4Gif(self.id, self.mpeg4_file_id)
        c = InlineQueryResultCachedMpeg4Gif(self.id, "")
        d = InlineQueryResultCachedMpeg4Gif("", self.mpeg4_file_id)
        e = InlineQueryResultCachedVoice(self.id, "", "")

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)