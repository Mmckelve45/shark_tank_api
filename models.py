from enum import Enum

from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY, JSON, Numeric


# ------- Tables -------
class Seasons(Base):
    __tablename__ = 'seasons'

    season_id = Column(Integer, primary_key=True, index=True)
    num_episodes = Column(Integer, nullable=False)
    summary = Column(String, nullable=False)
    shark_info = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)


class Episodes(Base):
    __tablename__ = 'episodes'

    episode_id = Column(Integer, primary_key=True, index=True)
    sharks = Column(ARRAY(String), nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.season_id'), nullable=False)
    episode = Column(Integer, nullable=False)
    # episode_all = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    date = Column(String, nullable=False)
    wikipedia_url = Column(String, nullable=False)
    companies = Column(ARRAY(JSON), nullable=False)


class Pitches(Base):
    __tablename__ = 'pitches'

    pitch_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.season_id'), nullable=False)
    # episode_id = Column(Integer, ForeignKey('episodes.episode_id'), nullable=False)
    episode = Column(Integer, nullable=False)
    air_date = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    entrepreneur_gender = Column(String, nullable=False)
    entrepreneur = Column(ARRAY(String), nullable=False)
    is_deal = Column(Boolean, nullable=False)
    ask_amt = Column(Integer, nullable=False)
    ask_perc = Column(Numeric(precision=10, scale=2), nullable=False)
    ask_valuation = Column(Integer, nullable=False)
    ask_summary = Column(String, nullable=False)
    deal_amt_equity = Column(Integer, nullable=True)
    deal_perc_equity = Column(Numeric(precision=10, scale=2), nullable=True)
    deal_amt_debt = Column(Integer, nullable=True)
    deal_valuation = Column(Integer, nullable=True)
    deal_summary = Column(String, nullable=True)
    bite = Column(Integer, nullable=True)
    investors = Column(ARRAY(String), nullable=True)
    deal_structure = Column(ARRAY(String), nullable=True)
    category = Column(String, nullable=False)
    status = Column(String, nullable=True)
    website = Column(String, nullable=True)


class Sharks(Base):
    __tablename__ = 'sharks'

    shark_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    summary = Column(String, nullable=False)
    description = Column(String, nullable=False)
    img = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    is_guest = Column(Boolean, nullable=False)


# ------- Enum Values -------
class Shark(str, Enum):

    mc = "Mark Cuban"
    lg = "Lori Greiner"
    dj = "Daymond John"
    kl = "Kevin O'Leary"
    rh = "Robert Herjavec"
    bc = "Barbara Corcoran"
    eg = "Emma Grede"
    kh = "Kevin Hart"
    pj = "Peter Jones"
    dl = "Daniel Lubetzky"
    nt = "Nirav Tolia"
    kha = "Kevin Harrington"
    cs = "Chris Sacca"
    jf = "Jeff Foxworthy"
    jpd = "John Paul Dejoria"
    st = "Steve Tisch"
    nw = "Nick Woodman"
    ak = "Ashton Kutcher"
    tc = "Troy Carter"
    rb = "Richard Branson"
    ro = "Rohan Oza"
    ar = "Alex Rodriguez"
    sb = "Sara Blakely"
    bf = "Bethenny Frankel"
    js = "Jamie Siminoff"
    mh = "Matt Higgins"
    cb = "Charles Barkley"
    aw = "Alli Webb"
    awo = "Anne Wojcicki"
    ms = "Maria Sharapova"
    kla = "Katrina Lake"
    bm = "Blake Mycoskie"
    ks = "Kendra Scott"
    gp = "Gwyneth Paltrow"
    tx = "Tony Xu"
    cn = "Candace Nelson"
    mr = "Michael Rubin"
    jb = "Jason Blum"


class Gender(str, Enum):
    male = 'Male'
    female = 'Female'
    hybrid = 'Hybrid'


class Category(str, Enum):
    food = "Food_Beverage"
    tech = "Software_Tech"
    children = "Children"
    services = "Services"
    clothing = "Clothing_Fashion"
    lifestyle = "Lifestyle_Home"
    education = "Education"
    accessories = "Accessories_Gadgets"
    fitness = "Fitness_Outdoors"
    pet = "PetProducts"
    cosmetics = "Cosmetics_Beauty"
    health = "Health_SelfCare"
    travel = "Travel_Auto"
    media = "Media_Entertainment"
    other = "Other"
