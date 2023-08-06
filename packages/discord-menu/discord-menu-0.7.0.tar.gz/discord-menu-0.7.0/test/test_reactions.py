from discordmenu.discord_client import update_embed_control
from discordmenu.intra_message_state import IntraMessageState
from test.test_menu import embed_menu_1


def _get_emoji_name(raw_reaction_add_event):
    emoji_obj = raw_reaction_add_event.emoji
    if isinstance(emoji_obj, str):
        return emoji_obj
    return raw_reaction_add_event.emoji.name


async def should_respond(reaction_filters, message, event):
    for reaction_filter in reaction_filters:
        allow = await reaction_filter.allow_reaction_raw(message, event)
        if not allow:
            return False
    return True


async def test_raw_reaction_add_better(self, event):
    channel = self.bot.get_channel(event.channel_id)
    message = await channel.fetch_message(event.message_id)

    ims = IntraMessageState.extract_data(message.embeds[0])
    original_author_id = ims['original_author_id']

    embed_menu = embed_menu_1(original_author_id)

    if not (await embed_menu.should_respond(message, event)):
        return

    emoji_name = _get_emoji_name(event)

    next_embed_control = await embed_menu.next_embed_control(message, emoji_name)
    emoji_diff = embed_menu.diff_emojis(message, next_embed_control)

    await update_embed_control(message, next_embed_control, emoji_diff)

# @commands.Cog.listener('on_reaction_add')
# async def on_reaction_add(self, reaction, member):
#     from discordmenu.on_reaction import ReactionResponder
#     responder = ReactionResponder(should_respond_custom=PadInfo.should_respond_custom)
#     func_map = {
#         '🧪': PadInfo.embed_2,
#         'bcookie': PadInfo.embed_1
#     }
#
#     from discordmenu.intra_message_state import IntraMessageState
#     ims = IntraMessageState.find_data(reaction.message.embeds[0])
#     print("ims", ims)
#
#     await responder.on_reaction_add_event(reaction, member, reaction.message, func_map, ims)
