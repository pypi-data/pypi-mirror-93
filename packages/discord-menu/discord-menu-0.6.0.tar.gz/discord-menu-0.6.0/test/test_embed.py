from discord import Embed

from discordmenu.embed.base import Box
from discordmenu.embed.components import EmbedField, EmbedFooter
from discordmenu.embed.components import EmbedMain
from discordmenu.embed.components import EmbedThumbnail
from discordmenu.embed.menu import EmbedView
from discordmenu.intra_message_state import IntraMessageState
from discordmenu.embed.text import BoldText
from discordmenu.embed.text import HighlightableLinks
from discordmenu.embed.text import LabeledText
from discordmenu.embed.text import LinkedText
from discordmenu.embed.text import Text


def embed_view(embed_control, number, **state):
    view = EmbedView(
        EmbedMain(
            color="ffaaff",
            title="[3260] EMBED NUMBER {}".format(number),
            url="http://www.puzzledragonx.com/en/monster.asp?n=3260",
            description=Box(
                BoldText("Dragon/God")
            )
        ),
        embed_thumbnail=EmbedThumbnail("https://d1kpnpud0qoyxf.cloudfront.net/media/icons/03260.png"),
        embed_fields=[
            EmbedField(
                "Inheritable",
                Box(
                    LabeledText("Rarity", "7"),
                    LabeledText("Cost", "36"),
                ),
                inline=True
            ),
            EmbedField(
                "Stats",
                Box(
                    Text("HP 12037"),
                    Text("ATK 123"),
                ),
                inline=True
            ), EmbedField(
                "Active Skill",
                Text("Create 5 Fire and Light orbs; Charge all allies' skills by 1 turn"),
            ), EmbedField(
                "Alternate Evos",
                HighlightableLinks(
                    links=[
                        LinkedText("2141", "http://www.puzzledragonx.com/en/monster.asp?n=2141"),
                        LinkedText("2142", "http://www.puzzledragonx.com/en/monster.asp?n=2142"),
                        LinkedText("2970", "http://www.puzzledragonx.com/en/monster.asp?n=2970"),
                        LinkedText("3260", "http://www.puzzledragonx.com/en/monster.asp?n=3260"),
                    ],
                    highlighted=3
                )
            )
        ],
        embed_footer=EmbedFooter(
            "whawlekrjlkwer",
            IntraMessageState.serialize(
                "https://d1kpnpud0qoyxf.cloudfront.net/media/icons/05135.png",
                {"original_author_id": state['original_author_id']}
            )
        )
    )

    return view


def embed_1(reaction_add_event, message, **state):
    embed = Embed(
        **EmbedMain(
            color="ffaaff",
            title="[3260] Yamato Flame Dragon Caller, Tsubaki",
            url="http://www.puzzledragonx.com/en/monster.asp?n=3260",
            description=Box(
                BoldText("Dragon/God")
            )
        )
    )
    embed.set_thumbnail(url="https://d1kpnpud0qoyxf.cloudfront.net/media/icons/03260.png")
    e_field1 = EmbedField(
        "Inheritable",
        Box(
            LabeledText("Rarity", "7"),
            LabeledText("Cost", "36"),
        ),
        inline=True
    )
    e_field2 = EmbedField(
        "Stats",
        Box(
            Text("HP 12037"),
            Text("ATK 123"),
        ),
        inline=True
    )
    e_field = EmbedField(
        "Active Skill",
        Text("Create 5 Fire and Light orbs; Charge all allies' skills by 1 turn"),
    )
    e_field4 = EmbedField(
        "Alternate Evos",
        HighlightableLinks(
            links=[
                LinkedText("2141", "http://www.puzzledragonx.com/en/monster.asp?n=2141"),
                LinkedText("2142", "http://www.puzzledragonx.com/en/monster.asp?n=2142"),
                LinkedText("2970", "http://www.puzzledragonx.com/en/monster.asp?n=2970"),
                LinkedText("3260", "http://www.puzzledragonx.com/en/monster.asp?n=3260"),
            ],
            highlighted=3
        )
    )
    e_footer = EmbedFooter(
        "whawlekrjlkwer",
        IntraMessageState.serialize(
            "https://d1kpnpud0qoyxf.cloudfront.net/media/icons/05135.png",
            {"original_author_id": state['original_author_id']}
        )
    )
    embed.add_field(**e_field1)
    embed.add_field(**e_field2)
    embed.add_field(**e_field)
    embed.add_field(**e_field4)
    embed.set_footer(**e_footer)
    return embed


def embed_2(reaction_add_event, message, **state):
    embed = Embed(
        **EmbedMain(
            color="ffaaff",
            title="[3260] Yamato Flame Dragon Caller, THIS THING CHNGED",
            url="http://www.puzzledragonx.com/en/monster.asp?n=3260",
            description=Box(
                BoldText("Dragon/God"),
            )
        )
    )
    embed.set_thumbnail(url="https://d1kpnpud0qoyxf.cloudfront.net/media/icons/03260.png")
    e_field1 = EmbedField(
        "Inheritable",
        Box(
            LabeledText("Rarity", "7"),
            LabeledText("Cost", "36"),
        ),
        inline=True
    )
    e_field2 = EmbedField(
        "Stats",
        Box(
            Text("HP 12037"),
            Text("ATK 123"),
        ),
        inline=True
    )
    e_field = EmbedField(
        "Active Skill",
        Text("Create 5 Fire and Light orbs; Charge all allies' skills by 1 turn"),
    )
    e_field4 = EmbedField(
        "Alternate Evos",
        HighlightableLinks(
            links=[
                LinkedText("2141", "http://www.puzzledragonx.com/en/monster.asp?n=2141"),
                LinkedText("2142", "http://www.puzzledragonx.com/en/monster.asp?n=2142"),
                LinkedText("2970", "http://www.puzzledragonx.com/en/monster.asp?n=2970"),
                LinkedText("3260", "http://www.puzzledragonx.com/en/monster.asp?n=3260"),
            ],
            highlighted=3
        )
    )
    e_footer = EmbedFooter(
        "whawlekrjlkwer",
        IntraMessageState.serialize(
            "https://d1kpnpud0qoyxf.cloudfront.net/media/icons/05135.png",
            {"original_author_id": state['original_author_id']}
        )
    )

    embed.add_field(**e_field1)
    embed.add_field(**e_field2)
    embed.add_field(**e_field)
    embed.add_field(**e_field4)
    embed.set_footer(**e_footer)
    return embed
