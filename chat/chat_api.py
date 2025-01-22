#!/usr/bin/env python3

import json
import socket
import mistletoe
import subprocess
import pprint as pp
import datetime as dt
from functools import partial

from flask import Flask, request, abort, jsonify

from bleach.sanitizer     import Cleaner
from bleach.css_sanitizer import CSSSanitizer
from bleach.linkifier     import LinkifyFilter
from bleach.sanitizer     import ALLOWED_PROTOCOLS
from bleach_allowlist     import print_tags, print_attrs, all_styles, markdown_tags

app = Flask(__name__)

allowed_attrs = {
    "*": ["id", "class", "style"],
    "img": ["src", "alt", "title"],
    "a": ["href", "alt", "title"],
}

MESSAGES = [{"username": "SYSTEM", "ip": socket.gethostname(), "timestamp": dt.datetime.now().isoformat(), "content": "hi hi hi."}]

@app.errorhandler(500)
def resource_not_found(e): return jsonify(e.response), 500

@app.errorhandler(404)
def resource_not_found(e): return jsonify(e.response), 404

@app.route('/api/node_chat/clear_messages')
def clear_messages():
    MESSAGES[:] = [
        {"username": "SYSTEM", "ip": socket.gethostname(), "timestamp": dt.datetime.now().isoformat(), "content": "hi hi hi."},
        {"username": "SYSTEM", "ip": socket.gethostname(), "timestamp": dt.datetime.now().isoformat(), "content": "SCREEN_CL"}
    ]
    return json.dumps({})

@app.route('/api/node_chat/message', methods=['POST'])
def message():
    cleaner = Cleaner(
        tags=print_tags + markdown_tags,
        attributes=allowed_attrs,
        filters=[partial(LinkifyFilter, skip_tags={'pre', 'code'}, parse_email=True)],
        strip_comments=False,
        protocols=set(ALLOWED_PROTOCOLS) | {'smb', 'data', 'ftp', 'file', 'magnet'},
        css_sanitizer=CSSSanitizer(allowed_css_properties=all_styles),
    )
    data     = request.get_json()
    response = {}

    MESSAGES.append({
        "username":  cleaner.clean(data['username'].strip().removeprefix("<p>").removesuffix("</p>")),
        "ip":        str(request.access_route[-1]),
        "timestamp": dt.datetime.now().isoformat(),
        "content":   cleaner.clean(mistletoe.markdown(data['content']).strip().removeprefix("<p>").removesuffix("</p>"))
    })

    return json.dumps(response, indent=4, sort_keys=True)

@app.route('/api/node_chat/messages', methods=['GET'])
def messages(): return json.dumps(MESSAGES, indent=4, sort_keys=True)


if __name__ == '__main__':
    app.run(debug=True, host='::', port=18051)
