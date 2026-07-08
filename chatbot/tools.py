from google.genai import types

##Tools Definitions
read_temp_func = types.FunctionDeclaration(
    name = "read_temp",
    description = "Read the current temperature",
    parameters = {"type" : "OBJECT", "properties": {}}
)


read_light_func = types.FunctionDeclaration(
    name = "read_light",
    description = "Read the current light level",
    parameters = {"type" : "OBJECT", "properties": {}}
)


all_off_func = types.FunctionDeclaration(
    name="all_off",
    description=("Turns off every tool"),
    parameters={"type": "OBJECT","properties": {}}
)


set_rgb_func = types.FunctionDeclaration(
    name="set_rgb",
    description=(
        "Controls the RGB LED"
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "red": {
                "type": "INTEGER",
                "description": "Red value"
            },
            "green": {
                "type": "INTEGER",
                "description": "Green value"
            },
            "blue": {
                "type": "INTEGER",
                "description": "Blue value"
            }
        },
        "required": ["red", "green", "blue"]
    }
)


fade_rgb_func = types.FunctionDeclaration(
    name="fade_rgb",
    description=(
        "Uses PWM controlled pin for the fade effect on RGB LED."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "red": {
                "type": "INTEGER",
                "description": "Red value"
            },
            "green": {
                "type": "INTEGER",
                "description": "Green value"
            },
            "blue": {
                "type": "INTEGER",
                "description": "Blue value"
            },
            "duration_ms": {
                "type": "INTEGER",
                "description": "Time between fading values."
            }
        },
        "required": ["red", "green", "blue", "duration_ms"]
    }
)


alert_func = types.FunctionDeclaration(
    name="alert",
    description=(
        "Uses the active buzzer to play an alarm"
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "pattern": {
                "type": "STRING",
                "enum": ["short", "long", "double_beep"],
                "description": "The buzzer pattern"
            },
            "repeat_count": {
                "type": "INTEGER",
                "description": "Number of times to repeat the pattern. Defaults to 1."
            }
        },
        "required": ["pattern"] #only pattern is required
    }
)


write_display_func = types.FunctionDeclaration(
    name="write_display",
    description=(
        "Writes text to a LCD display with 4 rows."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "text": {"type": "STRING", "description": "Text to display"},
            "row": {"type": "INTEGER", "description": "Row number (1-4) to write to. Defaults to row 1."},
            "clear": {"type": "BOOLEAN", "description": "Think of this as an writing 'fresh(true)' or 'appending(false)'. Defaults to false."}
        },
        "required": ["text"]
    }
)


play_tune_func = types.FunctionDeclaration(
    name="play_tune",
    description=(
        "Plays a tune on the passive buzzer."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "notes": {
                "type": "ARRAY",
                "items": {"type": "INTEGER"},
                "description": "Sequence of note frequencies in Hz (e.g. [262, 294, 330] for C4, D4, E4)"
            },
            "durations": {
                "type": "ARRAY",
                "items": {"type": "INTEGER"},
                "description": "Duration in milliseconds for each corresponding note"
            }
        },
        "required": ["notes", "durations"]
    }
)


set_led_func = types.FunctionDeclaration(
    name="set_led",
    description=(
        "Controls one of the individual single-color LEDs (red, blue, yellow, or white). "
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "led_color": {
                "type": "STRING",
                "enum": ["red", "blue", "yellow", "white"],
                "description": "Which LED to control"
            },
            "state": {
                "type": "STRING",
                "enum": ["on", "off"],
                "description": "Whether the LED should be on or off"
            },
            "count": {
                "type": "INTEGER",
                "description": "Number of times to blink. Omit for a steady on/off."
            },
            "interval_ms": {
                "type": "INTEGER",
                "description": "Delay in milliseconds between blinks. Only relevant if count is provided."
            }
        },
        "required": ["led_color", "state"]
    }
)


esp_tools = types.Tool(
    function_declarations=[
        read_temp_func,
        read_light_func,
        all_off_func,
        set_rgb_func,
        fade_rgb_func,
        alert_func,
        write_display_func,
        play_tune_func,
        set_led_func,
    ]
)