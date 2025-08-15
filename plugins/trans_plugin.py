#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  trans_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Parts of code Copyright © blacksmith-bot (http://blacksmith-bot.googlecode.com/)

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import urllib, urllib2, re

trans_langs={u'en': u'english', u'ja': u'japanese', u'ru': u'russian', u'auto': u'Determine language', u'sq': u'Albanian', u'ar': u'Arabic', u'af': u'Afrikaans', u'be': u'Belarusian', u'bg': u'Bulgarian', u'cy': u'Welsh', u'hu': u'Hungarian', u'vi': u'Vietnamese', u'gl': u'Galician', u'nl': u'Dutch', u'el': u'Greek', u'da': u'Danish',u'iw': u'Hebrew', u'yi': u'Yiddish', u'id': u'Indonesian', u'ga': u'Irish', u'is': u'Icelandic', u'es': u'Spanish', u'it': u'Italian', u'ca': u'Catalan', u'zh-CN': u'Chinese', u'ko': u'Korean', u'lv': u'Latvian', u'lt': u'Lithuanian',u'mk': u'Macedonian', u'ms': u'Malay', u'mt': u'Maltese', u'de': u'German', u'no': u'Norwegian', u'fa': u'Persian', u'pl': u'Polish', u'pt': u'Portuguese', u'ro': u'Romanian', u'sr': u'Serbian', u'sk': u'Slovak', u'sl': u'Slovenian', u'sw': u'Swahili', u'tl': u'Filipino', u'th': u'Thai', u'tr': u'Turkish', u'uk': u'Ukrainian', u'fi': u'Finnish', u'fr': u'French', u'hi': u'Hindi', u'hr': u'Croatian', u'cs': u'Czech', u'sv': u'Swedish', u'et': u'Estonian'}

def gTrans(fLang, tLang, text):
	url = "http://translate.google.ru/m?hl=ru&sl=%(fLang)s&tl=%(tLang)s&ie=UTF-8&prev=_m&q=%(text)s"
	text = urllib.quote(text.encode("utf-8"))
	try:
		req=urllib2.Request(url % vars())
		req.add_header("User-agent", "Opera/9.60")
		site = urllib2.urlopen(req)
		html = site.read()
		return re.search("class=\"t0\">((?:.|\s)+?)</div>", html, 16).group(1)
	except Exception, e:
		return "%s: %s" % (e.__class__.__name__, e.message)

def gAutoTrans(mType, source, text):
	if text:
		repl = gTrans("auto", "ru", text)
		if text == repl:
			repl = u"Translate %s => %s:\n%s" % ("auto", "en", gTrans("auto", "en", text))
		else:
			repl = u"Translate %s => %s:\n%s" % ("auto", "ru", repl)
	else:
		repl = u"Need more params."
	reply(mType, source, repl)

def gTransHandler(mType, source, args):
	if args and len(args.split()) > 2:
		(fLang, tLang, text) = args.split(None, 2)
		reply(mType, source, u"Translate %s => %s:\n%s" % (fLang, tLang, gTrans(fLang, tLang, text)))
	else:
		answer = u"\nAvailable languages:\n"
		for a, b in enumerate(sorted([x + u" — " + y for x, y in trans_langs.iteritems()])), 1:
			answer += u"%i. %s.\n" % (a, b)
		reply(mType, source, answer.encode("utf-8"))

register_command_handler(gTransHandler, 'trans', ['info','all'], 10, 'Translate from one language to another. Via Google Translate engine. Available languages for translation:\n' + ', '.join(sorted([x.encode('utf-8')+': '+y.encode('utf-8') for x,y in trans_langs.iteritems()])), 'trans <source_lang> <target_lang> <text>', ['trans en ru hello', 'trans ru en привет'])
