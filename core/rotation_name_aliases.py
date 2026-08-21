"""Compatibility aliases for names persisted in rotation data."""

ACTION_NAME_ALIASES: dict[str, str] = {
    "Combat Instinct": "Shooting Instinct",
    "Critical Splash": "Critical Blast",
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
}


def canonical_action_name(name: str) -> str:
    return ACTION_NAME_ALIASES.get(name, name)


def canonical_effect_name(name: str) -> str:
    return EFFECT_NAME_ALIASES.get(name, name)