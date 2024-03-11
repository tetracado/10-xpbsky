import xphid
import re
from atproto import Client, models
import typing as t

def maybethiswilluploadimages(imagepaths,textpost):
    allimages=[]
    print('running through uploadimages with image paths',imagepaths,'and textpost',textpost)
    for imagepath in imagepaths:
        with open(imagepath, 'rb') as file:
            img_data=file.read()
            print('read file')
            upload=bskyclient.com.atproto.repo.upload_blob(img_data)
            print('uploaded image')
            allimages.append(models.AppBskyEmbedImages.Image(alt='crossposted with xpbsky: no alt text available', image=upload.blob))
            file.close()
            print('uploaded image from',imagepath)
    embed = models.AppBskyEmbedImages.Main(images=allimages)
    bskyclient.com.atproto.repo.create_record(
        models.ComAtprotoRepoCreateRecord.Data(
            repo=bskyclient.me.did,
            collection=models.ids.AppBskyFeedPost,
            record=models.AppBskyFeedPost.Main(
                created_at=bskyclient.get_current_time_iso(), text=textpost, embed=embed
            ),
        )
    )
    print('posted image tweet')

def extract_url_byte_positions(text: str, *, encoding: str = 'UTF-8') -> t.List[t.Tuple[str, int, int]]:
    """This function will detect any links beginning with http or https."""
    #https://github.com/MarshalX/atproto/blob/main/examples/advanced_usage/auto_hyperlinks.py
    encoded_text = text.encode(encoding)

    # Adjusted URL matching pattern
    pattern = rb'https?://[^ \n\r\t]*'

    matches = re.finditer(pattern, encoded_text)
    url_byte_positions = []

    for match in matches:
        url_bytes = match.group(0)
        url = url_bytes.decode(encoding)
        url_byte_positions.append((url, match.start(), match.end()))

    return url_byte_positions

def injecturls(text: str):

    url_positions = extract_url_byte_positions(text)
    facets = []

    for link_data in url_positions:
        uri, byte_start, byte_end = link_data
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Link(uri=uri)],
                index=models.AppBskyRichtextFacet.ByteSlice(byte_start=byte_start, byte_end=byte_end),
            )
        )
    return facets

def sendtweet(text):
    bskyclient.send_post(text)
    print('bsky sent')


bskyclient=Client()
bskyclient.login('tetracado.bsky.social', xphid.bskyapppass)
print('logged in to bsky')

