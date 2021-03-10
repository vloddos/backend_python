import json
import threading
from pathlib import Path

from flask import request

from server.nails_tracker.app import app, db
from server.nails_tracker.app.models import Texture, User
from server.patch_nails import patch_nails, mock


@app.route('/api/photo/polish', methods=['POST'])
def apply_polish():
    data = request.get_json()

    patch_nails.input_queue.put(
        patch_nails.Patch(
            patch_function=patch_nails.apply_polish,
            photo_base64=data.get('photo'),
            texture_or_polish=data.get('polish')
        )
    )

    return json.dumps({'photo': patch_nails.output_queue.get()})


@app.route('/api/photo/texture', methods=['POST'])
def apply_texture():
    data = request.get_json()

    patch_nails.input_queue.put(
        patch_nails.Patch(
            patch_function=patch_nails.apply_texture,
            photo_base64=data.get('photo'),
            texture_or_polish=Texture.query.get(data.get('id')).file
        )
    )

    return json.dumps({'photo': patch_nails.output_queue.get()})


@app.route('/api/photo/dots', methods=['POST'])
def photo_dots():
    data = request.json
    method = data.get('method')

    if method == 'GET':
        patch_nails.input_queue.put(
            patch_nails.Patch(
                photo_base64=data.get('photo')
            )
        )
        return json.dumps({'dots': patch_nails.output_queue.get()})

    elif method == 'POST':
        texture_id = data.get('id')

        patch_nails.input_queue.put(
            patch_nails.Patch(
                patch_function=(patch_nails.apply_texture
                                if texture_id
                                else patch_nails.apply_polish),
                photo_base64=data.get('photo'),
                texture_or_polish=(Texture.query.get(texture_id).file
                                   if texture_id
                                   else data.get('polish')),
                dots=data.get('dots')
            )
        )
        return json.dumps({'photo': patch_nails.output_queue.get()})


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return json.dumps('hello get')

    elif request.method == 'POST':
        data = request.json

        print(type(data))
        print(data)

        return json.dumps('hello post')


@app.route('/api/textures', methods=['GET'])
def get_textures():
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))

    result = Texture \
        .query \
        .paginate(page=page, per_page=per_page)

    return json.dumps({
        'total': result.total,
        'pages': result.pages,
        'texture_list': [
            {'id': i.id, 'name': i.name, 'info': i.info, 'file': i.file}
            for i in result.items
        ]
    })


@app.route('/api/textures-mock', methods=['GET'])
def get_textures_mock():
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))

    with open(
            str(
                    Path(__file__)
                        .absolute()
                        .parent
                        .parent / 'textures-mock.txt'
            ),
            'rt'
    ) as f:
        lines = [i.split() for i in f.readlines()]

    total = len(lines)
    pages = -(-total // per_page)
    lines = lines[(page - 1) * per_page:page * per_page]

    return json.dumps({
        'total': total,
        'pages': pages,
        'texture_list': [
            {'id': i, 'name': j, 'info': k, 'file': None}
            for i, (j, k) in enumerate(lines, start=(page - 1) * per_page + 1)
        ]
    })


@app.route('/api/textures/count', methods=['GET'])
def textures_count():
    return json.dumps(Texture.query.count())


@app.route('/api/create-texture', methods=['POST'])
def create_texture():
    data = request.get_json()

    texture = Texture(
        name=data.get('name'),
        info=data.get('info'),
        file=data.get('file'),
        master=User.query.first()  # todo fix this crutch
    )

    db.session.add(texture)
    db.session.commit()

    return json.dumps(texture.id)


@app.before_first_request
def patch_nails_thread():
    # uncomment for real mask_rcnn test and comment line below
    thread = threading.Thread(target=patch_nails.patch_nails)

    # uncomment for test without mask_rcnn and comment line above
    # thread = threading.Thread(target=mock.patch_nails_mock)

    thread.start()
