import pygame

import gears
import pbge

LEFT_COLUMN = pbge.frects.Frect(-300,0,200,200)
CENTER_COLUMN = pbge.frects.Frect(-50,-200,200,400)
RIGHT_COLUMN = pbge.frects.Frect(175,-200,200,400)
PORTRAIT_AREA = pbge.frects.Frect(-450, -300, 400, 600)
UTIL_INFO = pbge.frects.Frect(-50,-200,300,200)
UTIL_MENU = pbge.frects.Frect(-50,50,300,150)

RIGHT_INFO = pbge.frects.Frect(175,-200,200,150)
RIGHT_MENU = pbge.frects.Frect(175,-20,200,170)

class MechasPilotBlock(object):
    # There should be an apostrophe in there, but y'know...
    def __init__(self, model, camp, font=None, width=220, **kwargs):
        self.model = model
        self.camp = camp
        self.width = width
        self.font = font or pbge.MEDIUMFONT
        self.update()
        self.height = self.image.get_height()
    def update(self):
        pilot = self.model.pilot
        if pilot not in self.camp.party:
            self.model.pilot = None
            pilot = None
        self.image = pbge.render_text(self.font,'Pilot: {}'.format(str(pilot)),self.width,justify=-1,color=pbge.INFO_HILIGHT)
    def render(self,x,y):
        pbge.my_state.screen.blit(self.image,pygame.Rect(x,y,self.width,self.height))


class PilotsMechaBlock(object):
    # There should be an apostrophe in there, but y'know...
    def __init__(self, model, camp, font=None, width=220, **kwargs):
        self.model = model
        self.camp = camp
        self.width = width
        self.font = font or pbge.MEDIUMFONT
        self.update()
        self.height = self.image.get_height()
    def update(self):
        mek = self.camp.get_pc_mecha(self.model)
        if mek:
            self.image = pbge.render_text(self.font,'Mecha: {}'.format(mek.get_full_name()),self.width,justify=-1,color=pbge.INFO_HILIGHT)
        else:
            self.image = pbge.render_text(self.font,'Mecha: None',self.width,justify=-1,color=pbge.INFO_HILIGHT)
    def render(self,x,y):
        pbge.my_state.screen.blit(self.image,pygame.Rect(x,y,self.width,self.height))


class CharaFHQIP(gears.info.InfoPanel):
    DEFAULT_BLOCKS = (gears.info.FullNameBlock, gears.info.ModuleStatusBlock, PilotsMechaBlock, gears.info.ExperienceBlock, gears.info.CharacterStatusBlock, gears.info.PrimaryStatsBlock, gears.info.NonComSkillBlock, gears.info.MeritBadgesBlock, gears.info.CharacterTagsBlock)


class MechaFHQIP(gears.info.InfoPanel):
    DEFAULT_BLOCKS = (gears.info.FullNameBlock, gears.info.ModuleStatusBlock, MechasPilotBlock, gears.info.MechaStatsBlock, gears.info.DescBlock)


class AssignMechaIP(gears.info.InfoPanel):
    DEFAULT_BLOCKS = (gears.info.FullNameBlock, gears.info.MechaFeaturesAndSpriteBlock)


class AssignPilotIP(gears.info.InfoPanel):
    DEFAULT_BLOCKS = (gears.info.FullNameBlock, gears.info.CharaPortraitAndSkillsBlock)