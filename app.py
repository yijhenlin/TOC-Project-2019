from bottle import route, run, request, abort, static_file

from fsm import TocMachine


VERIFY_TOKEN = "1111"
machine = TocMachine(
    states=[
        'user',
        'save',
        'load',
        'delete',
        'readdate',
        'readnumber',
        'check',
        'getdata',
        'deletedata',
        'other',
        'domemo',
        'memosave',
        'memoload'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'save',
            'conditions': 'is_going_to_save'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'load',
            'conditions': 'is_going_to_load'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'delete',
            'conditions': 'is_going_to_delete'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'other',
            'conditions': 'is_going_to_other'
        },
        {
            'trigger': 'advance',
            'source': 'other',
            'dest': 'domemo',
            'conditions': 'is_going_to_save'
        },
        {
            'trigger': 'advance',
            'source': 'domemo',
            'dest': 'memosave',
            'conditions': 'is_going_to_read'
        },
        {
            'trigger': 'advance',
            'source': 'other',
            'dest': 'memoload',
            'conditions': 'is_going_to_load'
        },
        {
            'trigger': 'advance',
            'source': 'save',
            'dest': 'readdate',
            'conditions': 'is_going_to_read'
        },
        {
            'trigger': 'advance',
            'source': 'readdate',
            'dest': 'readnumber',
            'conditions': 'is_going_to_read'
        },
        {
            'trigger': 'advance',
            'source': 'readnumber',
            'dest': 'check',
            'conditions': 'is_going_to_check'
        },
        {
            'trigger': 'advance',
            'source': 'readnumber',
            'dest': 'save',
            'conditions': 'is_going_to_retrun'
        },
        {
            'trigger': 'advance',
            'source': 'load',
            'dest': 'getdata',
            'conditions': 'is_going_to_data'
        },
        {
            'trigger': 'advance',
            'source': 'delete',
            'dest': 'deletedata',
            'conditions': 'is_going_to_data'
        },
        {
            'trigger': 'go_to_initial',
            'source': [
                'deletedata',
                'getdata',
                'check',
                'memosave',
                'memoload'
            ],
            'dest': 'user'
        },
        {
            'trigger': 'advance',
            'source': '*',
            'dest': 'user',
            'conditions': 'is_going_to_user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
