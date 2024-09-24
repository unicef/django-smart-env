---
title: Configuration
---

## Simple usage
    
Each entry can be one of the following:

- type
- (type, default_value)
- (type, default_value, bool)
- (type, default_value, bool, bool)
- (type, default_value, bool, bool, str)


    DOCS = {

    }

    SCHEME = {
        "DEBUG": bool,
        "STATIG_STORAGE": ("str", "default_value", False, False, "help_text"
    }
    env = SmartEnv()
