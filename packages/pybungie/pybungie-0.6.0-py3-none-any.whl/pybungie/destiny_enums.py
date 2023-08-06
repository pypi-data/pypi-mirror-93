from enum import Enum


class Definitions(Enum):
    ITEM = "DestinyInventoryItemDefinition"
    VENDOR = "DestinyVendorDefinition"
    VENDOR_ITEM = "DestinyVendorItemDefinition"


class Components(Enum):
    Profiles = 100
    VendorReceipts = 101
    ProfileInventories = 102
    ProfileCurrencies = 103
    ProfileProgression = 104
    PlatformSilver = 105
    Characters = 200
    CharacterInventories = 201
    CharacterProgressions = 202
    CharacterRenderData = 203
    CharacterActivities = 204
    CharacterEquipment = 205
    ItemInstances = 300
    ItemObjectives = 301
    ItemPerks = 302
    ItemRenderData = 303
    ItemStats = 304
    ItemSockets = 305
    ItemTalentGrids = 306
    ItemCommonData = 307
    ItemPlugStates = 308
    ItemPlugObjectives = 309
    ItemReusablePlugs = 310
    Vendors = 400
    VendorCategories = 401
    VendorSales = 402
    Kiosks = 500
    CurrencyLookups = 600
    PresentationNodes = 700
    Collectibles = 800
    Records = 900
    Transitory = 1000
    Metrics = 1100


class VendorHash(Enum):
    XUR = 2190858386
    SURAYA_HAWTHORNE = 3347378076
    COMMANDER_ZAVALA = 69482069
    IKORA_REY = 1976548992
    LORD_SHAXX = 3603221665
    MASTER_RAHOOL = 2255782930
    BANSHEE44 = 672118013
    AMANDA_HOLLIDAY = 460529231
    THE_DRIFTER = 248695599
    SAINT14 = 765357505
    QUEST_ARCHIVE = 3484140575
    MONUMENT_TO_LOST_LIGHTS = 4230408743
    TESS_EVERIS = 3361454721
    DEVRIM_KAY = 396892126
    FAILSAFE = 1576276905
    SPIDER = 863940356
    ERIS_MORN = 1616085565
    LECTERN_OF_ENCHANTMENT = 3411552308
    VARIKS_THE_LOYAL = 2531198101
    SHAW_HAN = 1816541247
    THE_CROW = 3611983588


class DamageType(Enum):
    """Enumeration type defining each Damage type as described in the Destiny API
    """

    NONE = 0
    KINETIC = 1
    ARC = 2
    SOLAR = 3
    VOID = 4
    RAID = 5
    STASIS = 6


class PlayerClass(Enum):
    """Enumeration type defining each player class as described in the Destiny API
    """

    TITAN = 0
    HUNTER = 1
    WARLOCK = 2
    UNKNOWN = 3


class MembershipType(Enum):
    NONE = 0
    XBOX = 1
    PSN = 2
    STEAM = 3
    BLIZZARD = 4
    STADIA = 5
    DEMON = 10
    BUNGIENEXT = 254
    All = -1


class DestinyItemSubType(Enum):
    NONE = 0
    AUTORIFLE = 6
    SHOTGUN = 7
    MACHINEGUN = 8
    HANDCANNON = 9
    ROCKETLAUNCHER = 10
    FUSIONRIFLE = 11
    SNIPERRIFLE = 12
    PULSERIFLE = 13
    SCOUTRIFLE = 14
    SIDEARM = 17
    SWORD = 18
    MASK = 19
    SHADER = 20
    ORNAMENT = 21
    FUSIONRIFLELINE = 22
    GRENADELAUNCHER = 23
    SUBMACHINEGUN = 24
    TRACERIFLE = 25
    HELMETARMOR = 26
    GAUNTLETSARMOR = 27
    CHESTARMOR = 28
    LEGARMOR = 29
    CLASSARMOR = 30
    BOW = 31
    DUMMYREPEATABLEBOUNTY = 32
