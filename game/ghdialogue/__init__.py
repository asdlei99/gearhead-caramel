
import pbge
from . import ghgrammar
from . import context
from . import ghdview
from . import ghreplies
from . import ghoffers
import gears

def trait_absorb(mygram,nugram,traits):
    for pat,gramdic in nugram.items():
        for k,v in gramdic.items():
            if k is ghgrammar.Default:
                if pat not in mygram:
                    mygram[pat] = list()
                mygram[pat] += v
            elif k in traits:
                if pat not in mygram:
                    mygram[pat] = list()
                mygram[pat] += v


def build_grammar( mygram, camp, speaker, audience ):
    speaker = speaker.get_pilot()
    tags = speaker.get_tags()
    if speaker.relationship and not speaker.relationship.met_before:
        tags.append(ghgrammar.FIRST_TIME)
    else:
        tags.append(ghgrammar.MET_BEFORE)
    if audience:
        audience = audience.get_pilot()
        react = speaker.get_reaction_score(audience,camp)
        if react > 60:
            tags += [ghgrammar.LIKE,ghgrammar.LOVE]
        elif react > 20:
            tags += [ghgrammar.LIKE,]
        elif react < -60:
            tags += [ghgrammar.DISLIKE,ghgrammar.HATE]
        elif react < -20:
            tags += [ghgrammar.DISLIKE,]
    trait_absorb(mygram,ghgrammar.DEFAULT_GRAMMAR,tags)
    for p in camp.active_plots():
        pgram = p.get_dialogue_grammar( speaker, camp )
        if pgram:
            mygram.absorb( pgram )

    mygram.absorb({"[speaker]":(str(speaker),),"[audience]":(str(audience),)})

def harvest( mod, class_to_collect ):
    mylist = []
    for name in dir( mod ):
        o = getattr( mod, name )
        if isinstance( o , class_to_collect ):
            mylist.append( o )
    return mylist

pbge.dialogue.GRAMMAR_BUILDER = build_grammar
pbge.dialogue.STANDARD_REPLIES = harvest(ghreplies,pbge.dialogue.Reply)
pbge.dialogue.STANDARD_OFFERS = harvest(ghoffers,pbge.dialogue.Offer)
pbge.dialogue.GENERIC_OFFERS.append(ghoffers.GOODBYE)
pbge.dialogue.GENERIC_OFFERS.append(ghoffers.CHAT)

HELLO_STARTER = pbge.dialogue.Cue(pbge.dialogue.ContextTag((context.HELLO,)))
ATTACK_STARTER = pbge.dialogue.Cue(pbge.dialogue.ContextTag((context.ATTACK,)))

def start_conversation(camp,pc,npc,cue=HELLO_STARTER):
    # If this NPC has no relationship with the PC, create that now.
    realnpc = npc.get_pilot()
    if realnpc and not realnpc.relationship:
        realnpc.relationship = gears.relationships.Relationship()
    cviz = ghdview.ConvoVisualizer(npc,camp,pc=pc)
    cviz.rollout()
    convo = pbge.dialogue.DynaConversation(camp,realnpc,pc,cue,visualizer=cviz)
    convo.converse()
    if realnpc:
        realnpc.relationship.met_before = True


