from googlesheettranslate.googlesheettech.modu.Translation import Translation

CFG_KEY_ID = 0
CFG_VALUE_ID = 1
CFG_KEY_VALUE_COLUMNS_NB = 2


def configurationFromPage(page):
    cfg = {}
    rawValues = page.get_all_values()
    for row in rawValues:
        key = row[CFG_KEY_ID]
        # Only take those rows that
        # * have key value pairs
        # * have keys
        if (len(key) and (len(row) >= CFG_KEY_VALUE_COLUMNS_NB)):
            value = row[CFG_VALUE_ID]
            cfg[key] = value
    return cfg


def parsePage(page, cfg):
    # Get raw page values.
    raw = page.get_all_values()

    translationsColumnId = int(cfg["TRANSLATION_COLUMN"]) - 1

    # Get list of languages.
    languagesRowId = int(cfg["LANGUAGES_ROW"]) - 1
    langRow = raw[languagesRowId]
    languagesNb = len(langRow)
    languages = []
    for columnId in range(translationsColumnId, languagesNb):
        languages.append(raw[languagesRowId][columnId])

    translationRowId = int(cfg["TRANSLATION_ROW"]) - 1
    # Comments column ids.
    commentKeyColumnId = int(cfg["COMMENT_KEY_COLUMN"]) - 1
    groupCommentKeyColumnId = int(cfg["GROUP_COMMENT_KEY_COLUMN"]) - 1
    # Key column ids.
    androidKeyColumnId = int(cfg["ANDROID_KEY_COLUMN"]) - 1
    iosKeyColumnId = int(cfg["IOS_KEY_COLUMN"]) - 1

    # Parse translations.
    translations = []
    for rowId in range(0, len(raw)):
        # Skip non-translation rows.
        if (rowId < translationRowId):
            continue
        tr = Translation()
        # Comment keys.
        comment = raw[rowId][commentKeyColumnId]
        tr.comment = comment if len(comment) else None
        groupComment = raw[rowId][groupCommentKeyColumnId]
        tr.groupComment = groupComment if len(groupComment) else None
        # Platform keys.
        androidKey = raw[rowId][androidKeyColumnId]
        tr.androidKey = androidKey if len(androidKey) else None
        iosKey = raw[rowId][iosKeyColumnId]
        tr.iosKey = iosKey if len(iosKey) else None
        # Get translations.
        for columnId in range(translationsColumnId, languagesNb):
            tr.translations.append(raw[rowId][columnId])
        translations.append(tr)

    return (languages, translations)
