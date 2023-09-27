from http.server import BaseHTTPRequestHandler, HTTPServer
import obsws_python as obs
import json

client = obs.ReqClient(host='localhost', port=4455, password='3H6XZbvhK4deeaQx', timeout=3)


class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json') 
        self.end_headers() 

    def _get_scenes(self):
        scenes = client.get_scene_list()
        outp_scenes = {}
        for scene in scenes.scenes:
            sources = client.get_scene_item_list(scene['sceneName'])
            outp_scenes[scene['sceneName']] = []

            for item in sources.scene_items:
                if item['inputKind'] == 'gstreamer-source':
                    outp_scenes[scene['sceneName']].append(item)
        data = json.dumps(outp_scenes)

        return bytes(data, 'utf-8')

    def do_GET(self):
        self._set_headers()
        scenes = self._get_scenes()
        self.wfile.write(scenes)

    def do_POST(self):...

    def do_PUT(self):...

host = ''
port = 80
HTTPServer((host, port), HandleRequests).serve_forever() 
