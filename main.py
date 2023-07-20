import json
from quart import Quart, request, jsonify, send_file, Response
from telegraph import Telegraph
import pyshorteners as sh
import quart_cors

app = quart_cors.cors(Quart(__name__), allow_origin="https://chat.openai.com")

telegraph = Telegraph()

s = sh.Shortener()

@app.route('/export', methods=['POST'])
async def export():
    try:
        data = await request.get_json()

        # Create a new Telegraph account
        telegraph.create_account(short_name='1337')

        response = telegraph.create_page(
            title=data.get('title', 'No Title Provided').replace('\n', '<br>').replace('h1', 'h3').replace(
                'h2', 'h4').replace('span', '').replace('html', ''),
            html_content=data.get('text', '')
        )

        return jsonify({'url': s.tinyurl.short(response['url'])})
    except Exception as e:
        print(f"Error in export route: {e}")
        return Response('Internal Server Error', status=500, mimetype='text/plain')


@app.route("/logo.jpg")
async def plugin_logo():
    filename = 'logo.jpg'
    return await send_file(filename, mimetype='image/jpg')



@app.route("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return Response(text, mimetype="text/json")


@app.route("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        return Response(text, mimetype="text/yaml")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5003)
