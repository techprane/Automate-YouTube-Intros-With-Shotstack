import os
import time
import shotstack_sdk as shotstack
from shotstack_sdk.api import edit_api
from shotstack_sdk.model.video_asset import VideoAsset
from shotstack_sdk.model.soundtrack import Soundtrack
from shotstack_sdk.model.clip import Clip
from shotstack_sdk.model.track import Track
from shotstack_sdk.model.timeline import Timeline
from shotstack_sdk.model.output import Output
from shotstack_sdk.model.edit import Edit

# Configure API (sandbox endpoint)
config = shotstack.Configuration(host="https://api.shotstack.io/stage")
config.api_key['DeveloperKey'] = os.getenv("SHOTSTACK_KEY")
assert config.api_key['DeveloperKey'], "SHOTSTACK_KEY is missing!"
api = edit_api.EditApi(shotstack.ApiClient(config))


def make_intro(intro_clip_url: str, music_url: str, duration=5.0):
    video = VideoAsset(src=intro_clip_url)
    clip = Clip(asset=video, start=0.0, length=duration)
    track_video = Track(clips=[clip])

# Add audio as soundtrack
    soundtrack = Soundtrack(src=music_url, volume=0.7, effect="fadeIn")
    timeline = Timeline(background="#000000", tracks=[
                        track_video], soundtrack=soundtrack)
    output = Output(format="mp4", resolution="sd")
    edit = Edit(timeline=timeline, output=output)

    render = api.post_render(edit)
    return render.response.id


def poll_status(rid):
    while True:
        r = api.get_render(rid, data=True).response
        print("Status:", r.status)
        if r.status == "done":
            return r.url
        elif r.status == "failed":
            print("Error message:", r.error)
            print("Timeline JSON:", r.data.timeline)
            return None
        time.sleep(2)


if __name__ == "__main__":
    intro_text = "Welcome to My Channel!",
    clip = "https://shotstack-assets.s3.amazonaws.com/footage/skater.hd.mp4"
    music = "https://shotstack-ingest-api-stage-renditions.s3.ap-southeast-2.amazonaws.com/t2siieowih/zzy8at4g-2gjx-uc2x-euzd-18aayh0tf1og/zzy8at4f-3zkf-wg1z-fgdh-2jhlrt1eqvcf.mp3"
    rid = make_intro(clip, music)
    print("Render ID:", rid)
    url = poll_status(rid)
    print("Done! URL:", url)
