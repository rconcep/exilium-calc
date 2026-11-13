"""Compatibility aliases for names persisted in rotation data."""

ACTION_NAME_ALIASES: dict[str, str] = {
    "Combat Instinct": "Shooting Instinct",
    "Critical Splash": "Critical Blast",
    "Predator's Pursuit": "Hunting Fang",
    "Ferocious Bite": "Vicious Bite",
    "Midnight Howl": "Lunar Howl",
    "Midnight Howl (Form Swap)": "Lunar Howl (Form Swap)",
    "Deadly Pounce": "Fatal Pounce",
    "Deadly Pounce (Passive)": "Fatal Pounce (Passive)",
    "Silent Takedown": "Hushed Erasure",
    "Conviction and Punishment": "Subjective Sanction",
    "Hour of Reckoning": "Judgement Blast",
    "Crime Backlash": "Iniquity's Retribution",
    "Case Detective": "Case Controller",
    "Cuspid Combo": "Burst Fang",
    "Triple Maule": "Triple Maul",
    "Triple Maule (follow-up)": "Triple Maul (follow-up)",
    "Scent Mark": "Scent Trail",
    "Loyal Hunt": "Loyal Dash",
    "Hunter's Instinct I": "Pursuit Instinct I",
    "Hunter's Instinct II": "Pursuit Instinct II",
    "Hunter's Instinct III": "Pursuit Instinct III",
}

ACTION_FIELD_ALIASES: dict[str, dict[str, str]] = {
    action_name: {"stacks_of_hunters_tracking": "stacks_of_hunt_tracking"}
    for action_name in (
        "Triple Maul",
        "Loyal Dash",
        "Pursuit Instinct I",
        "Pursuit Instinct II",
        "Pursuit Instinct III",
    )
}

EFFECT_NAME_ALIASES: dict[str, str] = {
    "Cover Mode (OTs-14)": "Cover Order (OTs-14)",
    "Demolition Mode (OTs-14)": "Demolition Order (OTs-14)",
    "Reconstruction: Burn (OTs-14)": "Reconfiguration - Burn (OTs-14)",
    "Reconstruction: Electric (OTs-14)": "Reconfiguration - Electric (OTs-14)",
    "Reconstruction: Freeze (OTs-14)": "Reconfiguration - Freeze (OTs-14)",
    "Reconstruction: Hydro (OTs-14)": "Reconfiguration - Hydro (OTs-14)",
    "Reconstruction: Zero (OTs-14)": "Reconfiguration - Zero (OTs-14)",
    "Reconstruction: Corrosion (OTs-14)": "Reconfiguration - Corrosion (OTs-14)",
    "Concentration (Nemesis: Gnosis)": "Mindfulness (Nemesis: Gnosis)",
    "Feral Factor (Soppo)": "Rabid Factor (Soppo)",
    "Feral Factor I (Soppo)": "Rabid Factor I (Soppo)",
    "Feral Factor II (Soppo)": "Rabid Factor II (Soppo)",
    "Feral Factor III (Soppo)": "Rabid Factor III (Soppo)",
    "Frost Strike": "Boreal Assault",
    "Deductive Obsession (Welrod)": "Deduction Obsession (Welrod)",
    "Case Detective (Welrod)": "Case Controller (Welrod)",
    "Hunter's Tracking (Faelynn)": "Hunt Tracking (Faelynn)",
    "Roving Bloodlust (Faelynn)": "Roving Ferocity (Faelynn)",
    "Scent Mark (Faelynn)": "Scent Trail (Faelynn)",
}


def canonical_action_name(name: str) -> str:
    return ACTION_NAME_ALIASES.get(name, name)


def canonical_action_field_name(action_name: str, field_name: str) -> str:
    return ACTION_FIELD_ALIASES.get(action_name, {}).get(field_name, field_name)


def canonical_effect_name(name: str) -> str:
    return EFFECT_NAME_ALIASES.get(name, name)
