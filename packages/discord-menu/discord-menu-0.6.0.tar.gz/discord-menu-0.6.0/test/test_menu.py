from discordmenu.discord_client import send_embed_control
from discordmenu.embed.menu import EmbedMenu, EmbedControl
from discordmenu.emoji_cache import EmojiCache
from discordmenu.reaction_filter import ValidEmojiReactionFilter, NotPosterEmojiReactionFilter, \
    MessageOwnerReactionFilter
from discordmenu.test_embed import embed_view

c = EmojiCache([713430119343063182])


def embed_menu_1(original_author_id):
    panes = {
        '🧪': embed_control_1,
        'bcookie': embed_control_2,
    }

    valid_emoji_names = [e.name for e in c.custom_emojis] + list(panes.keys())
    reaction_filters = [
        ValidEmojiReactionFilter(valid_emoji_names),
        NotPosterEmojiReactionFilter(),
        MessageOwnerReactionFilter(original_author_id)
    ]

    return EmbedMenu(reaction_filters, panes)


def embed_control_1(prev_embed_control, **state):
    emoji_button_names = ['bcookie', 'bnotdis', 'blobthinkingfast', 'googledog', 'tsubaki']
    return EmbedControl([embed_view(None, 1, **state)], [c.get_by_name(e) for e in emoji_button_names])


def embed_control_2(prev_embed_control, **state):
    emoji_button_names = ['🧪', 'bnotdis', 'bloblul', 'googlecat', 'googlecatface']
    return EmbedControl([embed_view(None, 2, **state)], [c.get_by_name(e) for e in emoji_button_names])


async def mt(self, ctx):
    original_author_id = ctx.message.author.id
    state = {'original_author_id': original_author_id}
    c.refresh_from_discord_bot(self.bot)
    menu = embed_menu_1(original_author_id)
    ec = menu.get_embed_control('🧪', state=state)
    await send_embed_control(ctx, ec)
