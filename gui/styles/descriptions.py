from core.types import StatType, DamageTag


def get_tag_description(tag: DamageTag) -> str:
    """Returns the description of tag."""
    descriptions: dict[DamageTag, str] = {
        DamageTag.ALL: "Applies to all types",
        DamageTag.PHASE: "Corrosion, Burn, Freeze, Hydro, or Electric",
        DamageTag.CONFECTANCE: "Consumes Confectance Index",
        DamageTag.PASSIVE: "Out-of-turn",
        DamageTag.EXPOSED: "Not protected by cover",
        DamageTag.STABILITY_BROKEN: "In stability break",
        DamageTag.BOSS: "Target is a boss",
        DamageTag.HAS_MOVEMENT_DEBUFF: "Target has a movement debuff",
        DamageTag.PHYSICAL_SUMMON: "Damage from physical summons",
        DamageTag.ONLY_HIT_ONE_TARGET: "Damage only hits one target",
        DamageTag.NEAR: "Target is within 3 tiles",
        DamageTag.FAR: "Target is more than 6 tiles away",
    }

    return descriptions.get(tag, "")


def get_stat_description(stat: StatType) -> str:
    """Returns the description of stat."""
    descriptions: dict[StatType, str] = {
        StatType.CRIT_RATE: "in %",
        StatType.CRIT_DAMAGE: "in %",
        StatType.STABILITY_DAMAGE_REDUCTION: "in %",
    }

    return descriptions.get(stat, "")
